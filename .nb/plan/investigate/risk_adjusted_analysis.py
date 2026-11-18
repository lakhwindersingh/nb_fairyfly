def get_risk_adjusted_analysis_prompt(
    symbol: str,
    current_date_str: str,
    strategy: str,
    horizon: int,
    legs_str: str,
    underlying_info: str,
    risk_range_info: str,
    options_chain_info: str,
    forecast_info: str,
    entry_info: str,
    greeks_info: str,
    leg_greeks_info: str,
) -> str:
    return (
        f"As an expert options trader and financial analyst, perform a comprehensive risk-adjusted analysis on the following strategy:\n\n"
        f"**IMPORTANT**: Use the provided Risk-Adjusted Price Range to evaluate the safety and profitability of this strategy. "
        f" Range provides appropriate range to target delta based on risk profile of an individual, this is reverse engineered using blackscholes by giving . "
        f" delta range, option type forcast model as an input "
        f"**Analysis Date**: {current_date_str}\n"
        f"**Symbol**: {symbol}\n"
        f"**Strategy**: {strategy}\n"
        f"**Time Horizon**: {horizon} days (to max expiration)\n"
        f"**Legs**: {legs_str}\n"
        f"### Underlying Information\n"
        f"{underlying_info}"
        f"{risk_range_info}"
        f"### Options Chain Summary\n"
        f"{options_chain_info}"
        f"### Quantitative Forecast Model Projections\n"
        f"{forecast_info}"
        f"{entry_info}"
        f"{greeks_info}"
        f"{leg_greeks_info}"
        f"Please provide your analysis in a structured format suitable for an elegant dashboard display. "
        f"Use sections like Executive Summary, Risk-Adjusted Verdict, Pricing & Risk Analysis, and Action Checklist (Triggers).\n"
        f"### Management Recommendation\n"
        f"Provide a detailed recommendation: Should the user exit now to lock in profits/limit losses, hold for further decay/move, or roll to a new strike/expiry? Provide specific targets.\n\n"
        f"### Pricing & Risk Analysis\n"
        f"Analyze the current value vs entry (if applicable) and risk profile given current market conditions.\n"
        f"### Expiration & Assignment Risk\n"
        f"Evaluate risks related to the chosen expiration dates and potential for early assignment.\n"
        f"### Current Risk & Reward Profile\n"
        f"- Max profit/loss potential remaining\n"
        f"- Current greeks exposure (if provided)\n"
        f"- Key risks (assignment, pin risk, vol crush, etc.)\n"
        f"### Greeks & Market Context Interpretation\n"
        f"Explain how current Greeks interact with today's technicals & forecast\n"
        f"### Directional Exposure (Delta/Gamma)\n"
        f"Explain how the position reacts to price moves and how that sensitivity changes.\n"
        f"### Volatility Sensitivity (Vega)\n"
        f"Explain how an increase or decrease in implied volatility will affect the P&L.\n"
        f"### Time Decay (Theta)\n"
        f"Explain how much value the position gains or loses daily from the passage of time.\n"
        f"### Risk Summary\n"
        f"A brief summary of the dominant risk factor for this position right now. Break it down by DTE groups.\n\n"
    )
