/**
 * Interactive Token Rev-Share & ROI Calculator
 */

export interface ROICalculatorInput {
  engineersCount: number;
  monthlyClaudeSpendUsd: number;
  dailyPullRequests: number;
}

export interface ROICalculatorOutput {
  projectedTokenSavingsUsd: number;
  revShareFeeUsd: number;
  netClientMonthlySavingsUsd: number;
  annualizedRoiUsd: number;
}

export function calculateEnterpriseROI(input: ROICalculatorInput): ROICalculatorOutput {
  const estimatedCompressionRate = 0.55; // 55% average reduction
  const grossSavings = input.monthlyClaudeSpendUsd * estimatedCompressionRate;
  const revShareFee = grossSavings * 0.15; // 15% performance fee
  const netMonthly = grossSavings - revShareFee;
  const annualized = netMonthly * 12;

  return {
    projectedTokenSavingsUsd: Math.round(grossSavings),
    revShareFeeUsd: Math.round(revShareFee),
    netClientMonthlySavingsUsd: Math.round(netMonthly),
    annualizedRoiUsd: Math.round(annualized),
  };
}
