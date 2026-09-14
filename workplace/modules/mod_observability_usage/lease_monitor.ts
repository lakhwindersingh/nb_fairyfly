/**
 * Active Ephemeral Worktree Lease Monitor
 */

export interface WorktreeLeaseView {
  agentId: string;
  sandboxPath: string;
  branch: string;
  remainingTtlSec: number;
  status: "ACTIVE" | "EXPIRED" | "TERMINATING";
}

export class LeaseMonitorService {
  static getActiveLeases(): WorktreeLeaseView[] {
    return [
      {
        agentId: "subagent_architect_01",
        sandboxPath: ".workspaces/wt_architect_01",
        branch: "wt_branch_architect_01",
        remainingTtlSec: 1840,
        status: "ACTIVE",
      },
      {
        agentId: "subagent_dev_gate_02",
        sandboxPath: ".workspaces/wt_dev_02",
        branch: "wt_branch_dev_02",
        remainingTtlSec: 3290,
        status: "ACTIVE",
      },
    ];
  }
}
