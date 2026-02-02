#pragma once

#include <pybind11/pybind11.h>
#include <wincalc/wincalc.h>

namespace py = pybind11;

// Trampoline class for UniversalSupportPillar
class Py_UniversalSupportPillar
    : public Tarcog::ISO15099::UniversalSupportPillar {
public:
  using Tarcog::ISO15099::UniversalSupportPillar::UniversalSupportPillar;

protected:
  double areaOfContact() override {
    PYBIND11_OVERRIDE_PURE(double, Tarcog::ISO15099::UniversalSupportPillar,
                           areaOfContact, );
  }
};

void register_pillar_bindings(py::module &mod);
