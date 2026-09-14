/**
 * Merkle DAG State Explorer Data Provider
 */

export interface DAGNode {
  id: string;
  blockId: number;
  label: string;
  hash: string;
  action: string;
  status: "GENESIS" | "VERIFIED" | "BOOTSTRAP";
  timestamp: string;
}

export interface DAGEdge {
  from: string;
  to: string;
}

export class MerkleExplorerService {
  static getDAGGraph(): { nodes: DAGNode[]; edges: DAGEdge[] } {
    const nodes: DAGNode[] = [
      {
        id: "node_0",
        blockId: 0,
        label: "Block 0 (Genesis)",
        hash: "7f8b9e4a3d2c1b0a...",
        action: "GENESIS_INITIALIZATION",
        status: "GENESIS",
        timestamp: "2026-09-13T21:45:52Z",
      },
      {
        id: "node_1",
        blockId: 1,
        label: "Block 1 (Bootstrap)",
        hash: "a3b2c1d0e9f8a7b6...",
        action: "QUAD_SPACE_AND_MULTI_MODULE_BOOTSTRAP",
        status: "BOOTSTRAP",
        timestamp: "2026-09-13T21:48:00Z",
      },
      {
        id: "node_2",
        blockId: 2,
        label: "Block 2 (PR Gate Audit)",
        hash: "f881b2be129be959...",
        action: "PR_GATE_VERIFICATION_PASS",
        status: "VERIFIED",
        timestamp: "2026-09-13T21:54:30Z",
      },
    ];

    const edges: DAGEdge[] = [
      { from: "node_0", to: "node_1" },
      { from: "node_1", to: "node_2" },
    ];

    return { nodes, edges };
  }
}
