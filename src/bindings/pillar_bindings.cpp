#include "pillar_bindings.h"
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

void register_pillar_bindings(py::module &mod) {
  py::class_<Tarcog::ISO15099::CIGUGapLayer,
             std::shared_ptr<Tarcog::ISO15099::CIGUGapLayer>>(mod, "IGUGapLayer")
      .def(py::init<double, double>(), py::arg("thickness"),
           py::arg("pressure"))
      .def(py::init<double, double, Gases::CGas const &>(),
           py::arg("thickness"), py::arg("pressure"), py::arg("gas"));

  py::enum_<Tarcog::ISO15099::CellSpacingType>(mod, "CellSpacingType",
                                               py::arithmetic())
      .value("SQUARE", Tarcog::ISO15099::CellSpacingType::Square)
      .value("SHIFTEDSQUARE", Tarcog::ISO15099::CellSpacingType::ShiftedSquare)
      .value("SHIFTEDROTATEDSQUARE",
             Tarcog::ISO15099::CellSpacingType::ShiftedRotatedSquare);

  mod.def("pillar_cell_area", Tarcog::ISO15099::pillarCellArea,
        py::arg("cell_spacing_type"), py::arg("sp"));

  py::enum_<Tarcog::ISO15099::PolygonType>(mod, "PolygonType", py::arithmetic())
      .value("TRIANGLE", Tarcog::ISO15099::PolygonType::Triangle)
      .value("PENTAGON", Tarcog::ISO15099::PolygonType::Pentagon)
      .value("HEXAGON", Tarcog::ISO15099::PolygonType::Hexagon);

  py::class_<Tarcog::ISO15099::UniversalSupportPillar,
             Py_UniversalSupportPillar, Tarcog::ISO15099::CIGUGapLayer,
             std::shared_ptr<Tarcog::ISO15099::UniversalSupportPillar>>(
      mod, "UniversalSupportPillar")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &, double, double>(),
           py::arg("gap_layer"), py::arg("material_conductivity"),
           py::arg("cell_area"));

  py::class_<Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::PillarData>>(mod, "PillarData")
      .def(py::init<double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"))
      .def_readwrite("height", &Tarcog::ISO15099::PillarData::height)
      .def_readwrite("material_conductivity",
                     &Tarcog::ISO15099::PillarData::materialConductivity)
      .def_readwrite("cell_area", &Tarcog::ISO15099::PillarData::cellArea);

  py::class_<Tarcog::ISO15099::CylindricalPillar, Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::CylindricalPillar>>(
      mod, "CylindricalPillar")
      .def(py::init<double, double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"),
           py::arg("radius"))
      .def_readwrite("radius", &Tarcog::ISO15099::CylindricalPillar::radius);

  py::class_<Tarcog::ISO15099::CylindricalPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::CylindricalPillarLayer>>(
      mod, "CylindricalPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::CylindricalPillar const &>(),
           py::arg("gap_layer"), py::arg("cylindrical_pillar"));

  py::class_<Tarcog::ISO15099::SphericalPillar, Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::SphericalPillar>>(
      mod, "SphericalPillar")
      .def(py::init<double, double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"),
           py::arg("radius_of_contact"))
      .def_readwrite("radius_of_contact",
                     &Tarcog::ISO15099::SphericalPillar::radiusOfContact);

  py::class_<Tarcog::ISO15099::SphericalPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::SphericalPillarLayer>>(
      mod, "SphericalPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::SphericalPillar const &>(),
           py::arg("gap_layer"), py::arg("spherical_pillar"));

  py::class_<Tarcog::ISO15099::RectangularPillar, Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::RectangularPillar>>(
      mod, "RectangularPillar")
      .def(py::init<double, double, double, double, double>(),
           py::arg("height"), py::arg("material_conductivity"),
           py::arg("cell_area"), py::arg("length"), py::arg("width"))
      .def_readwrite("length", &Tarcog::ISO15099::RectangularPillar::length)
      .def_readwrite("width", &Tarcog::ISO15099::RectangularPillar::width);

  py::class_<Tarcog::ISO15099::RectangularPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::RectangularPillarLayer>>(
      mod, "RectangularPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::RectangularPillar const &>(),
           py::arg("gap_layer"), py::arg("rectangular_pillar"));

  py::class_<Tarcog::ISO15099::PolygonalPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::PolygonalPillar>>(mod, "PolygonalPillar")
      .def(py::init<double, double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"), py::arg("length"))
      .def_readwrite("legnth", &Tarcog::ISO15099::PolygonalPillar::length);

  py::class_<Tarcog::ISO15099::TriangularPillar,
             Tarcog::ISO15099::PolygonalPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::TriangularPillar>>(mod, "TriangularPillar")
      .def(py::init<double, double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"), py::arg("length"));

  py::class_<Tarcog::ISO15099::TriangularPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::TriangularPillarLayer>>(
      mod, "TriangularPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::TriangularPillar const &>(),
           py::arg("gap_layer"), py::arg("polygon_pillar"));

  py::class_<Tarcog::ISO15099::PentagonPillar,
             Tarcog::ISO15099::PolygonalPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::PentagonPillar>>(mod, "PentagonPillar")
      .def(py::init<double, double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"), py::arg("length"));

  py::class_<Tarcog::ISO15099::PentagonPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::PentagonPillarLayer>>(
      mod, "PentagonPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::PentagonPillar const &>(),
           py::arg("gap_layer"), py::arg("polygon_pillar"));

  py::class_<Tarcog::ISO15099::HexagonPillar,
             Tarcog::ISO15099::PolygonalPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::HexagonPillar>>(mod, "HexagonPillar")
      .def(py::init<double, double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"), py::arg("length"));

  py::class_<Tarcog::ISO15099::HexagonPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::HexagonPillarLayer>>(
      mod, "HexagonPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::HexagonPillar const &>(),
           py::arg("gap_layer"), py::arg("polygon_pillar"));

  py::class_<Tarcog::ISO15099::LinearBearingPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::LinearBearingPillar>>(
      mod, "LinearBearingPillar")
      .def(py::init<double, double, double, double, double>(),
           py::arg("height"), py::arg("material_conductivity"),
           py::arg("cell_area"), py::arg("length"), py::arg("width"))
      .def_readwrite("length", &Tarcog::ISO15099::LinearBearingPillar::length)
      .def_readwrite("width", &Tarcog::ISO15099::LinearBearingPillar::width);

  py::class_<Tarcog::ISO15099::LinearBearingPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::LinearBearingPillarLayer>>(
      mod, "LinearBearingPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::LinearBearingPillar const &>(),
           py::arg("gap_layer"), py::arg("linear_bearing_pillar"));

  py::class_<Tarcog::ISO15099::TruncatedConePillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::TruncatedConePillar>>(
      mod, "TruncatedConePillar")
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
      mod, "TruncatedConePillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::TruncatedConePillar const &>(),
           py::arg("gap_layer"), py::arg("truncated_cone_pillar"));

  py::class_<Tarcog::ISO15099::AnnulusCylinderPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::AnnulusCylinderPillar>>(
      mod, "AnnulusCylinderPillar")
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
      mod, "AnnulusCylinderPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::AnnulusCylinderPillar const &>(),
           py::arg("gap_layer"), py::arg("annulus_cylinder_pillar"));

  py::class_<Tarcog::ISO15099::CShapedCylinderPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::CShapedCylinderPillar>>(
      mod, "CShapedCylinderPillar")
      .def(py::init<double, double, double, double, double, double>(),
           py::arg("height"), py::arg("material_conductivity"),
           py::arg("cell_area"), py::arg("inner_radius"),
           py::arg("outer_radius"), py::arg("fraction_covered"))
      .def_readwrite("inner_radius",
                     &Tarcog::ISO15099::CShapedCylinderPillar::innerRadius)
      .def_readwrite("outer_radius",
                     &Tarcog::ISO15099::CShapedCylinderPillar::outerRadius)
      .def_readwrite("fraction_covered",
                     &Tarcog::ISO15099::CShapedCylinderPillar::fractionCovered);

  py::class_<Tarcog::ISO15099::CShapedCylinderPillarLayer,
             Tarcog::ISO15099::UniversalSupportPillar,
             std::shared_ptr<Tarcog::ISO15099::CShapedCylinderPillarLayer>>(
      mod, "CShapedCylinderPillarLayer")
      .def(py::init<Tarcog::ISO15099::CIGUGapLayer const &,
                    Tarcog::ISO15099::CShapedCylinderPillar const &>(),
           py::arg("gap_layer"), py::arg("cshaped_cylinder_pillar"));

  py::class_<Tarcog::ISO15099::Glass, std::shared_ptr<Tarcog::ISO15099::Glass>>(
      mod, "Glass")
      .def(py::init<double, double, double>(), py::arg("thickness"),
           py::arg("conductivity"), py::arg("emissivity"))
      .def_readwrite("thickness", &Tarcog::ISO15099::Glass::thickness)
      .def_readwrite("conductivity", &Tarcog::ISO15099::Glass::conductivity)
      .def_readwrite("emissivity", &Tarcog::ISO15099::Glass::emissivity);

  py::class_<Tarcog::ISO15099::PillarMeasurement,
             std::shared_ptr<Tarcog::ISO15099::PillarMeasurement>>(
      mod, "PillarMeasurement")
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
      mod, "MeasuredPillarLayer")
      .def(py::init<Tarcog::ISO15099::PillarMeasurement const &>(),
           py::arg("pillar"));

  py::class_<Tarcog::ISO15099::CIGUVentilatedGapLayer,
             Tarcog::ISO15099::CIGUGapLayer,
             std::shared_ptr<Tarcog::ISO15099::CIGUVentilatedGapLayer>>(
      mod, "IGUVentilatedGapLayer")
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
      .def(
          "calculate_ventilated_airflow",
          &Tarcog::ISO15099::CIGUVentilatedGapLayer::calculateVentilatedAirflow,
          py::arg("inlet_temperature"))
      .def("calculate_thermally_driven_airflow_with_adjacent_gap",
           &Tarcog::ISO15099::CIGUVentilatedGapLayer::
               calculateThermallyDrivenAirflowWithAdjacentGap,
           py::arg("adjacent_gap"))
      .def("clone", &Tarcog::ISO15099::CIGUVentilatedGapLayer::clone);

  mod.def("forced_ventilation_gap",
        Tarcog::ISO15099::Layers::forcedVentilationGap, py::arg("gap"),
        py::arg("forced_ventilation_air_speed"),
        py::arg("forced_ventilation_air_temperature"));
}
