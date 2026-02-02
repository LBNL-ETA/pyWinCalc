"""
Tests for special single layer products (PV, woven shade, perforated screen).

Based on WinCalc test patterns.
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
)


class TestSingleLayerPvGeneric:
    """Test suite for single layer photovoltaic glass (generic_pv)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "generic_pv.json"
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
            test_name="1_layer/pv_generic/default",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/pv_generic/default",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/pv_generic/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/pv_generic/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )


class TestSingleLayerPerforatedScreen:
    """Test suite for single layer perforated screen (cgdb_18000)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "cgdb_18000.json"
        self.product = pywincalc.parse_json_file(str(product_path))
        self.standard = pywincalc.load_standard(str(standard_path))

        # Use full BSDF basis for perforated screen
        bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.FULL)

        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[self.product],
            gap_layers=[],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments(),
            bsdf_hemisphere=bsdf_hemisphere
        )

        self.glazing_system_shgc = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[self.product],
            gap_layers=[],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_shgc_environments(),
            bsdf_hemisphere=bsdf_hemisphere
        )

    def test_thermal_u_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/perforated_screen_cgdb_18000/full_basis",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/perforated_screen_cgdb_18000/full_basis",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/perforated_screen_cgdb_18000/full_basis",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/perforated_screen_cgdb_18000/full_basis",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )
