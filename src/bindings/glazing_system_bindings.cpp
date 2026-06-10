#include "glazing_system_bindings.h"
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

void register_glazing_system_bindings(py::module &mod) {
  py::enum_<SingleLayerOptics::BSDFBasis>(mod, "BSDFBasisType", py::arithmetic())
      .value("NANO", SingleLayerOptics::BSDFBasis::Nano)
      .value("SMALL", SingleLayerOptics::BSDFBasis::Small)
      .value("QUARTER", SingleLayerOptics::BSDFBasis::Quarter)
      .value("HALF", SingleLayerOptics::BSDFBasis::Half)
      .value("FULL", SingleLayerOptics::BSDFBasis::Full);

  py::class_<SingleLayerOptics::BSDFDefinition>(mod, "BSDFDefinition")
      .def(py::init<double, size_t>(),
           py::arg("theta"), py::arg("number_of_phis"))
      .def("theta", &SingleLayerOptics::BSDFDefinition::theta)
      .def("num_of_phis", &SingleLayerOptics::BSDFDefinition::numOfPhis);

  py::class_<SingleLayerOptics::BSDFHemisphere>(mod, "BSDFHemisphere")
      .def_static("create",
                  py::overload_cast<SingleLayerOptics::BSDFBasis>(
                      &SingleLayerOptics::BSDFHemisphere::create),
                  py::arg("bsdf_basis"))
      .def_static("create",
                  py::overload_cast<std::vector<SingleLayerOptics::BSDFDefinition> const &>(
                      &SingleLayerOptics::BSDFHemisphere::create),
                  py::arg("bsdf_definitions"))
      .def("get_directions", &SingleLayerOptics::BSDFHemisphere::getDirections);

  py::enum_<Tarcog::ISO15099::System>(mod, "TarcogSystemType", py::arithmetic())
      .value("U", Tarcog::ISO15099::System::Uvalue)
      .value("SHGC", Tarcog::ISO15099::System::SHGC);

  py::enum_<Tarcog::ISO15099::Environment>(mod, "TarcogEnvironmentType", py::arithmetic())
      .value("Indoor", Tarcog::ISO15099::Environment::Indoor)
      .value("Outdoor", Tarcog::ISO15099::Environment::Outdoor);

  py::enum_<wincalc::Spectal_Data_Wavelength_Range_Method>(
      mod, "SpectalDataWavelengthRangeMethodType", py::arithmetic())
      .value("FULL", wincalc::Spectal_Data_Wavelength_Range_Method::FULL)
      .value("ISO_9050",
             wincalc::Spectal_Data_Wavelength_Range_Method::ISO_9050)
      .value("CONDENSED",
             wincalc::Spectal_Data_Wavelength_Range_Method::CONDENSED);

  mod.def("nfrc_u_environments", &wincalc::nfrc_u_environments);
  mod.def("nfrc_shgc_environments", &wincalc::nfrc_shgc_environments);

  py::class_<wincalc::Deflection_Results>(mod, "DeflectionResults")
      .def_readwrite("layer_deflection_max",
                     &wincalc::Deflection_Results::layer_deflection_max)
      .def_readwrite("layer_deflection_mean",
                     &wincalc::Deflection_Results::layer_deflection_mean)
      .def_readwrite("panes_load", &wincalc::Deflection_Results::panes_load)
      .def_readwrite("gap_width_max",
                     &wincalc::Deflection_Results::gap_width_max)
      .def_readwrite("gap_width_mean",
                     &wincalc::Deflection_Results::gap_width_mean);

  py::class_<wincalc::Glazing_System>(mod, "GlazingSystem")
      .def(
          py::init<window_standards::Optical_Standard const &,
                   std::vector<wincalc::Product_Data_Optical_Thermal> const &,
                   std::vector<
                       std::shared_ptr<Tarcog::ISO15099::CIGUGapLayer>> const &,
                   double, double, double, wincalc::Environments const &,
                   std::optional<SingleLayerOptics::BSDFHemisphere> const &,
                   wincalc::Spectal_Data_Wavelength_Range_Method const &, int,
                   int>(),
          py::arg("optical_standard"), py::arg("solid_layers"),
          py::arg("gap_layers") =
              std::vector<std::shared_ptr<Tarcog::ISO15099::CIGUGapLayer>>(),
          py::arg("width_meters") = 1.0, py::arg("height_meters") = 1.0,
          py::arg("tilt_degrees") = 90,
          py::arg("environment") = wincalc::nfrc_u_environments(),
          py::arg("bsdf_hemisphere") =
              std::optional<SingleLayerOptics::BSDFHemisphere>(),
          py::arg("spectral_data_wavelength_range_method") =
              wincalc::Spectal_Data_Wavelength_Range_Method::FULL,
          py::arg("number_visible_bands") = 5,
          py::arg("number_solar_bands") = 10)
      .def(
          py::init<window_standards::Optical_Standard const &,
                   std::vector<OpticsParser::ProductData> const &,
                   std::vector<
                       std::shared_ptr<Tarcog::ISO15099::CIGUGapLayer>> const &,
                   double, double, double, wincalc::Environments const &,
                   std::optional<SingleLayerOptics::BSDFHemisphere> const &,
                   wincalc::Spectal_Data_Wavelength_Range_Method const &, int,
                   int>(),
          py::arg("optical_standard"), py::arg("solid_layers"),
          py::arg("gap_layers") =
              std::vector<std::shared_ptr<Tarcog::ISO15099::CIGUGapLayer>>(),
          py::arg("width_meters") = 1.0, py::arg("height_meters") = 1.0,
          py::arg("tilt_degrees") = 90,
          py::arg("environment") = wincalc::nfrc_u_environments(),
          py::arg("bsdf_hemisphere") =
              std::optional<SingleLayerOptics::BSDFHemisphere>(),
          py::arg("spectral_data_wavelength_range_method") =
              wincalc::Spectal_Data_Wavelength_Range_Method::FULL,
          py::arg("number_visible_bands") = 5,
          py::arg("number_solar_bands") = 10)
      .def(
          py::init<
              window_standards::Optical_Standard const &,
              std::vector<
                  std::variant<OpticsParser::ProductData,
                               wincalc::Product_Data_Optical_Thermal>> const &,
              std::vector<std::shared_ptr<Tarcog::ISO15099::CIGUGapLayer>> const
                  &,
              double, double, double, wincalc::Environments const &,
              std::optional<SingleLayerOptics::BSDFHemisphere> const &,
              wincalc::Spectal_Data_Wavelength_Range_Method const &, int,
              int>(),
          py::arg("optical_standard"), py::arg("solid_layers"),
          py::arg("gap_layers") =
              std::vector<std::shared_ptr<Tarcog::ISO15099::CIGUGapLayer>>(),
          py::arg("width_meters") = 1.0, py::arg("height_meters") = 1.0,
          py::arg("tilt_degrees") = 90,
          py::arg("environment") = wincalc::nfrc_u_environments(),
          py::arg("bsdf_hemisphere") =
              std::optional<SingleLayerOptics::BSDFHemisphere>(),
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
      .def("populate_layer_wavelength_matrices",
           &wincalc::Glazing_System::populate_layer_wavelength_matrices,
           "Compute per-layer wavelength matrices on demand (expensive).",
           py::arg("results"), py::arg("method_name"))
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
      .def("heat_flow",
          &wincalc::Glazing_System::heat_flow,
          py::arg("system_type"), py::arg("environment_type"), py::arg("theta") = 0, py::arg("phi") = 0)
      .def("h",
          &wincalc::Glazing_System::h,
          py::arg("system_type"), py::arg("environment_type"), py::arg("theta") = 0, py::arg("phi") = 0)
      .def("radiosities",
          &wincalc::Glazing_System::radiosities,
          py::arg("system_type"), py::arg("theta") = 0, py::arg("phi") = 0)
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
           py::overload_cast<double, double>(
               &wincalc::Glazing_System::set_deflection_properties),
           py::arg("temperature_at_construction"),
           py::arg("pressure_at_construction"))
      .def("set_deflection_properties",
           py::overload_cast<std::vector<double> const &>(
               &wincalc::Glazing_System::set_deflection_properties),
           py::arg("measured_deflected_gaps"))
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
           py::arg("tilt_degrees"))
      .def("flip_layer", &wincalc::Glazing_System::flip_layer,
           py::arg("layer_index"), py::arg("flipped"))
      .def("solid_layers",
           py::overload_cast<
               std::vector<wincalc::Product_Data_Optical_Thermal> const &>(
               &wincalc::Glazing_System::solid_layers),
           py::arg("solid_layers"))
      .def("solid_layers",
           py::overload_cast<>(&wincalc::Glazing_System::solid_layers,
                               py::const_));

  mod.def("convert_to_solid_layer", &wincalc::convert_to_solid_layer,
        "Convert product data into a solid layer that can be used in glazing "
        "systems.");

  mod.def("convert_to_solid_layers", &wincalc::convert_to_solid_layers,
        "Convert a list of product data into a solid layer that can be used in "
        "glazing systems.");

  mod.def("load_standard",
        py::overload_cast<std::string const &>(
            &window_standards::load_optical_standard),
        "Load standard from .std file");
  mod.def("parse_json", &OpticsParser::parseJSONString,
        "Load product data from json string");
  mod.def("parse_json_file", &OpticsParser::parseJSONFile,
        "Load product data from json file");
  mod.def("parse_optics_file", &OpticsParser::parseOpticsFile,
        "Load product data from optics file");
  mod.def("parse_bsdf_xml_file", &OpticsParser::parseBSDFXMLFile,
        "Load product data from BSDF xml file");
  mod.def("parse_bsdf_xml_string", &OpticsParser::parseBSDFXMLString,
        "Load product data from BSDF xml string");
  mod.def("parse_thmx_file", &thmxParser::parseFile, "Parse a THERM thmx file");
  mod.def("parse_thmx_string", &thmxParser::parseString,
        "Parse THERM thmx format from a string");

  mod.def("create_gas", &wincalc::create_gas, py::arg("components"),
        "Create a gas mixture from components: a list of pairs where the first "
        "in each item is the percent of the total and the second is the gas.");

  mod.def("create_venetian_blind",
        py::overload_cast<wincalc::Venetian_Geometry const &,
                          OpticsParser::ProductData const &>(
            &wincalc::create_venetian_blind),
        py::arg("geometry"), py::arg("material"),
        "Create a venetian blind from a geometry and parsed material.");

  mod.def("create_venetian_blind",
        py::overload_cast<wincalc::Venetian_Geometry const &,
                          std::shared_ptr<wincalc::Product_Data_Optical>,
                          std::shared_ptr<wincalc::Product_Data_Thermal>>(
            &wincalc::create_venetian_blind),
        py::arg("geometry"), py::arg("material_data_optical"),
        py::arg("material_data_thermal").none(true),
        "Create a venetian blind from a geometry and material optical and "
        "thermal data.");

  mod.def("create_woven_shade",
        py::overload_cast<wincalc::Woven_Geometry const &,
                          OpticsParser::ProductData const &>(
            &wincalc::create_woven_shade),
        py::arg("geometry"), py::arg("material"),
        "Create a woven shade from a geometry and parsed material.");

  mod.def("create_woven_shade",
        py::overload_cast<wincalc::Woven_Geometry const &,
                          std::shared_ptr<wincalc::Product_Data_Optical>,
                          std::shared_ptr<wincalc::Product_Data_Thermal>>(
            &wincalc::create_woven_shade),
        py::arg("geometry"), py::arg("material_data_optical"),
        py::arg("material_data_thermal").none(true),
        "Create a woven shade from a geometry and material optical and "
        "thermal data.");

  mod.def("create_perforated_screen",
        py::overload_cast<wincalc::Perforated_Geometry const &,
                          OpticsParser::ProductData const &>(
            &wincalc::create_perforated_screen),
        py::arg("geometry"), py::arg("material"),
        "Create a perforated screen from a geometry and parsed material.");

  mod.def("create_perforated_screen",
        py::overload_cast<wincalc::Perforated_Geometry const &,
                          std::shared_ptr<wincalc::Product_Data_Optical>,
                          std::shared_ptr<wincalc::Product_Data_Thermal>>(
            &wincalc::create_perforated_screen),
        py::arg("geometry"), py::arg("material_data_optical"),
        py::arg("material_data_thermal").none(true),
        "Create a perforated screen from a geometry and material optical and "
        "thermal data.");
}
