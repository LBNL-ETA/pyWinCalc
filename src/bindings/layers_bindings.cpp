#include "layers_bindings.h"
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

void register_layers_bindings(py::module &mod) {
  py::class_<EffectiveLayers::EffectiveMultipliers>(mod, "EffectiveMultipliers")
      .def(py::init<double, double, double, double, double, double>(),
          py::arg("front"),
          py::arg("left"),
          py::arg("right"),
          py::arg("top"),
          py::arg("bot"),
          py::arg("permeability_factor"))
      .def_readwrite("front", &EffectiveLayers::EffectiveMultipliers::Mfront)
      .def_readwrite("left", &EffectiveLayers::EffectiveMultipliers::Mleft)
      .def_readwrite("right", &EffectiveLayers::EffectiveMultipliers::Mright)
      .def_readwrite("top", &EffectiveLayers::EffectiveMultipliers::Mtop)
      .def_readwrite("bot", &EffectiveLayers::EffectiveMultipliers::Mbot)
      .def_readwrite("permeability_factor", &EffectiveLayers::EffectiveMultipliers::PermeabilityFactor);

  mod.def("is_closed", &EffectiveLayers::isClosed, py::arg("effective_openness"));

  py::module_ layers = mod.def_submodule("Layers", "Submodule for Tarcog Layers");

  layers.def("solid", py::overload_cast<double, double>(&Tarcog::ISO15099::Layers::solid),
             "Factory method for creating a solid Tarcog layer with basic parameters",
             py::arg("thickness"), py::arg("conductivity"));

  layers.def("solid", py::overload_cast<double, double, double, double, double, double>(&Tarcog::ISO15099::Layers::solid),
             "Factory method for creating a solid Tarcog layer including IR parameters",
             py::arg("thickness"), py::arg("conductivity"),
             py::arg("frontEmissivity") = 0.84,
             py::arg("frontIRTransmittance") = 0.0,
             py::arg("backEmissivity") = 0.84,
             py::arg("backIRTransmittance") = 0.0);

  layers.def("update_material_data",
             &Tarcog::ISO15099::Layers::updateMaterialData,
             "Static method for updating the material information for a "
             "solid Tarcog layer.",
             py::arg("layer"),
             py::arg("density") = Tarcog::MaterialConstants::GLASSDENSITY,
             py::arg("youngs_modulus") = Tarcog::DeflectionConstants::YOUNGSMODULUS);

  layers.def("shading", &Tarcog::ISO15099::Layers::shading,
             "Factory function to create a Tarcog shading layer.",
             py::arg("thickness"), py::arg("conductivity"),
             py::arg("effective_multipliers") = EffectiveLayers::EffectiveMultipliers{0, 0, 0, 0, 0, 0},
             py::arg("front_emissivity") = 0.84,
             py::arg("front_transmittance") = 0.0,
             py::arg("back_emissivity") = 0.84,
             py::arg("back_transmittance") = 0.0);

  layers.def("sealedLayer", &Tarcog::ISO15099::Layers::sealedLayer,
             "Factory function to create a Tarcog sealed layer.",
             py::arg("thickness"), py::arg("conductivity"),
             py::arg("front_emissivity") = 0.84,
             py::arg("front_transmittance") = 0.0,
             py::arg("back_emissivity") = 0.84,
             py::arg("back_transmittance") = 0.0);

  layers.def("gap", py::overload_cast<double, bool>(&Tarcog::ISO15099::Layers::gap),
             "Factory function to create a Tarcog gap with basic parameters",
             py::arg("thickness"), py::arg("is_dcenter") = false);

  layers.def("gap", py::overload_cast<double, double, bool>(&Tarcog::ISO15099::Layers::gap),
             "Factory function to create a Tarcog gap with thickness and pressure",
             py::arg("thickness"), py::arg("pressure") = 101325, py::arg("is_dcenter") = false);

  layers.def("gap", py::overload_cast<double, const Gases::CGas &, bool>(&Tarcog::ISO15099::Layers::gap),
             "Factory function to create a Tarcog gap with thickness and gas",
             py::arg("thickness"), py::arg("gas"), py::arg("is_dcenter") = false);

  layers.def("gap", py::overload_cast<double, double, const Gases::CGas &, bool>(&Tarcog::ISO15099::Layers::gap),
             "Factory function to create a Tarcog gap with thickness, pressure and gas",
             py::arg("thickness"), py::arg("pressure"), py::arg("gas"), py::arg("is_dcenter") = false);

  layers.def("gap", py::overload_cast<double, double, const Gases::CGas &, double, double, bool>(&Tarcog::ISO15099::Layers::gap),
             "Factory function to create a Tarcog gap with all parameters",
             py::arg("thickness"), py::arg("pressure"), py::arg("gas"),
             py::arg("accommodation1"), py::arg("accommodation2"), py::arg("is_dcenter") = false);

  layers.def("forced_ventilation_gap", &Tarcog::ISO15099::Layers::forcedVentilationGap,
             "Function to create a forced ventilation Tarcog gap",
             py::arg("gap"), py::arg("forcedVentilationAirSpeed"),
             py::arg("forcedVentilationAirTemperature"));

  layers.def("default_vacuum_mixture", &Tarcog::ISO15099::Layers::defaultVacuumMixture,
             "Function to get the default vacuum mixture");

  layers.def("create_pillar", py::overload_cast<const Tarcog::ISO15099::CylindricalPillar &, double, const Gases::CGas &, double, double>(&Tarcog::ISO15099::Layers::createPillar),
             "Static function to add a cylindrical pillar to a Tarcog gap",
             py::arg("pillar"), py::arg("pressure"), py::arg("gas") = Tarcog::ISO15099::Layers::defaultVacuumMixture(),
             py::arg("accommodation1") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT,
             py::arg("accommodation2") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT);

  layers.def("create_pillar", py::overload_cast<const Tarcog::ISO15099::SphericalPillar &, double, const Gases::CGas &, double, double>(&Tarcog::ISO15099::Layers::createPillar),
             "Static function to add a spherical pillar to a Tarcog gap",
             py::arg("pillar"), py::arg("pressure"), py::arg("gas") = Tarcog::ISO15099::Layers::defaultVacuumMixture(),
             py::arg("accommodation1") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT,
             py::arg("accommodation2") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT);

  layers.def("create_pillar", py::overload_cast<const Tarcog::ISO15099::RectangularPillar &, double, const Gases::CGas &, double, double>(&Tarcog::ISO15099::Layers::createPillar),
             "Static function to add a rectangular pillar to a Tarcog gap",
             py::arg("pillar"), py::arg("pressure"), py::arg("gas") = Tarcog::ISO15099::Layers::defaultVacuumMixture(),
             py::arg("accommodation1") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT,
             py::arg("accommodation2") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT);

  layers.def("create_pillar", py::overload_cast<const Tarcog::ISO15099::TriangularPillar &, double, const Gases::CGas &, double, double>(&Tarcog::ISO15099::Layers::createPillar),
             "Static function to add a triangular pillar to a Tarcog gap",
             py::arg("pillar"), py::arg("pressure"), py::arg("gas") = Tarcog::ISO15099::Layers::defaultVacuumMixture(),
             py::arg("accommodation1") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT,
             py::arg("accommodation2") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT);

  layers.def("create_pillar", py::overload_cast<const Tarcog::ISO15099::PentagonPillar &, double, const Gases::CGas &, double, double>(&Tarcog::ISO15099::Layers::createPillar),
             "Static function to add a pentagon pillar to a Tarcog gap",
             py::arg("pillar"), py::arg("pressure"), py::arg("gas") = Tarcog::ISO15099::Layers::defaultVacuumMixture(),
             py::arg("accommodation1") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT,
             py::arg("accommodation2") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT);

  layers.def("create_pillar", py::overload_cast<const Tarcog::ISO15099::HexagonPillar &, double, const Gases::CGas &, double, double>(&Tarcog::ISO15099::Layers::createPillar),
             "Static function to add a hexagon pillar to a Tarcog gap",
             py::arg("pillar"), py::arg("pressure"), py::arg("gas") = Tarcog::ISO15099::Layers::defaultVacuumMixture(),
             py::arg("accommodation1") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT,
             py::arg("accommodation2") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT);

  layers.def("create_pillar", py::overload_cast<const Tarcog::ISO15099::LinearBearingPillar &, double, const Gases::CGas &, double, double>(&Tarcog::ISO15099::Layers::createPillar),
             "Static function to add a linear bearing pillar to a Tarcog gap",
             py::arg("pillar"), py::arg("pressure"), py::arg("gas") = Tarcog::ISO15099::Layers::defaultVacuumMixture(),
             py::arg("accommodation1") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT,
             py::arg("accommodation2") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT);

  layers.def("create_pillar", py::overload_cast<const Tarcog::ISO15099::TruncatedConePillar &, double, const Gases::CGas &, double, double>(&Tarcog::ISO15099::Layers::createPillar),
             "Static function to add a truncated cone pillar to a Tarcog gap",
             py::arg("pillar"), py::arg("pressure"), py::arg("gas") = Tarcog::ISO15099::Layers::defaultVacuumMixture(),
             py::arg("accommodation1") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT,
             py::arg("accommodation2") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT);

  layers.def("create_pillar", py::overload_cast<const Tarcog::ISO15099::AnnulusCylinderPillar &, double, const Gases::CGas &, double, double>(&Tarcog::ISO15099::Layers::createPillar),
             "Static function to add an annulus cylinder pillar to a Tarcog gap",
             py::arg("pillar"), py::arg("pressure"), py::arg("gas") = Tarcog::ISO15099::Layers::defaultVacuumMixture(),
             py::arg("accommodation1") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT,
             py::arg("accommodation2") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT);

  layers.def("create_pillar", py::overload_cast<const Tarcog::ISO15099::CShapedCylinderPillar &, double, const Gases::CGas &, double, double>(&Tarcog::ISO15099::Layers::createPillar),
             "Static function to add a C-shaped cylinder pillar to a Tarcog gap",
             py::arg("pillar"), py::arg("pressure"), py::arg("gas") = Tarcog::ISO15099::Layers::defaultVacuumMixture(),
             py::arg("accommodation1") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT,
             py::arg("accommodation2") = ConstantsData::DEFAULT_SURFACE_ACCOMMODATION_COEFFICIENT);

  layers.def("create_pillar", py::overload_cast<const Tarcog::ISO15099::PillarMeasurement &>(&Tarcog::ISO15099::Layers::createPillar),
             "Static function to add a measured pillar to a Tarcog gap",
             py::arg("pillar"));
}
