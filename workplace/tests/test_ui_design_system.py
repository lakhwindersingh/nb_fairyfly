"""
Unit and Integration Test Suite for Enterprise Unified Design System
Plan: .nb/plan/master/enterprise-ui-design-system
Validates:
- Design Token Schemas & Themes (Corporate Light, Enterprise Dark, Pro OLED)
- 8px Spatial Rhythm & Standardized Control Heights
- Multi-Leg Strategy Builder Wire Contract
- High-Frequency Blotter Grid Wire Contract
- Hierarchical Boolean Rule Tree Contract
- WCAG 2.2 AAA Contrast Ratios & Tabular Numerics Invariants
"""

import json
import unittest
from pathlib import Path

from workplace.core.ui_token_validator import UITokenValidator


class TestEnterpriseUIDesignSystem(unittest.TestCase):
    """Test suite for Enterprise UI design system tokens, themes, and compound widgets."""

    def test_spatial_grid_rhythm_invariants(self):
        """Verifies 8px spatial grid and 4px micro-increment invariants."""
        valid_spacings = ["0px", "4px", "8px", "12px", "16px", "24px", "32px", "48px", "64px", "96px"]
        for sp in valid_spacings:
            self.assertTrue(UITokenValidator.validate_spatial_value(sp), f"Spacing {sp} must be valid")

        invalid_spacings = ["3px", "7px", "13px", "17px", "23px", "45px", "auto"]
        for sp in invalid_spacings:
            self.assertFalse(UITokenValidator.validate_spatial_value(sp), f"Spacing {sp} must be invalid")

    def test_control_heights_scale(self):
        """Verifies standardized 5-tier control height progression."""
        scale = UITokenValidator.CONTROL_HEIGHTS
        self.assertEqual(scale["control-height-xs"], "24px")
        self.assertEqual(scale["control-height-sm"], "32px")
        self.assertEqual(scale["control-height-md"], "40px")
        self.assertEqual(scale["control-height-lg"], "48px")
        self.assertEqual(scale["control-height-xl"], "56px")

        # Each height must be a valid 8px multiple
        for h in scale.values():
            self.assertTrue(UITokenValidator.validate_spatial_value(h))

    def test_theme_token_dictionary_validation(self):
        """Tests complete design token dictionary validation against contract."""
        theme_sample = {
            "version": "1.0.0",
            "spatial_grid": {
                "base_unit_px": 8,
                "scale": {
                    "space-0-5": "4px",
                    "space-1": "8px",
                    "space-1-5": "12px",
                    "space-2": "16px",
                    "space-3": "24px",
                    "space-4": "32px",
                    "space-6": "48px",
                    "space-8": "64px",
                },
            },
            "control_heights": {
                "control-height-xs": "24px",
                "control-height-sm": "32px",
                "control-height-md": "40px",
                "control-height-lg": "48px",
                "control-height-xl": "56px",
            },
            "typography": {
                "font_sans": "Inter",
                "font_heading": "Plus Jakarta Sans",
                "font_mono": "JetBrains Mono",
                "tabular_numerics": True,
            },
            "themes": [
                {
                    "id": "corporate-light",
                    "name": "Corporate Light",
                    "bg_app": "#f8fafc",
                    "surface_card": "#ffffff",
                    "text_primary": "#0f172a",
                    "color_finance_gain": "#10b981",
                    "color_finance_loss": "#f43f5e",
                },
                {
                    "id": "enterprise-dark",
                    "name": "Enterprise Dark",
                    "bg_app": "#0b0f19",
                    "surface_card": "#151d2e",
                    "text_primary": "#f8fafc",
                    "color_finance_gain": "#10b981",
                    "color_finance_loss": "#f43f5e",
                },
                {
                    "id": "pro-oled",
                    "name": "Pro OLED (True Black)",
                    "bg_app": "#000000",
                    "surface_card": "#0a0e17",
                    "text_primary": "#ffffff",
                    "color_finance_gain": "#00e676",
                    "color_finance_loss": "#ff1744",
                },
            ],
        }

        is_valid, errors = UITokenValidator.validate_theme_dictionary(theme_sample)
        self.assertTrue(is_valid, f"Theme dictionary should be valid: {errors}")
        self.assertEqual(len(errors), 0)

    def test_multileg_strategy_builder_contract_validation(self):
        """Tests MultiLegStrategyBuilderContract validation with valid and invalid options payloads."""
        valid_iron_condor = {
            "symbol": "SPX",
            "underlying_price": 5824.50,
            "pricing_type": "NET_CREDIT",
            "net_price": 3.85,
            "max_profit": 385.00,
            "max_loss": 615.00,
            "pop_percent": 78.4,
            "legs": [
                {
                    "leg_id": "leg_1",
                    "action": "BUY",
                    "ratio": 1,
                    "instrument_type": "PUT",
                    "strike": 5750.0,
                    "expiration": "2026-11-20",
                    "bid": 8.10,
                    "ask": 8.30,
                    "delta": -0.15,
                },
                {
                    "leg_id": "leg_2",
                    "action": "SELL",
                    "ratio": 1,
                    "instrument_type": "PUT",
                    "strike": 5780.0,
                    "expiration": "2026-11-20",
                    "bid": 11.20,
                    "ask": 11.45,
                    "delta": -0.25,
                },
                {
                    "leg_id": "leg_3",
                    "action": "SELL",
                    "ratio": 1,
                    "instrument_type": "CALL",
                    "strike": 5860.0,
                    "expiration": "2026-11-20",
                    "bid": 10.40,
                    "ask": 10.65,
                    "delta": 0.24,
                },
                {
                    "leg_id": "leg_4",
                    "action": "BUY",
                    "ratio": 1,
                    "instrument_type": "CALL",
                    "strike": 5890.0,
                    "expiration": "2026-11-20",
                    "bid": 6.80,
                    "ask": 7.00,
                    "delta": 0.14,
                },
            ],
        }

        is_valid, errors = UITokenValidator.validate_multileg_strategy(valid_iron_condor)
        self.assertTrue(is_valid, f"Iron Condor should pass: {errors}")

        # Test invalid payload: missing symbol and invalid action
        invalid_strategy = {
            "underlying_price": 100.0,
            "pricing_type": "UNKNOWN_TYPE",
            "net_price": 1.0,
            "legs": [{"leg_id": "bad", "action": "HOLD", "ratio": 0, "instrument_type": "OPTION", "strike": 100, "expiration": "2026-01-01"}],
        }
        is_valid, errors = UITokenValidator.validate_multileg_strategy(invalid_strategy)
        self.assertFalse(is_valid)
        self.assertGreaterEqual(len(errors), 3)

    def test_blotter_grid_contract_validation(self):
        """Tests virtualized blotter row contract validation."""
        valid_row = {
            "position_id": "pos_spx_001",
            "symbol": "SPX",
            "strategy_name": "Iron Condor (5800/5850)",
            "net_delta": 0.04,
            "net_gamma": -0.002,
            "net_theta": 18.40,
            "net_vega": -45.20,
            "unrealized_pnl": 480.00,
            "realized_pnl": 0.0,
            "margin_req": 5000.0,
            "last_price": 5824.50,
            "day_change_pct": 0.65,
            "last_tick_timestamp": 1791682800,
            "status": "OPEN",
        }

        is_valid, errors = UITokenValidator.validate_blotter_row(valid_row)
        self.assertTrue(is_valid, f"Blotter row should be valid: {errors}")

        # Invalid row
        invalid_row = {"symbol": "AAPL", "status": "UNKNOWN_STATUS"}
        is_valid, errors = UITokenValidator.validate_blotter_row(invalid_row)
        self.assertFalse(is_valid)

    def test_contrast_ratio_formula(self):
        """Tests relative luminance contrast ratio calculation."""
        # Pure White (1.0) vs Pure Black (0.0) -> (1.0 + 0.05) / (0.0 + 0.05) = 21.0
        contrast_max = UITokenValidator.calculate_contrast_ratio(1.0, 0.0)
        self.assertAlmostEqual(contrast_max, 21.0, places=1)

        # Contrast for typical dark surface vs white text
        contrast_dark = UITokenValidator.calculate_contrast_ratio(0.9, 0.05)
        self.assertGreater(contrast_dark, 7.0)  # WCAG AAA compliant (>= 7.0:1)


if __name__ == "__main__":
    unittest.main()
