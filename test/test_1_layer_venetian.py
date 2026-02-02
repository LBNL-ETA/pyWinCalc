"""
Tests for single layer venetian blinds from CGDB.

Based on WinCalc test patterns for venetian blinds.
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
)


class TestVenetianCgdb24000Open:
    """Test suite for venetian blind from CGDB (24000) - Open position."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "cgdb_24000_Alabaster Venetian Blind Open (Intigral)_Alabaster_0_12.5.json"
        self.product = pywincalc.parse_json_file(str(product_path))
        self.standard = pywincalc.load_standard(str(standard_path))

        # Use full BSDF basis
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
            test_name="1_layer/venetian_cgdb_24000/full_basis",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/venetian_cgdb_24000/full_basis",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/venetian_cgdb_24000/full_basis",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/venetian_cgdb_24000/full_basis",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )


class TestVenetianCgdb24001Closed:
    """Test suite for venetian blind from CGDB (24001) - Closed position (+70 degrees)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "cgdb_24001_Alabaster Venetian Blind Closed (Intigral)_Alabaster_+70_12.5.json"
        self.product = pywincalc.parse_json_file(str(product_path))
        self.standard = pywincalc.load_standard(str(standard_path))

        # Use full BSDF basis
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
            test_name="1_layer/venetian_cgdb_24001/full_basis",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/venetian_cgdb_24001/full_basis",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/venetian_cgdb_24001/full_basis",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/venetian_cgdb_24001/full_basis",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )


class TestVenetianCgdb24002Angled:
    """Test suite for venetian blind from CGDB (24002) - +45 degree position."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "cgdb_24002_Alabaster Venetian Blind +45 (Intigral)_Alabaster_+45_12.5.json"
        self.product = pywincalc.parse_json_file(str(product_path))
        self.standard = pywincalc.load_standard(str(standard_path))

        # Use full BSDF basis
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
            test_name="1_layer/venetian_cgdb_24002/full_basis",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/venetian_cgdb_24002/full_basis",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/venetian_cgdb_24002/full_basis",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/venetian_cgdb_24002/full_basis",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )
