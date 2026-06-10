"""
Tests for triple layer clear glass (CLEAR_3 + air + CLEAR_3 + air + CLEAR_3).

Based on WinCalc test pattern: 3_layers_nfrc_102_air_nfrc_102_air_nfrc_102_deflection_triple_clear.unit.cpp
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
    check_color_results,
)


class TestTripleClearGlass:
    """Test suite for triple layer clear glass with air gaps."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        # Load product data
        product_path = products_dir / "CLEAR_3.json"
        clear_glass = pywincalc.parse_json_file(str(product_path))

        # Load optical standard
        self.standard = pywincalc.load_standard(str(standard_path))

        # Create air gaps (6mm and 25mm as in WinCalc test)
        air_gap_1 = pywincalc.Layers.gap(thickness=0.006)
        air_gap_2 = pywincalc.Layers.gap(thickness=0.025)

        # Create glazing system with U-value environment
        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[clear_glass, clear_glass, clear_glass],
            gap_layers=[air_gap_1, air_gap_2],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments()
        )

        # Create glazing system with SHGC environment
        self.glazing_system_shgc = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[clear_glass, clear_glass, clear_glass],
            gap_layers=[air_gap_1, air_gap_2],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_shgc_environments()
        )

    def test_thermal_u_environment(self, update_results):
        """Test thermal results with U-value environment."""
        check_thermal_results(
            test_name="3_layers/nfrc_102_air_nfrc_102_air_nfrc_102/default",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_thermal_shgc_environment(self, update_results):
        """Test thermal results with SHGC environment."""
        check_thermal_results(
            test_name="3_layers/nfrc_102_air_nfrc_102_air_nfrc_102/default",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_solar(self, update_results):
        """Test solar optical results."""
        check_optical_results(
            test_name="3_layers/nfrc_102_air_nfrc_102_air_nfrc_102/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_photopic(self, update_results):
        """Test photopic (visible) optical results."""
        check_optical_results(
            test_name="3_layers/nfrc_102_air_nfrc_102_air_nfrc_102/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_tdw(self, update_results):
        """Test TDW (Transmittance Damage Weighted) optical results."""
        check_optical_results(
            test_name="3_layers/nfrc_102_air_nfrc_102_air_nfrc_102/default",
            method_name="TDW",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_tkr(self, update_results):
        """Test TKR (Krochmann) optical results."""
        check_optical_results(
            test_name="3_layers/nfrc_102_air_nfrc_102_air_nfrc_102/default",
            method_name="TKR",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_tuv(self, update_results):
        """Test TUV (UV transmittance) optical results."""
        check_optical_results(
            test_name="3_layers/nfrc_102_air_nfrc_102_air_nfrc_102/default",
            method_name="TUV",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_color(self, update_results):
        """Test color results (RGB, Lab, Trichromatic)."""
        check_color_results(
            test_name="3_layers/nfrc_102_air_nfrc_102_air_nfrc_102/default",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )
