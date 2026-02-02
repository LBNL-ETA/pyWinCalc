"""
Tests for single layer BSDF shades from XML files.

Based on WinCalc test patterns for BSDF shades.
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
)


class TestLouveredShadeBsdfXml:
    """Test suite for louvered shade from BSDF XML (SquareSlat_genBSDF.xml)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "SquareSlat_genBSDF.xml"
        self.product = pywincalc.parse_bsdf_xml_file(str(product_path))
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
            test_name="1_layer/louvered_shade_bsdf_xml/full_basis",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/louvered_shade_bsdf_xml/full_basis",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/louvered_shade_bsdf_xml/full_basis",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/louvered_shade_bsdf_xml/full_basis",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )


class TestCellularShadeBsdf:
    """Test suite for cellular shade from BSDF XML (CS03_genBSDF.xml).

    Note: Thermal tests skipped - product lacks conductivity data.
    """

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "CS03_genBSDF.xml"
        self.product = pywincalc.parse_bsdf_xml_file(str(product_path))
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

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/cellular_shade_CS03_genBSDF/full_basis",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/cellular_shade_CS03_genBSDF/full_basis",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )


class TestRomanShadeBsdf:
    """Test suite for roman shade from BSDF XML (roman_shade_FlatFoldTHM-2_GenBSDF.xml).

    Note: Thermal tests skipped - product lacks conductivity data.
    """

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "roman_shade_FlatFoldTHM-2_GenBSDF.xml"
        self.product = pywincalc.parse_bsdf_xml_file(str(product_path))
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

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/roman_shade_genBSDF/full_basis",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/roman_shade_genBSDF/full_basis",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )
