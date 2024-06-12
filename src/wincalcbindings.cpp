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

class Py_UniversalSupportPillar
    : public Tarcog::ISO15099::UniversalSupportPillar {
public:
  using Tarcog::ISO15099::UniversalSupportPillar::UniversalSupportPillar;

protected:
  double areaOfContact() override {
    PYBIND11_OVERRIDE_PURE(double, Tarcog::ISO15099::UniversalSupportPillar,
                           areaOfContact, );
  }
};

PYBIND11_MODULE(wincalcbindings, m) {
  m.doc() = "Python bindings for WinCalc";

  py::enum_<Gases::GasDef>(m, "PredefinedGasType", py::arithmetic())
      .value("AIR", Gases::GasDef::Air)
      .value("ARGON", Gases::GasDef::Argon)
      .value("KRYPTON", Gases::GasDef::Krypton)
      .value("XENON", Gases::GasDef::Xenon);

  py::class_<Gases::CIntCoeff>(m, "GasCoefficients")
      .def(py::init<double const, double const, double const>(), py::arg("A"),
           py::arg("B"), py::arg("C"));

  py::class_<Gases::CGasData>(m, "GasData")
      .def(py::init<std::string const &, double const, double const,
                    Gases::CIntCoeff const &, Gases::CIntCoeff const &,
                    Gases::CIntCoeff const &>(),
           py::arg("name"), py::arg("molecular_weight"),
           py::arg("specific_heat_ratio"), py::arg("Cp"),
           py::arg("thermal_conductivity"), py::arg("viscosity"))
      .def("get_molecular_weight", &Gases::CGasData::getMolecularWeight)
      .def("get_property_value", &Gases::CGasData::getPropertyValue,
           py::arg("type"), py::arg("temperature"))
      .def("get_specific_heat_ratio", &Gases::CGasData::getSpecificHeatRatio)
      .def("name", &Gases::CGasData::name);

  py::class_<Gases::CGas>(m, "Gas")
      .def(py::init<std::vector<Gases::CGasItem> const &>(), py::arg("gases"))
      .def("get_simple_gas_properties", &Gases::CGas::getSimpleGasProperties)
      .def("get_gas_properties", &Gases::CGas::getGasProperties)
      .def("set_temperature_and_pressure",
           &Gases::CGas::setTemperatureAndPressure)
      .def("gas_items", &Gases::CGas::gasItems)
      .def("total_percent", &Gases::CGas::totalPercent)
      .def("add_gas_items", &Gases::CGas::addGasItems)
      .def("add_gas_item",
           py::overload_cast<double, Gases::CGasData const &>(
               &Gases::CGas::addGasItem),
           py::arg("percent"), py::arg("gas_data"))
      .def("add_gas_item",
           py::overload_cast<double, Gases::GasDef>(&Gases::CGas::addGasItem),
           py::arg("percent"), py::arg("predefined_gas"));

  py::class_<Tarcog::ISO15099::CIGUGapLayer,
             std::shared_ptr<Tarcog::ISO15099::CIGUGapLayer>>(m, "IGUGapLayer")
      .def(py::init<double, double>(), py::arg("thickness"),
           py::arg("pressure"))
      .def(py::init<double, double, Gases::CGas const &>(),
           py::arg("thickness"), py::arg("pressure"), py::arg("gas"));

  py::enum_<Tarcog::ISO15099::CellSpacingType>(m, "CellSpacingType",
                                               py::arithmetic())
      .value("SQUARE", Tarcog::ISO15099::CellSpacingType::Square)
      .value("SHIFTEDSQUARE", Tarcog::ISO15099::CellSpacingType::ShiftedSquare)
      .value("SHIFTEDROTATEDSQUARE",
             Tarcog::ISO15099::CellSpacingType::ShiftedRotatedSquare);

  m.def("pillar_cell_area", Tarcog::ISO15099::pillarCellArea,
        py::arg("cell_spacing_type"), py::arg("sp"));

  py::enum_<Tarcog::ISO15099::PolygonType>(m, "PolygonType", py::arithmetic())
      .value("TRIANGLE", Tarcog::ISO15099::PolygonType::Triangle)
      .value("PENTAGON", Tarcog::ISO15099::PolygonType::Pentagon)
      .value("HEXAGON", Tarcog::ISO15099::PolygonType::Hexagon);

  py::class_<Tarcog::ISO15099::UniversalSupportPillar,
             Py_UniversalSupportPillar, Tarcog::ISO15099::CIGUGapLayer,
             std::shared_ptr<Tarcog::ISO15099::UniversalSupportPillar>>(
      m, "UniversalSupportPillar")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &, double, double>(),
           py::arg("gap_layer"), py::arg("material_conductivity"),
           py::arg("cell_area"));

  py::class_<Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::PillarData>>(m, "PillarData")
      .def(py::init<double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"))
      .def_readwrite("height", &Tarcog::ISO15099::PillarData::height)
      .def_readwrite("material_conductivity",
                     &Tarcog::ISO15099::PillarData::materialConductivity)
      .def_readwrite("cell_area", &Tarcog::ISO15099::PillarData::cellArea);

  py::class_<Tarcog::ISO15099::CylindricalPillar, Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::CylindricalPillar>>(
      m, "CylindricalPillar")
      .def(py::init<double, double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"),
           py::arg("radius"))
      .def_readwrite("radius", &Tarcog::ISO15099::CylindricalPillar::radius);

  py::class_<Tarcog::ISO15099::CylindricalPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::CylindricalPillarLayer>>(
      m, "CylindricalPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::CylindricalPillar const &>(),
           py::arg("gap_layer"), py::arg("cylindrical_pillar"));

  py::class_<Tarcog::ISO15099::SphericalPillar, Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::SphericalPillar>>(
      m, "SphericalPillar")
      .def(py::init<double, double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"),
           py::arg("radius_of_contact"))
      .def_readwrite("radius_of_contact",
                     &Tarcog::ISO15099::SphericalPillar::radiusOfContact);

  py::class_<Tarcog::ISO15099::SphericalPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::SphericalPillarLayer>>(
      m, "SphericalPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::SphericalPillar const &>(),
           py::arg("gap_layer"), py::arg("spherical_pillar"));

  py::class_<Tarcog::ISO15099::RectangularPillar, Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::RectangularPillar>>(
      m, "RectangularPillar")
      .def(py::init<double, double, double, double, double>(),
           py::arg("height"), py::arg("material_conductivity"),
           py::arg("cell_area"), py::arg("length"), py::arg("width"))
      .def_readwrite("length", &Tarcog::ISO15099::RectangularPillar::length)
      .def_readwrite("width", &Tarcog::ISO15099::RectangularPillar::width);

  py::class_<Tarcog::ISO15099::RectangularPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::RectangularPillarLayer>>(
      m, "RectangularPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::RectangularPillar const &>(),
           py::arg("gap_layer"), py::arg("rectangular_pillar"));

  py::class_<Tarcog::ISO15099::PolygonalPillar, Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::PolygonalPillar>>(
      m, "PolygonalPillar")
      .def(py::init<double, double, double, double,
                    Tarcog::ISO15099::PolygonType>(),
           py::arg("height"), py::arg("material_conductivity"),
           py::arg("cell_area"), py::arg("length"), py::arg("polygon_type"))
      .def_readwrite("length", &Tarcog::ISO15099::PolygonalPillar::length)
      .def_readwrite("polygon_type", &Tarcog::ISO15099::PolygonalPillar::type);

  py::class_<Tarcog::ISO15099::TriangularPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::TriangularPillarLayer>>(
      m, "TriangularPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::PolygonalPillar const &>(),
           py::arg("gap_layer"), py::arg("polygon_pillar"));

  py::class_<Tarcog::ISO15099::PentagonPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::PentagonPillarLayer>>(
      m, "PentagonPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::PolygonalPillar const &>(),
           py::arg("gap_layer"), py::arg("polygon_pillar"));

  py::class_<Tarcog::ISO15099::HexagonPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::HexagonPillarLayer>>(
      m, "HexagonPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::PolygonalPillar const &>(),
           py::arg("gap_layer"), py::arg("polygon_pillar"));

  py::class_<Tarcog::ISO15099::LinearBearingPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::LinearBearingPillar>>(
      m, "LinearBearingPillar")
      .def(py::init<double, double, double, double, double>(),
           py::arg("height"), py::arg("material_conductivity"),
           py::arg("cell_area"), py::arg("length"), py::arg("width"))
      .def_readwrite("length", &Tarcog::ISO15099::LinearBearingPillar::length)
      .def_readwrite("width", &Tarcog::ISO15099::LinearBearingPillar::width);

  py::class_<Tarcog::ISO15099::LinearBearingPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::LinearBearingPillarLayer>>(
      m, "LinearBearingPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::LinearBearingPillar const &>(),
           py::arg("gap_layer"), py::arg("linear_bearing_pillar"));

  py::class_<Tarcog::ISO15099::TruncatedConePillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::TruncatedConePillar>>(
      m, "TruncatedConePillar")
      .def(py::init<double, double, double, double, double>(),
           py::arg("height"), py::arg("material_conductivity"),
           py::arg("cell_area"), py::arg("radius_1"), py::arg("radius_2"))
      .def_readwrite("radius_1",
                     &Tarcog::ISO15099::TruncatedConePillar::radius1)
      .def_readwrite("radius_2",
                     &Tarcog::ISO15099::TruncatedConePillar::radius2);

  py::class_<Tarcog::ISO15099::TruncatedConePillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::TruncatedConePillarLayer>>(
      m, "TruncatedConePillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::TruncatedConePillar const &>(),
           py::arg("gap_layer"), py::arg("truncated_cone_pillar"));

  py::class_<Tarcog::ISO15099::AnnulusCylinderPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::AnnulusCylinderPillar>>(
      m, "AnnulusCylinderPillar")
      .def(py::init<double, double, double, double, double>(),
           py::arg("height"), py::arg("material_conductivity"),
           py::arg("cell_area"), py::arg("inner_radius"),
           py::arg("outer_radius"))
      .def_readwrite("inner_radius",
                     &Tarcog::ISO15099::AnnulusCylinderPillar::innerRadius)
      .def_readwrite("outer_radius",
                     &Tarcog::ISO15099::AnnulusCylinderPillar::outerRadius);

  py::class_<Tarcog::ISO15099::AnnulusCylinderPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::AnnulusCylinderPillarLayer>>(
      m, "AnnulusCylinderPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::AnnulusCylinderPillar const &>(),
           py::arg("gap_layer"), py::arg("annulus_cylinder_pillar"));

  py::class_<Tarcog::ISO15099::Glass, std::shared_ptr<Tarcog::ISO15099::Glass>>(
      m, "Glass")
      .def(py::init<double, double, double>(), py::arg("thickness"),
           py::arg("conductivity"), py::arg("emissivity"))
      .def_readwrite("thickness", &Tarcog::ISO15099::Glass::thickness)
      .def_readwrite("conductivity", &Tarcog::ISO15099::Glass::conductivity)
      .def_readwrite("emissivity", &Tarcog::ISO15099::Glass::emissivity);

  py::class_<Tarcog::ISO15099::PillarMeasurement,
             std::shared_ptr<Tarcog::ISO15099::PillarMeasurement>>(
      m, "PillarMeasurement")
      .def(py::init<double, double, double, double, Tarcog::ISO15099::Glass,
                    Tarcog::ISO15099::Glass>(),
           py::arg("total_thickness"), py::arg("conductivity"),
           py::arg("temperature_surface_1"), py::arg("temperature_surface_4"),
           py::arg("glass_1"), py::arg("glass_2"))
      .def_readwrite("total_thickness",
                     &Tarcog::ISO15099::PillarMeasurement::totalThickness)
      .def_readwrite("conductivity",
                     &Tarcog::ISO15099::PillarMeasurement::conductivity)
      .def_readwrite("temperature_surface_1",
                     &Tarcog::ISO15099::PillarMeasurement::temperatureSurface1)
      .def_readwrite("temperature_surface_4",
                     &Tarcog::ISO15099::PillarMeasurement::temperatureSurface4)
      .def_readwrite("glass_1", &Tarcog::ISO15099::PillarMeasurement::glass1)
      .def_readwrite("glass_2", &Tarcog::ISO15099::PillarMeasurement::glass2);

  py::class_<Tarcog::ISO15099::MeasuredPillarLayer,
             Tarcog::ISO15099::CIGUGapLayer,
             std::shared_ptr<Tarcog::ISO15099::MeasuredPillarLayer>>(
      m, "MeasuredPillarLayer")
      .def(py::init<Tarcog::ISO15099::PillarMeasurement const &>(),
           py::arg("pillar"));

  py::class_<Tarcog::ISO15099::CIGUVentilatedGapLayer,
             Tarcog::ISO15099::CIGUGapLayer,
             std::shared_ptr<Tarcog::ISO15099::CIGUVentilatedGapLayer>>(
      m, "IGUVentilatedGapLayer")
      .def(py::init<std::shared_ptr<Tarcog::ISO15099::CIGUGapLayer> const &>(),
           py::arg("gap_layer"))
      .def(py::init<std::shared_ptr<Tarcog::ISO15099::CIGUGapLayer>, double,
                    double>(),
           py::arg("gap_layer"), py::arg("inlet_temperature"),
           py::arg("inlet_speed"))
      .def("layer_temperature",
           &Tarcog::ISO15099::CIGUVentilatedGapLayer::averageLayerTemperature)
      .def("set_flow_geometry",
           &Tarcog::ISO15099::CIGUVentilatedGapLayer::setFlowGeometry,
           py::arg("a_in"), py::arg("a_out"))
      .def("set_inlet_temperature",
           &Tarcog::ISO15099::CIGUVentilatedGapLayer::setInletTemperature,
           py::arg("inlet_temperature"))
      .def("set_flow_temperatures",
           &Tarcog::ISO15099::CIGUVentilatedGapLayer::setFlowTemperatures,
           py::arg("inlet_temperature"), py::arg("outlet_temperature"))
      .def("set_flow_speed",
           &Tarcog::ISO15099::CIGUVentilatedGapLayer::setFlowSpeed,
           py::arg("speed"))
      .def("smooth_energy_gain",
           &Tarcog::ISO15099::CIGUVentilatedGapLayer::smoothEnergyGain,
           py::arg("qv1"), py::arg("qv2"))
      .def(
          "calculate_ventilated_airflow",
          &Tarcog::ISO15099::CIGUVentilatedGapLayer::calculateVentilatedAirflow,
          py::arg("inlet_temperature"))
      .def("calculate_thermally_driven_airflow_with_adjacent_gap",
           &Tarcog::ISO15099::CIGUVentilatedGapLayer::
               calculateThermallyDrivenAirflowWithAdjacentGap,
           py::arg("adjacent_gap"))
      .def("clone", &Tarcog::ISO15099::CIGUVentilatedGapLayer::clone);

  m.def("forced_ventilation_gap",
        Tarcog::ISO15099::Layers::forcedVentilationGap, py::arg("gap"),
        py::arg("forced_ventilation_air_speed"),
        py::arg("forced_ventilation_air_temperature"));

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

  py::class_<OpticsParser::PVWavelengthData>(m, "PVWavelengthData")
      .def(py::init<double, double>(), py::arg("eqe_front"),
           py::arg("eqe_back"))
      .def_readwrite("eqq_front", &OpticsParser::PVWavelengthData::eqef)
      .def_readwrite("eqe_back", &OpticsParser::PVWavelengthData::eqeb);

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
                     &OpticsParser::WLData::diffuseComponent)
      .def_readwrite("pv_component", &OpticsParser::WLData::pvComponent);

  py::class_<OpticsParser::ProductGeometry,
             std::shared_ptr<OpticsParser::ProductGeometry>>(m,
                                                             "ProductGeometry");

  py::class_<OpticsParser::VenetianGeometry, OpticsParser::ProductGeometry,
             std::shared_ptr<OpticsParser::VenetianGeometry>>(
      m, "ParsedVenetianGeometry")
      .def(py::init<double, double, double, double, std::string, int>(),
           py::arg("slat_width"), py::arg("slat_spacing"),
           py::arg("slat_curvature"), py::arg("slat_tilt") = 0,
           py::arg("tilt_choice") = "0", py::arg("number_segments") = 5)
      .def_readwrite("slat_width", &OpticsParser::VenetianGeometry::slatWidth)
      .def_readwrite("slat_spacing",
                     &OpticsParser::VenetianGeometry::slatSpacing)
      .def_readwrite("slat_curvature",
                     &OpticsParser::VenetianGeometry::slatCurvature)
      .def_readwrite("slat_tilt", &OpticsParser::VenetianGeometry::slatTilt)
      .def_readwrite("number_segments",
                     &OpticsParser::VenetianGeometry::numberSegments);

  py::class_<OpticsParser::WovenGeometry, OpticsParser::ProductGeometry,
             std::shared_ptr<OpticsParser::WovenGeometry>>(
      m, "ParsedWovenGeometry")
      .def(py::init<double, double, double>())
      .def_readwrite("thread_diameter",
                     &OpticsParser::WovenGeometry::threadDiameter)
      .def_readwrite("thread_spacing",
                     &OpticsParser::WovenGeometry::threadSpacing)
      .def_readwrite("shade_thickness",
                     &OpticsParser::WovenGeometry::shadeThickness);

  py::class_<OpticsParser::PerforatedGeometry, OpticsParser::ProductGeometry,
             std::shared_ptr<OpticsParser::PerforatedGeometry>>(
      m, "ParsedPerforatedGeometry")
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

  py::class_<OpticsParser::PVPowerProperty>(m, "PVPowerProperty")
      .def(py::init<double, double, double>(), py::arg("jsc"), py::arg("voc"),
           py::arg("ff"))
      .def_readwrite("jsc", &OpticsParser::PVPowerProperty::jsc)
      .def_readwrite("voc", &OpticsParser::PVPowerProperty::voc)
      .def_readwrite("ff", &OpticsParser::PVPowerProperty::ff);

  py::class_<OpticsParser::ProductData,
             std::shared_ptr<OpticsParser::ProductData>>(m, "ProductData")
      .def_readwrite("product_name", &OpticsParser::ProductData::productName)
      .def_readwrite("product_type", &OpticsParser::ProductData::productType)
      .def_readwrite("product_subtype",
                     &OpticsParser::ProductData::productSubtype)
      .def_readwrite("nfrc_id", &OpticsParser::ProductData::nfrcid)
      .def_readwrite("thickness", &OpticsParser::ProductData::thickness)
      .def_readwrite("conductivity", &OpticsParser::ProductData::conductivity)
      .def_readwrite("coating_name", &OpticsParser::ProductData::coatingName)
      .def_readwrite("coated_side", &OpticsParser::ProductData::coatedSide)
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
                     &OpticsParser::ProductData::youngsModulus)
      .def_readwrite("pv_power_properties",
                     &OpticsParser::ProductData::pvPowerProperties)
      .def_readwrite("composition", &OpticsParser::ProductData::composition);

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
           py::arg("opening_right") = 0)
      .def_readwrite("conductivity",
                     &wincalc::Product_Data_Thermal::conductivity)
      .def_readwrite("opening_top", &wincalc::Product_Data_Thermal::opening_top)
      .def_readwrite("opening_bottom",
                     &wincalc::Product_Data_Thermal::opening_bottom)
      .def_readwrite("opening_left",
                     &wincalc::Product_Data_Thermal::opening_left)
      .def_readwrite("opening_right",
                     &wincalc::Product_Data_Thermal::opening_right)
      .def_readwrite("effective_openness",
                     &wincalc::Product_Data_Thermal::effective_openness)
	  .def_readwrite("effective_thickness",
                     &wincalc::Product_Data_Thermal::effective_thickness)
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

  py::class_<
      wincalc::Product_Data_Dual_Band_Optical_Hemispheric,
      wincalc::Product_Data_Dual_Band_Optical,
      std::shared_ptr<wincalc::Product_Data_Dual_Band_Optical_Hemispheric>>(
      m, "ProductDataOpticalDualBandHemispheric")
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
      m, "ProductDataOpticalDualBandBSDF")
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

  py::class_<wincalc::Venetian_Geometry,
             std::shared_ptr<wincalc::Venetian_Geometry>>(m, "VenetianGeometry")
      .def(py::init<double, double, double, double, bool,
                    SingleLayerOptics::DistributionMethod, int>(),
           py::arg("slat_tilt_degrees"), py::arg("slat_width_meters"),
           py::arg("slat_spacing_meters"), py::arg("slat_curvature_meters"),
           py::arg("is_horizontal") = true,
           py::arg("distribution_method") =
               SingleLayerOptics::DistributionMethod::DirectionalDiffuse,
           py::arg("number_slat_segments") = 5)
      .def_readwrite("slat_tilt", &wincalc::Venetian_Geometry::slat_tilt)
      .def_readwrite("slat_width", &wincalc::Venetian_Geometry::slat_width)
      .def_readwrite("slat_spacing", &wincalc::Venetian_Geometry::slat_spacing)
      .def_readwrite("slat_curvature",
                     &wincalc::Venetian_Geometry::slat_curvature)
      .def_readwrite("number_slat_segments",
                     &wincalc::Venetian_Geometry::number_slat_segments)
      .def_readwrite("distribution_method",
                     &wincalc::Venetian_Geometry::distribution_method)
      .def_readwrite("is_horizontal",
                     &wincalc::Venetian_Geometry::is_horizontal);

  py::class_<wincalc::Product_Data_Optical_Venetian,
             wincalc::Product_Data_Optical_With_Material,
             std::shared_ptr<wincalc::Product_Data_Optical_Venetian>>(
      m, "ProductDataOpticalVenetian")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical> const &,
                    wincalc::Venetian_Geometry const &>(),
           py::arg("product_data_optical"), py::arg("geometry"))
      .def_readwrite("geometry",
                     &wincalc::Product_Data_Optical_Venetian::geometry);

  py::class_<wincalc::Woven_Geometry, std::shared_ptr<wincalc::Woven_Geometry>>(
      m, "WovenGeometry")
      .def(py::init<double, double, double>(), py::arg("thread_diamater"),
           py::arg("thread_spacing"), py::arg("shade_thickness"))
      .def_readwrite("thread_diameter",
                     &wincalc::Woven_Geometry::thread_diameter)
      .def_readwrite("thread_spacing", &wincalc::Woven_Geometry::thread_spacing)
      .def_readwrite("shade_thickness",
                     &wincalc::Woven_Geometry::shade_thickness);

  py::class_<wincalc::Product_Data_Optical_Woven_Shade,
             wincalc::Product_Data_Optical_With_Material,
             std::shared_ptr<wincalc::Product_Data_Optical_Woven_Shade>>(
      m, "ProductDataOpticalWovenShade")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical> const &,
                    wincalc::Woven_Geometry const &>(),
           py::arg("material_product_data_optical"), py::arg("geometry"))
      .def_readwrite("geometry",
                     &wincalc::Product_Data_Optical_Woven_Shade::geometry);

  py::class_<wincalc::Perforated_Geometry,
             std::shared_ptr<wincalc::Perforated_Geometry>>
      perforated_geometry(m, "PerforatedGeometry");

  perforated_geometry
      .def(py::init<double, double, double, double,
                    wincalc::Perforated_Geometry::Type>(),
           py::arg("spacing_x"), py::arg("spacing_y"), py::arg("dimension_x"),
           py::arg("dimension_y"), py::arg("perforation_type"))
      .def_readwrite("spacing_x", &wincalc::Perforated_Geometry::spacing_x)
      .def_readwrite("spacing_y", &wincalc::Perforated_Geometry::spacing_y)
      .def_readwrite("dimension_x", &wincalc::Perforated_Geometry::dimension_x)
      .def_readwrite("dimension_y", &wincalc::Perforated_Geometry::dimension_y)
      .def_readwrite("perforation_type",
                     &wincalc::Perforated_Geometry::perforation_type);

  py::enum_<wincalc::Perforated_Geometry::Type>(perforated_geometry, "Type")
      .value("CIRCULAR", wincalc::Perforated_Geometry::Type::CIRCULAR)
      .value("RECTANGULAR", wincalc::Perforated_Geometry::Type::RECTANGULAR)
      .value("SQUARE", wincalc::Perforated_Geometry::Type::SQUARE);

  py::class_<wincalc::Product_Data_Optical_Perforated_Screen,
             wincalc::Product_Data_Optical_With_Material,
             std::shared_ptr<wincalc::Product_Data_Optical_Perforated_Screen>>(
      m, "ProductDataOpticalPerforatedScreen")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical> const &,
                    wincalc::Perforated_Geometry const &>(),
           py::arg("material_product_data_optical"), py::arg("geometry"))
      .def_readwrite(
          "geometry",
          &wincalc::Product_Data_Optical_Perforated_Screen::geometry);

  py::class_<wincalc::Product_Data_Optical_Thermal>(
      m, "ProductDataOpticalAndThermal")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical>,
                    std::shared_ptr<wincalc::Product_Data_Thermal>>(),
           py::arg("product_data_optical"), py::arg("product_data_thermal"))
      .def_readwrite("optical_data",
                     &wincalc::Product_Data_Optical_Thermal::optical_data)
      .def_readwrite("thermal_data",
                     &wincalc::Product_Data_Optical_Thermal::thermal_data);

  py::enum_<SingleLayerOptics::BSDFBasis>(m, "BSDFBasisType", py::arithmetic())
      .value("SMALL", SingleLayerOptics::BSDFBasis::Small)
      .value("QUARTER", SingleLayerOptics::BSDFBasis::Quarter)
      .value("HALF", SingleLayerOptics::BSDFBasis::Half)
      .value("FULL", SingleLayerOptics::BSDFBasis::Full);

  py::class_<SingleLayerOptics::BSDFHemisphere>(m, "BSDFHemisphere")
      .def_static("create",
                  py::overload_cast<SingleLayerOptics::BSDFBasis>(
                      &SingleLayerOptics::BSDFHemisphere::create),
                  py::arg("bsdf_basis"))
      .def("get_directions", &SingleLayerOptics::BSDFHemisphere::getDirections);

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
      .def_readwrite("layer_deflection_max",
                     &wincalc::Deflection_Results::layer_deflection_max)
      .def_readwrite("layer_deflection_mean",
                     &wincalc::Deflection_Results::layer_deflection_mean)
      .def_readwrite("panes_load", &wincalc::Deflection_Results::panes_load)
      .def_readwrite("gap_width_max",
                     &wincalc::Deflection_Results::gap_width_max)
      .def_readwrite("gap_width_mean",
                     &wincalc::Deflection_Results::gap_width_mean);

  py::class_<wincalc::Glazing_System>(m, "GlazingSystem")
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

  m.def("create_gas", &wincalc::create_gas, py::arg("components"),
        "Create a gas mixture from components: a list of pairs where the first "
        "in each item is the percent of the total and the second is the gas.");

  m.def("create_venetian_blind",
        py::overload_cast<wincalc::Venetian_Geometry const &,
                          OpticsParser::ProductData const &>(
            &wincalc::create_venetian_blind),
        py::arg("geometry"), py::arg("material"),
        "Create a venetian blind from a geometry and parsed material.");

  m.def("create_venetian_blind",
        py::overload_cast<wincalc::Venetian_Geometry const &,
                          std::shared_ptr<wincalc::Product_Data_Optical>,
                          std::shared_ptr<wincalc::Product_Data_Thermal>>(
            &wincalc::create_venetian_blind),
        py::arg("geometry"), py::arg("material_data_optical"),
        py::arg("material_data_thermal").none(true),
        "Create a venetian blind from a geometry and material optical and "
        "thermal data.");

  m.def("create_woven_shade",
        py::overload_cast<wincalc::Woven_Geometry const &,
                          OpticsParser::ProductData const &>(
            &wincalc::create_woven_shade),
        py::arg("geometry"), py::arg("material"),
        "Create a woven shade from a geometry and parsed material.");

  m.def("create_woven_shade",
        py::overload_cast<wincalc::Woven_Geometry const &,
                          std::shared_ptr<wincalc::Product_Data_Optical>,
                          std::shared_ptr<wincalc::Product_Data_Thermal>>(
            &wincalc::create_woven_shade),
        py::arg("geometry"), py::arg("material_data_optical"),
        py::arg("material_data_thermal").none(true),
        "Create a woven shade from a geometry and material optical and "
        "thermal data.");

  m.def("create_perforated_screen",
        py::overload_cast<wincalc::Perforated_Geometry const &,
                          OpticsParser::ProductData const &>(
            &wincalc::create_perforated_screen),
        py::arg("geometry"), py::arg("material"),
        "Create a perforated screen from a geometry and parsed material.");

  m.def("create_perforated_screen",
        py::overload_cast<wincalc::Perforated_Geometry const &,
                          std::shared_ptr<wincalc::Product_Data_Optical>,
                          std::shared_ptr<wincalc::Product_Data_Thermal>>(
            &wincalc::create_perforated_screen),
        py::arg("geometry"), py::arg("material_data_optical"),
        py::arg("material_data_thermal").none(true),
        "Create a perforated screen from a geometry and material optical and "
        "thermal data.");

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

  m.def("calc_thermal_ir", &wincalc::calc_thermal_ir,
        py::arg("optical_standard"), py::arg("product_data"));

  m.def("get_spacer_keff", &wincalc::get_spacer_keff,
        "Calculate the effective conductivity of a spacer from a THERM thmx "
        "file.");
  m.def("get_cma_window_single_vision",
        py::overload_cast<thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &, double, double>(
            &wincalc::get_cma_window_single_vision),
        "Get the CMA template for a single vision window.");
  m.def(
      "get_cma_window_single_vision",
      py::overload_cast<
          CMA::CMAFrame const &, CMA::CMAFrame const &, CMA::CMAFrame const &,
          CMA::CMAFrame const &, double, double, double, double,
          CMA::CMABestWorstUFactors const &, CMA::CMABestWorstUFactors const &>(
          &wincalc::get_cma_window_single_vision),
      "Get the CMA template for a single vision window.");
  m.def("get_cma_window_double_vision_vertical",
        py::overload_cast<thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &, double, double>(
            &wincalc::get_cma_window_double_vision_vertical),
        "Get the CMA template for a double vision vertical window.");
  m.def(
      "get_cma_window_double_vision_vertical",
      py::overload_cast<
          CMA::CMAFrame const &, CMA::CMAFrame const &, CMA::CMAFrame const &,
          CMA::CMAFrame const &, CMA::CMAFrame const &, CMA::CMAFrame const &,
          CMA::CMAFrame const &, double, double, double, double,
          CMA::CMABestWorstUFactors const &, CMA::CMABestWorstUFactors const &>(
          &wincalc::get_cma_window_double_vision_vertical),
      "Get the CMA template for a double vision vertical window.");
  m.def("get_cma_window_double_vision_horizontal",
        py::overload_cast<thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &,
                          thmxParser::ThmxFileContents const &, double, double>(
            &wincalc::get_cma_window_double_vision_horizontal),
        "Get the CMA template for a double vision horizontal window.");
  m.def(
      "get_cma_window_double_vision_horizontal",
      py::overload_cast<
          CMA::CMAFrame const &, CMA::CMAFrame const &, CMA::CMAFrame const &,
          CMA::CMAFrame const &, CMA::CMAFrame const &, CMA::CMAFrame const &,
          CMA::CMAFrame const &, double, double, double, double,
          CMA::CMABestWorstUFactors const &, CMA::CMABestWorstUFactors const &>(
          &wincalc::get_cma_window_double_vision_horizontal),
      "Get the CMA template for a double vision horizontal window.");

  py::class_<wincalc::CMAResult>(m, "CMAResult")
      .def_readwrite("u", &wincalc::CMAResult::u)
      .def_readwrite("shgc", &wincalc::CMAResult::shgc)
      .def_readwrite("vt", &wincalc::CMAResult::vt);

  m.def("calc_cma", &wincalc::calc_cma, "Get CMA results.");

  py::enum_<SingleLayerOptics::BSDFDirection>(m, "BSDFDirection",
                                              py::arithmetic())
      .value("Incoming", SingleLayerOptics::BSDFDirection::Incoming)
      .value("Outgoing", SingleLayerOptics::BSDFDirection::Outgoing);

  py::enum_<FenestrationCommon::Side>(m, "Side", py::arithmetic())
      .value("Front", FenestrationCommon::Side::Front)
      .value("Back", FenestrationCommon::Side::Back);

  py::enum_<FenestrationCommon::PropertySimple>(m, "PropertySimple",
                                                py::arithmetic())
      .value("T", FenestrationCommon::PropertySimple::T)
      .value("R", FenestrationCommon::PropertySimple::R);

  py::class_<FenestrationCommon::SquareMatrix>(m, "SquareMatrix")
      .def(py::init<std::vector<std::vector<double>> const &>(),
           py::arg("input"))
      .def("size", &FenestrationCommon::SquareMatrix::size)
      .def("set_zeros", &FenestrationCommon::SquareMatrix::setZeros)
      .def("set_identity", &FenestrationCommon::SquareMatrix::setIdentity)
      .def("set_diagonal", &FenestrationCommon::SquareMatrix::setDiagonal)
      .def("make_upper_triangular",
           &FenestrationCommon::SquareMatrix::makeUpperTriangular)
      .def("inverse", &FenestrationCommon::SquareMatrix::inverse)
      .def("mmult_rows", &FenestrationCommon::SquareMatrix::mmultRows)
      .def("get_matrix", &FenestrationCommon::SquareMatrix::getMatrix);

  py::class_<SingleLayerOptics::BSDFDirections>(m, "BSDFDirections")
      .def(py::init<>())
      .def(py::init<std::vector<SingleLayerOptics::BSDFDefinition> const &,
                    SingleLayerOptics::BSDFDirection>(),
           py::arg("definitions"), py::arg("side"))
      .def("lambda_vector", &SingleLayerOptics::BSDFDirections::lambdaVector)
      .def("profile_angles", &SingleLayerOptics::BSDFDirections::profileAngles)
      .def("lambda_matrix", &SingleLayerOptics::BSDFDirections::lambdaMatrix)
      .def("get_nearest_beam_index",
           &SingleLayerOptics::BSDFDirections::getNearestBeamIndex);

  py::class_<SingleLayerOptics::BSDFIntegrator>(m, "BSDFIntegrator")
      .def(py::init<SingleLayerOptics::BSDFDirections const &>(),
           py::arg("directions"))
      .def("get_matrix", &SingleLayerOptics::BSDFIntegrator::getMatrix)
      .def("at", &SingleLayerOptics::BSDFIntegrator::at)
      .def("set_matrices", &SingleLayerOptics::BSDFIntegrator::setMatrices)
      .def(
          "direct_direct",
          py::overload_cast<FenestrationCommon::Side,
                            FenestrationCommon::PropertySimple, double, double>(
              &SingleLayerOptics::BSDFIntegrator::DirDir, py::const_))
      .def("direct_direct",
           py::overload_cast<FenestrationCommon::Side,
                             FenestrationCommon::PropertySimple, size_t>(
               &SingleLayerOptics::BSDFIntegrator::DirDir, py::const_))
      .def("direct_hemispheric",
           py::overload_cast<FenestrationCommon::Side,
                             FenestrationCommon::PropertySimple>(
               &SingleLayerOptics::BSDFIntegrator::DirHem))
      .def(
          "direct_hemispheric",
          py::overload_cast<FenestrationCommon::Side,
                            FenestrationCommon::PropertySimple, double, double>(
              &SingleLayerOptics::BSDFIntegrator::DirHem))
      .def("absorptance", py::overload_cast<FenestrationCommon::Side>(
                              &SingleLayerOptics::BSDFIntegrator::Abs))
      .def("absorptance",
           py::overload_cast<FenestrationCommon::Side, double, double>(
               &SingleLayerOptics::BSDFIntegrator::Abs))
      .def("absorptance", py::overload_cast<FenestrationCommon::Side, size_t>(
                              &SingleLayerOptics::BSDFIntegrator::Abs))
      .def("diffuse_diffuse", &SingleLayerOptics::BSDFIntegrator::DiffDiff)
      .def("absorptance_diffuse_diffuse",
           &SingleLayerOptics::BSDFIntegrator::AbsDiffDiff)
      .def("lambda_vector", &SingleLayerOptics::BSDFIntegrator::lambdaVector)
      .def("lambda_matrix", &SingleLayerOptics::BSDFIntegrator::lambdaMatrix)
      .def("get_nearest_beam_index",
           &SingleLayerOptics::BSDFIntegrator::getNearestBeamIndex);

  py::class_<EffectiveLayers::EffectiveOpenness>(m, "EffectiveOpenness")
      .def(py::init<double, double, double, double, double, double>(),
           py::arg("ah"), py::arg("al"), py::arg("ar"), py::arg("atop"),
           py::arg("abot"), py::arg("front_porosity"))
      .def_readwrite("ah", &EffectiveLayers::EffectiveOpenness::Ah)
      .def_readwrite("al", &EffectiveLayers::EffectiveOpenness::Al)
      .def_readwrite("ar", &EffectiveLayers::EffectiveOpenness::Ar)
      .def_readwrite("atop", &EffectiveLayers::EffectiveOpenness::Atop)
      .def_readwrite("abot", &EffectiveLayers::EffectiveOpenness::Abot)
      .def_readwrite("front_porosity",
                     &EffectiveLayers::EffectiveOpenness::FrontPorosity);
	
	m.def("is_closed", &EffectiveLayers::isClosed, py::arg("effective_openness"));

  py::class_<Tarcog::ISO15099::Layers>(m, "Layers")
      .def_static("solid", &Tarcog::ISO15099::Layers::solid,
                  "Factory method for creating a solid Tarcog layer",
                  py::arg("thickness"), py::arg("conductivity"),
                  py::arg("frontEmissivity") = 0.84,
                  py::arg("frontIRTransmittance") = 0.0,
                  py::arg("backEmissivity") = 0.84,
                  py::arg("backIRTransmittance") = 0.0)
      .def_static("update_material_data",
                  &Tarcog::ISO15099::Layers::updateMaterialData,
                  "Static method for updating the material information for a "
                  "solid Tarcog layer.",
                  py::arg("layer"),
                  py::arg("density") = Tarcog::MaterialConstants::GLASSDENSITY,
                  py::arg("youngs_modulus") =
                      Tarcog::DeflectionConstants::YOUNGSMODULUS)
      .def_static("shading", &Tarcog::ISO15099::Layers::shading,
                  "Factory function to create a Tarcog shading layer.",
                  py::arg("thickness"), py::arg("conductivity"),
                  py::arg("effective_openness") =
                      EffectiveLayers::EffectiveOpenness(0, 0, 0, 0, 0, 0),
                  py::arg("front_emissivity") = 0.84,
                  py::arg("front_transmittance") = 0.0,
                  py::arg("back_emissivity") = 0.84,
                  py::arg("back_transmittance") = 0.0)
      .def_static(
          "gap",
          py::overload_cast<double, double>(&Tarcog::ISO15099::Layers::gap),
          "Factory function to create a Tarcog air gap", py::arg("thickness"),
          py::arg("pressure") = 101325)
      .def_static("gap",
                  py::overload_cast<double, Gases::CGas const &, double>(
                      &Tarcog::ISO15099::Layers::gap),
                  "Factory function to create a Tarcog gap from a gas",
                  py::arg("thickness"), py::arg("gas"),
                  py::arg("pressure") = 101325)
      .def_static(
          "create_pillar",
          py::overload_cast<Tarcog::ISO15099::CylindricalPillar const &,
                            double>(&Tarcog::ISO15099::Layers::createPillar),
          "Static function to add a cylindrical pillar to a Tarcog gap",
          py::arg("pillar"), py::arg("pressure"))
      .def_static(
          "create_pillar",
          py::overload_cast<Tarcog::ISO15099::SphericalPillar const &, double>(
              &Tarcog::ISO15099::Layers::createPillar),
          "Static function to add a spherical pillar to a Tarcog gap",
          py::arg("pillar"), py::arg("pressure"))
      .def_static(
          "create_pillar",
          py::overload_cast<Tarcog::ISO15099::RectangularPillar const &,
                            double>(&Tarcog::ISO15099::Layers::createPillar),
          "Static function to add a rectangular pillar to a Tarcog gap",
          py::arg("pillar"), py::arg("pressure"))
      .def_static(
          "create_pillar",
          py::overload_cast<Tarcog::ISO15099::TriangularPillar const &, double>(
              &Tarcog::ISO15099::Layers::createPillar),
          "Static function to add a triangular pillar to a Tarcog gap",
          py::arg("pillar"), py::arg("pressure"))
	  .def_static(
          "create_pillar",
          py::overload_cast<Tarcog::ISO15099::PentagonPillar const &, double>(
              &Tarcog::ISO15099::Layers::createPillar),
          "Static function to add a pentagon pillar to a Tarcog gap",
          py::arg("pillar"), py::arg("pressure"))
	  .def_static(
          "create_pillar",
          py::overload_cast<Tarcog::ISO15099::HexagonPillar const &, double>(
              &Tarcog::ISO15099::Layers::createPillar),
          "Static function to add a hexagon pillar to a Tarcog gap",
          py::arg("pillar"), py::arg("pressure"))
      .def_static(
          "create_pillar",
          py::overload_cast<Tarcog::ISO15099::LinearBearingPillar const &,
                            double>(&Tarcog::ISO15099::Layers::createPillar),
          "Static function to add a linear bearing pillar to a Tarcog gap",
          py::arg("pillar"), py::arg("pressure"))
      .def_static(
          "create_pillar",
          py::overload_cast<Tarcog::ISO15099::TruncatedConePillar const &,
                            double>(&Tarcog::ISO15099::Layers::createPillar),
          "Static function to add a truncated cone pillar to a Tarcog gap",
          py::arg("pillar"), py::arg("pressure"))
      .def_static(
          "create_pillar",
          py::overload_cast<Tarcog::ISO15099::AnnulusCylinderPillar const &,
                            double>(&Tarcog::ISO15099::Layers::createPillar),
          "Static function to add a annulus cylinder pillar to a Tarcog gap",
          py::arg("pillar"), py::arg("pressure"))
      .def_static(
          "create_pillar",
          py::overload_cast<Tarcog::ISO15099::PillarMeasurement const &>(
              &Tarcog::ISO15099::Layers::createPillar),
          "Static function to add a measured pillar to a Tarcog gap",
          py::arg("pillar"));
}
