#include "standards_bindings.h"
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>
#include "optical_results_templates.h"

void register_standards_bindings(py::module &mod) {
  py::enum_<window_standards::Spectrum_Type>(mod, "SpectrumType",
                                             py::arithmetic())
      .value("NONE", window_standards::Spectrum_Type::NONE)
      .value("FILE", window_standards::Spectrum_Type::FILE)
      .value("BLACKBODY", window_standards::Spectrum_Type::BLACKBODY)
      .value("UV_ACTION", window_standards::Spectrum_Type::UV_ACTION)
      .value("KROCHMANN", window_standards::Spectrum_Type::KROCHMANN);

  py::class_<window_standards::Spectrum>(mod, "Spectrum")
      .def_readwrite("type", &window_standards::Spectrum::type)
      .def_readwrite("description", &window_standards::Spectrum::description)
      .def_readwrite("t", &window_standards::Spectrum::t)
      .def_readwrite("a", &window_standards::Spectrum::a)
      .def_readwrite("b", &window_standards::Spectrum::b)
      .def_readwrite("values", &window_standards::Spectrum::values);

  py::enum_<window_standards::Wavelength_Set_Type>(mod, "WavelengthSetType",
                                                   py::arithmetic())
      .value("FILE", window_standards::Wavelength_Set_Type::FILE)
      .value("SOURCE", window_standards::Wavelength_Set_Type::SOURCE)
      .value("DATA", window_standards::Wavelength_Set_Type::DATA);

  py::class_<window_standards::Wavelength_Set>(mod, "WavelengthSet")
      .def_readwrite("type", &window_standards::Wavelength_Set::type)
      .def_readwrite("description",
                     &window_standards::Wavelength_Set::description)
      .def_readwrite("values", &window_standards::Wavelength_Set::values);

  py::enum_<window_standards::Wavelength_Boundary_Type>(
      mod, "WavelengthBoundaryType", py::arithmetic())
      .value("NUMBER", window_standards::Wavelength_Boundary_Type::NUMBER)
      .value("WAVELENGTH_SET",
             window_standards::Wavelength_Boundary_Type::WAVELENGTH_SET);

  py::class_<window_standards::Wavelength_Boundary>(mod, "WavelengthBoundary")
      .def_readwrite("type", &window_standards::Wavelength_Boundary::type)
      .def_readwrite("value", &window_standards::Wavelength_Boundary::value);

  py::enum_<window_standards::Integration_Rule_Type>(mod, "IntegrationRuleType",
                                                     py::arithmetic())
      .value("TRAPEZOIDAL",
             window_standards::Integration_Rule_Type::TRAPEZOIDAL)
      .value("RECTANGULAR",
             window_standards::Integration_Rule_Type::RECTANGULAR)
      .value("TABLE", window_standards::Integration_Rule_Type::TABLE);

  py::class_<window_standards::Integration_Rule>(mod, "IntegrationRule")
      .def_readwrite("type", &window_standards::Integration_Rule::type)
      .def_readwrite("k", &window_standards::Integration_Rule::k);

  py::class_<window_standards::Optical_Standard_Method>(mod,
                                                        "OpticalStandardMethod")
      .def_readwrite("name", &window_standards::Optical_Standard_Method::name)
      .def_readwrite("description",
                     &window_standards::Optical_Standard_Method::description)
      .def_readwrite(
          "source_spectrum",
          &window_standards::Optical_Standard_Method::source_spectrum)
      .def_readwrite(
          "detector_spectrum",
          &window_standards::Optical_Standard_Method::detector_spectrum)
      .def_readwrite("wavelength_set",
                     &window_standards::Optical_Standard_Method::wavelength_set)
      .def_readwrite(
          "integration_rule",
          &window_standards::Optical_Standard_Method::integration_rule)
      .def_readwrite("min_wavelength",
                     &window_standards::Optical_Standard_Method::min_wavelength)
      .def_readwrite(
          "max_wavelength",
          &window_standards::Optical_Standard_Method::max_wavelength);

  py::class_<window_standards::Optical_Standard>(mod, "OpticalStandard")
      .def_readwrite("name", &window_standards::Optical_Standard::name)
      .def_readwrite("description",
                     &window_standards::Optical_Standard::description)
      .def_readwrite("file", &window_standards::Optical_Standard::file)
      .def_readwrite("methods", &window_standards::Optical_Standard::methods);

  py::class_<wincalc::Trichromatic>(mod, "Trichromatic")
      .def_readwrite("X", &wincalc::Trichromatic::X)
      .def_readwrite("Y", &wincalc::Trichromatic::Y)
      .def_readwrite("Z", &wincalc::Trichromatic::Z);

  py::class_<wincalc::WinCalc_RGB>(mod, "RGB")
      .def_readwrite("R", &wincalc::WinCalc_RGB::R)
      .def_readwrite("G", &wincalc::WinCalc_RGB::G)
      .def_readwrite("B", &wincalc::WinCalc_RGB::B);

  py::class_<wincalc::Lab>(mod, "Lab")
      .def_readwrite("L", &wincalc::Lab::L)
      .def_readwrite("a", &wincalc::Lab::a)
      .def_readwrite("b", &wincalc::Lab::b);

  py::class_<wincalc::DominantWavelengthPurity>(mod, "DominantWavelengthPurity")
      .def_readwrite("dominant_wavelength", &wincalc::DominantWavelengthPurity::dominant_wavelength)
      .def_readwrite("purity", &wincalc::DominantWavelengthPurity::purity);

  py::class_<wincalc::Color_Result>(mod, "ColorResult")
      .def_readwrite("trichromatic", &wincalc::Color_Result::trichromatic)
      .def_readwrite("rgb", &wincalc::Color_Result::rgb)
      .def_readwrite("lab", &wincalc::Color_Result::lab)
      .def_readwrite("dominant_wavelength_purity", &wincalc::Color_Result::dominant_wavelength_purity);

  declare_wce_optical_results_template<double>(mod, "");
  declare_wce_optical_results_template<wincalc::Color_Result>(mod, "Color");
}
