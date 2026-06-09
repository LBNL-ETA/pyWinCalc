#include "product_data_bindings.h"
#include <pybind11/stl.h>

void register_product_data_bindings(py::module &mod) {
  py::enum_<Tarcog::ISO15099::BoundaryConditionsCoeffModel>(
      mod, "BoundaryConditionsCoefficientModelType", py::arithmetic())
      .value("CALCULATED_H",
             Tarcog::ISO15099::BoundaryConditionsCoeffModel::CalculateH)
      .value("H_PRESCRIBED",
             Tarcog::ISO15099::BoundaryConditionsCoeffModel::HPrescribed)
      .value("HC_PRESCRIBED",
             Tarcog::ISO15099::BoundaryConditionsCoeffModel::HcPrescribed);

  py::enum_<Tarcog::ISO15099::AirHorizontalDirection>(
      mod, "AirHorizontalDirection", py::arithmetic())
      .value("NONE", Tarcog::ISO15099::AirHorizontalDirection::None)
      .value("LEEWARD", Tarcog::ISO15099::AirHorizontalDirection::Leeward)
      .value("WINDWARD", Tarcog::ISO15099::AirHorizontalDirection::Windward);

  py::class_<wincalc::Environment>(mod, "Environment")
      .def(py::init<double, double, double,
                    Tarcog::ISO15099::BoundaryConditionsCoeffModel, double,
                    double, double, Tarcog::ISO15099::AirHorizontalDirection,
                    double>(),
           py::arg("air_temperature"), py::arg("pressure"),
           py::arg("convection_coefficient"), py::arg("coefficient_model"),
           py::arg("radiation_temperature"), py::arg("emissivity"),
           py::arg("air_speed") = 0,
           py::arg("air_direction") =
               Tarcog::ISO15099::AirHorizontalDirection::None,
           py::arg("direct_solar_radiation") = 0)
      .def_readwrite("air_temperature", &wincalc::Environment::air_temperature)
      .def_readwrite("pressure", &wincalc::Environment::pressure)
      .def_readwrite("convection_coefficient",
                     &wincalc::Environment::convection_coefficient)
      .def_readwrite("coefficient_model",
                     &wincalc::Environment::coefficient_model)
      .def_readwrite("radiation_temperature",
                     &wincalc::Environment::radiation_temperature)
      .def_readwrite("emissivity", &wincalc::Environment::emissivity)
      .def_readwrite("air_speed", &wincalc::Environment::air_speed)
      .def_readwrite("air_direction", &wincalc::Environment::air_direction)
      .def_readwrite("direct_solar_radiation",
                     &wincalc::Environment::direct_solar_radiation);

  py::class_<wincalc::Environments>(mod, "Environments")
      .def(py::init<wincalc::Environment, wincalc::Environment>(),
           py::arg("outside"), py::arg("inside"))
      .def_readwrite("outside", &wincalc::Environments::outside)
      .def_readwrite("inside", &wincalc::Environments::inside);

  mod.def("nfrc_u_environments", &wincalc::nfrc_u_environments,
        "Returns the default environments for running a NFRC U-Value "
        "calculation.");
  mod.def(
      "nfrc_shgc_environments", &wincalc::nfrc_shgc_environments,
      "Returns the default environments for running a NFRC SHGC calculation.");

  py::class_<wincalc::Flippable_Solid_Layer,
             std::shared_ptr<wincalc::Flippable_Solid_Layer>>(
      mod, "FlippableSolidLayer")
      .def(py::init<double, bool>(), py::arg("thickness_meters"),
           py::arg("flipped") = false)
      .def_readwrite("thickness_meters",
                     &wincalc::Flippable_Solid_Layer::thickness_meters)
      .def_readwrite("flipped", &wincalc::Flippable_Solid_Layer::flipped);

  py::class_<wincalc::Product_Data_Thermal, wincalc::Flippable_Solid_Layer,
             std::shared_ptr<wincalc::Product_Data_Thermal>>(
      mod, "ProductDataThermal")
      .def(py::init<std::optional<double>, double, bool, double, double, double, double, double, double, std::optional<double>, std::optional<double>>(),
           py::arg("conductivity"),
           py::arg("thickness_meters"),
           py::arg("flipped"),
           py::arg("opening_top") = 0,
           py::arg("opening_bottom") = 0,
           py::arg("opening_left") = 0,
           py::arg("opening_right") = 0,
           py::arg("effective_front_thermal_openness_area") = 0,
           py::arg("permeability_factor") = 0,
           py::arg("youngs_modulus") = Tarcog::DeflectionConstants::YOUNGSMODULUS,
           py::arg("density") = Tarcog::MaterialConstants::GLASSDENSITY)
      .def_readwrite("conductivity",
                     &wincalc::Product_Data_Thermal::conductivity)
      .def_readwrite("opening_top", &wincalc::Product_Data_Thermal::opening_top)
      .def_readwrite("opening_bottom",
                     &wincalc::Product_Data_Thermal::opening_bottom)
      .def_readwrite("opening_left",
                     &wincalc::Product_Data_Thermal::opening_left)
      .def_readwrite("opening_right",
                     &wincalc::Product_Data_Thermal::opening_right)
      .def_readwrite("effective_front_thermal_openness_area",
                     &wincalc::Product_Data_Thermal::effective_front_thermal_openness_area)
      .def_readwrite("permeability_factor",
                     &wincalc::Product_Data_Thermal::permeability_factor)
      .def_readwrite("youngs_modulus",
                     &wincalc::Product_Data_Thermal::youngs_modulus)
      .def_readwrite("density", &wincalc::Product_Data_Thermal::density);

  py::class_<wincalc::Product_Data_Optical, Py_Product_Data_Optical,
             std::shared_ptr<wincalc::Product_Data_Optical>>(
      mod, "ProductDataOptical")
      .def(py::init<double, std::optional<double>, std::optional<double>,
                    std::optional<double>, std::optional<double>, bool>(),
           py::arg("thickness_meters"),
           py::arg("ir_transmittance_front") = std::optional<double>(),
           py::arg("ir_transmittance_back") = std::optional<double>(),
           py::arg("emissivity_front") = std::optional<double>(),
           py::arg("emissivity_back") = std::optional<double>(),
           py::arg("flipped") = false)
      .def("effective_thermal_values",
           &wincalc::Product_Data_Optical::effective_thermal_values)
      .def("wavelengths", &wincalc::Product_Data_Optical::wavelengths)
      .def_readwrite("ir_transmittance_front", &wincalc::Product_Data_Optical::ir_transmittance_front)
      .def_readwrite("ir_transmittance_back", &wincalc::Product_Data_Optical::ir_transmittance_back)
      .def_readwrite("emissivity_front", &wincalc::Product_Data_Optical::emissivity_front)
      .def_readwrite("emissivity_back", &wincalc::Product_Data_Optical::emissivity_back);

  py::enum_<FenestrationCommon::MaterialType>(mod, "MaterialType",
                                              py::arithmetic())
      .value("APPLIED_FILM", FenestrationCommon::MaterialType::AppliedFilm)
      .value("COATED", FenestrationCommon::MaterialType::Coated)
      .value("ELECTROCHROMIC", FenestrationCommon::MaterialType::Electrochromic)
      .value("FILM", FenestrationCommon::MaterialType::Film)
      .value("INTERLAYER", FenestrationCommon::MaterialType::Interlayer)
      .value("LAMINATE", FenestrationCommon::MaterialType::Laminate)
      .value("MONOLITHIC", FenestrationCommon::MaterialType::Monolithic)
      .value("THERMOCHROMIC", FenestrationCommon::MaterialType::Thermochromic);

  py::enum_<wincalc::CoatedSide>(mod, "CoatedSide", py::arithmetic())
      .value("FRONT", wincalc::CoatedSide::FRONT)
      .value("BACK", wincalc::CoatedSide::BACK)
      .value("BOTH", wincalc::CoatedSide::BOTH)
      .value("NEITHER", wincalc::CoatedSide::NEITHER);

  py::class_<wincalc::Product_Data_N_Band_Optical,
             wincalc::Product_Data_Optical,
             std::shared_ptr<wincalc::Product_Data_N_Band_Optical>>(
      mod, "ProductDataOpticalNBand")
      .def(py::init<FenestrationCommon::MaterialType, double,
                    std::vector<OpticsParser::WLData>,
                    std::optional<wincalc::CoatedSide>, std::optional<double>,
                    std::optional<double>, std::optional<double>,
                    std::optional<double>, bool>(),
           py::arg("material_type"), py::arg("thickness_meters"),
           py::arg("wavelength_data"),
           py::arg("coated_side") = std::optional<wincalc::CoatedSide>(),
           py::arg("ir_transmittance_front") = std::optional<double>(),
           py::arg("ir_transmittance_back") = std::optional<double>(),
           py::arg("emissivity_front") = std::optional<double>(),
           py::arg("emissivity_back") = std::optional<double>(),
           py::arg("flipped") = false)
      .def("wavelengths", &wincalc::Product_Data_N_Band_Optical::wavelengths)
      .def_readwrite("material_type",
                     &wincalc::Product_Data_N_Band_Optical::material_type)
      .def_readwrite("wavelength_data",
                     &wincalc::Product_Data_N_Band_Optical::wavelength_data);

  py::class_<wincalc::Product_Data_Dual_Band_Optical,
             wincalc::Product_Data_Optical,
             std::shared_ptr<wincalc::Product_Data_Dual_Band_Optical>>(
      mod, "ProductDataOpticalDualBand")
      .def(py::init<double, std::optional<double>, std::optional<double>,
                    std::optional<double>, std::optional<double>,
                    bool>(),
           py::arg("thickness_meters"),
           py::arg("ir_transmittance_front") = std::optional<double>(),
           py::arg("ir_transmittance_back") = std::optional<double>(),
           py::arg("emissivity_front") = std::optional<double>(),
           py::arg("emissivity_back") = std::optional<double>(),
           py::arg("flipped") = false)
      .def("wavelengths",
           &wincalc::Product_Data_Dual_Band_Optical::wavelengths);

  py::class_<
      wincalc::Product_Data_Dual_Band_Optical_Hemispheric,
      wincalc::Product_Data_Dual_Band_Optical,
      std::shared_ptr<wincalc::Product_Data_Dual_Band_Optical_Hemispheric>>(
      mod, "ProductDataOpticalDualBandHemispheric")
      .def(py::init<double, double, double, double, double, double, double,
                    double, double, std::optional<double>,
                    std::optional<double>, std::optional<double>,
                    std::optional<double>, bool>(),
           py::arg("solar_transmittance_front"),
           py::arg("solar_transmittance_back"),
           py::arg("solar_reflectance_front"),
           py::arg("solar_reflectance_back"),
           py::arg("visible_transmittance_front"),
           py::arg("visible_transmittance_back"),
           py::arg("visible_reflectance_front"),
           py::arg("visible_reflectance_back"), py::arg("thickness_meters"),
           py::arg("ir_transmittance_front") = std::optional<double>(),
           py::arg("ir_transmittance_back") = std::optional<double>(),
           py::arg("emissivity_front") = std::optional<double>(),
           py::arg("emissivity_back") = std::optional<double>(),
           py::arg("flipped") = false)
      .def_readwrite(
          "solar_transmittance_front",
          &wincalc::Product_Data_Dual_Band_Optical_Hemispheric::tf_solar)
      .def_readwrite(
          "solar_transmittance_back",
          &wincalc::Product_Data_Dual_Band_Optical_Hemispheric::tb_solar)
      .def_readwrite(
          "solar_reflectance_front",
          &wincalc::Product_Data_Dual_Band_Optical_Hemispheric::rf_solar)
      .def_readwrite(
          "solar_reflectance_back",
          &wincalc::Product_Data_Dual_Band_Optical_Hemispheric::rb_solar)
      .def_readwrite(
          "visible_transmittance_front",
          &wincalc::Product_Data_Dual_Band_Optical_Hemispheric::tf_visible)
      .def_readwrite(
          "visible_transmittance_back",
          &wincalc::Product_Data_Dual_Band_Optical_Hemispheric::tb_visible)
      .def_readwrite(
          "visible_reflectance_front",
          &wincalc::Product_Data_Dual_Band_Optical_Hemispheric::rf_visible)
      .def_readwrite(
          "visible_reflectance_back",
          &wincalc::Product_Data_Dual_Band_Optical_Hemispheric::rb_visible);

  py::class_<wincalc::Product_Data_Dual_Band_Optical_BSDF,
             wincalc::Product_Data_Dual_Band_Optical,
             std::shared_ptr<wincalc::Product_Data_Dual_Band_Optical_BSDF>>(
      mod, "ProductDataOpticalDualBandBSDF")
      .def(py::init<std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    SingleLayerOptics::BSDFHemisphere const &, double,
                    std::optional<double>, std::optional<double>,
                    std::optional<double>, std::optional<double>,
                    bool, bool>(),
           py::arg("solar_transmittance_front"),
           py::arg("solar_transmittance_back"),
           py::arg("solar_reflectance_front"),
           py::arg("solar_reflectance_back"),
           py::arg("visible_transmittance_front"),
           py::arg("visible_transmittance_back"),
           py::arg("visible_reflectance_front"),
           py::arg("visible_reflectance_back"), py::arg("bsdf_hemisphere"),
           py::arg("thickness_meters"),
           py::arg("ir_transmittance_front") = std::optional<double>(),
           py::arg("ir_transmittance_back") = std::optional<double>(),
           py::arg("emissivity_front") = std::optional<double>(),
           py::arg("emissivity_back") = std::optional<double>(),
           py::arg("flipped") = false, py::arg("user_defined_effective_values") = false)
      .def_readwrite("solar_transmittance_front",
                     &wincalc::Product_Data_Dual_Band_Optical_BSDF::tf_solar)
      .def_readwrite("solar_transmittance_back",
                     &wincalc::Product_Data_Dual_Band_Optical_BSDF::tb_solar)
      .def_readwrite("solar_reflectance_front",
                     &wincalc::Product_Data_Dual_Band_Optical_BSDF::rf_solar)
      .def_readwrite("solar_reflectance_back",
                     &wincalc::Product_Data_Dual_Band_Optical_BSDF::rb_solar)
      .def_readwrite("visible_transmittance_front",
                     &wincalc::Product_Data_Dual_Band_Optical_BSDF::tf_visible)
      .def_readwrite("visible_transmittance_back",
                     &wincalc::Product_Data_Dual_Band_Optical_BSDF::tb_visible)
      .def_readwrite("visible_reflectance_front",
                     &wincalc::Product_Data_Dual_Band_Optical_BSDF::rf_visible)
      .def_readwrite("visible_reflectance_back",
                     &wincalc::Product_Data_Dual_Band_Optical_BSDF::rb_visible)
      .def_readwrite("user_defined_effective_values",
                     &wincalc::Product_Data_Dual_Band_Optical_BSDF::user_defined_effective_values)
      .def("effective_thermal_values",
           &wincalc::Product_Data_Dual_Band_Optical_BSDF::
               effective_thermal_values);

  py::class_<wincalc::Product_Data_Optical_With_Material,
             wincalc::Product_Data_Optical,
             std::shared_ptr<wincalc::Product_Data_Optical_With_Material>>(
      mod, "ProductDataOpticalWithMaterial")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical> const &>(),
           py::arg("product_data_optical"))
      .def("optical_data",
           &wincalc::Product_Data_Optical_With_Material::optical_data)
      .def("wavelengths",
           &wincalc::Product_Data_Optical_With_Material::wavelengths)
      .def_readwrite(
          "material_optical_data",
          &wincalc::Product_Data_Optical_With_Material::material_optical_data);
}
