#include <pybind11/pybind11.h>

#include <calc_from_disk.h>

namespace py = pybind11;

using namespace pybind11::literals;

PYBIND11_MODULE(pywincalc, m)
{
	m.doc() = "Python bindings for WinCalc";
	
	py::class_<Gap_Data>(m, "Gap_Data")
		.def_readwrite("name", &Gap_Data::name)
		.def_readwrite("thickness", &Gap_Data::thickness);
	
	m.def("calc_u", &calc_u, "Calculate U-value");
	m.def("calc_shgc", &calc_shgc, "Calculate SHGC");
}
