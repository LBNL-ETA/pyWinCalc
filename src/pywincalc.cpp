#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <wincalc/wincalc.h>

namespace py = pybind11;

using namespace pybind11::literals;


template <typename T>
void declare_wce_optical_result_simple(py::module &m, std::string typestr) {
  using Class = WCE_Optical_Result_Simple<T>;
  declare_optical_result_by_transmittance<T>(m, typestr);
  std::string pyclass_name = std::string("WCE_Optical_Result_Simple") + typestr;
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("direct_direct", &Class::direct_direct)
      .def_readwrite("direct_diffuse", &Class::direct_diffuse)
      .def_readwrite("diffuse_diffuse", &Class::diffuse_diffuse)
	  .def_readwrite("hemispherical", &Class::hemispherical);
}

template <>
void declare_wce_optical_result_simple<Color_Result>(py::module &m, std::string typestr) {
  using Class = WCE_Optical_Result_Simple<T>;
  declare_optical_result_by_transmittance<T>(m, typestr);
  std::string pyclass_name = std::string("WCE_Optical_Result_Simple") + typestr;
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("direct_direct", &Class::direct_direct)
      .def_readwrite("direct_diffuse", &Class::direct_diffuse)
      .def_readwrite("diffuse_diffuse", &Class::diffuse_diffuse)
}

template <typename T>
void declare_wce_optical_result_absorptance(py::module &m, std::string typestr) {
  using Class = WCE_Optical_Result_Absorptance<T>;
  declare_optical_result_by_transmittance<T>(m, typestr);
  std::string pyclass_name = std::string("WCE_Optical_Result_Absorptance") + typestr;
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("direct", &Class::direct)
      .def_readwrite("diffuse", &Class::diffuse)
      .def_readwrite("hemispherical", &Class::hemispherical);
}

template <typename T>
void declare_optical_result_by_side(py::module &m,
                                             std::string typestr) {
  using Class = WCE_Optical_Result_By_Side<T>;
  declare_wce_optical_result_simple<T>(m, typestr);
  declare_wce_optical_result_absorptance<T>(m, typestr);
  std::string pyclass_name = std::string("WCE_Optical_Result") + typestr;
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("tf", &Class::tf)
      .def_readwrite("tb", &Class::tb)
      .def_readwrite("rf", &Class::rf)
      .def_readwrite("rb", &Class::rb)
	  .def_readwrite("absorptances_front", &Class::absorptances_front)
	  .def_readwrite("absorptances_back", &Class::absorptances_back);	  
}

template <>
void declare_optical_result_by_side<Color_Result>(py::module &m,
                                             std::string typestr) {
  using Class = WCE_Optical_Result_By_Side<T>;
  declare_wce_optical_result_simple<Color_Result>(m, typestr);
  std::string pyclass_name = std::string("WCE_Optical_Result");
  py::class_<Class>(m, pyclass_name.c_str(), py::buffer_protocol(),
                    py::dynamic_attr())
      .def_readwrite("tf", &Class::tf)
      .def_readwrite("tb", &Class::tb)
      .def_readwrite("rf", &Class::rf)
      .def_readwrite("rb", &Class::rb);	  
}




PYBIND11_MODULE(pywincalc, m) {
  m.doc() = "Python bindings for WinCalc";

  py::enum_<Gases::GasDef>(m, "Predefined_Gas_Type", py::arithmetic())
      .value("AIR", Gases::GasDef::Air)
      .value("ARGON", Gases::GasDef::Argon)
      .value("KRYPTON", Gases::GasDef::Krypton)
      .value("XENON", Gases::GasDef::Xenon);
	  
  py::class_<Predefined_Gas_Mixture_Component>(m, "Predefined_Gas_Mixture_Component")
      .def(py::init<Gases::GasDef const &, double>())
      .def_readwrite("gas", &Predefined_Gas_Mixture_Component::gas)
      .def_readwrite("percent", &Predefined_Gas_Mixture_Component::percent);

  py::class_<Gases::CIntCoeff >(m, "Gas_Coefficients")
      .def(py::init<double const, double const, double const>());
	  
  py::class_<Gases::CGasData>(m, "Custom_Gas_Data")
      .def(py::init<std::string const &, double const, double const, Gases::CIntCoeff const&, Gases::CIntCoeff const&, Gases::CIntCoeff const&>());
	
  py::class_<Engine_Gas_Mixture_Component>(m, "Engine_Gas_Mixture_Component")
      .def(py::init<Gases::CGasData const &, double>())
      .def_readwrite("gas", &Engine_Gas_Mixture_Component::gas)
      .def_readwrite("percent", &Engine_Gas_Mixture_Component::percent);	
	  
  py::class_<Engine_Gap_Info>(m, "Gap_Data")
      .def(py::init<Gases::CGasData const &, double>())
	  .def(py::init<std::vector<Engine_Gas_Mixture_Component> const &, double>())
	  .def(py::init<Gases::GasDef const &, double>())
	  .def(py::init<std::vector<Predefined_Gas_Mixture_Component> const &, double>())
      .def_readwrite("gases", &Engine_Gas_Mixture_Component::gas)
      .def_readwrite("thickness", &Gap_Data::thickness);

  py::class_<OpticsParser::WLData>(m, "Wavelength_Data")
      .def_readwrite("wavelength", &OpticsParser::WLData::wavelength)
      .def_readwrite("t", &OpticsParser::WLData::T)
      .def_readwrite("rf", &OpticsParser::WLData::frontR)
      .def_readwrite("rb", &OpticsParser::WLData::backR);

  py::class_<OpticsParser::ProductData>(m, "Product_Data")
      .def_readwrite("product_name", &OpticsParser::ProductData::productName)
      .def_readwrite("product_type", &OpticsParser::ProductData::productType)
      .def_readwrite("nfrc_id", &OpticsParser::ProductData::nfrcid)
      .def_readwrite("thickness", &OpticsParser::ProductData::thickness)
      .def_readwrite("conductivity", &OpticsParser::ProductData::conductivity)
      .def_readwrite("tir", &OpticsParser::ProductData::IRTransmittance)
      .def_readwrite("ef", &OpticsParser::ProductData::frontEmissivity)
      .def_readwrite("eb", &OpticsParser::ProductData::backEmissivity)
      .def_readwrite("measurements", &OpticsParser::ProductData::measurements);

  py::enum_<window_standards::Spectrum_Type>(m, "Spectrum_Type", py::arithmetic())
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

  py::enum_<window_standards::Wavelength_Set_Type>(m, "Wavelength_Set_Type", py::arithmetic())
      .value("FILE", window_standards::Wavelength_Set_Type::FILE)
      .value("SOURCE", window_standards::Wavelength_Set_Type::SOURCE)
      .value("DATA", window_standards::Wavelength_Set_Type::DATA);

  py::class_<window_standards::Wavelength_Set>(m, "Wavelength_Set")
      .def_readwrite("type", &window_standards::Wavelength_Set::type)
      .def_readwrite("description", &window_standards::Wavelength_Set::description)
      .def_readwrite("values", &window_standards::Wavelength_Set::values);

  py::enum_<window_standards::Wavelength_Boundary_Type>(m, "Wavelength_Boundary_Type",
                                      py::arithmetic())
      .value("NUMBER", window_standards::Wavelength_Boundary_Type::NUMBER)
      .value("WAVELENGTH_SET", window_standards::Wavelength_Boundary_Type::WAVELENGTH_SET);

  py::class_<window_standards::Wavelength_Boundary>(m, "Wavelength_Boundary")
      .def_readwrite("type", &window_standards::Wavelength_Boundary::type)
      .def_readwrite("value", &window_standards::Wavelength_Boundary::value);

  py::enum_<window_standards::Integration_Rule_Type>(m, "Integration_Rule_Type", py::arithmetic())
      .value("TRAPEZOIDAL", window_standards::Integration_Rule_Type::TRAPEZOIDAL)
      .value("RECTANGULAR", window_standards::Integration_Rule_Type::RECTANGULAR)
      .value("TABLE", window_standards::Integration_Rule_Type::TABLE);

  py::class_<window_standards::Integration_Rule>(m, "Integration_Rule")
      .def_readwrite("type", &window_standards::Integration_Rule::type)
      .def_readwrite("k", &window_standards::Integration_Rule::k);

  py::enum_<window_standards::Optical_Standard_Method_Type>(m, "Optical_Method_Type", py::arithmetic())
      .value("SOLAR", window_standards::Optical_Standard_Method_Type::SOLAR)
      .value("PHOTOPIC", window_standards::Optical_Standard_Method_Type::PHOTOPIC)
      .value("COLOR_TRISTIMX", window_standards::Optical_Standard_Method_Type::COLOR_TRISTIMX)
      .value("COLOR_TRISTIMY", window_standards::Optical_Standard_Method_Type::COLOR_TRISTIMY)
      .value("COLOR_TRISTIMZ", window_standards::Optical_Standard_Method_Type::COLOR_TRISTIMZ)
      .value("THERMAL_IR", window_standards::Optical_Standard_Method_Type::THERMAL_IR)
      .value("TUV", window_standards::Optical_Standard_Method_Type::TUV)
      .value("SPF", window_standards::Optical_Standard_Method_Type::SPF)
      .value("TDW", window_standards::Optical_Standard_Method_Type::TDW)
      .value("TKR", window_standards::Optical_Standard_Method_Type::TKR);

  py::class_<window_standards::Optical_Standard_Method>(m, "Optical_Standard_Method")
      .def_readwrite("type", &window_standards::Optical_Standard_Method::type)
      .def_readwrite("description", &window_standards::Optical_Standard_Method::description)
      .def_readwrite("source_spectrum", &window_standards::Optical_Standard_Method::source_spectrum)
      .def_readwrite("detector_spectrum", &window_standards::Optical_Standard_Method::detector_spectrum)
      .def_readwrite("wavelength_set", &window_standards::Optical_Standard_Method::wavelength_set)
      .def_readwrite("integration_rule", &window_standards::Optical_Standard_Method::integration_rule)
      .def_readwrite("min_wavelength", &window_standards::Optical_Standard_Method::min_wavelength)
      .def_readwrite("max_wavelength", &window_standards::Optical_Standard_Method::max_wavelength);

  py::class_<window_standards::Optical_Standard>(m, "Optical_Standard")
      .def_readwrite("name", &window_standards::Optical_Standard::name)
      .def_readwrite("description", &window_standards::Optical_Standard::description)
	  .def_readwrite("file", &window_standards::Optical_Standard::file)
      .def_readwrite("methods", &window_standards::Optical_Standard::methods);

  py::class_<wincalc::Trichromatic>(m, "Trichromatic")
      .def_readwrite("X", &Trichromatic::X)
      .def_readwrite("Y", &Trichromatic::Y)
      .def_readwrite("Z", &Trichromatic::Z);

  py::class_<wincalc::Wincalc_RGB>(m, "RGB")
      .def_readwrite("R", &RGB::R)
      .def_readwrite("G", &RGB::G)
      .def_readwrite("B", &RGB::B);

  py::class_<wincalc::Lab>(m, "Lab")
      .def_readwrite("L", &Lab::L)
      .def_readwrite("a", &Lab::a)
      .def_readwrite("b", &Lab::b);

  py::class_<wincalc::Color_Result>(m, "Color_Result")
      .def_readwrite("trichromatic", &wincalc::Color_Result::trichromatic)
      .def_readwrite("rgb", &wincalc::Color_Result::rgb)
      .def_readwrite("lab", &wincalc::Color_Result::lab);

  declare_optical_result_by_side<double>(m, "");
  declare_optical_result_by_side<wincalc::Color_Result>(m, "_Color");
  
  py::enum_<Tarcog::ISO15099::BoundaryConditionsCoeffModel>(m, "Boundary_Conditions_Coefficient_Model", py::arithmetic())
      .value("CalculateH", Tarcog::ISO15099::BoundaryConditionsCoeffModel::CalculateH)
      .value("HPrescribed", Tarcog::ISO15099::BoundaryConditionsCoeffModel::HPrescribed)
      .value("HcPrescribed", Tarcog::ISO15099::BoundaryConditionsCoeffModel::HcPrescribed);
	  
  py::enum_<Tarcog::ISO15099::AirHorizontalDirection>(m, "Air_Horizontal_Direction", py::arithmetic())
      .value("None", Tarcog::ISO15099::AirHorizontalDirection::None)
      .value("Leeward", Tarcog::ISO15099::AirHorizontalDirection::Leeward)
      .value("Windward", Tarcog::ISO15099::AirHorizontalDirection::Windward);
  
  py::class_<wincalc::Environment>(m, "Environment")
      .def_readwrite("air_temperature", &wincalc::Environment::air_temperature)
	  .def_readwrite("pressure", &wincalc::Environment::pressure)
	  .def_readwrite("convection_coefficient", &wincalc::Environment::convection_coefficient)
	  .def_readwrite("coefficient_model", &wincalc::Environment::coefficient_model)
	  .def_readwrite("radiation_temperature", &wincalc::Environment::radiation_temperature)
	  .def_readwrite("emissivity", &wincalc::Environment::emissivity)
	  .def_readwrite("air_speed", &wincalc::Environment::air_speed)
	  .def_readwrite("air_direction", &wincalc::Environment::air_direction)
	  .def_readwrite("direct_solar_radiation", &wincalc::Environment::direct_solar_radiation);

  py::class_<wincalc::Environments>(m, "Environments")
      .def_readwrite("outside", &wincalc::Environments::outside)
	  .def_readwrite("inside", &wincalc::Environments::inside);

  m.def("nfrc_u_environments", &wincalc::nfrc_u_environments, "Returns the default environments for running a NFRC U-Value calculation.");
  m.def("nfrc_shgc_environments", &wincalc::nfrc_shgc_environments, "Returns the default environments for running a NFRC SHGC calculation.");

  py::class_<wincalc::Flippable_Solid_Layer>(m, "Flippable_Solid_Layer")
      .def(py::init<double, bool>())
      .def_readwrite("thickness_meters", &wincalc::Flippable_Solid_Layer::thickness_meters)
      .def_readwrite("flipped", &wincalc::Flippable_Solid_Layer::flipped);
  
  py::class_<wincalc::Product_Data_Thermal, wincalc::Flippable_Solid_Layer>(m, "Product_Data_Thermal")
      .def(py::init<double, 
					double, 
					std::optional<double>, 
					std::optional<double>, 
					std::optional<double>, 
					std::optional<double>, 
					bool>()
			py::arg("ir_transmittance_front") = std::optional<double>(), 
			py::arg("ir_transmittance_back") = std::optional<double>(),
			py::arg("emissivity_front") = std::optional<double>(),
			py::arg("emissivity_back") = std::optional<double>(),
			py::arg("flipped") = false())
      .def_readwrite("conductivity", &wincalc::Product_Data_Thermal::conductivity)
      .def_readwrite("ir_transmittance_front", &wincalc::Product_Data_Thermal::ir_transmittance_front)
	  .def_readwrite("ir_transmittance_back", &wincalc::Product_Data_Thermal::ir_transmittance_back)
	  .def_readwrite("emissivity_front", &wincalc::Product_Data_Thermal::emissivity_front)
	  .def_readwrite("emissivity_back"), &wincalc::Product_Data_Thermal::emissivity_back);
  
  py::class_<wincalc::Product_Data_Optical, wincalc::Flippable_Solid_Layer>(m, "Product_Data_Optical")
      .def(py::init<double, bool>(), py::arg("flipped") = false());
	  

  py::class_<wincalc::Wavelength_Data>(m, "Wavelength_Data")
      .def_readwrite("wavelength", &wincalc::Wavelength_Data::wavelength)
      .def_readwrite("transmittance_front", &wincalc::Wavelength_Data::transmittance_front)
      .def_readwrite("transmittance_back", &wincalc::Wavelength_Data::transmittance_back)
	  .def_readwrite("reflectance_front", &wincalc::Wavelength_Data::reflectance_front)
      .def_readwrite("reflectance_back", &wincalc::Wavelength_Data::reflectance_back);
	
  py::class_<wincalc::Product_Data_N_Band_Optical, wincalc::Product_Data_Optical>(m, "Product_Data_N_Band_Optical")
      .def(py::init<FenestrationCommon::MaterialType, double, std::vector<wincalc::Wavelength_Data>, bool>(), py::arg("flipped") = false())
	  .def_readwrite("material_type", &wincalc::Product_Data_N_Band_Optical::material_type)
	  .def_readwrite("wavelength_data", &wincalc::Product_Data_N_Band_Optical::wavelength_data);
  
  py::class_<wincalc::Product_Data_Optical_Thermal>(m, "Product_Data_Optical_Thermal")
      .def_readwrite("optical_data", &wincalc::Product_Data_Optical_Thermal::optical_data)
      .def_readwrite("thermal_data", &wincalc::Product_Data_Optical_Thermal::thermal_data);
  
  
  py::class_<wincalc::Glazing_System_Optical_Interface>(m, "Glazing_System_Optical_Interface")
      .def(py::init<window_standards::Optical_Standard>())
      .def("all_method_values", &wincalc::Glazing_System_Optical_Interface::all_method_values,
                     "Returns all optical results for angles theta (default = 0) and phi (default = 0) for a given optical standard calculation method.")
      .def("color", &wincalc::Glazing_System_Optical_Interface::color,
                     "Returns all color results for angles theta (default = 0) and phi (default = 0).")
      .def("optical_standard", py::overload_cast<void>(&wincalc::Glazing_System_Optical_Interface::optical_standard), "Get the optical standard.")
	  .def("optical_standard", py::overload_cast<window_standards::Optical_Standard>(&wincalc::Glazing_System_Optical_Interface::optical_standard), "Set the optical standard.");
	  
  py::class_<wincalc::Glazing_System_Thermal_Interface>(m, "Glazing_System_Thermal_Interface")
      .def("u", &wincalc::Glazing_System_Thermal_Interface::u,
                     "Returns the U-value for the system")
      .def("shgc", &wincalc::Glazing_System_Thermal_Interface::shgc,
                     "Returns the SHGC for the system at given absorptances and total solar transmittance.")
      .def("layer_temperatures", &wincalc::Glazing_System_Thermal_Interface::layer_temperatures, "Returns the temperatures of each layer in the system based on the given system calculation type (U or SHGC) and front absorptances.")
	  .def("solid_layers_effective_conductivities", &wincalc::Glazing_System_Thermal_Interface::solid_layers_effective_conductivities, "Returns the effective conductivity of each solid layer in the system based on the given calculation type (U or SHGC).")
	  .def("gap_layers_effective_conductivities", &wincalc::Glazing_System_Thermal_Interface::gap_layers_effective_conductivities, "Returns the effective conductivity of each gap layer in the system based on the given calculation type (U or SHGC).")
	  .def("system_effective_conductivity", &wincalc::Glazing_System_Thermal_Interface::system_effective_conductivity, "Returns the effective conductivity of the entire system system based on the given calculation type (U or SHGC).")
	  .def("relative_heat_gain", &wincalc::Glazing_System_Thermal_Interface::relative_heat_gain, "Returns the the relative heat gain for the given solar transmittance.");
	  
py::class_<wincalc::Glazing_System_Optical, wincalc::Glazing_System_Optical_Interface>(m, "Glazing_System_Optical")
      .def(py::init<std::vector<std::shared_ptr<wincalc::Product_Data_Optical>> const&, window_standards::Optical_Standard const&>())
      .def("all_method_values", &wincalc::Glazing_System_Optical_Interface::all_method_values,
                     "Returns all optical results for angles theta (default = 0) and phi (default = 0) for a given optical standard calculation method.")
      .def("color", &wincalc::Glazing_System_Optical_Interface::color,
                     "Returns all color results for angles theta (default = 0) and phi (default = 0).");
	  
  py::class_<wincalc::Glazing_System_Thermal, wincalc::Glazing_System_Thermal_Interface>(m, "Glazing_System_Thermal")
      .def(py::init<std::vector<std::shared_ptr<wincalc::Product_Data_Thermal>> const&, 
			std::vector<wincalc::Engine_Gap_Info> const&, 
			double, 
			double, 
			wincalc::Environments const& >(), 
		   py::arg("width") = 1.0,
		   py::arg("height") = 1.0,
		   py::arg("environment") = wincalc::nfrc_u_environments())
      .def("u", &wincalc::Glazing_System_Thermal_Interface::u,
                     "Returns the U-value for the system")
      .def("shgc", &wincalc::Glazing_System_Thermal_Interface::shgc,
                     "Returns the SHGC for the system at given absorptances and total solar transmittance.")
      .def("layer_temperatures", &wincalc::Glazing_System_Thermal_Interface::layer_temperatures, "Returns the temperatures of each layer in the system based on the given system calculation type (U or SHGC) and front absorptances.")
	  .def("solid_layers_effective_conductivities", &wincalc::Glazing_System_Thermal_Interface::solid_layers_effective_conductivities, "Returns the effective conductivity of each solid layer in the system based on the given calculation type (U or SHGC).")
	  .def("gap_layers_effective_conductivities", &wincalc::Glazing_System_Thermal_Interface::gap_layers_effective_conductivities, "Returns the effective conductivity of each gap layer in the system based on the given calculation type (U or SHGC).")
	  .def("system_effective_conductivity", &wincalc::Glazing_System_Thermal_Interface::system_effective_conductivity, "Returns the effective conductivity of the entire system system based on the given calculation type (U or SHGC).")
	  .def("relative_heat_gain", &wincalc::Glazing_System_Thermal_Interface::relative_heat_gain, "Returns the the relative heat gain for the given solar transmittance.");


  py::class_<wincalc::Glazing_System_Thermal_And_Optical, wincalc::Glazing_System_Optical, wincalc::Glazing_System_Thermal>(m, "Glazing_System_Thermal_And_Optical")
      .def(py::init<std::vector<std::shared_ptr<wincalc::Product_Data_Thermal>> const&, 
			std::vector<wincalc::Engine_Gap_Info> const&, 
			windows_standards::Optical_Standard
			double, 
			double, 
			wincalc::Environments const& >(), 
		   py::arg("width") = 1.0,
		   py::arg("height") = 1.0,
		   py::arg("environment") = wincalc::nfrc_u_environments())	
      .def(py::init<std::vector<OpticsParser::ProductData> const&, 
			std::vector<wincalc::Engine_Gap_Info> const&, 
			windows_standards::Optical_Standard
			double, 
			double, 
			wincalc::Environments const& >(), 
		   py::arg("width") = 1.0,
		   py::arg("height") = 1.0,
		   py::arg("environment") = wincalc::nfrc_u_environments())
      .def("shgc", &wincalc::Glazing_System_Thermal_And_Optical::shgc,
           "Calculate the SHGC of the glazing system at given theta and phi.",
		   py::arg("theta") = 0,
		   py::arg("phi") = 0)
      .def("layer_temperatures", &wincalc::Glazing_System_Thermal_And_Optical::layer_temperatures,
           "Returns the temperatures of each layer in the system based on the given system calculation type (U or SHGC) and given theta and phi.", 
		   py::arg("theta") = 0,
		   py::arg("phi") = 0);

  m.def("load_standard", py::overload_cast<std::string const &>(&load_standard),
        "Load standard from .std.file");
  m.def("parse_json", &OpticsParser::parseJSONString,
        "Load product data from json string");
  m.def("parse_json_file", &OpticsParser::parseJSONFile,
        "Load product data from json file");
  m.def("parse_optics_file", &OpticsParser::parseFile,
        "Load product data from optics file");
}
