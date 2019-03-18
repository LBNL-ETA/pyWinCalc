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

	py::class_<OpticsParser::WLData>(m, "Wavelength_Data")
		.def_readwrite("wavelength", &OpticsParser::WLData::wavelength)
		.def_readwrite("t", &OpticsParser::WLData::T)
		.def_readwrite("rf", &OpticsParser::WLData::frontR)
		.def_readwrite("rb", &OpticsParser::WLData::backR);
		
	py::class_<OpticsParser::ProductData>(m, "Product_Data")
		.def_readwrite("product_name", &OpticsParser::ProductData::productName)
		.def_readwrite("product_type", &OpticsParser::ProductData::productType)
		.def_readwrite("nfrc_id", &OpticsParser::ProductData::nfrcid)
		.def_readwrite("thickness", &OpticsParser::ProductData::thickness)
		.def_readwrite("conductivity", &OpticsParser::ProductData::conductivity)
		.def_readwrite("tir", &OpticsParser::ProductData::IRTransmittance)
		.def_readwrite("ef", &OpticsParser::ProductData::frontEmissivity)
		.def_readwrite("eb", &OpticsParser::ProductData::backEmissivity)
		.def_readwrite("measurements", &OpticsParser::ProductData::measurements);
		

	py::enum_<Spectrum_Type>(m, "Spectrum_Type", py::arithmetic())
		.value("NONE", Spectrum_Type::NONE)
		.value("FILE", Spectrum_Type::FILE)
		.value("BLACKBODY", Spectrum_Type::BLACKBODY)
		.value("UV_ACTION", Spectrum_Type::UV_ACTION)
		.value("KROCHMANN", Spectrum_Type::KROCHMANN);
		
		
	py::class_<Spectrum>(m, "Spectrum")
		.def_readwrite("type", &Spectrum::type)
		.def_readwrite("description", &Spectrum::description)
		.def_readwrite("t", &Spectrum::t)
		.def_readwrite("a", &Spectrum::a)
		.def_readwrite("b", &Spectrum::b)
		.def_readwrite("values", &Spectrum::values);
		
	py::enum_<Wavelength_Set_Type>(m, "Wavelength_Set_Type", py::arithmetic())
		.value("FILE", Wavelength_Set_Type::FILE)
		.value("SOURCE", Wavelength_Set_Type::SOURCE)
		.value("DATA", Wavelength_Set_Type::DATA);
		
		
	py::class_<Wavelength_Set>(m, "Wavelength_Set")
		.def_readwrite("type", &Wavelength_Set::type)
		.def_readwrite("description", &Wavelength_Set::description)
		.def_readwrite("values", &Wavelength_Set::values);
	
	
	py::enum_<Wavelength_Boundary_Type>(m, "Wavelength_Boundary_Type", py::arithmetic())
		.value("NUMBER", Wavelength_Boundary_Type::NUMBER)
		.value("WAVELENGTH_SET", Wavelength_Boundary_Type::WAVELENGTH_SET);
		
		
	py::class_<Wavelength_Boundary>(m, "Wavelength_Boundary")
		.def_readwrite("type", &Wavelength_Boundary::type)
		.def_readwrite("value", &Wavelength_Boundary::value);		
		
			
	py::enum_<Integration_Rule_Type>(m, "Integration_Rule_Type", py::arithmetic())
		.value("TRAPEZOIDAL", Integration_Rule_Type::TRAPEZOIDAL)
		.value("RECTANGULAR", Integration_Rule_Type::RECTANGULAR)
		.value("TABLE", Integration_Rule_Type::TABLE);
		
		
	py::class_<Integration_Rule>(m, "Integration_Rule")
		.def_readwrite("type", &Integration_Rule::type)
		.def_readwrite("k", &Integration_Rule::k);
	
	py::enum_<Method_Type>(m, "Method_Type", py::arithmetic())
		.value("SOLAR", Method_Type::SOLAR)
		.value("PHOTOPIC", Method_Type::PHOTOPIC)
		.value("COLOR_TRISTIMX", Method_Type::COLOR_TRISTIMX)
		.value("COLOR_TRISTIMY", Method_Type::COLOR_TRISTIMY)
		.value("COLOR_TRISTIMZ", Method_Type::COLOR_TRISTIMZ)
		.value("THERMAL_IR", Method_Type::THERMAL_IR)
		.value("TUV", Method_Type::TUV)
		.value("SPF", Method_Type::SPF)
		.value("TDW", Method_Type::TDW)
		.value("TKR", Method_Type::TKR);
	
	py::class_<Method>(m, "Method")
		.def_readwrite("type", &Method::type)
		.def_readwrite("description", &Method::description)
		.def_readwrite("source_spectrum", &Method::source_spectrum)
		.def_readwrite("detector_spectrum", &Method::detector_spectrum)
		.def_readwrite("wavelength_set", &Method::wavelength_set)
		.def_readwrite("integration_rule", &Method::integration_rule)
		.def_readwrite("min_wavelength", &Method::min_wavelength)
		.def_readwrite("max_wavelength", &Method::max_wavelength);
		
		
	py::class_<Standard>(m, "Standard")
		.def_readwrite("name", &Standard::name)
		.def_readwrite("description", &Standard::description)
		.def_readwrite("methods", &Standard::methods);
	
	m.def("load_standard", py::overload_cast<std::string const&>(&load_standard), "Load standard from .std.file");
	m.def("parse_json", &OpticsParser::parseJSONString, "Load product data from json string");
	m.def("parse_json_file", &OpticsParser::parseJSONFile, "Load product data from json file");
	m.def("parse_optics_file", &OpticsParser::parseFile, "Load product data from optics file");
	m.def("calc_u", &calc_u, "Calculate U-value using optics files for measured data");
	m.def("calc_shgc", &calc_shgc, "Calculate SHGC using optics files for measured data");
	
}
