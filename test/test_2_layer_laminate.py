"""
Tests for 2-layer glazing systems with laminate glass.

Based on WinCalc test patterns for laminate configurations.
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
)


class TestLaminateNfrc18000WithClear:
    """Test suite for laminate (nfrc_18000) + clear glass (CLEAR_3)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        laminate_path = products_dir / "nfrc_18000.json"
        clear_path = products_dir / "CLEAR_3.json"

        laminate_glass = pywincalc.parse_json_file(str(laminate_path))
        clear_glass = pywincalc.parse_json_file(str(clear_path))

        self.standard = pywincalc.load_standard(str(standard_path))

        # Create air gap (12.7mm)
        air_gap = pywincalc.Layers.gap(thickness=0.0127)

        # Use quarter BSDF basis for laminate
        bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.QUARTER)

        # Laminate on exterior, clear on interior
        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[laminate_glass, clear_glass],
            gap_layers=[air_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments(),
            bsdf_hemisphere=bsdf_hemisphere
        )

        self.glazing_system_shgc = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[laminate_glass, clear_glass],
            gap_layers=[air_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_shgc_environments(),
            bsdf_hemisphere=bsdf_hemisphere
        )

    def test_thermal_u_environment(self, update_results):
        check_thermal_results(
            test_name="2_layers/laminate_nfrc_18000_air_nfrc_102/quarter_basis",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="2_layers/laminate_nfrc_18000_air_nfrc_102/quarter_basis",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="2_layers/laminate_nfrc_18000_air_nfrc_102/quarter_basis",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="2_layers/laminate_nfrc_18000_air_nfrc_102/quarter_basis",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )
