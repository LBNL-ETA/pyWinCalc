"""
Tests for 2-layer glazing systems with CGDB venetian blinds.

Based on WinCalc test patterns for CGDB venetian blinds with glass.
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
)


class TestVenetianCgdb3001WithGlass:
    """Test suite for CGDB venetian blind (cgdb_3001) + clear glass."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        # Load products
        clear_path = products_dir / "CLEAR_3.json"
        venetian_path = products_dir / "cgdb_3001.json"

        clear_glass = pywincalc.parse_json_file(str(clear_path))
        venetian_blind = pywincalc.parse_json_file(str(venetian_path))

        # Load optical standard
        self.standard = pywincalc.load_standard(str(standard_path))

        # Create air gap (12.7mm)
        air_gap = pywincalc.Layers.gap(thickness=0.0127)

        # Use full BSDF basis for CGDB venetian blinds
        bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.FULL)

        # Venetian blind on exterior, clear glass on interior
        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[venetian_blind, clear_glass],
            gap_layers=[air_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments(),
            bsdf_hemisphere=bsdf_hemisphere
        )

        self.glazing_system_shgc = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[venetian_blind, clear_glass],
            gap_layers=[air_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_shgc_environments(),
            bsdf_hemisphere=bsdf_hemisphere
        )

    def test_thermal_u_environment(self, update_results):
        check_thermal_results(
            test_name="2_layers/venetian_cgdb_3001_air_nfrc_102/full_basis",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="2_layers/venetian_cgdb_3001_air_nfrc_102/full_basis",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="2_layers/venetian_cgdb_3001_air_nfrc_102/full_basis",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="2_layers/venetian_cgdb_3001_air_nfrc_102/full_basis",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )
