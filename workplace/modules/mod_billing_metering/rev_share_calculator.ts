import { BillingUsageEvent } from "../../shared/dto";

/**
 * Usage Metering & 15% Token Savings Rev-Share Engine
 */
export class RevShareBillingEngine {
  private static REV_SHARE_RATE = 0.15;
  private static BLENDED_TOKEN_PRICE_PER_M = 3.00; // $3.00 per 1M tokens

  static calculateEventFee(uncompressedTokens: number, prunedTokens: number): { grossSavingsUsd: number; revShareDueUsd: number } {
    const savedTokens = Math.max(0, uncompressedTokens - prunedTokens);
    const grossSavingsUsd = (savedTokens / 1_000_000) * this.BLENDED_TOKEN_PRICE_PER_M;
    const revShareDueUsd = grossSavingsUsd * this.REV_SHARE_RATE;
    return {
      grossSavingsUsd: Number(grossSavingsUsd.toFixed(4)),
      revShareDueUsd: Number(revShareDueUsd.toFixed(4)),
    };
  }

  static processEvent(event: BillingUsageEvent): BillingUsageEvent {
    if (event.eventType === "token_savings_realized" && event.payload.tokensUncompressed && event.payload.tokensPruned) {
      const { grossSavingsUsd, revShareDueUsd } = this.calculateEventFee(
        event.payload.tokensUncompressed,
        event.payload.tokensPruned
      );
      event.payload.grossTokenSavingsUsd = grossSavingsUsd;
      event.payload.revShareDueUsd = revShareDueUsd;
    }
    return event;
  }
}
