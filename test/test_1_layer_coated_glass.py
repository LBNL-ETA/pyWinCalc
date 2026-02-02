"""
Tests for single layer coated glass (NFRC 6046).

Based on WinCalc test pattern: 1_layer_coated_nfrc_6046.unit.cpp
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
)


class TestSingleLayerCoatedGlass:
    """Test suite for single layer coated glass (nfrc_6046.json)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        # Load product data
        product_path = products_dir / "nfrc_6046.json"
        self.product = pywincalc.parse_json_file(str(product_path))

        # Load optical standard
        self.standard = pywincalc.load_standard(str(standard_path))

        # Create glazing system with U-value environment
        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[self.product],
            gap_layers=[],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments()
        )

        # Create glazing system with SHGC environment
        self.glazing_system_shgc = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[self.product],
            gap_layers=[],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_shgc_environments()
        )

    def test_thermal_u_environment(self, update_results):
        """Test thermal results with U-value environment."""
        check_thermal_results(
            test_name="1_layer/coated_nfrc_6046/default",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_thermal_shgc_environment(self, update_results):
        """Test thermal results with SHGC environment."""
        check_thermal_results(
            test_name="1_layer/coated_nfrc_6046/default",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_solar(self, update_results):
        """Test solar optical results."""
        check_optical_results(
            test_name="1_layer/coated_nfrc_6046/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_photopic(self, update_results):
        """Test photopic (visible) optical results."""
        check_optical_results(
            test_name="1_layer/coated_nfrc_6046/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )
