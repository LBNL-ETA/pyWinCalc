#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

namespace py = pybind11;

// Trampoline class for Product_Data_Optical
class Py_Product_Data_Optical : public wincalc::Product_Data_Optical {
public:
  using wincalc::Product_Data_Optical::Product_Data_Optical;

  std::vector<double> wavelengths() const override {
    PYBIND11_OVERRIDE_PURE(std::vector<double>, wincalc::Product_Data_Optical,
                           wavelengths, );
  }
};

void register_product_data_bindings(py::module &mod);
