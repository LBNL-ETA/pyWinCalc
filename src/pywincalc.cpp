#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <wincalc/wincalc.h>

namespace py = pybind11;

using namespace pybind11::literals;

PYBIND11_MODULE(pywincalc, m)
{
	m.doc() = "Python bindings for WinCalc";

	py::enum_<Gas_Type>(m, "Gas_Type", py::arithmetic())
		.value("AIR", Gas_Type::AIR)
		.value("ARGON", Gas_Type::ARGON)
		.value("KRYPTON", Gas_Type::KRYPTON)
		.value("XENON", Gas_Type::XENON);
	
	py::class_<Gap_Data>(m, "Gap_Data")
		.def(py::init<Gas_Type const&, double>())
		.def_readwrite("gas", &Gap_Data::gas)
		.def_readwrite("thickness", &Gap_Data::thickness);
	
	py::class_<Thermal_Result>(m, "Thermal_Result")
		.def(py::init<double, double, std::vector<double>>())
		.def_readwrite("result", &Thermal_Result::result)	
		.def_readwrite("t_sol", &Thermal_Result::t_sol)
		.def_readwrite("layer_solar_absorptances", &Thermal_Result::layer_solar_absorptances);


	m.def("calc_u_optics_file", &calc_u_optics_file, "Calculate U-value using optics files for measured data");
	m.def("calc_shgc_optics_file", &calc_shgc_optics_file, "Calculate SHGC using optics files for measured data");
	m.def("calc_u_json_data", &calc_u_json_data, "Calculate U-value using json for measured data");
	m.def("calc_shgc_json_data", &calc_shgc_json_data, "Calculate SHGC using json for measured data");
}
