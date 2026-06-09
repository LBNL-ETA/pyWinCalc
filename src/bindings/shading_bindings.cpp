#include "shading_bindings.h"
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

void register_shading_bindings(py::module &mod) {
  py::enum_<SingleLayerOptics::DistributionMethod>(mod, "DistributionMethodType",
                                                   py::arithmetic())
      .value("UNIFORM_DIFFUSE",
             SingleLayerOptics::DistributionMethod::UniformDiffuse)
      .value("DIRECTIONAL_DIFFUSE",
             SingleLayerOptics::DistributionMethod::DirectionalDiffuse);

  py::class_<wincalc::Venetian_Geometry,
             std::shared_ptr<wincalc::Venetian_Geometry>>(mod, "VenetianGeometry")
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
      mod, "ProductDataOpticalVenetian")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical> const &,
                    wincalc::Venetian_Geometry const &>(),
           py::arg("product_data_optical"), py::arg("geometry"))
      .def_readwrite("geometry",
                     &wincalc::Product_Data_Optical_Venetian::geometry);

  py::class_<wincalc::Woven_Geometry, std::shared_ptr<wincalc::Woven_Geometry>>(
      mod, "WovenGeometry")
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
      mod, "ProductDataOpticalWovenShade")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical> const &,
                    wincalc::Woven_Geometry const &>(),
           py::arg("material_product_data_optical"), py::arg("geometry"))
      .def_readwrite("geometry",
                     &wincalc::Product_Data_Optical_Woven_Shade::geometry);

  py::class_<wincalc::Perforated_Geometry,
             std::shared_ptr<wincalc::Perforated_Geometry>>
      perforated_geometry(mod, "PerforatedGeometry");

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
      mod, "ProductDataOpticalPerforatedScreen")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical> const &,
                    wincalc::Perforated_Geometry const &>(),
           py::arg("material_product_data_optical"), py::arg("geometry"))
      .def_readwrite(
          "geometry",
          &wincalc::Product_Data_Optical_Perforated_Screen::geometry);

  py::class_<wincalc::Product_Data_Optical_Thermal>(
      mod, "ProductDataOpticalAndThermal")
      .def(py::init<std::shared_ptr<wincalc::Product_Data_Optical>,
                    std::shared_ptr<wincalc::Product_Data_Thermal>>(),
           py::arg("product_data_optical"), py::arg("product_data_thermal"))
      .def_readwrite("optical_data",
                     &wincalc::Product_Data_Optical_Thermal::optical_data)
      .def_readwrite("thermal_data",
                     &wincalc::Product_Data_Optical_Thermal::thermal_data);
}
