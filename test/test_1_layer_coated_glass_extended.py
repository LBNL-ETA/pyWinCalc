"""
Tests for additional single layer coated glass products.

Based on WinCalc test patterns.
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
    check_color_results,
)


class TestSingleLayerCoatedNfrc6046:
    """Test suite for single layer coated glass (nfrc_6046)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "nfrc_6046.json"
        self.product = pywincalc.parse_json_file(str(product_path))
        self.standard = pywincalc.load_standard(str(standard_path))

        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[self.product],
            gap_layers=[],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments()
        )

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
        check_thermal_results(
            test_name="1_layer/coated_nfrc_6046/default",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/coated_nfrc_6046/default",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_6046/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_6046/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_tdw(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_6046/default",
            method_name="TDW",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_tkr(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_6046/default",
            method_name="TKR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_tuv(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_6046/default",
            method_name="TUV",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_color(self, update_results):
        check_color_results(
            test_name="1_layer/coated_nfrc_6046/default",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )


class TestSingleLayerCoatedNfrc6400:
    """Test suite for single layer coated glass (nfrc_6400)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "nfrc_6400.json"
        self.product = pywincalc.parse_json_file(str(product_path))
        self.standard = pywincalc.load_standard(str(standard_path))

        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[self.product],
            gap_layers=[],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments()
        )

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
        check_thermal_results(
            test_name="1_layer/coated_nfrc_6400/default",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/coated_nfrc_6400/default",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_6400/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_6400/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_tdw(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_6400/default",
            method_name="TDW",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_tkr(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_6400/default",
            method_name="TKR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_tuv(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_6400/default",
            method_name="TUV",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_color(self, update_results):
        check_color_results(
            test_name="1_layer/coated_nfrc_6400/default",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )
