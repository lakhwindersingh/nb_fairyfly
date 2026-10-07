#!/usr/bin/env python3
"""
Unit and integration test suite for GitBundleTransport (TODO-DEWS-03).
Verifies cryptographic packaging, extraction, uncommitted diff inclusion,
streaming HTTP chunking, and 100% hash parity in round-trip swarm transport.
"""

import json
from pathlib import Path
import subprocess
import tempfile
import pytest

from workplace.core.git_bundle_transport import (
    GitBundleTransport,
    BundleManifest,
    BundleReceipt,
    ExtractReceipt,
)


@pytest.fixture
def temp_workspace():
    """Provides an isolated workspace directory with two git repositories."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        local_repo = root / "local_station"
        remote_repo = root / "remote_fleet"
        bundles_dir = root / "bundles"
        bundles_dir.mkdir(parents=True, exist_ok=True)

        for p in [local_repo, remote_repo]:
            p.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "init", "-b", "main"], cwd=p, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Percipience Swarm"], cwd=p, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "swarm@percipience.ai"], cwd=p, check=True, capture_output=True)
            (p / "README.md").write_text("# Project Root\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=p, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial root commit"], cwd=p, check=True, capture_output=True)

        yield {
            "root": root,
            "local": local_repo,
            "remote": remote_repo,
            "bundles": bundles_dir
        }


def test_bundle_manifest_and_receipt_dataclasses():
    """Validates serialization, deserialization, and schema integrity of models."""
    manifest = BundleManifest(
        bundle_id="b_123",
        agent_id="agent_billing",
        repo_name="nb_fairyfly",
        source_branch="wt_branch_billing",
        head_commit="abcd1234abcd1234",
        bundle_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        file_size_bytes=4096,
        created_at="2026-10-07T14:00:00Z",
        has_uncommitted=True,
        metadata={"priority": "high", "wave": "1"}
    )
    d = manifest.to_dict()
    assert d["bundle_id"] == "b_123"
    assert d["has_uncommitted"] is True
    assert d["metadata"]["wave"] == "1"

    recon = BundleManifest.from_dict(d)
    assert recon.bundle_id == manifest.bundle_id
    assert recon.bundle_sha256 == manifest.bundle_sha256

    receipt = BundleReceipt(
        status="SUCCESS",
        bundle_id="b_123",
        bundle_path="/tmp/test.bundle",
        manifest=manifest,
        duration_ms=45.2
    )
    rec_d = receipt.to_dict()
    assert rec_d["status"] == "SUCCESS"
    assert rec_d["manifest"]["agent_id"] == "agent_billing"

    ext_receipt = ExtractReceipt(
        status="SUCCESS",
        bundle_id="b_123",
        target_branch="wt_branch_billing",
        head_commit="abcd1234",
        verified=True,
        merged=True
    )
    assert ext_receipt.to_dict()["merged"] is True


def test_create_and_verify_clean_bundle(temp_workspace):
    """Verifies standard commit bundling and cryptographic verification."""
    local = temp_workspace["local"]
    transport = GitBundleTransport(storage_dir=temp_workspace["bundles"])

    # Create a feature branch with a commit
    subprocess.run(["git", "checkout", "-b", "feature/billing"], cwd=local, check=True, capture_output=True)
    (local / "billing.py").write_text("class BillingEngine: pass\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=local, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Add billing engine"], cwd=local, check=True, capture_output=True)

    receipt = transport.create_bundle(
        repo_path=local,
        branch="feature/billing",
        base_ref="main",
        agent_id="agent_dev"
    )

    assert receipt.status == "SUCCESS"
    assert receipt.manifest is not None
    assert receipt.manifest.source_branch == "feature/billing"
    assert receipt.manifest.has_uncommitted is False
    assert Path(receipt.bundle_path).exists()
    assert Path(receipt.bundle_path).stat().st_size > 0

    # Manifest file written alongside
    manifest_file = Path(receipt.bundle_path).with_suffix(".bundle.manifest.json")
    assert manifest_file.exists()
    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert manifest_data["agent_id"] == "agent_dev"

    # Verify bundle
    is_valid, msg, heads = transport.verify_bundle(Path(receipt.bundle_path), local)
    assert is_valid is True
    assert "verified successfully" in msg
    assert len(heads) >= 1
    assert heads[0][1] == "refs/heads/feature/billing"


def test_create_bundle_with_uncommitted_changes(temp_workspace):
    """Verifies that uncommitted working-tree edits are committed to checkpoint and bundled."""
    local = temp_workspace["local"]
    transport = GitBundleTransport(storage_dir=temp_workspace["bundles"])

    subprocess.run(["git", "checkout", "-b", "feature/auth"], cwd=local, check=True, capture_output=True)
    # Dirty state: uncommitted file
    (local / "auth_provider.py").write_text("# in progress uncommitted code\n", encoding="utf-8")
    assert transport.has_uncommitted_changes(local) is True

    receipt = transport.create_bundle(
        repo_path=local,
        branch="feature/auth",
        agent_id="agent_auth",
        include_uncommitted=True
    )

    assert receipt.status == "SUCCESS"
    assert receipt.manifest.has_uncommitted is True
    # Working tree is clean after checkpoint
    assert transport.has_uncommitted_changes(local) is False

    is_valid, _, heads = transport.verify_bundle(Path(receipt.bundle_path))
    assert is_valid is True
    assert heads[0][1] == "refs/heads/feature/auth"


def test_full_round_trip_remote_swarm_workflow(temp_workspace):
    """
    Executes acceptance criteria:
    Local uncommitted branch -> bundle -> remote extraction -> remote commit ->
    result bundle -> local merge passes with 100% hash parity.
    """
    local = temp_workspace["local"]
    remote = temp_workspace["remote"]
    transport = GitBundleTransport(storage_dir=temp_workspace["bundles"])

    # 1. Developer on local workstation creates branch with uncommitted work
    subprocess.run(["git", "checkout", "-b", "task/data_pipeline"], cwd=local, check=True, capture_output=True)
    (local / "pipeline.py").write_text("def ingest_data(): return [1, 2, 3]\n", encoding="utf-8")

    # 2. Package into dispatch bundle
    dispatch_receipt = transport.create_bundle(
        repo_path=local,
        branch="task/data_pipeline",
        agent_id="dev_station_01",
        include_uncommitted=True
    )
    assert dispatch_receipt.status == "SUCCESS"
    dispatch_bundle = Path(dispatch_receipt.bundle_path)

    # 3. Remote fleet container extracts dispatch bundle into remote repo
    extract_receipt = transport.extract_bundle(
        bundle_path=dispatch_bundle,
        target_repo_path=remote,
        target_branch="task/data_pipeline",
        checkout=True
    )
    assert extract_receipt.status == "SUCCESS"
    assert (remote / "pipeline.py").exists()
    assert "ingest_data" in (remote / "pipeline.py").read_text(encoding="utf-8")

    # 4. Remote Claude/Aider agent synthesizes code & commits on remote
    (remote / "pipeline.py").write_text(
        "def ingest_data(): return [1, 2, 3]\n\ndef process_stream(): return True\n",
        encoding="utf-8"
    )
    (remote / "test_pipeline.py").write_text(
        "from pipeline import ingest_data, process_stream\ndef test_p(): assert process_stream() is True\n",
        encoding="utf-8"
    )
    subprocess.run(["git", "add", "."], cwd=remote, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "feat: remote agent synthesized pipeline logic"], cwd=remote, check=True, capture_output=True)
    remote_head = transport.get_head_commit(remote, "task/data_pipeline")

    # 5. Remote container creates result bundle
    result_receipt = transport.create_bundle(
        repo_path=remote,
        branch="task/data_pipeline",
        agent_id="remote_agent_runner",
        include_uncommitted=False
    )
    assert result_receipt.status == "SUCCESS"
    result_bundle = Path(result_receipt.bundle_path)

    # 6. Local workstation receives result bundle and merges into local branch
    local_extract = transport.extract_bundle(
        bundle_path=result_bundle,
        target_repo_path=local,
        target_branch="task/data_pipeline_result",
        checkout=False,
        auto_merge_into="task/data_pipeline"
    )
    assert local_extract.status == "SUCCESS"
    assert local_extract.merged is True

    # 7. Verify 100% Hash Parity & File Integrity
    local_head = transport.get_head_commit(local, "task/data_pipeline")
    assert local_head == remote_head, f"Hash parity failure: local {local_head} != remote {remote_head}"
    assert (local / "test_pipeline.py").exists()
    assert (local / "pipeline.py").read_text(encoding="utf-8") == (remote / "pipeline.py").read_text(encoding="utf-8")


def test_streaming_bundle_chunk_adapters(temp_workspace):
    """Verifies chunk streaming generator and on-the-fly SHA-256 verification."""
    local = temp_workspace["local"]
    transport = GitBundleTransport(storage_dir=temp_workspace["bundles"])

    subprocess.run(["git", "checkout", "-b", "stream_branch"], cwd=local, check=True, capture_output=True)
    (local / "stream_payload.dat").write_text("A" * 100000, encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=local, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Large payload for streaming"], cwd=local, check=True, capture_output=True)

    receipt = transport.create_bundle(repo_path=local, branch="stream_branch")
    assert receipt.status == "SUCCESS"
    bundle_path = Path(receipt.bundle_path)

    # Stream chunks
    chunks = list(transport.stream_bundle_chunks(bundle_path, chunk_size=128))
    assert len(chunks) > 1

    # Receive stream at destination
    dest_path = temp_workspace["bundles"] / "streamed_received.bundle"
    bytes_written, digest = transport.receive_streaming_bundle(chunks, dest_path)

    assert bytes_written == bundle_path.stat().st_size
    assert digest == receipt.manifest.bundle_sha256

    # Verify received bundle
    is_valid, _, heads = transport.verify_bundle(dest_path)
    assert is_valid is True
    assert heads[0][1] == "refs/heads/stream_branch"
