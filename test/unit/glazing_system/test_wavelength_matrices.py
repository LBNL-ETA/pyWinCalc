"""
Unit tests for the on-demand per-layer wavelength matrices
(src/bindings/glazing_system_bindings.cpp: populate_layer_wavelength_matrices,
and src/bindings/bsdf_bindings.cpp: MatrixAtWavelength).

Invariant-based - NO golden data. The matrices are huge (basis-size square per
wavelength per layer), so we assert structure/contract, not values:
  * opt-in: fields are None until populate_layer_wavelength_matrices is called
  * populated for a BSDF system, all four (front/back x T/R) lists filled
  * shape: each matrix is square with a consistent dimension; wavelengths finite
    and monotonic
  * no-op: a specular (non-BSDF) system leaves the fields None

SMALL basis is used to keep the matrices tiny and the test fast.
"""
import math

import pytest
import pywincalc


VENETIAN_PRODUCT = "cgdb_24000_Alabaster Venetian Blind Open (Intigral)_Alabaster_0_12.5.json"
METHOD = "SOLAR"


class TestBSDFBasisType:
    def test_expected_values_present_including_nano(self):
        for name in ("NANO", "SMALL", "QUARTER", "HALF", "FULL"):
            assert hasattr(pywincalc.BSDFBasisType, name)


class TestWavelengthMatricesBsdf:
    @pytest.fixture(autouse=True)
    def setup(self, products_dir, standard_path):
        standard = pywincalc.load_standard(str(standard_path))
        product = pywincalc.parse_json_file(str(products_dir / VENETIAN_PRODUCT))
        hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.SMALL)
        self.glazing_system = pywincalc.GlazingSystem(
            optical_standard=standard,
            solid_layers=[product],
            gap_layers=[],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments(),
            bsdf_hemisphere=hemisphere,
        )

    def test_opt_in_none_before_populate(self):
        results = self.glazing_system.optical_method_results(METHOD)
        front = results.layer_results[0].front
        assert front.transmittance_wavelength_matrices is None
        assert front.reflectance_wavelength_matrices is None

    def test_all_four_lists_populated(self):
        results = self.glazing_system.optical_method_results(METHOD)
        self.glazing_system.populate_layer_wavelength_matrices(results, METHOD)
        layer = results.layer_results[0]
        for side in (layer.front, layer.back):
            for matrices in (side.transmittance_wavelength_matrices,
                             side.reflectance_wavelength_matrices):
                assert matrices is not None
                assert len(matrices) > 0

    def test_matrix_and_wavelength_invariants(self):
        results = self.glazing_system.optical_method_results(METHOD)
        self.glazing_system.populate_layer_wavelength_matrices(results, METHOD)
        matrices = results.layer_results[0].front.transmittance_wavelength_matrices

        dimension = matrices[0].matrix.size()
        assert dimension > 0
        # every entry is a square matrix of the same (basis) dimension
        assert all(entry.matrix.size() == dimension for entry in matrices)

        wavelengths = [entry.wavelength for entry in matrices]
        assert all(math.isfinite(value) for value in wavelengths)
        assert wavelengths == sorted(wavelengths)   # monotonic non-decreasing


class TestPopulateNoOpOnSpecular:
    def test_specular_system_stays_none(self, products_dir, standard_path):
        standard = pywincalc.load_standard(str(standard_path))
        clear = pywincalc.parse_json_file(str(products_dir / "CLEAR_3.json"))
        glazing_system = pywincalc.GlazingSystem(
            optical_standard=standard,
            solid_layers=[clear],
            gap_layers=[],
            width_meters=1.0,
            height_meters=1.0,
            tilt_degrees=90,
            environment=pywincalc.nfrc_u_environments(),
        )
        results = glazing_system.optical_method_results(METHOD)
        glazing_system.populate_layer_wavelength_matrices(results, METHOD)
        assert results.layer_results[0].front.transmittance_wavelength_matrices is None
