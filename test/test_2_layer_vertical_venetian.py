"""
Tests for 2-layer glazing systems with vertical venetian blinds.

Based on WinCalc test patterns for vertical venetian configurations.
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
)


class TestVerticalVenetianUserGeometry:
    """Test suite for vertical venetian blind with user-defined geometry + clear glass."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        # Load products
        clear_path = products_dir / "CLEAR_3.json"
        shade_material_path = products_dir / "pella_white_venetian_blind_slat.json"

        clear_glass = pywincalc.parse_json_file(str(clear_path))
        shade_material = pywincalc.parse_json_file(str(shade_material_path))

        # Create vertical venetian blind geometry: slat_tilt=45, slat_width=0.03, slat_spacing=0.08, slat_curvature=0.03
        # is_horizontal=False indicates vertical blinds
        geometry = pywincalc.VenetianGeometry(
            slat_tilt_degrees=45,
            slat_width_meters=0.03,
            slat_spacing_meters=0.08,
            slat_curvature_meters=0.03,
            is_horizontal=False
        )
        venetian_blind = pywincalc.create_venetian_blind(geometry, shade_material)

        # Load optical standard
        self.standard = pywincalc.load_standard(str(standard_path))

        # Create air gap (12.7mm)
        air_gap = pywincalc.Layers.gap(thickness=0.0127)

        # Use quarter BSDF basis for venetian blinds
        bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.QUARTER)

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
            test_name="2_layers/vertical_venetian_pella_white_venetian_blind_slat_user_geometry_air_nfrc_102/quarter_basis",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="2_layers/vertical_venetian_pella_white_venetian_blind_slat_user_geometry_air_nfrc_102/quarter_basis",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="2_layers/vertical_venetian_pella_white_venetian_blind_slat_user_geometry_air_nfrc_102/quarter_basis",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="2_layers/vertical_venetian_pella_white_venetian_blind_slat_user_geometry_air_nfrc_102/quarter_basis",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )
