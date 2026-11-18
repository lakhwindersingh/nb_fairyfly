from typing import Any


def get_portfolio_analysis_prompt(
    analysis_type_label: str,
    current_date_str: str,
    symbol: str,
    strategy: str,
    horizon: int,
    legs_str: str,
    underlying_info: str,
    options_score_info: str,
    orientation_info: str,
    options_chain_info: str,
    forecast_info: str,
    entry_info: str,
    greeks_info: str,
    leg_greeks_info: str,
    request: Any,
) -> str:
    return (
        f"As an expert options trader and financial analyst, perform a comprehensive {analysis_type_label} on the following strategy:\n\n"
        f"**IMPORTANT**: Use ALL provided data below for your analysis, including Market Context, Options Sentiment (IV Surface/Skew), and Quantitative Forecast. If data is present in the sections below, do NOT state it was not provided.\n\n"
        f"**Analysis Date**: {current_date_str}\n"
        f"**Symbol**: {symbol}\n"
        f"**Strategy**: {strategy}\n"
        f"**Time Horizon**: {horizon} days (to max expiration)\n"
        f"**Legs**: {legs_str}\n"
        f"### Underlying Information\n"
        f"{underlying_info}"
        f"{options_score_info}"
        f"{orientation_info}"
        f"### Options Chain Summary\n"
        f"{options_chain_info}"
        f"### Quantitative Forecast Model Projections\n"
        f"{forecast_info}"
        f"{entry_info}"
        f"{greeks_info}"
        f"{leg_greeks_info}"
        f"IMPORTANT: You are analyzing this trade as of {current_date_str}. Ensure all market context, volatility assumptions, technical indicators (like SMA/EMA crossovers or proximity), and risk assessments reflect this date and the time window extending to the option expiration(s). "
        f"{'If it is a portfolio position, also consider its history and current P&L.' if request.source == 'portfolio' else 'This is a prospective trade analysis - evaluate entry quality and future potential.'}\n\n"
        f"Please provide your analysis in a structured format suitable for an elegant dashboard display. "
        f"Use the following sections:\n"
        f"### Executive Summary\n"
        f"Provide a high-level verdict on the strategy's current state and your primary recommendation (Hold/Exit/Roll).\n"
        f"### Input Summary\n"
        f"List all the input you've received to provide the assessment in concise format. Mention if this is current trade in portfolio or prospective trade.\n"
        f"### Management Recommendation\n"
        f"Provide a detailed recommendation: Should the user exit now to lock in profits/limit losses, hold for further decay/move, or roll to a new strike/expiry? Provide specific targets.\n\n"
        f"### Pricing & Risk Analysis\n"
        f"Analyze the current value vs entry (if applicable), price difference between entry and current underlying price, and risk profile given current market conditions.\n"
        f"### Expiration & Assignment Risk\n"
        f"Evaluate risks related to the chosen expiration dates and potential for early assignment.\n"
        # f"### Management Checklist\n"
        # f"Provide a detailed pointed checklist for variables like DTE, greeks, underlying price, technical indicator at Point in time, where action of some sort is required.\n\n"
        f"### Current Risk & Reward Profile\n"
        f"- Max profit/loss potential remaining\n"
        f"- Current greeks exposure (if provided)\n"
        f"- Key risks (assignment, pin risk, vol crush, etc.)\n"
        f"### Greeks & Market Context Interpretation\n"
        f"Explain how current Greeks interact with today's technicals, **Recent Candlestick Patterns**, & forecast\n"
        f"### Directional Exposure (Delta/Gamma)\n"
        f"Explain how the position reacts to price moves and how that sensitivity changes.\n"
        f"### Volatility Sensitivity (Vega)\n"
        f"Explain how an increase or decrease in implied volatility will affect the P&L.\n"
        f"### Time Decay (Theta)\n"
        f"Explain how much value the position gains or loses daily from the passage of time.\n"
        f"### Risk Summary\n"
        f"A brief summary of the dominant risk factor for this position right now. Break it down by DTE groups.\n\n"
        f"### Management Recommendation\n"
        f"Detailed action plan:\n"
        f"- Hold: under what conditions?\n"
        f"- Exit: target price or P&L level?\n"
        f"- Roll: suggested strikes/expiries (be specific)\n"
        f"- Details : Provide a detailed recommendation: Should the user exit now to lock in profits/limit losses, hold for further decay/move, or roll to a new strike/expiry? Provide specific targets. "
        f"If you provide price targets or action triggers, ensure they are formatted as 'Price > 450' or 'Underlying at 460' for visual plotting.\n\n"
        f"### Action Checklist (Triggers)\n"
        f"Bullet list of conditions that should trigger immediate review or action. Provide conditions against most of the relevant input values. Provide markup table with following fields Ticker, Variable, Description, Current Value, Condition, Action Required, Justification, Risk/Reward, Horizon, Delta, Gamma, Vega, Theta\n"
        f'(e.g. "Delta > 0.75", "DTE < 21", "IV Rank drops below 30", etc.)\n'
        f"### Management Checklist\n"
        f"Provide a detailed pointed checklist with description for above variables for point in time, where action is required. Provide markup table with following fields Ticker, Variable, Description, Current Value, Action Required, Justification, Risk/Reward, Horizon, Delta, Gamma, Vega, Theta\n\n"
        f"### Alternative Recommendation\n"
        f"Provide an alternative strategy recommendation, with strike prices and acceptable Bid/Mid/Ask values. Provide specific targets. **Mathematical Accuracy**: You MUST provide REALISTIC non-zero estimates for mid/bid/ask and Greeks (Delta, Gamma, Vega, Theta) for any suggested trade or roll based on the provided market context. Do NOT use 0.0 or N/A.\n\n"
        f"### Trade Ticket\n"
        f"If you recommend an alternative strategy or a roll, provide a single structured JSON block representing the strategy legs. Use exactly this format:\n"
        f"```json\n"
        f"{{\n"
        f'  "action_type": "alternative" | "roll",\n'
        f'  "strategy_name": "Name of strategy",\n'
        f'  "risk_reward": "1:3",\n'
        f'  "horizon": "10 days",\n'
        f'  "legs": [\n'
        f'    {{"action": "buy"|"sell", "type": "call"|"put", "strike": price, "expiry": "YYYY-MM-DD", "qty": quantity}}\n'
        f"  ]\n"
        f"}}\n"
        f"```\n\n"
        f"### Monitoring Guard Rules\n"
        f"Provide a structured JSON block for monitoring this position's health. Use GoRules (Zen Engine) compatible format. "
        f"Focus on the following set input fields: `pnl_pct`, `days_to_expiry`, `underlying_price`, `delta`, `gamma`, `vega`, `theta`, and leg level greeks like `leg1_delta`, `leg1_gamma`, etc. "
        f"Use exactly this format and provide as many checks as possible:\n"
        f"```json\n"
        f"{{\n"
        f'  "contentType": "application/vnd.gorules.decision",\n'
        f'  "nodes": [\n'
        f'    {{"id": "input-node", "type": "inputNode", "name": "Input"}},\n'
        f'    {{"id": "output-node", "type": "outputNode", "name": "Output"}},\n'
        f'    {{"id": "guard-table", "type": "decisionTableNode", "name": "Trade Guard Rules", "content": {{\n'
        f'      "hitPolicy": "collect",\n'
        f'      "inputs": [\n'
        f'        {{"id": "pnl-pct", "field": "pnl_pct", "name": "P&L %"}},\n'
        f'        {{"id": "dte", "field": "days_to_expiry", "name": "DTE"}},\n'
        f'        {{"id": "spot", "field": "underlying_price", "name": "Spot Price"}},\n'
        f'        {{"id": "delta", "field": "delta", "name": "Delta"}},\n'
        f'        {{"id": "gamma", "field": "gamma", "name": "Gamma"}},\n'
        f'        {{"id": "theta", "field": "theta", "name": "Theta"}},\n'
        f'        {{"id": "vega", "field": "vega", "name": "Vega"}},\n'
        f'        {{"id": "leg1-delta", "field": "leg1_delta", "name": "Leg 1 Delta"}},\n'
        f'        {{"id": "leg1-gamma", "field": "leg1_gamma", "name": "Leg 1 Gamma"}},\n'
        f'        {{"id": "leg1-theta", "field": "leg1_theta", "name": "Leg 1 Theta"}},\n'
        f'        {{"id": "leg1-vega", "field": "leg1_vega", "name": "Leg 1 Vega"}},\n'
        f'        {{"id": "leg2-delta", "field": "leg2_delta", "name": "Leg 2 Delta"}},\n'
        f'        {{"id": "leg2-gamma", "field": "leg2_gamma", "name": "Leg 2 Gamma"}},\n'
        f'        {{"id": "leg2-theta", "field": "leg2_theta", "name": "Leg 2 Theta"}},\n'
        f'        {{"id": "leg2-vega", "field": "leg2_vega", "name": "Leg 2 Vega"}}\n'
        f"      ],\n"
        f'      "outputs": [\n'
        f'        {{"id": "severity", "field": "severity", "name": "Severity"}},\n'
        f'        {{"id": "action", "field": "action", "name": "Action"}},\n'
        f'        {{"id": "target", "field": "target", "name": "Target"}},\n'
        f'        {{"id": "message", "field": "message", "name": "Message"}}\n'
        f"      ],\n"
        f'      "rules": [\n'
        f'        {{"_id": "r1", "pnl-pct": "<= -30", "severity": "\\"critical\\"", "action": "\\"exit\\"","target": "\\"leg1-delta\\"", "message": "\\"Max loss reached\\""}}\n'
        f"      ]\n"
        f"    }}}}\n"
        f"  ],\n"
        f'  "edges": [\n'
        f'    {{"id": "e1", "sourceId": "input-node", "targetId": "guard-table"}},\n'
        f'    {{"id": "e2", "sourceId": "guard-table", "targetId": "output-node"}}\n'
        f"  ]\n"
        f"}}\n"
        f"```\n\n"
        f"Formatting Guidelines:\n"
        f"- Use ### for headers.\n"
        f"- Use **bold** for emphasis.\n"
        f"- Use bullet points for lists.\n"
        f"- Keep the tone professional, objective, and concise."
    )
