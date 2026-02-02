"""
Tests for single layer pleated shades from BSDF XML files.

Based on WinCalc test patterns for pleated shades.
Note: genBSDF products lack conductivity data, so only optical tests are run.
"""
import pytest
import pywincalc

from util import (
    check_optical_results,
)


class TestPleatedShadeCgdb24040:
    """Test suite for pleated shade from BSDF XML (cgdb_24040).

    Note: Thermal tests skipped - genBSDF product lacks conductivity data.
    """

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "cgdb_24040_Intigral_SL_Vanity_C000_White_Pleated_Shade_20mm_genBSDF.xml"
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
            test_name="1_layer/pleated_shade_genBSDF_cgdb_24040/full_basis",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/pleated_shade_genBSDF_cgdb_24040/full_basis",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )
