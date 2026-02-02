"""
Tests for single layer clear glass (NFRC 102 / CLEAR_3).

Based on WinCalc test pattern: 1_layer_nfrc_102.unit.cpp
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
)


class TestSingleLayerClearGlass:
    """Test suite for single layer clear glass (CLEAR_3.json)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        # Load product data
        product_path = products_dir / "CLEAR_3.json"
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
            test_name="1_layer/nfrc_102/default",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_thermal_shgc_environment(self, update_results):
        """Test thermal results with SHGC environment."""
        check_thermal_results(
            test_name="1_layer/nfrc_102/default",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_solar(self, update_results):
        """Test solar optical results."""
        check_optical_results(
            test_name="1_layer/nfrc_102/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_photopic(self, update_results):
        """Test photopic (visible) optical results."""
        check_optical_results(
            test_name="1_layer/nfrc_102/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )


class TestSingleLayerClearGlassAngled:
    """Test suite for single layer clear glass at oblique angles."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        # Load product data
        product_path = products_dir / "CLEAR_3.json"
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

    @pytest.mark.parametrize("theta,phi", [(15, 270)])
    def test_optical_solar_angled(self, update_results, theta, phi):
        """Test solar optical results at oblique angle."""
        check_optical_results(
            test_name="1_layer/nfrc_102/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=theta,
            phi=phi
        )

    @pytest.mark.parametrize("theta,phi", [(15, 270)])
    def test_optical_photopic_angled(self, update_results, theta, phi):
        """Test photopic optical results at oblique angle."""
        check_optical_results(
            test_name="1_layer/nfrc_102/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=theta,
            phi=phi
        )
