"""
Unit tests for the standards bindings (src/bindings/standards_bindings.cpp):
the optical-standard enums and load_standard -> OpticalStandard.

The color result classes (Trichromatic/RGB/Lab/ColorResult) have no Python
constructor (they are returned by color() only), so they are not unit-tested
here in isolation.
"""
import pywincalc


class TestStandardEnums:
    def test_spectrum_type(self):
        for name in ("NONE", "FILE", "BLACKBODY", "UV_ACTION", "KROCHMANN"):
            assert hasattr(pywincalc.SpectrumType, name)

    def test_wavelength_set_type(self):
        for name in ("FILE", "SOURCE", "DATA"):
            assert hasattr(pywincalc.WavelengthSetType, name)

    def test_integration_rule_type(self):
        for name in ("TRAPEZOIDAL", "RECTANGULAR", "TABLE"):
            assert hasattr(pywincalc.IntegrationRuleType, name)


class TestLoadStandard:
    def test_loads_optical_standard_with_methods(self, standard_path):
        standard = pywincalc.load_standard(str(standard_path))
        assert isinstance(standard.methods, dict)
        # the NFRC standard defines the core optical methods
        for method in ("SOLAR", "PHOTOPIC"):
            assert method in standard.methods

    def test_standard_metadata_accessible(self, standard_path):
        standard = pywincalc.load_standard(str(standard_path))
        # metadata attributes exist and are readable (non-None)
        assert standard.name is not None
        assert standard.description is not None
