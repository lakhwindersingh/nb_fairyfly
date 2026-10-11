"""
Unit Tests for Enterprise UI Design System Tokens & Component Contracts
Verifies 8px spatial grid, control heights, multi-theme contracts,
and universal data grid row specifications.
"""

import unittest
from workplace.core.ui_token_validator import UITokenValidator


class TestUIDesignSystem(unittest.TestCase):
    """Test suite for Enterprise Unified Design System invariants and contracts."""

    def test_spatial_grid_8px_increments(self):
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
            "version": "2.0.0",
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
                    "color_status_success": "#10b981",
                    "color_status_error": "#f43f5e",
                },
                {
                    "id": "enterprise-dark",
                    "name": "Enterprise Dark",
                    "bg_app": "#0b0f19",
                    "surface_card": "#151d2e",
                    "text_primary": "#f8fafc",
                    "color_status_success": "#10b981",
                    "color_status_error": "#f43f5e",
                },
                {
                    "id": "pro-oled",
                    "name": "Pro OLED (True Black)",
                    "bg_app": "#000000",
                    "surface_card": "#0a0e17",
                    "text_primary": "#ffffff",
                    "color_status_success": "#00e676",
                    "color_status_error": "#ff1744",
                },
            ],
        }

        is_valid, errors = UITokenValidator.validate_theme_dictionary(theme_sample)
        self.assertTrue(is_valid, f"Theme dictionary should be valid: {errors}")
        self.assertEqual(len(errors), 0)

    def test_data_grid_contract_validation(self):
        """Tests virtualized data grid row contract validation."""
        valid_row = {
            "row_id": "service_gateway_01",
            "name": "API Context Gateway",
            "category": "Networking",
            "status": "ACTIVE",
            "primary_metric": 14280.0,
            "secondary_metric": 18.4,
            "change_pct": 2.5,
            "timestamp": 1791682800,
        }

        is_valid, errors = UITokenValidator.validate_data_grid_row(valid_row)
        self.assertTrue(is_valid, f"Data grid row should be valid: {errors}")

        # Invalid row: missing required fields and invalid status
        invalid_row = {"row_id": "service_02", "status": "UNKNOWN_STATUS"}
        is_valid, errors = UITokenValidator.validate_data_grid_row(invalid_row)
        self.assertFalse(is_valid)
        self.assertGreaterEqual(len(errors), 2)

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
