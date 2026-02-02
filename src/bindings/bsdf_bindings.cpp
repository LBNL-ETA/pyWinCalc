#include "bsdf_bindings.h"
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

void register_bsdf_bindings(py::module &mod) {
  py::enum_<SingleLayerOptics::BSDFDirection>(mod, "BSDFDirection",
                                              py::arithmetic())
      .value("Incoming", SingleLayerOptics::BSDFDirection::Incoming)
      .value("Outgoing", SingleLayerOptics::BSDFDirection::Outgoing);

  py::enum_<FenestrationCommon::Side>(mod, "Side", py::arithmetic())
      .value("Front", FenestrationCommon::Side::Front)
      .value("Back", FenestrationCommon::Side::Back);

  py::enum_<FenestrationCommon::PropertySurface>(mod, "PropertySurface",
                                                py::arithmetic())
      .value("T", FenestrationCommon::PropertySurface::T)
      .value("R", FenestrationCommon::PropertySurface::R);

  py::class_<FenestrationCommon::SquareMatrix>(mod, "SquareMatrix")
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

  py::class_<SingleLayerOptics::BSDFDirections>(mod, "BSDFDirections")
      .def(py::init<>())
      .def(py::init<std::vector<SingleLayerOptics::BSDFDefinition> const &>(),
           py::arg("definitions"))
      .def("lambda_vector", &SingleLayerOptics::BSDFDirections::lambdaVector)
      .def("profile_angles", &SingleLayerOptics::BSDFDirections::profileAngles)
      .def("lambda_matrix", &SingleLayerOptics::BSDFDirections::lambdaMatrix)
      .def("get_nearest_beam_index",
           &SingleLayerOptics::BSDFDirections::getNearestBeamIndex);

  py::class_<SingleLayerOptics::BSDFIntegrator>(mod, "BSDFIntegrator")
      .def(py::init<SingleLayerOptics::BSDFDirections const &>(),
           py::arg("directions"))
      .def("get_matrix", &SingleLayerOptics::BSDFIntegrator::getMatrix)
      .def("at", &SingleLayerOptics::BSDFIntegrator::at)
      .def("set_matrices", &SingleLayerOptics::BSDFIntegrator::setMatrices)
      .def(
          "direct_direct",
          py::overload_cast<FenestrationCommon::Side,
                            FenestrationCommon::PropertySurface, double, double>(
              &SingleLayerOptics::BSDFIntegrator::DirDir, py::const_))
      .def("direct_direct",
           py::overload_cast<FenestrationCommon::Side,
                             FenestrationCommon::PropertySurface, size_t>(
               &SingleLayerOptics::BSDFIntegrator::DirDir, py::const_))
      .def("direct_hemispheric",
           py::overload_cast<FenestrationCommon::Side,
                             FenestrationCommon::PropertySurface>(
               &SingleLayerOptics::BSDFIntegrator::DirHem))
      .def(
          "direct_hemispheric",
          py::overload_cast<FenestrationCommon::Side,
                            FenestrationCommon::PropertySurface, double, double>(
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
}
