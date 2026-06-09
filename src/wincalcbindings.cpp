#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <wincalc/wincalc.h>

#include "bindings/gas_bindings.h"
#include "bindings/pillar_bindings.h"
#include "bindings/optical_parser_bindings.h"
#include "bindings/standards_bindings.h"
#include "bindings/product_data_bindings.h"
#include "bindings/shading_bindings.h"
#include "bindings/glazing_system_bindings.h"
#include "bindings/thmx_bindings.h"
#include "bindings/cma_bindings.h"
#include "bindings/bsdf_bindings.h"
#include "bindings/layers_bindings.h"

namespace py = pybind11;

PYBIND11_MODULE(wincalcbindings, mod) {
  mod.doc() = "Python bindings for WinCalc";

  // Register all bindings from separate modules
  register_gas_bindings(mod);
  register_pillar_bindings(mod);
  register_optical_parser_bindings(mod);
  register_standards_bindings(mod);
  register_product_data_bindings(mod);
  register_shading_bindings(mod);
  register_glazing_system_bindings(mod);
  register_thmx_bindings(mod);
  register_cma_bindings(mod);
  register_bsdf_bindings(mod);
  register_layers_bindings(mod);
}
