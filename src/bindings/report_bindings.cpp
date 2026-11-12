#include "report_bindings.h"
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

// Reports of a solved glazing system (WinCalc src/report). A report is plain, read-only data;
// the same data can be written as JSON or XML. The structure of the thermal report is
// described by thermal_report.xsd in WinCalc.

namespace
{
    void register_thermal_report_parts(py::module & mod)
    {
        using Environment = wincalc::Thermal_Report_Environment;
        py::class_<Environment>(mod, "ThermalReportEnvironment")
          .def_readonly("air_temperature", &Environment::air_temperature)
          .def_readonly("radiation_temperature", &Environment::radiation_temperature)
          .def_readonly("infrared_irradiance", &Environment::infrared_irradiance)
          .def_readonly("heat_flow", &Environment::heat_flow)
          .def_readonly("convective_heat_flow", &Environment::convective_heat_flow)
          .def_readonly("radiative_heat_flow", &Environment::radiative_heat_flow)
          .def_readonly("convective_coefficient", &Environment::convective_coefficient)
          .def_readonly("radiative_coefficient", &Environment::radiative_coefficient)
          .def_readonly("shading_emissivity_ratio", &Environment::shading_emissivity_ratio)
          .def_readonly("shading_convective_coefficient_ratio",
                        &Environment::shading_convective_coefficient_ratio);

        using Surface = wincalc::Thermal_Report_Surface;
        py::class_<Surface>(mod, "ThermalReportSurface")
          .def_readonly("temperature", &Surface::temperature)
          .def_readonly("radiosity", &Surface::radiosity)
          .def_readonly("emissivity", &Surface::emissivity);

        using SolidLayer = wincalc::Thermal_Report_Solid_Layer;
        py::class_<SolidLayer>(mod, "ThermalReportSolidLayer")
          .def_readonly("thickness", &SolidLayer::thickness)
          .def_readonly("is_shade", &SolidLayer::is_shade)
          .def_readonly("front", &SolidLayer::front)
          .def_readonly("back", &SolidLayer::back)
          .def_readonly("heat_flow", &SolidLayer::heat_flow)
          .def_readonly("absorbed_solar_radiation", &SolidLayer::absorbed_solar_radiation)
          .def_readonly("effective_conductivity", &SolidLayer::effective_conductivity);

        using Gap = wincalc::Thermal_Report_Gap;
        py::class_<Gap>(mod, "ThermalReportGap")
          .def_readonly("thickness", &Gap::thickness)
          .def_readonly("pressure", &Gap::pressure)
          .def_readonly("average_temperature", &Gap::average_temperature)
          .def_readonly("heat_flow", &Gap::heat_flow)
          .def_readonly("convective_heat_flow", &Gap::convective_heat_flow)
          .def_readonly("radiative_heat_flow", &Gap::radiative_heat_flow)
          .def_readonly("ventilation_heat_gain", &Gap::ventilation_heat_gain)
          .def_readonly("convective_coefficient", &Gap::convective_coefficient)
          .def_readonly("effective_conductivity", &Gap::effective_conductivity);
    }

    void register_thermal_report(py::module & mod)
    {
        using Report = wincalc::Thermal_Report;
        py::class_<Report>(mod, "ThermalReport")
          .def_readonly("system_type", &Report::system_type)
          .def_readonly("theta", &Report::theta)
          .def_readonly("phi", &Report::phi)
          .def_readonly("number_of_iterations", &Report::number_of_iterations)
          .def_readonly("system_effective_conductivity", &Report::system_effective_conductivity)
          .def_readonly("outdoor", &Report::outdoor)
          .def_readonly("indoor", &Report::indoor)
          .def_readonly("solid_layers", &Report::solid_layers)
          .def_readonly("gaps", &Report::gaps)
          .def("to_json", &wincalc::thermal_report_to_json)
          .def("to_xml", &wincalc::thermal_report_to_xml)
          .def("save",
               &wincalc::save_thermal_report,
               py::arg("file_name"),
               "Writes the report to a .json or .xml file. Returns 0 on success.");

        mod.def("thermal_report",
                &wincalc::thermal_report,
                py::arg("glazing_system"),
                py::arg("system_type"),
                py::arg("theta") = 0.0,
                py::arg("phi") = 0.0,
                "Solves the glazing system if needed and returns its detailed thermal state "
                "(SI units) for one ISO 15099 run.");
        mod.def("thermal_report_to_json", &wincalc::thermal_report_to_json, py::arg("report"));
        mod.def("thermal_report_to_xml", &wincalc::thermal_report_to_xml, py::arg("report"));
        mod.def("save_thermal_report",
                &wincalc::save_thermal_report,
                py::arg("report"),
                py::arg("file_name"));
    }
}   // namespace

void register_report_bindings(py::module & mod)
{
    register_thermal_report_parts(mod);
    register_thermal_report(mod);
}
