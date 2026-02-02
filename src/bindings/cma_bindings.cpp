#include "cma_bindings.h"
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

void register_cma_bindings(py::module &mod) {
  py::class_<Tarcog::IGUDimensions>(mod, "GlazingSystemDimensions")
      .def_readwrite("width", &Tarcog::IGUDimensions::width)
      .def_readwrite("height", &Tarcog::IGUDimensions::height);

  py::class_<CMA::ICMAWindow, std::shared_ptr<CMA::ICMAWindow>>(mod, "CMAWindow")
      .def("u", &CMA::ICMAWindow::uValue)
      .def("shgc", &CMA::ICMAWindow::shgc)
      .def("vt", &CMA::ICMAWindow::vt)
      .def("glazing_system_dimensions", &CMA::ICMAWindow::getIGUDimensions);

  py::class_<CMA::CMABestWorstUFactors,
             std::shared_ptr<CMA::CMABestWorstUFactors>>(mod,
                                                         "CMABestWorstUFactors")
      .def(py::init<>())
      .def(py::init<double, double, double>())
      .def(py::init<double, double, double, double, double, double, double,
                    double, double, double, double>())
      .def("u", &CMA::CMABestWorstUFactors::uValue)
      .def("hc_out", &CMA::CMABestWorstUFactors::hcout);

  mod.def("create_best_worst_u_factor_option",
        &CMA::CreateBestWorstUFactorOption);

  py::class_<CMA::CMAWindowSingleVision, CMA::ICMAWindow,
             std::shared_ptr<CMA::CMAWindowSingleVision>>(
      mod, "CMAWindowSingleVision")
      .def(py::init<double, double, double, double, CMA::CMABestWorstUFactors,
                    CMA::CMABestWorstUFactors>(),
           py::arg("width"), py::arg("height"),
           py::arg("spacer_best_keff") = 0.01,
           py::arg("spacer_worst_keff") = 10.0,
           py::arg("best_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Best),
           py::arg("worst_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Worst))
      .def("set_frame_data", py::overload_cast<Tarcog::ISO15099::SingleVisionFramePosition, CMA::CMAFrame &>(
          &CMA::CMAWindowSingleVision::setFrameData),
          py::arg("position"), py::arg("cma_frame_data"))
      .def("set_frame_data", py::overload_cast<CMA::SingleVisionFrameMap const&>(
          &CMA::CMAWindowSingleVision::setFrameData),
          py::arg("frames"))
      .def("set_dividers", &CMA::CMAWindowSingleVision::setDividers);

  py::class_<CMA::CMAWindowDualVisionHorizontal, CMA::ICMAWindow,
             std::shared_ptr<CMA::CMAWindowDualVisionHorizontal>>(
      mod, "CMAWindowDualVisionHorizontal")
      .def(py::init<double, double, double, double, CMA::CMABestWorstUFactors,
                    CMA::CMABestWorstUFactors>(),
           py::arg("width"), py::arg("height"),
           py::arg("spacer_best_keff") = 0.01,
           py::arg("spacer_worst_keff") = 10.0,
           py::arg("best_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Best),
           py::arg("worst_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Worst))
      .def("set_frame_data", py::overload_cast<Tarcog::ISO15099::DualHorizontalFramePosition, CMA::CMAFrame&>(
          &CMA::CMAWindowDualVisionHorizontal::setFrameData),
          py::arg("position"), py::arg("cma_frame_data"))
      .def("set_frame_data", py::overload_cast<CMA::DualHorizontalFrameMap const&>(
          &CMA::CMAWindowDualVisionHorizontal::setFrameData),
          py::arg("frames"))
      .def("set_dividers", &CMA::CMAWindowDualVisionHorizontal::setDividers);

  py::class_<CMA::CMAWindowDualVisionVertical, CMA::ICMAWindow,
             std::shared_ptr<CMA::CMAWindowDualVisionVertical>>(
      mod, "CMAWindowDualVisionVertical")
      .def(py::init<double, double, double, double, CMA::CMABestWorstUFactors,
                    CMA::CMABestWorstUFactors>(),
           py::arg("width"), py::arg("height"),
           py::arg("spacer_best_keff") = 0.01,
           py::arg("spacer_worst_keff") = 10.0,
           py::arg("best_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Best),
           py::arg("worst_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Worst))
      .def("set_frame_data", py::overload_cast<Tarcog::ISO15099::DualVerticalFramePosition, CMA::CMAFrame&>(
          &CMA::CMAWindowDualVisionVertical::setFrameData),
          py::arg("position"), py::arg("cma_frame_data"))
      .def("set_frame_data", py::overload_cast<CMA::DualVerticalFrameMap const&>(
          &CMA::CMAWindowDualVisionVertical::setFrameData),
          py::arg("frames"))
      .def("set_dividers", &CMA::CMAWindowDualVisionVertical::setDividers);

  py::class_<wincalc::ThermalIRResults>(mod, "ThermalIRResults")
      .def_readwrite(
          "transmittance_front_diffuse_diffuse",
          &wincalc::ThermalIRResults::transmittance_front_diffuse_diffuse)
      .def_readwrite(
          "transmittance_back_diffuse_diffuse",
          &wincalc::ThermalIRResults::transmittance_back_diffuse_diffuse)
      .def_readwrite("emissivity_front_hemispheric",
                     &wincalc::ThermalIRResults::emissivity_front_hemispheric)
      .def_readwrite("emissivity_back_hemispheric",
                     &wincalc::ThermalIRResults::emissivity_back_hemispheric);

  mod.def("calc_thermal_ir", &wincalc::calc_thermal_ir,
        py::arg("optical_standard"), py::arg("product_data"));

  mod.def("get_spacer_keff", &wincalc::get_spacer_keff,
        "Calculate the effective conductivity of a spacer from a THERM thmx "
        "file.");
  mod.def("get_cma_window_single_vision",
        py::overload_cast<thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &, double, double>(
            &wincalc::get_cma_window_single_vision),
        "Get the CMA template for a single vision window.");
  mod.def(
      "get_cma_window_single_vision",
      py::overload_cast<
          CMA::CMAFrame const &, CMA::CMAFrame const &, CMA::CMAFrame const &,
          CMA::CMAFrame const &, double, double, double, double,
          CMA::CMABestWorstUFactors const &, CMA::CMABestWorstUFactors const &>(
          &wincalc::get_cma_window_single_vision),
      "Get the CMA template for a single vision window.");
  mod.def("get_cma_window_double_vision_vertical",
        py::overload_cast<thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &, double, double>(
            &wincalc::get_cma_window_double_vision_vertical),
        "Get the CMA template for a double vision vertical window.");
  mod.def(
      "get_cma_window_double_vision_vertical",
      py::overload_cast<
          CMA::CMAFrame const &, CMA::CMAFrame const &, CMA::CMAFrame const &,
          CMA::CMAFrame const &, CMA::CMAFrame const &, CMA::CMAFrame const &,
          CMA::CMAFrame const &, double, double, double, double,
          CMA::CMABestWorstUFactors const &, CMA::CMABestWorstUFactors const &>(
          &wincalc::get_cma_window_double_vision_vertical),
      "Get the CMA template for a double vision vertical window.");
  mod.def("get_cma_window_double_vision_horizontal",
        py::overload_cast<thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &, double, double>(
            &wincalc::get_cma_window_double_vision_horizontal),
        "Get the CMA template for a double vision horizontal window.");
  mod.def(
      "get_cma_window_double_vision_horizontal",
      py::overload_cast<
          CMA::CMAFrame const &, CMA::CMAFrame const &, CMA::CMAFrame const &,
          CMA::CMAFrame const &, CMA::CMAFrame const &, CMA::CMAFrame const &,
          CMA::CMAFrame const &, double, double, double, double,
          CMA::CMABestWorstUFactors const &, CMA::CMABestWorstUFactors const &>(
          &wincalc::get_cma_window_double_vision_horizontal),
      "Get the CMA template for a double vision horizontal window.");

  py::class_<wincalc::CMAResult>(mod, "CMAResult")
      .def_readwrite("u", &wincalc::CMAResult::u)
      .def_readwrite("shgc", &wincalc::CMAResult::shgc)
      .def_readwrite("vt", &wincalc::CMAResult::vt);

  mod.def("calc_cma", &wincalc::calc_cma, "Get CMA results.");
}
