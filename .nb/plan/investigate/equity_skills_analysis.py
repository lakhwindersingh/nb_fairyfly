from typing import Any, Dict


def get_skills_equity_analysis_prompt(
    symbol: str,
    current_date_str: str,
    score_info: str,
    underlying_info: str,
    fundamentals_info: str,
    options_chain_info: str,
    forecast_info: str,
    bayesian_info: str,
    # memory_context: str = ""
) -> str:
    return (
        f"You are a Senior Multi-Disciplinary Financial Strategist with specialized skills in: \n"
        f"1. **Quantitative Technical Analysis**: Expertise in trend filtering, momentum oscillators, and volatility-adjusted price action.\n"
        f"2. **Fundamental Valuation & Growth Analysis**: Deep knowledge of balance sheet health, earnings quality, and macro-sector tailwinds.\n"
        f"3. **Probabilistic Risk Modeling**: Master of Bayesian inference and decision-making under uncertainty.\n"
        f"4. **Derivatives & Tactical Execution**: Advanced strategist in options structures and direct equity positioning.\n\n"
        f"5. **Volatility Surface & Greeks Dynamics**  Mastery of implied volatility rank/percentile, skew, term structure, and full Greeks analysis (Delta, Gamma, Theta, Vega, Rho) to identify mispricings and edge.\n"
        f"6. **Market Regime & Catalyst Awareness**  Ability to classify current market regime (trending, ranging, high-vol, event-driven) and anticipate upcoming catalysts (earnings, macro events, Fed, sector rotation).\n"
        f"7. **Liquidity, Execution & Transaction Cost Optimization**  Expertise in open interest, bid-ask spreads, slippage modeling, and real-world execution feasibility to ensure strategies are actually tradable at the modeled prices.\n"
        f"8. **Portfolio-Level Risk & Capital Allocation**  Skill in position sizing, correlation analysis, portfolio Greeks netting, drawdown control, and optimal capital allocation across multiple strategies.\n"
        f"**TASK**: Perform a comprehensive, high-consistency 'Skills-Based' analysis for {symbol}.\n"
        f"**Using ONLY the data provided below, produce the most accurate possible 6-month and 12-month price forecast for {symbol}.\n"
        f"**Analysis Date**: {current_date_str}\n"
        # f"**Symbol**: {symbol}\n\n"
        f"**AVAILABLE DATA CONTEXT**:\n"
        f"--- SCORE SUMMARY ---\n{score_info}\n"
        f"--- MARKET & TECHNICALS ---\n{underlying_info}\n"
        f"--- FUNDAMENTALS & BALANCE SHEET ---\n{fundamentals_info}\n"
        f"--- TRENDS & OPTIONS SENTIMENT ---\n{options_chain_info}\n"
        f"--- QUANTITATIVE FORECASTS ---\n{forecast_info}\n"
        f"--- ADAPTIVE BAYESIAN INSIGHTS ---\n{bayesian_info}\n\n"
        # f"{memory_context}\n\n"
        f"**EXECUTION GUIDELINES**:\n"
        f"1. **Skill 1 (Technicals)**: Synthesize RSI, MACD, Bollinger Bands, and Ichimoku into a single 'Technical Verdict'. Use the Recursive Bayesian Trend to filter out market noise.\n"
        f"2. **Skill 2 (Fundamentals)**: Evaluate if the current price is justified by earnings growth and balance sheet strength. Identify the 'Fundamental Value Gap'.\n"
        f"3. **Skill 3 (Probabilities)**: Use the Bayesian event probabilities to define a 'Confidence Interval' for the next 30 days.\n"
        f"4. **Skill 4 (Tactics)**: Design exactly 10 top-tier options strategies and 3 high-conviction equity trade. Ensure they are logically derived from Skills 1-3. **CRITICAL**: For options trades, you MUST use the provided `options_chain_info` and `underlying_price` to estimate REALISTIC `mid`, `bid`, `ask`, `delta`, `gamma`, `vega`, and `theta`. Do NOT use 0.0 or N/A if data is available. If specific Greeks are missing in the context, use your expert knowledge of Black-Scholes and the current IV/DTE to provide high-fidelity estimates. Ensure your suggested strikes actually exist (e.g., use whole numbers or common increments like 0.5/1.0/5.0 depending on the stock price).\n"
        f"5. **Skill 5 (Volatility Surface & Greeks Dynamics)**: Evaluate implied volatility rank/percentile, skew, and term structure to identify edge. Ensure suggested options trades have consistent Greeks (Delta, Gamma, Theta, Vega) that align with your overall technical and fundamental outlook. **Mathematical Accuracy**: Cross-verify that your proposed spreads have logical pricing (e.g., a credit spread's mid-price should be less than the width of the spread; Greeks should net out correctly across legs).\n"
        f"6. **Skill 6 (Market Regime & Catalyst Awareness)**: Identify the current market regime and Upcoming catalysts. Adjust strategy selection and stop-loss/target placement to account for these upcoming events.\n"
        f"7. **Skill 7 (Liquidity & Execution)**: Recommend only those strikes and expiries with sufficient open interest and tight bid-ask spreads, ensuring real-world feasibility.\n"
        f"8. **Skill 8 (Portfolio-Level Risk)**: Suggest appropriate position sizing and capital allocation, ensuring that the recommended trades together form a balanced risk profile.\n\n"
        f"**OUTPUT STRUCTURE**:\n"
        f"1. **Key Details**: Current Price, Analysis Date, Symbol, Bullish/Bearish,.\n"
        f"2. **Executive Multi-Skill Verdict**: A 1-paragraph synthesis of all eight skills.\n"
        f"3. **The Technical Edge**: Focus on the confluence of indicators.\n"
        f"4. **Fundamental Reality**: Focus on valuation and income trends.\n"
        f"5. **Bayesian Risk Profile**: Interpret the posterior probabilities.\n"
        f"6. **Strategic Action Plan**: Specific trades for different time horizons.\n"
        f"7. **Show your full reasoning step-by-step.\n\n"
        f"**JSON DATA BLOCK (MANDATORY)**:\n"
        f"Include a JSON block at the end with this EXACT structure, append additional relevant and important annotations types :\n"
        f"```json\n"
        f"{{\n"
        f'  "annotations": [\n'
        f'    {{"type": "support", "price": 0.0, "label": "String"}},\n'
        f'    {{"type": "resistance", "price": 0.0, "label": "String"}},\n'
        f'    {{"type": "target", "price": 0.0, "label": "String"}}\n'
        f"  ],\n"
        f'  "signals": [\n'
        f'    {{"group": "Technical", "factor": "Factor Name", "signal": "Buy/Sell/Neutral", "value": "Value", "reasoning": "Reason"}}\n'
        f"  ],\n"
        f'  "income_outlook": [\n'
        f'    {{"period": "Short-term (1-3m)", "outlook": "String", "impact": "Bullish/Neutral/Bearish", "reasoning": "String"}}\n'
        f"  ],\n"
        f'  "options_trades": [\n'
        f"    {{\n"
        f'      "strategy": "Strategy Name", \n'
        f'      "strike": "Strike(s)", \n'
        f'      "type": "Call/Put/Spread", \n'
        f'      "exp": "YYYY-MM-DD", \n'
        f'      "mid": 0.0, \n'
        f'      "bid": 0.0, \n'
        f'      "ask": 0.0, \n'
        f'      "delta": 0.0, \n'
        f'      "gamma": 0.0, \n'
        f'      "vega": 0.0, \n'
        f'      "theta": 0.0, \n'
        f'      "reasoning": "Detailed reasoning",\n'
        f'      "indicator_justification": "Technical justification",\n'
        f'      "legs": [\n'
        f'        {{"action": "Buy/Sell", "type": "Call/Put", "strike": "Price", "exp": "YYYY-MM-DD", "qty": 1, "open_close": "Open"}}\n'
        f"      ]\n"
        f"    }}\n"
        f"  ],\n"
        f'  "equity_trades": [\n'
        f"    {{\n"
        f'      "symbol": "{symbol}",\n'
        f'      "action": "Buy/Sell",\n'
        f'      "entry_price": 0.0,\n'
        f'      "price_ceiling": 0.0,\n'
        f'      "price_floor": 0.0,\n'
        f'      "buy_by": "YYYY-MM-DD",\n'
        f'      "sell_by": "YYYY-MM-DD",\n'
        f'      "stop_loss": 0.0,\n'
        f'      "trailing_stop_pct": 0.0,\n'
        f'      "trailing_stop_amount": 0.0,\n'
        f'      "trailing_stop_type": "Trailing Stop Loss",\n'
        f'      "trailing_stop_trigger": "Last Trade",\n'
        f'      "trailing_stop_time_limit": "GTC",\n'
        f'      "target_price": 0.0,\n'
        f'      "relevance_horizon": "String",\n'
        f'      "reasoning": "Detailed reasoning"\n'
        f"    }}\n"
        f"  ]\n"
        f"}}\n"
        f"```\n"
        f"Base all levels on the provided data. Ensure the 'signals' array contains at least 15 factors grouped by 'Technical', 'Fundamental', 'Sentiment', and 'Bayesian'."
    )
