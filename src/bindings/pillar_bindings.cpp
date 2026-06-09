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

  py::class_<Tarcog::ISO15099::SphericalPillar, Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::SphericalPillar>>(
      mod, "SphericalPillar")
      .def(py::init<double, double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"),
           py::arg("radius_of_contact"))
      .def_readwrite("radius_of_contact",
                     &Tarcog::ISO15099::SphericalPillar::radiusOfContact);

  py::class_<Tarcog::ISO15099::RectangularPillar, Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::RectangularPillar>>(
      mod, "RectangularPillar")
      .def(py::init<double, double, double, double, double>(),
           py::arg("height"), py::arg("material_conductivity"),
           py::arg("cell_area"), py::arg("length"), py::arg("width"))
      .def_readwrite("length", &Tarcog::ISO15099::RectangularPillar::length)
      .def_readwrite("width", &Tarcog::ISO15099::RectangularPillar::width);

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

  py::class_<Tarcog::ISO15099::PentagonPillar,
             Tarcog::ISO15099::PolygonalPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::PentagonPillar>>(mod, "PentagonPillar")
      .def(py::init<double, double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"), py::arg("length"));

  py::class_<Tarcog::ISO15099::HexagonPillar,
             Tarcog::ISO15099::PolygonalPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::HexagonPillar>>(mod, "HexagonPillar")
      .def(py::init<double, double, double, double>(), py::arg("height"),
           py::arg("material_conductivity"), py::arg("cell_area"), py::arg("length"));

  py::class_<Tarcog::ISO15099::LinearBearingPillar,
             Tarcog::ISO15099::PillarData,
             std::shared_ptr<Tarcog::ISO15099::LinearBearingPillar>>(
      mod, "LinearBearingPillar")
      .def(py::init<double, double, double, double, double>(),
           py::arg("height"), py::arg("material_conductivity"),
           py::arg("cell_area"), py::arg("length"), py::arg("width"))
      .def_readwrite("length", &Tarcog::ISO15099::LinearBearingPillar::length)
      .def_readwrite("width", &Tarcog::ISO15099::LinearBearingPillar::width);

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

  mod.def("forced_ventilation_gap",
        Tarcog::ISO15099::Layers::forcedVentilationGap, py::arg("gap"),
        py::arg("forced_ventilation_air_speed"),
        py::arg("forced_ventilation_air_temperature"));
}
