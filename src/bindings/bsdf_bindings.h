#pragma once

#include <pybind11/pybind11.h>

namespace py = pybind11;

void register_bsdf_bindings(py::module &mod);
