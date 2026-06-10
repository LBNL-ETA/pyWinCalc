#include "gas_bindings.h"
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

void register_gas_bindings(py::module &mod) {
  py::enum_<Gases::GasDef>(mod, "PredefinedGasType", py::arithmetic())
      .value("AIR", Gases::GasDef::Air)
      .value("ARGON", Gases::GasDef::Argon)
      .value("KRYPTON", Gases::GasDef::Krypton)
      .value("XENON", Gases::GasDef::Xenon);

  py::class_<Gases::CIntCoeff>(mod, "GasCoefficients")
      .def(py::init<double const, double const, double const>(), py::arg("A"),
           py::arg("B"), py::arg("C"));

  py::class_<Gases::CGasData>(mod, "GasData")
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

  py::class_<Gases::GasProperties>(mod, "GasProperties")
      .def_readwrite("thermal_conductivity",
                     &Gases::GasProperties::m_ThermalConductivity)
      .def_readwrite("viscosity", &Gases::GasProperties::m_Viscosity)
      .def_readwrite("specific_heat", &Gases::GasProperties::m_SpecificHeat)
      .def_readwrite("density", &Gases::GasProperties::m_Density)
      .def_readwrite("molecular_weight",
                     &Gases::GasProperties::m_MolecularWeight)
      .def_readwrite("prandl_number", &Gases::GasProperties::m_PrandlNumber)
      .def_readwrite("properties_calculated",
                     &Gases::GasProperties::m_PropertiesCalculated);

  py::class_<Gases::CGasItem>(mod, "GasItem")
      .def(py::init<double, Gases::CGasData const &>(), py::arg("fraction"),
           py::arg("gas_data"))
      .def(py::init<double, Gases::GasDef>(), py::arg("fraction"),
           py::arg("predefined_gas"))
      .def("fraction", &Gases::CGasItem::fraction)
      .def("name", &Gases::CGasItem::name)
      .def("gas_data", &Gases::CGasItem::gasData);

  py::class_<Gases::CGas>(mod, "Gas")
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
}
