#include "optical_parser_bindings.h"
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

void register_optical_parser_bindings(py::module &mod) {
  py::class_<OpticsParser::MeasurementComponent>(mod,
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

  py::class_<OpticsParser::PVWavelengthData>(mod, "PVWavelengthData")
      .def(py::init<double, double>(), py::arg("eqe_front"),
           py::arg("eqe_back"))
      .def_readwrite("eqq_front", &OpticsParser::PVWavelengthData::eqef)
      .def_readwrite("eqe_back", &OpticsParser::PVWavelengthData::eqeb);

  py::class_<OpticsParser::WLData>(mod, "WavelengthData")
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
             std::shared_ptr<OpticsParser::ProductGeometry>>(mod,
                                                             "ProductGeometry");

  py::class_<OpticsParser::VenetianGeometry, OpticsParser::ProductGeometry,
             std::shared_ptr<OpticsParser::VenetianGeometry>>(
      mod, "ParsedVenetianGeometry")
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
      mod, "ParsedWovenGeometry")
      .def(py::init<double, double, double>())
      .def_readwrite("thread_diameter",
                     &OpticsParser::WovenGeometry::threadDiameter)
      .def_readwrite("thread_spacing",
                     &OpticsParser::WovenGeometry::threadSpacing)
      .def_readwrite("shade_thickness",
                     &OpticsParser::WovenGeometry::shadeThickness);

  py::class_<OpticsParser::PerforatedGeometry, OpticsParser::ProductGeometry,
             std::shared_ptr<OpticsParser::PerforatedGeometry>>(
      mod, "ParsedPerforatedGeometry")
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

  py::class_<OpticsParser::BSDF>(mod, "BSDF")
      .def_readwrite("data", &OpticsParser::BSDF::data)
      .def_readwrite("row_angle_basis_name",
                     &OpticsParser::BSDF::rowAngleBasisName)
      .def_readwrite("column_angle_basis_name",
                     &OpticsParser::BSDF::columnAngleBasisName);

  py::class_<OpticsParser::WavelengthBSDFs>(mod, "WavelengthBSDFs")
      .def_readwrite("transmittance_front", &OpticsParser::WavelengthBSDFs::tf)
      .def_readwrite("transmittance_back", &OpticsParser::WavelengthBSDFs::tb)
      .def_readwrite("reflectance_front", &OpticsParser::WavelengthBSDFs::rf)
      .def_readwrite("reflectance_back", &OpticsParser::WavelengthBSDFs::rb);

  py::class_<OpticsParser::DualBandBSDF>(mod, "DualBandBSDF")
      .def_readwrite("solar", &OpticsParser::DualBandBSDF::solar)
      .def_readwrite("visible", &OpticsParser::DualBandBSDF::visible);

  py::class_<OpticsParser::PVPowerProperty>(mod, "PVPowerProperty")
      .def(py::init<double, double, double>(), py::arg("jsc"), py::arg("voc"),
           py::arg("ff"))
      .def_readwrite("jsc", &OpticsParser::PVPowerProperty::jsc)
      .def_readwrite("voc", &OpticsParser::PVPowerProperty::voc)
      .def_readwrite("ff", &OpticsParser::PVPowerProperty::ff);

  py::class_<OpticsParser::ProductData,
             std::shared_ptr<OpticsParser::ProductData>>(mod, "ProductData")
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
      .def_readwrite("material_definition", &OpticsParser::ProductData::materialDefinition)
      .def_readwrite("geometry", &OpticsParser::ProductData::geometry);
}
