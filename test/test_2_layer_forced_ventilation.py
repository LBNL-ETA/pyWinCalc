"""
Tests for 2-layer glazing systems with forced ventilation.

Based on WinCalc test patterns for forced ventilation gaps.
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
    check_color_results,
)


class TestDoubleGlassForcedVentilation:
    """Test suite for double clear glass with forced ventilation gap."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        clear_path = products_dir / "CLEAR_3.json"
        clear_glass = pywincalc.parse_json_file(str(clear_path))
        self.standard = pywincalc.load_standard(str(standard_path))

        # Create forced ventilation gap (12.7mm)
        gap_thickness = 0.0127
        gap_air_speed = 1.0
        gap_inlet_air_temperature = 294.15

        # First create a regular gap, then convert to forced ventilation
        gap_layer = pywincalc.Layers.gap(thickness=gap_thickness)
        ventilated_gap = pywincalc.Layers.forced_ventilation_gap(
            gap_layer,
            gap_air_speed,
            gap_inlet_air_temperature
        )

        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[clear_glass, clear_glass],
            gap_layers=[ventilated_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments()
        )

        self.glazing_system_shgc = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[clear_glass, clear_glass],
            gap_layers=[ventilated_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_shgc_environments()
        )

    def test_thermal_u_environment(self, update_results):
        check_thermal_results(
            test_name="2_layers/nfrc_102_air_nfrc_102/forced_ventilation",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="2_layers/nfrc_102_air_nfrc_102/forced_ventilation",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_air_nfrc_102/forced_ventilation",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_air_nfrc_102/forced_ventilation",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_tdw(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_air_nfrc_102/forced_ventilation",
            method_name="TDW",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_tkr(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_air_nfrc_102/forced_ventilation",
            method_name="TKR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_tuv(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_air_nfrc_102/forced_ventilation",
            method_name="TUV",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_color(self, update_results):
        check_color_results(
            test_name="2_layers/nfrc_102_air_nfrc_102/forced_ventilation",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )
