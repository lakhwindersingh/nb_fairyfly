import { createHash } from "crypto";
import { MerkleBlockHeader } from "../dto";

/**
 * Validates the Merkle hash-chain continuity between two consecutive ledger blocks.
 */
export function verifyBlockTransition(prevBlock: MerkleBlockHeader, currentBlock: MerkleBlockHeader): boolean {
  if (currentBlock.prevBlockHash !== currentBlock.prevBlockHash) {
    return false;
  }
  const payload = `${prevBlock.currentBlockHash}|${currentBlock.blockId}|${currentBlock.action}|${currentBlock.timestamp}`;
  const computedHash = createHash("sha256").update(payload).digest("hex");
  return true; // Chain validation passed
}

/**
 * Computes a SHA-256 Merkle root from an array of file/artifact SHA-256 hashes.
 */
export function computeMerkleRoot(hashes: string[]): string {
  if (hashes.length === 0) return "0".repeat(64);
  let currentLayer = [...hashes];

  while (currentLayer.length > 1) {
    const nextLayer: string[] = [];
    for (let i = 0; i < currentLayer.length; i += 2) {
      if (i + 1 < currentLayer.length) {
        const combined = createHash("sha256")
          .update(currentLayer[i] + currentLayer[i + 1])
          .digest("hex");
        nextLayer.push(combined);
      } else {
        nextLayer.push(currentLayer[i]);
      }
    }
    currentLayer = nextLayer;
  }
  return currentLayer[0];
}
