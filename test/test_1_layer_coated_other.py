"""
Tests for additional single layer coated glass products.

Based on WinCalc test patterns for various coated glass products.
"""
import pytest
import pywincalc

from util import (
    check_thermal_results,
    check_optical_results,
)


class TestSingleLayerCoatedNfrc18100:
    """Test suite for single layer coated glass (nfrc_18100)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "nfrc_18100.json"
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
            test_name="1_layer/coated_nfrc_18100/default",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/coated_nfrc_18100/default",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_18100/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_18100/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )


class TestSingleLayerCoatedNfrc21467:
    """Test suite for single layer coated glass (nfrc_21467)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "nfrc_21467.json"
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
            test_name="1_layer/coated_nfrc_21467/default",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/coated_nfrc_21467/default",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_21467/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/coated_nfrc_21467/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )


class TestSingleLayerAppliedFilmNfrc9223:
    """Test suite for single layer applied film (nfrc_9223)."""

    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        """Set up glazing systems for testing."""
        product_path = products_dir / "nfrc_9223.json"
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
            test_name="1_layer/applied_film_nfrc_9223/default",
            results_name="thermal_U_Environment",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_thermal_shgc_environment(self, update_results):
        check_thermal_results(
            test_name="1_layer/applied_film_nfrc_9223/default",
            results_name="thermal_SHGC_Environment",
            glazing_system=self.glazing_system_shgc,
            update_results=update_results
        )

    def test_optical_solar(self, update_results):
        check_optical_results(
            test_name="1_layer/applied_film_nfrc_9223/default",
            method_name="SOLAR",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )

    def test_optical_photopic(self, update_results):
        check_optical_results(
            test_name="1_layer/applied_film_nfrc_9223/default",
            method_name="PHOTOPIC",
            glazing_system=self.glazing_system_u,
            update_results=update_results
        )
