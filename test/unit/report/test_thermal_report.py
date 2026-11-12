"""
Unit tests for the report bindings (src/bindings/report_bindings.cpp):
thermal_report, ThermalReport and its parts, and the JSON / XML output.

Contract and invariant checks against the existing GlazingSystem results - no golden data.
"""
import json
import math
import xml.etree.ElementTree as ElementTree

import pytest

import pywincalc


TOL = 1e-6


@pytest.fixture(scope="module")
def triple_clear(products_dir):
    clear_3 = pywincalc.parse_json_file(str(products_dir / "CLEAR_3.json"))
    gap = pywincalc.Layers.gap(thickness=0.0127)
    return pywincalc.GlazingSystem(
        solid_layers=[clear_3, clear_3, clear_3],
        gap_layers=[gap, gap],
        environment=pywincalc.nfrc_u_environments(),
    )


@pytest.fixture(scope="module")
def report(triple_clear):
    return pywincalc.thermal_report(
        glazing_system=triple_clear, system_type=pywincalc.TarcogSystemType.U
    )


class TestThermalReport:
    def test_structure(self, report):
        assert isinstance(report, pywincalc.ThermalReport)
        assert report.system_type == "U"
        assert len(report.solid_layers) == 3
        assert len(report.gaps) == 2
        assert isinstance(report.outdoor, pywincalc.ThermalReportEnvironment)
        assert isinstance(report.solid_layers[0], pywincalc.ThermalReportSolidLayer)
        assert isinstance(report.solid_layers[0].front, pywincalc.ThermalReportSurface)
        assert isinstance(report.gaps[0], pywincalc.ThermalReportGap)

    def test_surfaces_match_glazing_system(self, triple_clear, report):
        system_type = pywincalc.TarcogSystemType.U
        temperatures = triple_clear.layer_temperatures(system_type)
        radiosities = triple_clear.radiosities(system_type)
        for index, layer in enumerate(report.solid_layers):
            assert math.isclose(layer.front.temperature, temperatures[2 * index], abs_tol=TOL)
            assert math.isclose(layer.back.temperature, temperatures[2 * index + 1], abs_tol=TOL)
            assert math.isclose(layer.front.radiosity, radiosities[2 * index], abs_tol=TOL)
            assert math.isclose(layer.back.radiosity, radiosities[2 * index + 1], abs_tol=TOL)

    def test_effective_conductivities_match_glazing_system(self, triple_clear, report):
        system_type = pywincalc.TarcogSystemType.U
        solid = triple_clear.solid_layers_effective_conductivities(system_type)
        gaps = triple_clear.gap_layers_effective_conductivities(system_type)
        for layer, expected in zip(report.solid_layers, solid):
            assert math.isclose(layer.effective_conductivity, expected, abs_tol=TOL)
        for gap, expected in zip(report.gaps, gaps):
            assert math.isclose(gap.effective_conductivity, expected, abs_tol=TOL)

    def test_gap_heat_flow_is_convective_plus_radiative(self, report):
        for gap in report.gaps:
            assert math.isclose(
                gap.heat_flow, gap.convective_heat_flow + gap.radiative_heat_flow, abs_tol=TOL
            )

    def test_report_is_read_only(self, report):
        with pytest.raises(AttributeError):
            report.system_type = "SHGC"


class TestThermalReportOutput:
    def test_json_has_numbers_and_lists(self, report):
        data = json.loads(report.to_json())["ThermalReport"]
        assert data["SystemType"] == "U"
        assert isinstance(data["Outdoor"]["HeatFlow"], float)
        assert isinstance(data["SolidLayers"]["SolidLayer"], list)
        assert len(data["SolidLayers"]["SolidLayer"]) == 3
        assert len(data["Gaps"]["Gap"]) == 2
        assert data["SolidLayers"]["SolidLayer"][0]["IsShade"] is False

    def test_xml_has_the_same_structure(self, report):
        root = ElementTree.fromstring(report.to_xml())
        assert root.tag == "ThermalReport"
        assert root.findtext("SystemType") == "U"
        assert len(root.findall("SolidLayers/SolidLayer")) == 3
        assert len(root.findall("Gaps/Gap")) == 2

    def test_module_functions_match_methods(self, report):
        assert pywincalc.thermal_report_to_json(report) == report.to_json()
        assert pywincalc.thermal_report_to_xml(report) == report.to_xml()

    def test_save_follows_the_extension(self, report, tmp_path):
        json_file = tmp_path / "report.json"
        xml_file = tmp_path / "report.xml"
        assert report.save(str(json_file)) == 0
        assert pywincalc.save_thermal_report(report, str(xml_file)) == 0
        assert json.loads(json_file.read_text())["ThermalReport"]["SystemType"] == "U"
        assert ElementTree.parse(xml_file).getroot().tag == "ThermalReport"
