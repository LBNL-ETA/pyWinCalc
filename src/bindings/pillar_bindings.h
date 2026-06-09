#pragma once

#include <pybind11/pybind11.h>
#include <wincalc/wincalc.h>

namespace py = pybind11;

void register_pillar_bindings(py::module &mod);
