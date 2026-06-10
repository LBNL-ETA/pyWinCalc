"""
Tests for double layer vacuum glazing (CLEAR_3 + vacuum + CLEAR_3).

Based on WinCalc test pattern: 2_layers_nfrc_102_vacuum_nfrc_102.unit.cpp
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
    check_color_results,
)


class TestDoubleVacuumGlassCylindrical:
    """Test suite for double layer vacuum glazing with cylindrical pillars."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        # Load product data
        product_path = products_dir / "CLEAR_3.json"
        clear_glass = pywincalc.parse_json_file(str(product_path))

        # Load optical standard
        self.standard = pywincalc.load_standard(str(standard_path))

        # Create vacuum gap with cylindrical pillars
        pillar_height = 0.0001
        gap_pressure = 0.1333
        pillar_conductivity = 999.0
        pillar_area = 0.03 * 0.03
        pillar_radius = 0.0002

        pillar = pywincalc.CylindricalPillar(
            height=pillar_height,
            material_conductivity=pillar_conductivity,
            cell_area=pillar_area,
            radius=pillar_radius
        )
        vacuum_gap = pywincalc.Layers.create_pillar(pillar, gap_pressure)

        # Create glazing system with U-value environment
        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[clear_glass, clear_glass],
            gap_layers=[vacuum_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments()
        )

        # Create glazing system with SHGC environment
        self.glazing_system_shgc = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[clear_glass, clear_glass],
            gap_layers=[vacuum_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_shgc_environments()
        )

    def test_thermal_u_environment(self, update_results):
        """Test thermal results with U-value environment."""
        check_thermal_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/cylindrical",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_thermal_shgc_environment(self, update_results):
        """Test thermal results with SHGC environment."""
        check_thermal_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/cylindrical",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/cylindrical",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/cylindrical",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_tdw(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/cylindrical",
            method_name="TDW",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_tkr(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/cylindrical",
            method_name="TKR",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_tuv(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/cylindrical",
            method_name="TUV",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_color(self, update_results):
        check_color_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/cylindrical",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )


class TestDoubleVacuumGlassSpherical:
    """Test suite for double layer vacuum glazing with spherical pillars."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        # Load product data
        product_path = products_dir / "CLEAR_3.json"
        clear_glass = pywincalc.parse_json_file(str(product_path))

        # Load optical standard
        self.standard = pywincalc.load_standard(str(standard_path))

        # Create vacuum gap with spherical pillars
        pillar_height = 0.0001
        gap_pressure = 0.1333
        pillar_conductivity = 999.0
        pillar_area = 0.03 * 0.03
        radius_of_contact = 0.02e-3

        pillar = pywincalc.SphericalPillar(
            height=pillar_height,
            material_conductivity=pillar_conductivity,
            cell_area=pillar_area,
            radius_of_contact=radius_of_contact
        )
        vacuum_gap = pywincalc.Layers.create_pillar(pillar, gap_pressure)

        # Create glazing system with U-value environment
        self.glazing_system_u = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[clear_glass, clear_glass],
            gap_layers=[vacuum_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments()
        )

        # Create glazing system with SHGC environment
        self.glazing_system_shgc = pywincalc.GlazingSystem(
            optical_standard=self.standard,
            solid_layers=[clear_glass, clear_glass],
            gap_layers=[vacuum_gap],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_shgc_environments()
        )

    def test_thermal_u_environment(self, update_results):
        """Test thermal results with U-value environment."""
        check_thermal_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/spherical",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_thermal_shgc_environment(self, update_results):
        """Test thermal results with SHGC environment."""
        check_thermal_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/spherical",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/spherical",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/spherical",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_tdw(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/spherical",
            method_name="TDW",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_tkr(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/spherical",
            method_name="TKR",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_optical_tuv(self, update_results):
        check_optical_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/spherical",
            method_name="TUV",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )

    def test_color(self, update_results):
        check_color_results(
            test_name="2_layers/nfrc_102_vacuum_nfrc_102/spherical",
            glazing_system=self.glazing_system_u,
            update_results=update_results,
            theta=0,
            phi=0
        )
