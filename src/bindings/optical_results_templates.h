#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

namespace py = pybind11;

template <typename T>
void declare_wce_optical_result_simple(py::module &mod, std::string typestr) {
  using Class = wincalc::WCE_Optical_Result_Simple<T>;
  std::string pyclass_name = std::string("OpticalResultFluxType") + typestr;
  py::class_<Class>(mod, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("direct_direct", &Class::direct_direct)
      .def_readwrite("direct_diffuse", &Class::direct_diffuse)
      .def_readwrite("diffuse_diffuse", &Class::diffuse_diffuse)
      .def_readwrite("direct_hemispherical", &Class::direct_hemispherical)
      .def_readwrite("matrix", &Class::matrix)
      .def_readwrite("wavelength_matrices", &Class::wavelength_matrices);
}

template <typename T>
void declare_wce_optical_result_absorptance(py::module &mod,
                                            std::string typestr) {
  using Class = wincalc::WCE_Optical_Result_Absorptance<T>;
  std::string pyclass_name = std::string("OpticalResultAbsorptance") + typestr;
  py::class_<Class>(mod, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("direct", &Class::total_direct)
      .def_readwrite("diffuse", &Class::total_diffuse)
      .def_readwrite("total_direct", &Class::total_direct)
      .def_readwrite("total_diffuse", &Class::total_diffuse)
      .def_readwrite("heat_direct", &Class::heat_direct)
      .def_readwrite("heat_diffuse", &Class::heat_diffuse)
      .def_readwrite("electricity_direct", &Class::electricity_direct)
      .def_readwrite("electricity_diffuse", &Class::electricity_diffuse)
      .def_readwrite("angular_total", &Class::angular_total)
      .def_readwrite("angular_heat", &Class::angular_heat)
      .def_readwrite("angular_electricity", &Class::angular_electricity);
}

template <typename T>
void declare_wce_optical_result_layer(py::module &mod, std::string typestr) {
  using Class = wincalc::WCE_Optical_Result_Layer<T>;
  declare_wce_optical_result_absorptance<T>(mod, typestr);
  std::string pyclass_name = std::string("OpticalResultLayer") + typestr;
  py::class_<Class>(mod, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("absorptance", &Class::absorptance)
      .def_readwrite("transmittance_wavelength_matrices",
                     &Class::transmittance_wavelength_matrices)
      .def_readwrite("reflectance_wavelength_matrices",
                     &Class::reflectance_wavelength_matrices);
}

template <typename T>
void declare_wce_optical_transmission_result(py::module &mod,
                                             std::string typestr) {
  using Class = wincalc::WCE_Optical_Transmission_Result<T>;
  std::string pyclass_name = std::string("OpticalResultTransmission") + typestr;
  py::class_<Class>(mod, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("transmittance", &Class::transmittance)
      .def_readwrite("reflectance", &Class::reflectance);
}

template <typename T>
void declare_wce_optical_result_by_side(py::module &mod, std::string typestr) {
  using Class = wincalc::WCE_Optical_Result_By_Side<T>;
  std::string pyclass_name = std::string("OpticalResultSide") + typestr;
  py::class_<Class>(mod, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("front", &Class::front)
      .def_readwrite("back", &Class::back);
}

template <typename T>
void declare_wce_optical_results_template(py::module &mod, std::string typestr) {
  using Class = wincalc::WCE_Optical_Results_Template<T>;
  declare_wce_optical_result_simple<T>(mod, typestr);
  declare_wce_optical_transmission_result<
      wincalc::WCE_Optical_Result_Simple<T>>(mod, typestr);
  declare_wce_optical_result_by_side<wincalc::WCE_Optical_Transmission_Result<
      wincalc::WCE_Optical_Result_Simple<T>>>(mod, typestr);
  declare_wce_optical_result_layer<T>(mod, typestr);
  declare_wce_optical_result_by_side<wincalc::WCE_Optical_Result_Layer<T>>(
      mod, typestr + "_Layer");
  std::string pyclass_name = std::string("OpticalResults") + typestr;
  py::class_<Class>(mod, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("system_results", &Class::system_results,
                     "Results for the entire system.")
      .def_readwrite("layer_results", &Class::layer_results,
                     "A list of results where each item in the list contains "
                     "the results for one layer in the system.");
}

template <>
inline void declare_wce_optical_results_template<wincalc::Color_Result>(
    py::module &mod, std::string typestr) {
  using Class = wincalc::WCE_Optical_Results_Template<wincalc::Color_Result>;
  declare_wce_optical_result_simple<wincalc::Color_Result>(mod, typestr);
  declare_wce_optical_transmission_result<
      wincalc::WCE_Optical_Result_Simple<wincalc::Color_Result>>(mod, typestr);
  declare_wce_optical_result_by_side<wincalc::WCE_Optical_Transmission_Result<
      wincalc::WCE_Optical_Result_Simple<wincalc::Color_Result>>>(mod, typestr);
  std::string pyclass_name = std::string("OpticalResults") + typestr;
  py::class_<Class>(mod, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("system_results", &Class::system_results,
                     "Results for the entire system.  Layer results for colors "
                     "are not currently supported.");
}
