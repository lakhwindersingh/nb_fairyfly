"""
Script to instantiate Enterprise UI Design System contracts, rules, and subagents.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# 1. Contracts
contracts_dir = REPO_ROOT / ".nb" / "context" / "contracts"
contracts_dir.mkdir(parents=True, exist_ok=True)

theme_contract = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "UIThemeTokenContract",
    "description": "W3C Design Token Schema validating enterprise themes, typography, 8px spatial grid, and financial colors.",
    "type": "object",
    "required": ["version", "themes", "spatial_grid", "control_heights", "typography"],
    "properties": {
        "version": {"type": "string"},
        "spatial_grid": {
            "type": "object",
            "required": ["base_unit_px", "scale"],
            "properties": {
                "base_unit_px": {"type": "integer", "enum": [8]},
                "scale": {
                    "type": "object",
                    "required": ["space-0-5", "space-1", "space-2", "space-3", "space-4", "space-6", "space-8"],
                    "properties": {
                        "space-0-5": {"type": "string", "pattern": "^4px$"},
                        "space-1": {"type": "string", "pattern": "^8px$"},
                        "space-1-5": {"type": "string", "pattern": "^12px$"},
                        "space-2": {"type": "string", "pattern": "^16px$"},
                        "space-3": {"type": "string", "pattern": "^24px$"},
                        "space-4": {"type": "string", "pattern": "^32px$"},
                        "space-6": {"type": "string", "pattern": "^48px$"},
                        "space-8": {"type": "string", "pattern": "^64px$"},
                    },
                },
            },
        },
        "control_heights": {
            "type": "object",
            "required": ["control-height-xs", "control-height-sm", "control-height-md", "control-height-lg", "control-height-xl"],
            "properties": {
                "control-height-xs": {"type": "string", "pattern": "^24px$"},
                "control-height-sm": {"type": "string", "pattern": "^32px$"},
                "control-height-md": {"type": "string", "pattern": "^40px$"},
                "control-height-lg": {"type": "string", "pattern": "^48px$"},
                "control-height-xl": {"type": "string", "pattern": "^56px$"},
            },
        },
        "typography": {
            "type": "object",
            "required": ["font_sans", "font_heading", "font_mono", "tabular_numerics"],
            "properties": {
                "font_sans": {"type": "string"},
                "font_heading": {"type": "string"},
                "font_mono": {"type": "string"},
                "tabular_numerics": {"type": "boolean", "enum": [True]},
            },
        },
        "themes": {
            "type": "array",
            "minItems": 3,
            "items": {
                "type": "object",
                "required": ["id", "name", "bg_app", "surface_card", "text_primary", "color_finance_gain", "color_finance_loss"],
                "properties": {
                    "id": {"type": "string", "enum": ["corporate-light", "enterprise-dark", "pro-oled"]},
                    "name": {"type": "string"},
                    "bg_app": {"type": "string"},
                    "surface_card": {"type": "string"},
                    "text_primary": {"type": "string"},
                    "color_finance_gain": {"type": "string"},
                    "color_finance_loss": {"type": "string"},
                },
            },
        },
    },
}

multileg_contract = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "MultiLegStrategyBuilderContract",
    "type": "object",
    "required": ["symbol", "underlying_price", "legs", "net_price", "pricing_type"],
    "properties": {
        "symbol": {"type": "string"},
        "underlying_price": {"type": "number", "minimum": 0.0},
        "pricing_type": {"type": "string", "enum": ["NET_DEBIT", "NET_CREDIT", "EVEN"]},
        "net_price": {"type": "number"},
        "max_profit": {"type": "number"},
        "max_loss": {"type": "number"},
        "pop_percent": {"type": "number", "minimum": 0.0, "maximum": 100.0},
        "legs": {
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": {
                "type": "object",
                "required": ["leg_id", "action", "ratio", "instrument_type", "strike", "expiration"],
                "properties": {
                    "leg_id": {"type": "string"},
                    "action": {"type": "string", "enum": ["BUY", "SELL"]},
                    "ratio": {"type": "integer", "minimum": 1, "maximum": 10},
                    "instrument_type": {"type": "string", "enum": ["CALL", "PUT", "STOCK", "FUTURE"]},
                    "strike": {"type": "number", "minimum": 0.0},
                    "expiration": {"type": "string"},
                    "bid": {"type": "number"},
                    "ask": {"type": "number"},
                    "delta": {"type": "number", "minimum": -1.0, "maximum": 1.0},
                },
            },
        },
    },
}

blotter_contract = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "BlotterGridContract",
    "type": "object",
    "required": ["positions", "total_count", "unrealized_total_pnl"],
    "properties": {
        "total_count": {"type": "integer", "minimum": 0},
        "unrealized_total_pnl": {"type": "number"},
        "positions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["position_id", "symbol", "strategy_name", "net_delta", "net_gamma", "net_theta", "unrealized_pnl", "last_price", "status"],
                "properties": {
                    "position_id": {"type": "string"},
                    "symbol": {"type": "string"},
                    "strategy_name": {"type": "string"},
                    "net_delta": {"type": "number"},
                    "net_gamma": {"type": "number"},
                    "net_theta": {"type": "number"},
                    "net_vega": {"type": "number"},
                    "unrealized_pnl": {"type": "number"},
                    "realized_pnl": {"type": "number"},
                    "margin_req": {"type": "number"},
                    "last_price": {"type": "number"},
                    "day_change_pct": {"type": "number"},
                    "last_tick_timestamp": {"type": "integer"},
                    "status": {"type": "string", "enum": ["OPEN", "ADJUSTED", "ROLLED", "CLOSED"]},
                },
            },
        },
    },
}

rule_contract = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "HierarchicalRuleContract",
    "type": "object",
    "required": ["rule_id", "condition", "rules"],
    "properties": {
        "rule_id": {"type": "string"},
        "condition": {"type": "string", "enum": ["AND", "OR"]},
        "rules": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["field", "operator", "value"],
                "properties": {
                    "field": {"type": "string"},
                    "operator": {"type": "string", "enum": [">", ">=", "<", "<=", "==", "!=", "between", "in"]},
                    "value": {},
                },
            },
        },
    },
}

with open(contracts_dir / "ui_theme_token_contract.json", "w", encoding="utf-8") as f:
    json.dump(theme_contract, f, indent=2)

with open(contracts_dir / "multileg_strategy_builder_contract.json", "w", encoding="utf-8") as f:
    json.dump(multileg_contract, f, indent=2)

with open(contracts_dir / "blotter_grid_contract.json", "w", encoding="utf-8") as f:
    json.dump(blotter_contract, f, indent=2)

with open(contracts_dir / "hierarchical_rule_contract.json", "w", encoding="utf-8") as f:
    json.dump(rule_contract, f, indent=2)

print("Contracts created successfully.")
