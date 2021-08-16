#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

namespace py = pybind11;

using namespace pybind11::literals;

template <typename T>
void declare_wce_optical_result_simple(py::module &m, std::string typestr) {
  using Class = wincalc::WCE_Optical_Result_Simple<T>;
  std::string pyclass_name = std::string("OpticalResultFluxType") + typestr;
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("direct_direct", &Class::direct_direct)
      .def_readwrite("direct_diffuse", &Class::direct_diffuse)
      .def_readwrite("diffuse_diffuse", &Class::diffuse_diffuse)
      .def_readwrite("direct_hemispherical", &Class::direct_hemispherical)
      .def_readwrite("matrix", &Class::matrix);
}

template <typename T>
void declare_wce_optical_result_absorptance(py::module &m,
                                            std::string typestr) {
  using Class = wincalc::WCE_Optical_Result_Absorptance<T>;
  std::string pyclass_name = std::string("OpticalResultAbsorptance") + typestr;
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("direct", &Class::direct)
      .def_readwrite("diffuse", &Class::diffuse);
}

template <typename T>
void declare_wce_optical_result_layer(py::module &m, std::string typestr) {
  using Class = wincalc::WCE_Optical_Result_Layer<T>;
  declare_wce_optical_result_absorptance<T>(m, typestr);
  std::string pyclass_name = std::string("OpticalResultLayer") + typestr;
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("absorptance", &Class::absorptance);
}

template <typename T>
void declare_wce_optical_transmission_result(py::module &m,
                                             std::string typestr) {
  using Class = wincalc::WCE_Optical_Transmission_Result<T>;
  std::string pyclass_name = std::string("OpticalResultTransmission") + typestr;
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("transmittance", &Class::transmittance)
      .def_readwrite("reflectance", &Class::reflectance);
}

template <typename T>
void declare_wce_optical_result_by_side(py::module &m, std::string typestr) {
  using Class = wincalc::WCE_Optical_Result_By_Side<T>;
  std::string pyclass_name = std::string("OpticalResultSide") + typestr;
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("front", &Class::front)
      .def_readwrite("back", &Class::back);
}

template <typename T>
void declare_wce_optical_results_template(py::module &m, std::string typestr) {
  using Class = wincalc::WCE_Optical_Results_Template<T>;
  declare_wce_optical_result_simple<T>(m, typestr);
  declare_wce_optical_transmission_result<
      wincalc::WCE_Optical_Result_Simple<T>>(m, typestr);
  declare_wce_optical_result_by_side<wincalc::WCE_Optical_Transmission_Result<
      wincalc::WCE_Optical_Result_Simple<T>>>(m, typestr);
  declare_wce_optical_result_layer<T>(m, typestr);
  declare_wce_optical_result_by_side<wincalc::WCE_Optical_Result_Layer<T>>(
      m, typestr + "_Layer");
  std::string pyclass_name = std::string("OpticalResults") + typestr;
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("system_results", &Class::system_results,
                     "Results for the entire system.")
      .def_readwrite("layer_results", &Class::layer_results,
                     "A list of results where each item in the list contains "
                     "the results for one layer in the system.");
}

template <>
void declare_wce_optical_results_template<wincalc::Color_Result>(
    py::module &m, std::string typestr) {
  using Class = wincalc::WCE_Optical_Results_Template<wincalc::Color_Result>;
  declare_wce_optical_result_simple<wincalc::Color_Result>(m, typestr);
  declare_wce_optical_transmission_result<
      wincalc::WCE_Optical_Result_Simple<wincalc::Color_Result>>(m, typestr);
  declare_wce_optical_result_by_side<wincalc::WCE_Optical_Transmission_Result<
      wincalc::WCE_Optical_Result_Simple<wincalc::Color_Result>>>(m, typestr);
  std::string pyclass_name = std::string("OpticalResults") + typestr;
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("system_results", &Class::system_results,
                     "Results for the entire system.  Layer results for colors "
                     "are not currently supported.");
}

class Py_Product_Data_Optical : public wincalc::Product_Data_Optical //_Base
{
public:
  using wincalc::Product_Data_Optical::Product_Data_Optical; // Inherit
                                                             // constructors
  std::vector<double> wavelengths() const override {
    PYBIND11_OVERRIDE_PURE(std::vector<double>, wincalc::Product_Data_Optical,
                           wavelengths, );
  }
};

#if 0
template <class Product_Data_N_Band_Optical_Base =
              wincalc::Product_Data_N_Band_Optical>
class Py_Product_Data_N_Band_Optical
    : public Py_Product_Data_Optical<Product_Data_N_Band_Optical_Base> {
public:
  using Py_Product_Data_Optical<Product_Data_N_Band_Optical_Base>::
      Py_Product_Data_Optical; // Inherit constructors
  // Override PyAnimal's pure virtual go() with a non-pure one:
  std::vector<double> wavelengths() const override {
    PYBIND11_OVERRIDE(std::vector<double>, Product_Data_N_Band_Optical_Base,
                      wavelengths, );
  }
};
#endif

PYBIND11_MODULE(_pywincalc, m) {
  m.doc() = "Python bindings for WinCalc";

  py::enum_<Gases::GasDef>(m, "PredefinedGasType", py::arithmetic())
      .value("AIR", Gases::GasDef::Air)
      .value("ARGON", Gases::GasDef::Argon)
      .value("KRYPTON", Gases::GasDef::Krypton)
      .value("XENON", Gases::GasDef::Xenon);

  py::class_<wincalc::Predefined_Gas_Mixture_Component>(
      m, "PredefinedGasMixtureComponent")
      .def(py::init<Gases::GasDef const &, double>(), py::arg("gas"),
           py::arg("percent"))
      .def_readwrite("gas", &wincalc::Predefined_Gas_Mixture_Component::gas)
      .def_readwrite("percent",
                     &wincalc::Predefined_Gas_Mixture_Component::percent);

  py::class_<Gases::CIntCoeff>(m, "GasCoefficients")
      .def(py::init<double const, double const, double const>(), py::arg("A"),
           py::arg("B"), py::arg("C"));

  py::class_<Gases::CGasData>(m, "CustomGasData")
      .def(py::init<std::string const &, double const, double const,
                    Gases::CIntCoeff const &, Gases::CIntCoeff const &,
                    Gases::CIntCoeff const &>(),
           py::arg("name"), py::arg("molecular_weight"),
           py::arg("specific_heat_ratio"), py::arg("Cp"),
           py::arg("thermal_conductivity"), py::arg("viscosity"));

  py::class_<wincalc::Engine_Gas_Mixture_Component>(m,
                                                    "CustomGasMixtureComponent")
      .def(py::init<Gases::CGasData const &, double>(), py::arg("gas"),
           py::arg("percent"))
      .def_readwrite("gas", &wincalc::Engine_Gas_Mixture_Component::gas)
      .def_readwrite("percent",
                     &wincalc::Engine_Gas_Mixture_Component::percent);

  py::class_<wincalc::Engine_Gap_Info>(m, "Gap")
      .def(py::init<Gases::CGasData const &, double>(),
           py::arg("custom_gas_data"), py::arg("thickness_meters"))
      .def(py::init<std::vector<wincalc::Engine_Gas_Mixture_Component> const &,
                    double>(),
           py::arg("engine_gas_mixture_component_list"),
           py::arg("thickness_meters"))
      .def(py::init<Gases::GasDef const &, double>(),
           py::arg("predefined_gas_type"), py::arg("thickness_meters"))
      .def(py::init<
               std::vector<wincalc::Predefined_Gas_Mixture_Component> const &,
               double>(),
           py::arg("predefined_gas_type_list"), py::arg("thickness_meters"))
      .def(py::init<std::vector<std::variant<
                        wincalc::Predefined_Gas_Mixture_Component,
                        wincalc::Engine_Gas_Mixture_Component>> const &,
                    double>(),
           py::arg("gas_list"), py::arg("thickness_meters"))
      .def_readwrite("gases", &wincalc::Engine_Gap_Info::gases)
      .def_readwrite("thickness", &wincalc::Engine_Gap_Info::thickness);

  py::class_<OpticsParser::MeasurementComponent>(m,
                                                 "OpticalMeasurementComponent")
      .def(py::init<double, double, double, double>(),
           py::arg("transmittance_front"), py::arg("transmittance_back"),
           py::arg("reflectance_front"), py::arg("reflectance_back"))
      .def_readwrite("transmittance_front",
                     &OpticsParser::MeasurementComponent::tf)
      .def_readwrite("transmittance_back",
                     &OpticsParser::MeasurementComponent::tb)
      .def_readwrite("reflectance_front",
                     &OpticsParser::MeasurementComponent::rf)
      .def_readwrite("reflectance_back",
                     &OpticsParser::MeasurementComponent::rb);

  py::class_<OpticsParser::WLData>(m, "WavelengthData")
      .def(py::init<double, OpticsParser::MeasurementComponent,
                    std::optional<OpticsParser::MeasurementComponent>>(),
           py::arg("wavelength_microns"), py::arg("direct_component"),
           py::arg("diffuse_component") =
               std::optional<OpticsParser::MeasurementComponent>())
      .def(py::init<double, double, double, double>(),
           py::arg("wavelength_microns"), py::arg("direct_transmittance"),
           py::arg("direct_reflectance_front"),
           py::arg("direct_reflectance_back"))
      .def(py::init<double, double, double, double, double, double, double,
                    double, double>(),
           py::arg("wavelength_microns"), py::arg("direct_transmittance_front"),
           py::arg("diffuse_transmittance_front"),
           py::arg("direct_transmittance_back"),
           py::arg("diffuse_transmittance_back"),
           py::arg("direct_reflectance_front"),
           py::arg("diffuse_reflectance_front"),
           py::arg("direct_reflectance_back"),
           py::arg("diffuse_reflectance_back"))
      .def_readwrite("wavelength", &OpticsParser::WLData::wavelength)
      .def_readwrite("direct_component", &OpticsParser::WLData::directComponent)
      .def_readwrite("diffuse_component",
                     &OpticsParser::WLData::diffuseComponent);

  py::class_<OpticsParser::ProductGeometry,
             std::shared_ptr<OpticsParser::ProductGeometry>>(m,
                                                             "ProductGeometry");

  py::class_<OpticsParser::VenetianGeometry, OpticsParser::ProductGeometry,
             std::shared_ptr<OpticsParser::VenetianGeometry>>(
      m, "VenetianGeometry")
      .def(py::init<double, double, double, double, int>(),
           py::arg("slat_width"), py::arg("slat_spacing"),
           py::arg("slat_curvature"), py::arg("slat_tilt") = 0,
           py::arg("number_segments") = 5)
      .def_readwrite("slat_width", &OpticsParser::VenetianGeometry::slatWidth)
      .def_readwrite("slat_spacing",
                     &OpticsParser::VenetianGeometry::slatSpacing)
      .def_readwrite("slat_curvature",
                     &OpticsParser::VenetianGeometry::slatCurvature)
      .def_readwrite("slat_tilt", &OpticsParser::VenetianGeometry::slatTilt)
      .def_readwrite("number_segments",
                     &OpticsParser::VenetianGeometry::numberSegments);

  py::class_<OpticsParser::WovenGeometry, OpticsParser::ProductGeometry,
             std::shared_ptr<OpticsParser::WovenGeometry>>(m, "WovenGeometry")
      .def(py::init<double, double, double>())
      .def_readwrite("thread_diameter",
                     &OpticsParser::WovenGeometry::threadDiameter)
      .def_readwrite("thread_spacing",
                     &OpticsParser::WovenGeometry::threadSpacing)
      .def_readwrite("shade_thickness",
                     &OpticsParser::WovenGeometry::shadeThickness);

  py::class_<OpticsParser::PerforatedGeometry, OpticsParser::ProductGeometry,
             std::shared_ptr<OpticsParser::PerforatedGeometry>>(
      m, "PerforatedGeometry")
      .def(py::init<double, double, double, double, std::string>(),
           py::arg("spacing_x_meters"), py::arg("spacing_y_meters"),
           py::arg("dimension_x_meters"), py::arg("dimension_y_meters"),
           py::arg("perforation_type"))
      .def_readwrite("spacing_x", &OpticsParser::PerforatedGeometry::spacingX)
      .def_readwrite("spacing_y", &OpticsParser::PerforatedGeometry::spacingY)
      .def_readwrite("dimension_x",
                     &OpticsParser::PerforatedGeometry::dimensionX)
      .def_readwrite("dimension_y",
                     &OpticsParser::PerforatedGeometry::dimensionY)
      .def_readwrite("perforation_type",
                     &OpticsParser::PerforatedGeometry::perforationType);

  py::class_<OpticsParser::BSDF>(m, "BSDF")
      .def_readwrite("data", &OpticsParser::BSDF::data)
      .def_readwrite("row_angle_basis_name",
                     &OpticsParser::BSDF::rowAngleBasisName)
      .def_readwrite("column_angle_basis_name",
                     &OpticsParser::BSDF::columnAngleBasisName);

  py::class_<OpticsParser::WavelengthBSDFs>(m, "WavelengthBSDFs")
      .def_readwrite("transmittance_front", &OpticsParser::WavelengthBSDFs::tf)
      .def_readwrite("transmittance_back", &OpticsParser::WavelengthBSDFs::tb)
      .def_readwrite("reflectance_front", &OpticsParser::WavelengthBSDFs::rf)
      .def_readwrite("reflectance_back", &OpticsParser::WavelengthBSDFs::rb);

  py::class_<OpticsParser::DualBandBSDF>(m, "DualBandBSDF")
      .def_readwrite("solar", &OpticsParser::DualBandBSDF::solar)
      .def_readwrite("visible", &OpticsParser::DualBandBSDF::visible);

  py::class_<OpticsParser::ProductData,
             std::shared_ptr<OpticsParser::ProductData>>(m, "ProductData")
      .def("composed_product", &OpticsParser::ProductData::composedProduct)
      .def_readwrite("product_name", &OpticsParser::ProductData::productName)
      .def_readwrite("product_type", &OpticsParser::ProductData::productType)
      .def_readwrite("nfrc_id", &OpticsParser::ProductData::nfrcid)
      .def_readwrite("thickness", &OpticsParser::ProductData::thickness)
      .def_readwrite("conductivity", &OpticsParser::ProductData::conductivity)
      .def_readwrite("ir_transmittance",
                     &OpticsParser::ProductData::IRTransmittance)
      .def_readwrite("emissivity_front",
                     &OpticsParser::ProductData::frontEmissivity)
      .def_readwrite("emissivity_back",
                     &OpticsParser::ProductData::backEmissivity)
      .def_readwrite("measurements", &OpticsParser::ProductData::measurements)
      .def_readwrite("permeability_factor",
                     &OpticsParser::ProductData::permeabilityFactor)
      .def_readwrite("density", &OpticsParser::ProductData::density)
      .def_readwrite("youngs_modulus",
                     &OpticsParser::ProductData::youngsModulus);

  py::class_<OpticsParser::CompositionInformation,
             std::shared_ptr<OpticsParser::CompositionInformation>>(
      m, "ProductComposistionData")
      .def(py::init<std::shared_ptr<OpticsParser::ProductData>,
                    std::shared_ptr<OpticsParser::ProductGeometry>>(),
           py::arg("solid_layers"), py::arg("product_geometry"))
      .def_readwrite("material",
                     &OpticsParser::CompositionInformation::material)
      .def_readwrite("geometry",
                     &OpticsParser::CompositionInformation::geometry);

  py::class_<OpticsParser::ComposedProductData, OpticsParser::ProductData,
             std::shared_ptr<OpticsParser::ComposedProductData>>(
      m, "ComposedProductData")
      .def(py::init<OpticsParser::ProductData const &,
                    std::shared_ptr<OpticsParser::CompositionInformation>>(),
           py::arg("solid_layers"), py::arg("product_composition_data"))
      .def(py::init<std::shared_ptr<OpticsParser::CompositionInformation>>(),
           py::arg("product_composition_data"))
      .def("composed_product",
           &OpticsParser::ComposedProductData::composedProduct)
      .def_readwrite(
          "product_composition_data",
          &OpticsParser::ComposedProductData::compositionInformation);

  py::enum_<window_standards::Spectrum_Type>(m, "SpectrumType",
                                             py::arithmetic())
      .value("NONE", window_standards::Spectrum_Type::NONE)
      .value("FILE", window_standards::Spectrum_Type::FILE)
      .value("BLACKBODY", window_standards::Spectrum_Type::BLACKBODY)
      .value("UV_ACTION", window_standards::Spectrum_Type::UV_ACTION)
      .value("KROCHMANN", window_standards::Spectrum_Type::KROCHMANN);

  py::class_<window_standards::Spectrum>(m, "Spectrum")
      .def_readwrite("type", &window_standards::Spectrum::type)
      .def_readwrite("description", &window_standards::Spectrum::description)
      .def_readwrite("t", &window_standards::Spectrum::t)
      .def_readwrite("a", &window_standards::Spectrum::a)
      .def_readwrite("b", &window_standards::Spectrum::b)
      .def_readwrite("values", &window_standards::Spectrum::values);

  py::enum_<window_standards::Wavelength_Set_Type>(m, "WavelengthSetType",
                                                   py::arithmetic())
      .value("FILE", window_standards::Wavelength_Set_Type::FILE)
      .value("SOURCE", window_standards::Wavelength_Set_Type::SOURCE)
      .value("DATA", window_standards::Wavelength_Set_Type::DATA);

  py::class_<window_standards::Wavelength_Set>(m, "WavelengthSet")
      .def_readwrite("type", &window_standards::Wavelength_Set::type)
      .def_readwrite("description",
                     &window_standards::Wavelength_Set::description)
      .def_readwrite("values", &window_standards::Wavelength_Set::values);

  py::enum_<window_standards::Wavelength_Boundary_Type>(
      m, "WavelengthBoundaryType", py::arithmetic())
      .value("NUMBER", window_standards::Wavelength_Boundary_Type::NUMBER)
      .value("WAVELENGTH_SET",
             window_standards::Wavelength_Boundary_Type::WAVELENGTH_SET);

  py::class_<window_standards::Wavelength_Boundary>(m, "WavelengthBoundary")
      .def_readwrite("type", &window_standards::Wavelength_Boundary::type)
      .def_readwrite("value", &window_standards::Wavelength_Boundary::value);

  py::enum_<window_standards::Integration_Rule_Type>(m, "IntegrationRuleType",
                                                     py::arithmetic())
      .value("TRAPEZOIDAL",
             window_standards::Integration_Rule_Type::TRAPEZOIDAL)
      .value("RECTANGULAR",
             window_standards::Integration_Rule_Type::RECTANGULAR)
      .value("TABLE", window_standards::Integration_Rule_Type::TABLE);

  py::class_<window_standards::Integration_Rule>(m, "IntegrationRule")
      .def_readwrite("type", &window_standards::Integration_Rule::type)
      .def_readwrite("k", &window_standards::Integration_Rule::k);

  py::class_<window_standards::Optical_Standard_Method>(m,
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

  py::class_<window_standards::Optical_Standard>(m, "OpticalStandard")
      .def_readwrite("name", &window_standards::Optical_Standard::name)
      .def_readwrite("description",
                     &window_standards::Optical_Standard::description)
      .def_readwrite("file", &window_standards::Optical_Standard::file)
      .def_readwrite("methods", &window_standards::Optical_Standard::methods);

  py::class_<wincalc::Trichromatic>(m, "Trichromatic")
      .def_readwrite("X", &wincalc::Trichromatic::X)
      .def_readwrite("Y", &wincalc::Trichromatic::Y)
      .def_readwrite("Z", &wincalc::Trichromatic::Z);

  py::class_<wincalc::WinCalc_RGB>(m, "RGB")
      .def_readwrite("R", &wincalc::WinCalc_RGB::R)
      .def_readwrite("G", &wincalc::WinCalc_RGB::G)
      .def_readwrite("B", &wincalc::WinCalc_RGB::B);

  py::class_<wincalc::Lab>(m, "Lab")
      .def_readwrite("L", &wincalc::Lab::L)
      .def_readwrite("a", &wincalc::Lab::a)
      .def_readwrite("b", &wincalc::Lab::b);

  py::class_<wincalc::Color_Result>(m, "ColorResult")
      .def_readwrite("trichromatic", &wincalc::Color_Result::trichromatic)
      .def_readwrite("rgb", &wincalc::Color_Result::rgb)
      .def_readwrite("lab", &wincalc::Color_Result::lab);

  declare_wce_optical_results_template<double>(m, "");
  declare_wce_optical_results_template<wincalc::Color_Result>(m, "Color");

  py::enum_<Tarcog::ISO15099::BoundaryConditionsCoeffModel>(
      m, "BoundaryConditionsCoefficientModelType", py::arithmetic())
      .value("CALCULATED_H",
             Tarcog::ISO15099::BoundaryConditionsCoeffModel::CalculateH)
      .value("H_PRESCRIBED",
             Tarcog::ISO15099::BoundaryConditionsCoeffModel::HPrescribed)
      .value("HC_PRESCRIBED",
             Tarcog::ISO15099::BoundaryConditionsCoeffModel::HcPrescribed);

  py::enum_<Tarcog::ISO15099::AirHorizontalDirection>(
      m, "AirHorizontalDirection", py::arithmetic())
      .value("NONE", Tarcog::ISO15099::AirHorizontalDirection::None)
      .value("LEEWARD", Tarcog::ISO15099::AirHorizontalDirection::Leeward)
      .value("WINDWARD", Tarcog::ISO15099::AirHorizontalDirection::Windward);

  py::class_<wincalc::Environment>(m, "Environment")
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

  py::class_<wincalc::Environments>(m, "Environments")
      .def(py::init<wincalc::Environment, wincalc::Environment>(),
           py::arg("outside"), py::arg("inside"))
      .def_readwrite("outside", &wincalc::Environments::outside)
      .def_readwrite("inside", &wincalc::Environments::inside);

  m.def("nfrc_u_environments", &wincalc::nfrc_u_environments,
        "Returns the default environments for running a NFRC U-Value "
        "calculation.");
  m.def(
      "nfrc_shgc_environments", &wincalc::nfrc_shgc_environments,
      "Returns the default environments for running a NFRC SHGC calculation.");

  py::class_<wincalc::Flippable_Solid_Layer,
             std::shared_ptr<wincalc::Flippable_Solid_Layer>>(
      m, "FlippableSolidLayer")
      .def(py::init<double, bool>(), py::arg("thickness_meters"),
           py::arg("flipped") = false)
      .def_readwrite("thickness_meters",
                     &wincalc::Flippable_Solid_Layer::thickness_meters)
      .def_readwrite("flipped", &wincalc::Flippable_Solid_Layer::flipped);

  py::class_<wincalc::Product_Data_Thermal, wincalc::Flippable_Solid_Layer,
             std::shared_ptr<wincalc::Product_Data_Thermal>>(
      m, "ProductDataThermal")
      .def(py::init<double, double, bool, double, double, double, double,
                    double>(),
           py::arg("conductivity"), py::arg("thickness_meters"),
           py::arg("flipped") = false, py::arg("opening_top") = 0,
           py::arg("opening_bottom") = 0, py::arg("opening_left") = 0,
           py::arg("opening_right") = 0, py::arg("opening_front") = 0)
      .def_readwrite("conductivity",
                     &wincalc::Product_Data_Thermal::conductivity)
      .def_readwrite("opening_top", &wincalc::Product_Data_Thermal::opening_top)
      .def_readwrite("opening_bottom",
                     &wincalc::Product_Data_Thermal::opening_bottom)
      .def_readwrite("opening_left",
                     &wincalc::Product_Data_Thermal::opening_left)
      .def_readwrite("opening_right",
                     &wincalc::Product_Data_Thermal::opening_right)
      .def_readwrite("opening_front",
                     &wincalc::Product_Data_Thermal::opening_front)
      .def_readwrite("youngs_modulus",
                     &wincalc::Product_Data_Thermal::youngs_modulus)
      .def_readwrite("density", &wincalc::Product_Data_Thermal::density);

  py::class_<wincalc::Product_Data_Optical, Py_Product_Data_Optical,
             std::shared_ptr<wincalc::Product_Data_Optical>>(
      m, "ProductDataOptical")
      .def(py::init<double, std::optional<double>, std::optional<double>,
                    std::optional<double>, std::optional<double>, double,
                    bool>(),
           py::arg("thickness_meters"),
           py::arg("ir_transmittance_front") = std::optional<double>(),
           py::arg("ir_transmittance_back") = std::optional<double>(),
           py::arg("emissivity_front") = std::optional<double>(),
           py::arg("emissivity_back") = std::optional<double>(),
           py::arg("permeability_factor") = 0.0, py::arg("flipped") = false)
      .def("effective_thermal_values",
           &wincalc::Product_Data_Optical::effective_thermal_values)
      .def("wavelengths", &wincalc::Product_Data_Optical::wavelengths)
      .def_readwrite("ir_transmittance_front",
                     &wincalc::Product_Data_Optical::ir_transmittance_front)
      .def_readwrite("ir_transmittance_back",
                     &wincalc::Product_Data_Optical::ir_transmittance_back)
      .def_readwrite("emissivity_front",
                     &wincalc::Product_Data_Optical::emissivity_front)
      .def_readwrite("emissivity_back",
                     &wincalc::Product_Data_Optical::emissivity_back)
      .def_readwrite("permeability_factor",
                     &wincalc::Product_Data_Optical::permeability_factor);

  py::enum_<FenestrationCommon::MaterialType>(m, "MaterialType",
                                              py::arithmetic())
      .value("APPLIED_FILM", FenestrationCommon::MaterialType::AppliedFilm)
      .value("COATED", FenestrationCommon::MaterialType::Coated)
      .value("ELECTROCHROMIC", FenestrationCommon::MaterialType::Electrochromic)
      .value("FILM", FenestrationCommon::MaterialType::Film)
      .value("INTERLAYER", FenestrationCommon::MaterialType::Interlayer)
      .value("LAMINATE", FenestrationCommon::MaterialType::Laminate)
      .value("MONOLITHIC", FenestrationCommon::MaterialType::Monolithic)
      .value("THERMOCHROMIC", FenestrationCommon::MaterialType::Thermochromic);

  py::enum_<wincalc::CoatedSide>(m, "CoatedSide", py::arithmetic())
      .value("FRONT", wincalc::CoatedSide::FRONT)
      .value("BACK", wincalc::CoatedSide::BACK)
      .value("BOTH", wincalc::CoatedSide::BOTH)
      .value("NEITHER", wincalc::CoatedSide::NEITHER);

  py::class_<wincalc::Product_Data_N_Band_Optical,
             wincalc::Product_Data_Optical,
             std::shared_ptr<wincalc::Product_Data_N_Band_Optical>>(
      m, "ProductDataOpticalNBand")
      .def(py::init<FenestrationCommon::MaterialType, double,
                    std::vector<OpticsParser::WLData>,
                    std::optional<wincalc::CoatedSide>, std::optional<double>,
                    std::optional<double>, std::optional<double>,
                    std::optional<double>, double, bool>(),
           py::arg("material_type"), py::arg("thickness_meters"),
           py::arg("wavelength_data"),
           py::arg("coated_side") = std::optional<wincalc::CoatedSide>(),
           py::arg("ir_transmittance_front") = std::optional<double>(),
           py::arg("ir_transmittance_back") = std::optional<double>(),
           py::arg("emissivity_front") = std::optional<double>(),
           py::arg("emissivity_back") = std::optional<double>(),
           py::arg("permeability_factor") = 0, py::arg("flipped") = false)
      .def("wavelengths", &wincalc::Product_Data_N_Band_Optical::wavelengths)
      .def_readwrite("material_type",
                     &wincalc::Product_Data_N_Band_Optical::material_type)
      .def_readwrite("wavelength_data",
                     &wincalc::Product_Data_N_Band_Optical::wavelength_data);

  py::class_<wincalc::Product_Data_Dual_Band_Optical,
             wincalc::Product_Data_Optical,
             std::shared_ptr<wincalc::Product_Data_Dual_Band_Optical>>(
      m, "ProductDataOpticalDualBand")
      .def(py::init<double, std::optional<double>, std::optional<double>,
                    std::optional<double>, std::optional<double>, double,
                    bool>(),
           py::arg("thickness_meters"),
           py::arg("ir_transmittance_front") = std::optional<double>(),
           py::arg("ir_transmittance_back") = std::optional<double>(),
           py::arg("emissivity_front") = std::optional<double>(),
           py::arg("emissivity_back") = std::optional<double>(),
           py::arg("permeability_factor") = 0.0, py::arg("flipped") = false)
      .def("wavelengths",
           &wincalc::Product_Data_Dual_Band_Optical::wavelengths);

  py::class_<wincalc::Product_Data_Dual_Band_Optical_Specular,
             wincalc::Product_Data_Dual_Band_Optical,
             std::shared_ptr<wincalc::Product_Data_Dual_Band_Optical_Specular>>(
      m, "ProductDataOpticalDualBandSpecular")
      .def(py::init<double, double, double, double, double, double, double,
                    double, double, std::optional<double>,
                    std::optional<double>, std::optional<double>,
                    std::optional<double>, double, bool>(),
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
           py::arg("permeability_factor") = 0.0, py::arg("flipped") = false)
      .def_readwrite(
          "solar_transmittance_front",
          &wincalc::Product_Data_Dual_Band_Optical_Specular::tf_solar)
      .def_readwrite(
          "solar_transmittance_back",
          &wincalc::Product_Data_Dual_Band_Optical_Specular::tb_solar)
      .def_readwrite(
          "solar_reflectance_front",
          &wincalc::Product_Data_Dual_Band_Optical_Specular::rf_solar)
      .def_readwrite(
          "solar_reflectance_back",
          &wincalc::Product_Data_Dual_Band_Optical_Specular::rb_solar)
      .def_readwrite(
          "visible_transmittance_front",
          &wincalc::Product_Data_Dual_Band_Optical_Specular::tf_visible)
      .def_readwrite(
          "visible_transmittance_back",
          &wincalc::Product_Data_Dual_Band_Optical_Specular::tb_visible)
      .def_readwrite(
          "visible_reflectance_front",
          &wincalc::Product_Data_Dual_Band_Optical_Specular::rf_visible)
      .def_readwrite(
          "visible_reflectance_back",
          &wincalc::Product_Data_Dual_Band_Optical_Specular::rb_visible);

  py::class_<wincalc::Product_Data_Dual_Band_Optical_BSDF,
             wincalc::Product_Data_Dual_Band_Optical,
             std::shared_ptr<wincalc::Product_Data_Dual_Band_Optical_BSDF>>(
      m, "ProductDataOpticalDualBandBSDF")
      .def(py::init<std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    std::vector<std::vector<double>> const &,
                    SingleLayerOptics::CBSDFHemisphere const &, double,
                    std::optional<double>, std::optional<double>,
                    std::optional<double>, std::optional<double>, double,
                    bool>(),
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
           py::arg("permeability_factor") = 0.0, py::arg("flipped") = false)
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
      .def("effective_thermal_values",
           &wincalc::Product_Data_Dual_Band_Optical_BSDF::
               effective_thermal_values);

  py::class_<wincalc::Product_Data_Optical_With_Material,
             wincalc::Product_Data_Optical,
             std::shared_ptr<wincalc::Product_Data_Optical_With_Material>>(
      m, "ProductDataOpticalWithMaterial")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical> const &>(),
           py::arg("product_data_optical"))
      .def("optical_data",
           &wincalc::Product_Data_Optical_With_Material::optical_data)
      .def("wavelengths",
           &wincalc::Product_Data_Optical_With_Material::wavelengths)
      .def_readwrite(
          "material_optical_data",
          &wincalc::Product_Data_Optical_With_Material::material_optical_data);

  py::enum_<SingleLayerOptics::DistributionMethod>(m, "DistributionMethodType",
                                                   py::arithmetic())
      .value("UNIFORM_DIFFUSE",
             SingleLayerOptics::DistributionMethod::UniformDiffuse)
      .value("DIRECTIONAL_DIFFUSE",
             SingleLayerOptics::DistributionMethod::DirectionalDiffuse);

  py::class_<wincalc::Product_Data_Optical_Venetian,
             wincalc::Product_Data_Optical_With_Material,
             std::shared_ptr<wincalc::Product_Data_Optical_Venetian>>(
      m, "ProductDataOpticalVenetian")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical> const &,
                    double, double, double, double, int,
                    SingleLayerOptics::DistributionMethod>(),
           py::arg("product_data_optical"), py::arg("slat_tilt_meters"),
           py::arg("slat_width_meters"), py::arg("slat_spacing_meters"),
           py::arg("slat_curvature_meters"), py::arg("numbers_slats"),
           py::arg("distribution_method") =
               SingleLayerOptics::DistributionMethod::DirectionalDiffuse)
      .def_readwrite("slat_tilt",
                     &wincalc::Product_Data_Optical_Venetian::slat_tilt)
      .def_readwrite("slat_width",
                     &wincalc::Product_Data_Optical_Venetian::slat_width)
      .def_readwrite("slat_spacing",
                     &wincalc::Product_Data_Optical_Venetian::slat_spacing)
      .def_readwrite("slat_curvature",
                     &wincalc::Product_Data_Optical_Venetian::slat_curvature)
      .def_readwrite("number_slats",
                     &wincalc::Product_Data_Optical_Venetian::number_slats)
      .def_readwrite(
          "distribution_method",
          &wincalc::Product_Data_Optical_Venetian::distribution_method);

  py::class_<wincalc::Product_Data_Optical_Woven_Shade,
             wincalc::Product_Data_Optical_With_Material,
             std::shared_ptr<wincalc::Product_Data_Optical_Woven_Shade>>(
      m, "ProductDataOpticalWovenShade")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical> const &,
                    double, double, double>(),
           py::arg("material_product_data_optical"), py::arg("thread_diamater"),
           py::arg("thread_spacing"), py::arg("shade_thickness"))
      .def_readwrite(
          "thread_diameter",
          &wincalc::Product_Data_Optical_Woven_Shade::thread_diameter)
      .def_readwrite("thread_spacing",
                     &wincalc::Product_Data_Optical_Woven_Shade::thread_spacing)
      .def_readwrite(
          "shade_thickness",
          &wincalc::Product_Data_Optical_Woven_Shade::shade_thickness);

  py::class_<wincalc::Product_Data_Optical_Perforated_Screen,
             wincalc::Product_Data_Optical_With_Material,
             std::shared_ptr<wincalc::Product_Data_Optical_Perforated_Screen>>
      product_data_optical_perforated_screen(
          m, "ProductDataOpticalPerforatedScreen");

  product_data_optical_perforated_screen
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical> const &,
                    double, double, double, double,
                    wincalc::Product_Data_Optical_Perforated_Screen::Type>(),
           py::arg("material_product_data_optical"), py::arg("spacing_x"),
           py::arg("spacing_y"), py::arg("dimension_x"), py::arg("dimension_y"),
           py::arg("perforation_type"))
      .def_readwrite(
          "spacing_x",
          &wincalc::Product_Data_Optical_Perforated_Screen::spacing_x)
      .def_readwrite(
          "spacing_y",
          &wincalc::Product_Data_Optical_Perforated_Screen::spacing_y)
      .def_readwrite(
          "dimension_x",
          &wincalc::Product_Data_Optical_Perforated_Screen::dimension_x)
      .def_readwrite(
          "dimension_y",
          &wincalc::Product_Data_Optical_Perforated_Screen::dimension_y)
      .def_readwrite(
          "perforation_type",
          &wincalc::Product_Data_Optical_Perforated_Screen::perforation_type);

  py::enum_<wincalc::Product_Data_Optical_Perforated_Screen::Type>(
      product_data_optical_perforated_screen, "Type")
      .value("CIRCULAR",
             wincalc::Product_Data_Optical_Perforated_Screen::Type::CIRCULAR)
      .value("RECTANGULAR",
             wincalc::Product_Data_Optical_Perforated_Screen::Type::RECTANGULAR)
      .value("SQUARE",
             wincalc::Product_Data_Optical_Perforated_Screen::Type::SQUARE);

  py::class_<wincalc::Product_Data_Optical_Thermal>(
      m, "ProductDataOpticalAndThermal")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical>,
                    std::shared_ptr<wincalc::Product_Data_Thermal>>(),
           py::arg("prouct_data_optical"), py::arg("product_data_thermal"))
      .def_readwrite("optical_data",
                     &wincalc::Product_Data_Optical_Thermal::optical_data)
      .def_readwrite("thermal_data",
                     &wincalc::Product_Data_Optical_Thermal::thermal_data);

  py::enum_<SingleLayerOptics::BSDFBasis>(m, "BSDFBasisType", py::arithmetic())
      .value("SMALL", SingleLayerOptics::BSDFBasis::Small)
      .value("QUARTER", SingleLayerOptics::BSDFBasis::Quarter)
      .value("HALF", SingleLayerOptics::BSDFBasis::Half)
      .value("FULL", SingleLayerOptics::BSDFBasis::Full);

  py::class_<SingleLayerOptics::CBSDFHemisphere>(m, "BSDFHemisphere")
      .def_static("create",
                  py::overload_cast<SingleLayerOptics::BSDFBasis>(
                      &SingleLayerOptics::CBSDFHemisphere::create),
                  py::arg("bsdf_basis"))
      .def("get_directions",
           &SingleLayerOptics::CBSDFHemisphere::getDirections);

  py::enum_<Tarcog::ISO15099::System>(m, "TarcogSystemType", py::arithmetic())
      .value("U", Tarcog::ISO15099::System::Uvalue)
      .value("SHGC", Tarcog::ISO15099::System::SHGC);

  py::enum_<wincalc::Spectal_Data_Wavelength_Range_Method>(
      m, "SpectalDataWavelengthRangeMethodType", py::arithmetic())
      .value("FULL", wincalc::Spectal_Data_Wavelength_Range_Method::FULL)
      .value("ISO_9050",
             wincalc::Spectal_Data_Wavelength_Range_Method::ISO_9050)
      .value("CONDENSED",
             wincalc::Spectal_Data_Wavelength_Range_Method::CONDENSED);

  m.def("nfrc_u_environments", &wincalc::nfrc_u_environments);
  m.def("nfrc_shgc_environments", &wincalc::nfrc_shgc_environments);

  py::class_<wincalc::Deflection_Results>(m, "DeflectionResults")
      .def_readwrite("deflection_max",
                     &wincalc::Deflection_Results::deflection_max)
      .def_readwrite("deflection_mean",
                     &wincalc::Deflection_Results::deflection_mean)
      .def_readwrite("panes_load", &wincalc::Deflection_Results::panes_load);

  py::class_<wincalc::Glazing_System>(m, "GlazingSystem")
      .def(py::init<window_standards::Optical_Standard const &,
                    std::vector<wincalc::Product_Data_Optical_Thermal> const &,
                    std::vector<wincalc::Engine_Gap_Info> const &, double,
                    double, double, wincalc::Environments const &,
                    std::optional<SingleLayerOptics::CBSDFHemisphere> const &,
                    wincalc::Spectal_Data_Wavelength_Range_Method const &, int,
                    int>(),
           py::arg("optical_standard"), py::arg("solid_layers"),
           py::arg("gap_layers") = std::vector<wincalc::Engine_Gap_Info>(),
           py::arg("width_meters") = 1.0, py::arg("height_meters") = 1.0,
           py::arg("tilt_degrees") = 90,
           py::arg("environment") = wincalc::nfrc_u_environments(),
           py::arg("bsdf_hemisphere") =
               std::optional<SingleLayerOptics::CBSDFHemisphere>(),
           py::arg("spectral_data_wavelength_range_method") =
               wincalc::Spectal_Data_Wavelength_Range_Method::FULL,
           py::arg("number_visible_bands") = 5,
           py::arg("number_solar_bands") = 10)
      .def(py::init<
               window_standards::Optical_Standard const &,
               std::vector<std::shared_ptr<OpticsParser::ProductData>> const &,
               std::vector<wincalc::Engine_Gap_Info> const &, double, double,
               double, wincalc::Environments const &,
               std::optional<SingleLayerOptics::CBSDFHemisphere> const &,
               wincalc::Spectal_Data_Wavelength_Range_Method const &, int,
               int>(),
           py::arg("optical_standard"), py::arg("solid_layers"),
           py::arg("gap_layers") = std::vector<wincalc::Engine_Gap_Info>(),
           py::arg("width_meters") = 1.0, py::arg("height_meters") = 1.0,
           py::arg("tilt_degrees") = 90,
           py::arg("environment") = wincalc::nfrc_u_environments(),
           py::arg("bsdf_hemisphere") =
               std::optional<SingleLayerOptics::CBSDFHemisphere>(),
           py::arg("spectral_data_wavelength_range_method") =
               wincalc::Spectal_Data_Wavelength_Range_Method::FULL,
           py::arg("number_visible_bands") = 5,
           py::arg("number_solar_bands") = 10)
      .def(py::init<window_standards::Optical_Standard const &,
                    std::vector<std::variant<
                        std::shared_ptr<OpticsParser::ProductData>,
                        wincalc::Product_Data_Optical_Thermal>> const &,
                    std::vector<wincalc::Engine_Gap_Info> const &, double,
                    double, double, wincalc::Environments const &,
                    std::optional<SingleLayerOptics::CBSDFHemisphere> const &,
                    wincalc::Spectal_Data_Wavelength_Range_Method const &, int,
                    int>(),
           py::arg("optical_standard"), py::arg("solid_layers"),
           py::arg("gap_layers") = std::vector<wincalc::Engine_Gap_Info>(),
           py::arg("width_meters") = 1.0, py::arg("height_meters") = 1.0,
           py::arg("tilt_degrees") = 90,
           py::arg("environment") = wincalc::nfrc_u_environments(),
           py::arg("bsdf_hemisphere") =
               std::optional<SingleLayerOptics::CBSDFHemisphere>(),
           py::arg("spectral_data_wavelength_range_method") =
               wincalc::Spectal_Data_Wavelength_Range_Method::FULL,
           py::arg("number_visible_bands") = 5,
           py::arg("number_solar_bands") = 10)
      .def("u", &wincalc::Glazing_System::u, py::arg("theta") = 0,
           py::arg("phi") = 0)
      .def("shgc", &wincalc::Glazing_System::shgc, py::arg("theta") = 0,
           py::arg("phi") = 0)
      .def("layer_temperatures", &wincalc::Glazing_System::layer_temperatures,
           py::arg("system_type"), py::arg("theta") = 0, py::arg("phi") = 0)
      .def("optical_method_results",
           &wincalc::Glazing_System::optical_method_results,
           py::arg("method_name"), py::arg("theta") = 0, py::arg("phi") = 0)
      .def("color", &wincalc::Glazing_System::color, py::arg("theta") = 0,
           py::arg("phi") = 0,
           py::arg("tristimulus_x_method") = "COLOR_TRISTIMX",
           py::arg("tristimulus_y_method") = "COLOR_TRISTIMY",
           py::arg("tristimulus_z_method") = "COLOR_TRISTIMZ")
      .def("solid_layers_effective_conductivities",
           &wincalc::Glazing_System::solid_layers_effective_conductivities,
           py::arg("system_type"), py::arg("theta") = 0, py::arg("phi") = 0)
      .def("gap_layers_effective_conductivities",
           &wincalc::Glazing_System::gap_layers_effective_conductivities,
           py::arg("system_type"), py::arg("theta") = 0, py::arg("phi") = 0)
      .def("system_effective_conductivity",
           &wincalc::Glazing_System::system_effective_conductivity,
           py::arg("system_type"), py::arg("theta") = 0, py::arg("phi") = 0)
      .def("relative_heat_gain", &wincalc::Glazing_System::relative_heat_gain,
           py::arg("theta") = 0, py::arg("phi") = 0)
      .def("environments",
           py::overload_cast<wincalc::Environments const &>(
               &wincalc::Glazing_System::environments),
           py::arg("environments"))
      .def("environments",
           py::overload_cast<>(&wincalc::Glazing_System::environments,
                               py::const_))
      .def("enable_deflection", &wincalc::Glazing_System::enable_deflection,
           py::arg("enable"))
      .def("set_deflection_properties",
           &wincalc::Glazing_System::set_deflection_properties,
           py::arg("temperature_initial"), py::arg("pressure_initial"))
      .def("calc_deflection_properties",
           &wincalc::Glazing_System::calc_deflection_properties,
           py::arg("system_type"), py::arg("theta") = 0, py::arg("phi") = 0)
      .def("set_applied_loads", &wincalc::Glazing_System::set_applied_loads,
           py::arg("loads"))
      .def("set_height", &wincalc::Glazing_System::set_height,
           py::arg("height_meters"))
      .def("set_width", &wincalc::Glazing_System::set_width,
           py::arg("width_meters"))
      .def("set_tilt", &wincalc::Glazing_System::set_tilt,
           py::arg("tilt_degrees"));

  m.def("convert_to_solid_layer", &wincalc::convert_to_solid_layer,
        "Convert product data into a solid layer that can be used in glazing "
        "systems.");

  m.def("convert_to_solid_layers", &wincalc::convert_to_solid_layers,
        "Convert a list of product data into a solid layer that can be used in "
        "glazing systems.");

  m.def("load_standard",
        py::overload_cast<std::string const &>(
            &window_standards::load_optical_standard),
        "Load standard from .std file");
  m.def("parse_json", &OpticsParser::parseJSONString,
        "Load product data from json string");
  m.def("parse_json_file", &OpticsParser::parseJSONFile,
        "Load product data from json file");
  m.def("parse_optics_file", &OpticsParser::parseOpticsFile,
        "Load product data from optics file");
  m.def("parse_bsdf_xml_file", &OpticsParser::parseBSDFXMLFile,
        "Load product data from BSDF xml file");
  m.def("parse_bsdf_xml_string", &OpticsParser::parseBSDFXMLString,
        "Load product data from BSDF xml string");
  m.def("parse_thmx_file", &thmxParser::parseFile, "Parse a THERM thmx file");
  m.def("parse_thmx_string", &thmxParser::parseString,
        "Parse THERM thmx format from a string");

  py::class_<thmxParser::MeshParameters>(m, "ThmxMeshParameters")
      .def_readwrite("quad_tree_mesh_level",
                     &thmxParser::MeshParameters::quadTreeMeshLevel)
      .def_readwrite("error_check_flag",
                     &thmxParser::MeshParameters::errorCheckFlag)
      .def_readwrite("error_limit", &thmxParser::MeshParameters::errorLimit)
      .def_readwrite("max_iterations",
                     &thmxParser::MeshParameters::maxIterations)
      .def_readwrite("cma_flag", &thmxParser::MeshParameters::cmaFlag);

  py::class_<thmxParser::ColorRGB>(m, "ThmxRGB")
      .def_readwrite("r", &thmxParser::ColorRGB::r)
      .def_readwrite("g", &thmxParser::ColorRGB::g)
      .def_readwrite("b", &thmxParser::ColorRGB::b);

  py::class_<thmxParser::Material>(m, "ThmxMaterial")
      .def_readwrite("name", &thmxParser::Material::name)
      .def_readwrite("type", &thmxParser::Material::type)
      .def_readwrite("conductivity", &thmxParser::Material::conductivity)
      .def_readwrite("emissivity_front", &thmxParser::Material::emissivityFront)
      .def_readwrite("emissivity_back", &thmxParser::Material::emissivityBack)
      .def_readwrite("tir", &thmxParser::Material::tir)
      .def_readwrite("color", &thmxParser::Material::color)
      .def_readwrite("cavity_model", &thmxParser::Material::cavityModel)
      .def_readwrite("transmittances", &thmxParser::Material::transmittances)
      .def_readwrite("reflectances", &thmxParser::Material::reflectances);

  py::class_<thmxParser::BoundaryCondition>(m, "ThmxBoundaryCondition")
      .def_readwrite("name", &thmxParser::BoundaryCondition::name)
      .def_readwrite("type", &thmxParser::BoundaryCondition::type)
      .def_readwrite("H", &thmxParser::BoundaryCondition::H)
      .def_readwrite("heat_flux", &thmxParser::BoundaryCondition::heatFlux)
      .def_readwrite("temperature", &thmxParser::BoundaryCondition::temperature)
      .def_readwrite("color", &thmxParser::BoundaryCondition::color)
      .def_readwrite("Tr", &thmxParser::BoundaryCondition::Tr)
      .def_readwrite("Hr", &thmxParser::BoundaryCondition::Hr)
      .def_readwrite("Ei", &thmxParser::BoundaryCondition::Ei)
      .def_readwrite("view_factor", &thmxParser::BoundaryCondition::viewFactor)
      .def_readwrite("radiation_model",
                     &thmxParser::BoundaryCondition::radiationModel)
      .def_readwrite("convection_flag",
                     &thmxParser::BoundaryCondition::convectionFlag)
      .def_readwrite("flux_flag", &thmxParser::BoundaryCondition::fluxFlag)
      .def_readwrite("radiation_flag",
                     &thmxParser::BoundaryCondition::radiationFlag)
      .def_readwrite("constant_temperature_flag",
                     &thmxParser::BoundaryCondition::constantTemperatureFlag)
      .def_readwrite("emissivity_modifier",
                     &thmxParser::BoundaryCondition::emissivityModifier);

  py::class_<thmxParser::PolygonPoint>(m, "ThmxPolygonPoint")
      .def_readwrite("index", &thmxParser::PolygonPoint::index)
      .def_readwrite("x", &thmxParser::PolygonPoint::x)
      .def_readwrite("y", &thmxParser::PolygonPoint::y);

  py::class_<thmxParser::Polygon>(m, "ThmxPolygon")
      .def_readwrite("id", &thmxParser::Polygon::id)
      .def_readwrite("material", &thmxParser::Polygon::material)
      .def_readwrite("points", &thmxParser::Polygon::points);

  py::class_<thmxParser::BoundaryConditionPolygon>(
      m, "ThmxBoundaryConditionPolygon")
      .def_readwrite("id", &thmxParser::BoundaryConditionPolygon::id)
      .def_readwrite("name", &thmxParser::BoundaryConditionPolygon::name)
      .def_readwrite("polygon_id",
                     &thmxParser::BoundaryConditionPolygon::polygonId)
      .def_readwrite("enclosure_id",
                     &thmxParser::BoundaryConditionPolygon::enclosureId)
      .def_readwrite("ufactor_tag",
                     &thmxParser::BoundaryConditionPolygon::ufactorTag)
      .def_readwrite("ratation_model",
                     &thmxParser::BoundaryConditionPolygon::ratationModel)
      .def_readwrite("emissivity",
                     &thmxParser::BoundaryConditionPolygon::emissivity)
      .def_readwrite("surfaceSide",
                     &thmxParser::BoundaryConditionPolygon::surfaceSide)
      .def_readwrite("illuminated_surface",
                     &thmxParser::BoundaryConditionPolygon::illuminatedSurface)
      .def_readwrite("points", &thmxParser::BoundaryConditionPolygon::points);

  py::class_<thmxParser::CMABestWorstOption>(m, "ThmxCMABestWorstOption")
      .def_readwrite("option", &thmxParser::CMABestWorstOption::option)
      .def_readwrite(
          "inside_convective_film_coefficient",
          &thmxParser::CMABestWorstOption::insideConvectiveFilmCoefficient)
      .def_readwrite(
          "outside_convective_film_coefficient",
          &thmxParser::CMABestWorstOption::outsideConvectiveFilmCoefficient)
      .def_readwrite("glazing_gap_conductance",
                     &thmxParser::CMABestWorstOption::glazingGapConductance)
      .def_readwrite("spacer_conductance",
                     &thmxParser::CMABestWorstOption::spacerConductance);

  py::class_<thmxParser::CMAOptions>(m, "ThmxCMAOptions")
      .def_readwrite("interior_layer_conductivity",
                     &thmxParser::CMAOptions::interiorLayerConductivity)
      .def_readwrite("interior_layer_thickness",
                     &thmxParser::CMAOptions::interiorLayerThickness)
      .def_readwrite("interior_layer_emissivity",
                     &thmxParser::CMAOptions::interiorLayerEmissivity)
      .def_readwrite("exterior_layer_conductivity",
                     &thmxParser::CMAOptions::exteriorLayerConductivity)
      .def_readwrite("exterior_layer_thickness",
                     &thmxParser::CMAOptions::exteriorLayerThickness)
      .def_readwrite("exterior_layer_emissivity",
                     &thmxParser::CMAOptions::exteriorLayerEmissivity)
      .def_readwrite("interior_temperature",
                     &thmxParser::CMAOptions::interiorTemperature)
      .def_readwrite("exterior_temperature",
                     &thmxParser::CMAOptions::exteriorTemperature)
      .def_readwrite("best_worst_options",
                     &thmxParser::CMAOptions::bestWorstOptions);

  py::class_<thmxParser::UFactorProjectionResult>(m,
                                                  "ThmxUFactorProjectionResult")
      .def_readwrite("length_type",
                     &thmxParser::UFactorProjectionResult::lengthType)
      .def_readwrite("length_units",
                     &thmxParser::UFactorProjectionResult::lengthUnits)
      .def_readwrite("length", &thmxParser::UFactorProjectionResult::length)
      .def_readwrite("ufactor_units",
                     &thmxParser::UFactorProjectionResult::ufactorUnits)
      .def_readwrite("ufactor", &thmxParser::UFactorProjectionResult::ufactor);

  py::class_<thmxParser::UFactorResults>(m, "ThmxUFactorResults")
      .def_readwrite("tag", &thmxParser::UFactorResults::tag)
      .def_readwrite("delta_t_units", &thmxParser::UFactorResults::deltaTUnits)
      .def_readwrite("delta_t", &thmxParser::UFactorResults::deltaT)
      .def_readwrite("projection_results",
                     &thmxParser::UFactorResults::projectionResults);

  py::class_<thmxParser::Result>(m, "ThmxResult")
      .def_readwrite("model_type", &thmxParser::Result::modelType)
      .def_readwrite("glazing_case", &thmxParser::Result::glazingCase)
      .def_readwrite("spacer_case", &thmxParser::Result::spacerCase)
      .def_readwrite("ufactor_results", &thmxParser::Result::ufactorResults);

  py::class_<thmxParser::ThmxFileContents>(m, "ThmxFileContents")
      .def_readwrite("file_version", &thmxParser::ThmxFileContents::fileVersion)
      .def_readwrite("mesh_parameters",
                     &thmxParser::ThmxFileContents::meshParameters)
      .def_readwrite("materials", &thmxParser::ThmxFileContents::materials)
      .def_readwrite("boundary_conditions",
                     &thmxParser::ThmxFileContents::boundaryConditions)
      .def_readwrite("polygons", &thmxParser::ThmxFileContents::polygons)
      .def_readwrite("boundary_condition_polygons",
                     &thmxParser::ThmxFileContents::boundaryConditionPolygons)
      .def_readwrite("cma_options", &thmxParser::ThmxFileContents::cmaOptions)
      .def_readwrite("results", &thmxParser::ThmxFileContents::results);

  py::class_<Tarcog::IGUDimensions>(m, "GlazingSystemDimensions")
      .def_readwrite("width", &Tarcog::IGUDimensions::width)
      .def_readwrite("height", &Tarcog::IGUDimensions::height);

  py::class_<CMA::ICMAWindow, std::shared_ptr<CMA::ICMAWindow>>(m, "CMAWindow")
      .def("u", &CMA::ICMAWindow::uValue)
      .def("shgc", &CMA::ICMAWindow::shgc)
      .def("vt", &CMA::ICMAWindow::vt)
      .def("glazing_system_dimensions", &CMA::ICMAWindow::getIGUDimensions);

  py::class_<CMA::CMABestWorstUFactors,
             std::shared_ptr<CMA::CMABestWorstUFactors>>(m,
                                                         "CMABestWorstUFactors")
      .def(py::init<>())
      .def(py::init<double, double, double>())
      .def(py::init<double, double, double, double, double, double, double,
                    double, double, double, double>())
      .def("u", &CMA::CMABestWorstUFactors::uValue)
      .def("hc_out", &CMA::CMABestWorstUFactors::hcout);

  m.def("create_best_worst_u_factor_option",
        &CMA::CreateBestWorstUFactorOption);

  py::class_<CMA::CMAWindowSingleVision, CMA::ICMAWindow,
             std::shared_ptr<CMA::CMAWindowSingleVision>>(
      m, "CMAWindowSingleVision")
      .def(py::init<double, double, double, double, CMA::CMABestWorstUFactors,
                    CMA::CMABestWorstUFactors>(),
           py::arg("width"), py::arg("height"),
           py::arg("spacer_best_keff") = 0.01,
           py::arg("spacer_worst_keff") = 10.0,
           py::arg("best_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Best),
           py::arg("worst_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Worst))
      .def("set_frame_top", &CMA::CMAWindowSingleVision::setFrameTop)
      .def("set_frame_bottom", &CMA::CMAWindowSingleVision::setFrameBottom)
      .def("set_frame_left", &CMA::CMAWindowSingleVision::setFrameLeft)
      .def("set_frame_right", &CMA::CMAWindowSingleVision::setFrameRight)
      .def("set_dividers", &CMA::CMAWindowSingleVision::setDividers);

  py::class_<CMA::CMAWindowDualVisionHorizontal, CMA::ICMAWindow,
             std::shared_ptr<CMA::CMAWindowDualVisionHorizontal>>(
      m, "CMAWindowDualVisionHorizontal")
      .def(py::init<double, double, double, double, CMA::CMABestWorstUFactors,
                    CMA::CMABestWorstUFactors>(),
           py::arg("width"), py::arg("height"),
           py::arg("spacer_best_keff") = 0.01,
           py::arg("spacer_worst_keff") = 10.0,
           py::arg("best_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Best),
           py::arg("worst_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Worst))
      .def("set_frame_top_left",
           &CMA::CMAWindowDualVisionHorizontal::setFrameTopLeft)
      .def("set_frame_top_right",
           &CMA::CMAWindowDualVisionHorizontal::setFrameTopRight)
      .def("set_frame_bottom_left",
           &CMA::CMAWindowDualVisionHorizontal::setFrameBottomLeft)
      .def("set_frame_bottom_right",
           &CMA::CMAWindowDualVisionHorizontal::setFrameBottomRight)
      .def("set_frame_left", &CMA::CMAWindowDualVisionHorizontal::setFrameLeft)
      .def("set_frame_right",
           &CMA::CMAWindowDualVisionHorizontal::setFrameRight)
      .def("set_frame_meeting_rail",
           &CMA::CMAWindowDualVisionHorizontal::setFrameMeetingRail)
      .def("set_dividers", &CMA::CMAWindowDualVisionHorizontal::setDividers);

  py::class_<CMA::CMAWindowDualVisionVertical, CMA::ICMAWindow,
             std::shared_ptr<CMA::CMAWindowDualVisionVertical>>(
      m, "CMAWindowDualVisionVertical")
      .def(py::init<double, double, double, double, CMA::CMABestWorstUFactors,
                    CMA::CMABestWorstUFactors>(),
           py::arg("width"), py::arg("height"),
           py::arg("spacer_best_keff") = 0.01,
           py::arg("spacer_worst_keff") = 10.0,
           py::arg("best_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Best),
           py::arg("worst_u_factor_options") =
               CMA::CreateBestWorstUFactorOption(CMA::Option::Worst))
      .def("set_frame_top", &CMA::CMAWindowDualVisionVertical::setFrameTop)
      .def("set_frame_bottom",
           &CMA::CMAWindowDualVisionVertical::setFrameBottom)
      .def("set_frame_top_left",
           &CMA::CMAWindowDualVisionVertical::setFrameTopLeft)
      .def("set_frame_top_right",
           &CMA::CMAWindowDualVisionVertical::setFrameTopRight)
      .def("set_frame_bottom_left",
           &CMA::CMAWindowDualVisionVertical::setFrameBottomLeft)
      .def("set_frame_bottom_right",
           &CMA::CMAWindowDualVisionVertical::setFrameBottomRight)
      .def("set_frame_meeting_rail",
           &CMA::CMAWindowDualVisionVertical::setFrameMeetingRail)
      .def("set_dividers", &CMA::CMAWindowDualVisionVertical::setDividers);
	  
  py::class_<wincalc::ThermalIRResults>(m, "ThermalIRResults")
      .def_readwrite("transmittance_front_diffuse_diffuse", &wincalc::ThermalIRResults::transmittance_front_diffuse_diffuse)
      .def_readwrite("transmittance_back_diffuse_diffuse", &wincalc::ThermalIRResults::transmittance_back_diffuse_diffuse)
	  .def_readwrite("emissivity_front_hemispheric", &wincalc::ThermalIRResults::emissivity_front_hemispheric)
      .def_readwrite("emissivity_back_hemispheric", &wincalc::ThermalIRResults::emissivity_back_hemispheric);

  m.def("calc_thermal_ir", &wincalc::calc_thermal_ir, py::arg("optical_standard"), py::arg("product_data"), 
		py::arg("wavelength_range_method") = wincalc::Spectal_Data_Wavelength_Range_Method::FULL,
		py::arg("number_visible_bands") = 5, py::arg("number_solar_bands") = 10);
#if 0	  
  m.def("calc_thermal_ir", py::overload_cast<window_standards::Optical_Standard const&, wincalc::Product_Data_Optical_Thermal const&,
		wincalc::Spectal_Data_Wavelength_Range_Method const&,int,int>(&wincalc::calc_thermal_ir), py::arg("optical_standard"), py::arg("product_data"), 
		py::arg("wavelength_range_method") = wincalc::Spectal_Data_Wavelength_Range_Method::FULL,
		py::arg("number_visible_bands") = 5, py::arg("number_solar_bands") = 10);
		
//  m.def("calc_thermal_ir", py::overload_cast<window_standards::Optical_Standard const&, std::shared_ptr<OpticsParser::ProductData> const&,
//		wincalc::Spectal_Data_Wavelength_Range_Method const&,int,int>(&wincalc::calc_thermal_ir), py::arg("optical_standard"), py::arg("product_data"), 
//		py::arg("wavelength_range_method") = wincalc::Spectal_Data_Wavelength_Range_Method::FULL,
//		py::arg("number_visible_bands") = 5, py::arg("number_solar_bands") = 10);
#endif 
  m.def("get_spacer_keff", &wincalc::get_spacer_keff,
        "Calculate the effective conductivity of a spacer from a THERM thmx "
        "file.");
  m.def("get_cma_window_single_vision", &wincalc::get_cma_window_single_vision,
        "Get the CMA template for a single vision window.");
  m.def("get_cma_window_double_vision_vertical",
        &wincalc::get_cma_window_double_vision_vertical,
        "Get the CMA template for a double vision vertical window.");
  m.def("get_cma_window_double_vision_horizontal",
        &wincalc::get_cma_window_double_vision_horizontal,
        "Get the CMA template for a double vision horizontal window.");

  py::class_<wincalc::CMAResult>(m, "CMAResult")
      .def_readwrite("u", &wincalc::CMAResult::u)
      .def_readwrite("shgc", &wincalc::CMAResult::shgc)
      .def_readwrite("vt", &wincalc::CMAResult::vt);

  m.def("calc_cma", &wincalc::calc_cma, "Get CMA results.");
}
