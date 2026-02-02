"""
Tests for 3-layer glazing systems with deflection calculations.

Based on WinCalc test patterns for triple clear glass deflection.
"""
import pytest
import pywincalc

from util import (
    check_deflection_results,
)


class TestTripleGlassDeflection:
    """Test suite for triple clear glass with deflection calculations."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        clear_path = products_dir / "CLEAR_3.json"
        clear_glass = pywincalc.parse_json_file(str(clear_path))
        self.standard = pywincalc.load_standard(str(standard_path))

        # Create two air gaps (6mm and 25mm like in test_3_layer_clear_glass.py)
        gap_1 = pywincalc.Layers.gap(thickness=0.006)
        gap_2 = pywincalc.Layers.gap(thickness=0.025)

        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[clear_glass, clear_glass, clear_glass],
            gap_layers=[gap_1, gap_2],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments()
        )

        self.glazing_system_shgc = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[clear_glass, clear_glass, clear_glass],
            gap_layers=[gap_1, gap_2],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_shgc_environments()
        )

    def test_deflection_off(self, update_results):
        check_deflection_results(
            test_name="3_layers/nfrc_102_air_nfrc_102_air_nfrc_102/deflection",
            results_name="deflection_off",
            glazing_system=self.glazing_system_u,
            system_type="U",
            update_results=update_results
        )

    def test_deflection_on_winter_u_run(self, update_results):
        self.glazing_system_u.enable_deflection(True)
        check_deflection_results(
            test_name="3_layers/nfrc_102_air_nfrc_102_air_nfrc_102/deflection",
            results_name="deflection_on_winter_u_run",
            glazing_system=self.glazing_system_u,
            system_type="U",
            update_results=update_results
        )

    def test_deflection_on_summer_shgc_run(self, update_results):
        self.glazing_system_shgc.enable_deflection(True)
        check_deflection_results(
            test_name="3_layers/nfrc_102_air_nfrc_102_air_nfrc_102/deflection",
            results_name="deflection_on_summer_shgc_run",
            glazing_system=self.glazing_system_shgc,
            system_type="SHGC",
            update_results=update_results
        )
