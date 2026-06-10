"""
Unit tests for the optical product parsers
(bound in src/bindings/glazing_system_bindings.cpp, producing the
OpticsParser::ProductData types from src/bindings/optical_parser_bindings.cpp):
parse_json_file, parse_optics_file, parse_bsdf_xml_file.

Assertions are attribute-based on the parsed ProductData (not isinstance), so
they don't depend on ProductData being re-exported in pywincalc/__init__.py.
"""
import pywincalc


class TestParsers:
    def test_parse_json_file(self, products_dir):
        product = pywincalc.parse_json_file(str(products_dir / "CLEAR_3.json"))
        # CLEAR_3 is NFRC 102 glazing with 111 wavelength measurements
        assert product.nfrc_id == 102
        assert product.product_type == "glazing"
        assert len(product.measurements) == 111

    def test_parse_optics_file(self, products_dir):
        product = pywincalc.parse_optics_file(str(products_dir / "CLEAR_3.DAT"))
        assert product.product_type == "glazing"
        # same CLEAR_3 spectral data as the JSON -> identical measurement count
        assert len(product.measurements) == 111

    def test_parse_bsdf_xml_file(self, products_dir):
        product = pywincalc.parse_bsdf_xml_file(str(products_dir / "2011-SA1.XML"))
        # parsed BSDF product is returned and carries geometry/measurement data
        assert product is not None
        assert product.product_type is not None
