#include "thmx_bindings.h"
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

void register_thmx_bindings(py::module &mod) {
  py::class_<thmxParser::MeshParameters>(mod, "ThmxMeshParameters")
      .def_readwrite("quad_tree_mesh_level",
                     &thmxParser::MeshParameters::quadTreeMeshLevel)
      .def_readwrite("error_check_flag",
                     &thmxParser::MeshParameters::errorCheckFlag)
      .def_readwrite("error_limit", &thmxParser::MeshParameters::errorLimit)
      .def_readwrite("max_iterations",
                     &thmxParser::MeshParameters::maxIterations)
      .def_readwrite("cma_flag", &thmxParser::MeshParameters::cmaFlag);

  py::class_<thmxParser::ColorRGB>(mod, "ThmxRGB")
      .def_readwrite("r", &thmxParser::ColorRGB::r)
      .def_readwrite("g", &thmxParser::ColorRGB::g)
      .def_readwrite("b", &thmxParser::ColorRGB::b);

  py::class_<thmxParser::Material>(mod, "ThmxMaterial")
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

  py::class_<thmxParser::BoundaryCondition>(mod, "ThmxBoundaryCondition")
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

  py::class_<thmxParser::PolygonPoint>(mod, "ThmxPolygonPoint")
      .def_readwrite("index", &thmxParser::PolygonPoint::index)
      .def_readwrite("x", &thmxParser::PolygonPoint::x)
      .def_readwrite("y", &thmxParser::PolygonPoint::y);

  py::class_<thmxParser::Polygon>(mod, "ThmxPolygon")
      .def_readwrite("id", &thmxParser::Polygon::id)
      .def_readwrite("material", &thmxParser::Polygon::material)
      .def_readwrite("points", &thmxParser::Polygon::points);

  py::class_<thmxParser::BoundaryConditionPolygon>(
      mod, "ThmxBoundaryConditionPolygon")
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

  py::class_<thmxParser::CMABestWorstOption>(mod, "ThmxCMABestWorstOption")
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

  py::class_<thmxParser::CMAOptions>(mod, "ThmxCMAOptions")
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

  py::class_<thmxParser::UFactorProjectionResult>(mod,
                                                  "ThmxUFactorProjectionResult")
      .def_readwrite("length_type",
                     &thmxParser::UFactorProjectionResult::lengthType)
      .def_readwrite("length_units",
                     &thmxParser::UFactorProjectionResult::lengthUnits)
      .def_readwrite("length", &thmxParser::UFactorProjectionResult::length)
      .def_readwrite("ufactor_units",
                     &thmxParser::UFactorProjectionResult::ufactorUnits)
      .def_readwrite("ufactor", &thmxParser::UFactorProjectionResult::ufactor);

  py::class_<thmxParser::UFactorResults>(mod, "ThmxUFactorResults")
      .def_readwrite("tag", &thmxParser::UFactorResults::tag)
      .def_readwrite("delta_t_units", &thmxParser::UFactorResults::deltaTUnits)
      .def_readwrite("delta_t", &thmxParser::UFactorResults::deltaT)
      .def_readwrite("projection_results",
                     &thmxParser::UFactorResults::projectionResults);

  py::class_<thmxParser::Result>(mod, "ThmxResult")
      .def_readwrite("model_type", &thmxParser::Result::modelType)
      .def_readwrite("glazing_case", &thmxParser::Result::glazingCase)
      .def_readwrite("spacer_case", &thmxParser::Result::spacerCase)
      .def_readwrite("ufactor_results", &thmxParser::Result::ufactorResults);

  py::class_<thmxParser::ThmxFileContents>(mod, "ThmxFileContents")
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
}
