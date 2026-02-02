"""
Tests for 2-layer glazing systems with various Low-E glass configurations.

Based on WinCalc test patterns for Low-E glass combinations.
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
)


class TestLowENfrc9962WithClear:
    """Test suite for Low-E (nfrc_9962) + clear glass (CLEAR_3)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        low_e_path = products_dir / "nfrc_9962.json"
        clear_path = products_dir / "CLEAR_3.json"

        low_e_glass = pywincalc.parse_json_file(str(low_e_path))
        clear_glass = pywincalc.parse_json_file(str(clear_path))

        self.standard = pywincalc.load_standard(str(standard_path))

        # Create air gap (12.7mm)
        air_gap = pywincalc.Layers.gap(thickness=0.0127)

        # Low-E on exterior (#2 surface), clear on interior
        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[low_e_glass, clear_glass],
            gap_layers=[air_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments()
        )

        self.glazing_system_shgc = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[low_e_glass, clear_glass],
            gap_layers=[air_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_shgc_environments()
        )

    def test_thermal_u_environment(self, update_results):
        check_thermal_results(
            test_name="2_layers/low_e_nfrc_9962_air_nfrc_102/default",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="2_layers/low_e_nfrc_9962_air_nfrc_102/default",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="2_layers/low_e_nfrc_9962_air_nfrc_102/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="2_layers/low_e_nfrc_9962_air_nfrc_102/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )


class TestLowENfrc11561WithClear:
    """Test suite for Low-E (nfrc_11561) + clear glass (CLEAR_3)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        low_e_path = products_dir / "nfrc_11561.json"
        clear_path = products_dir / "CLEAR_3.json"

        low_e_glass = pywincalc.parse_json_file(str(low_e_path))
        clear_glass = pywincalc.parse_json_file(str(clear_path))

        self.standard = pywincalc.load_standard(str(standard_path))

        # Create air gap (12.7mm)
        air_gap = pywincalc.Layers.gap(thickness=0.0127)

        # Low-E on exterior, clear on interior
        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[low_e_glass, clear_glass],
            gap_layers=[air_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments()
        )

        self.glazing_system_shgc = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[low_e_glass, clear_glass],
            gap_layers=[air_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_shgc_environments()
        )

    def test_thermal_u_environment(self, update_results):
        check_thermal_results(
            test_name="2_layers/low_e_nfrc_11561_air_nfrc_102/default",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="2_layers/low_e_nfrc_11561_air_nfrc_102/default",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="2_layers/low_e_nfrc_11561_air_nfrc_102/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="2_layers/low_e_nfrc_11561_air_nfrc_102/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )
