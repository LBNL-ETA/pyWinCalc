

Berkeley Lab WINDOW Calc Engine (CalcEngine) Copyright (c) 2016 - 2020, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Dept. of Energy).  All rights reserved.

If you have questions about your rights to use or distribute this software, please contact Berkeley Lab's Innovation & Partnerships Office at IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department of Energy and the U.S. Government consequently retains certain rights.  As such, the U.S. Government has been granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the Software to reproduce, distribute copies to the public, prepare derivative works, and perform publicly and display publicly, and to permit other to do so.


# pywincalc

This module provides a simplified method for calculating various thermal and optical properties of glazing systems.

Version 2 has substantially more features but the interface has also changed as a result.  For help updating existing code see [Migrating from version 1](#Migrating-from-version-1)

# Table of contents
1. [Requirements](#Requirements)
	1. [Windows](#Windows)
	2. [Linux/Mac](#Linux/Mac)
	3. [Building from source](#Building-from-source)
2. [Installation](#Install)
	1. [From PyPi](#From-PyPi)
	2. [Building from source](#Building-from-source)
		1. [Building From Source On Windows](#Building-from-source-on-windows)
3. [Use](#Use)
	1. [Overview](#Overview)
		1. [Optical Calculations](#Optical-Calculations)
		2. [Thermal Calculations](#Thermal-Calculations) 
	2. [Units](#Units)
	3. [Optical Standards](#Optical-Standards)
		1. [Optical Standard File](#Optical-Standard-File) 
	4. [Solid Layers](#Solid-Layers)
		1. [Supported Solid Layer Types](#Supported-solid-layer-types)
	5. [Gaps](#Gaps)
	6. [BSDF (Bidirectional scattering distribution function) Calculations](#BSDF-Calculations)
	7. [Example Use Cases](#Example-Use-Cases)
		1. [Examples](#Examples) 
	8. [pywincalc objects](#pywincalc-objects)
		1. [GlazingSystem](#GlazingSystem)
		2. [Optical Results](#Optical-Results)
			1. [Matrix Optical Results](#Matrix-Optical-Results)
			2. [Color Results](#Color-Results)
			3. [Thermal IR Results](#Thermal-IR-Results)
		3. [Environmental Conditions](#Environmental-Conditions)
		4. [Gases](#Gases)
			1. [Predefined gases](#Predefined-gases)
			2. [Custom gases](#Custom-gases)
			3. [Gas mixtures](#Gas-mixtures)
		5. [Pydoc Class Documentation](#Pydoc-Class-Documentation)
	9. [CMA](#CMA)
		1. [Context and Background](#Context-and-Background)
		2. [THERM](#THERM)
		3. [CMA Calculations](#CMA-Calculations)
		4. [CMA Examples](#CMA-Examples)
	10. [Migrating from version 1](#Migrating-from-version-1)
		1.	[Migrating Glazing_System](#Migrating-Glazing_System)
		2.	[Migrating Results](#Migrating-Results)
			1. [Migrating Optical Results](#Migrating-Optical-Results)
			2. [Migrating Thermal Results](#Migrating-Thermal-Results)
	11. [IGSDB v2 JSON format](#IGSDB-v2-JSON-format) 
	12. [Changelog](#Changelog) 


### Requirements

#### Windows
Windows requires a version of the Microsoft C++ redistributable >= the version of Visual Studio used to build the library.  Currently the wheels on pypi are generated using Visual Studio 16 2019.  However in general installing the latest version of the C++ runtime for your architecture should always be sufficient.  Installation packages are available from Microsoft here: https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist

#### Linux/Mac
The pre-built wheels provided at pypi should work on any x86/x64 version of Linux or Mac that supports at least C++17.

#### Building from source
[Git](https://git-scm.com/)

[CMake](https://cmake.org/) - Not required for installing from wheel files on Windows.

## Install

### From PyPi
Once the requirements have been installed this can be installed with pip by doing

` pip install pywincalc `

### Building from source
Once the requirements have been installed this can be installed with pip by doing

` pip install git+https://github.com/LBNL-ETA/pyWinCalc.git `

#### Building from source on windows
Building Python packages from source on Windows is more complicated than Mac/Linux.  First the correct C++ compiler first needs to be installed as well as CMake.  See https://wiki.python.org/moin/WindowsCompilers for more information about C++ compilers for Python packages on Windows.  Once that has been installed pyWinCalc can be built following the build from source steps.

## Use

### Overview
We recognize that there is a fair amount of complexity in the functionality provided by this library.  To attempt to mitigate this somewhat we have provided a selection of [examples](#Examples) that we hope cover all potential use cases between them.  It may be beneficial to begin by looking at whichever example(s) seem to cover your particular use case and then consulting the rest of this and other documentation.

For example, if you are interested in exploring the effect various gas fills have on glazing systems made from combinations of existing commercial glass products contained in the [IGSDB](igsdb.lbl.gov) you could look at the [gases](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/gases.py) example and the  [igsdb_double_clear_glass.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_double_clear_glass.py ) example

Most of the functionality provided by pywincalc is based around a glazing system.  That is the solid and gap layers that make up a window not including frames or dividers.  One exception is CMA calculations using frames are also provided, see the [CMA](#CMA) section for more information about the CMA process and calculations.

For glazing systems calculations can be grouped into two broad categories:  optical and thermal calculations.

In the context of this program `optical` and `thermal` refer to the algorithms used to perform the calculations and not the part of the spectrum used in the calculations.  E.g. the calculation for the transmittance of the infrared spectrum is considered an optical calculation here not a thermal calculation.

#### Optical Calculations
Optical calculations are based on optical standards which are defined by `.std` files and are not affected by environmental conditions.  The optical standards define various methods that can be used to generate [optical results](#Optical-Results).

Since optical standards are free to define which methods are provided as well as the names of the methods `pywincalc`provides a general way of calculating optical results via a `optical_method_results` method in the [GlazingSystem](#GlazingSystem) class.

There are a few important exceptions to this.  See the section on [optical calculation details](#Optical-Calculation-Details) for more details.

#### Thermal Calculations
Currently only [ISO 15099](https://www.iso.org/standard/26425.html) thermal calculations are supported.

Thermal calculations depend on the [environmental conditions](#Environmental-Conditions) and, in some cases, optical results calculated using specific methods.  E.g. the [SHGC](https://www.energy.gov/energysaver/energy-performance-ratings-windows-doors-and-skylights) calculations can depend on optical results calculated using the `SOLAR`method from the optical standard.

It is important to note that it is possible to calculate thermal results using an optical standard that does not necessarily conform to the ISO 15099 standard so care should be used when selecting which optical standard is used for thermal calculations.

### Units

With the exception of wavelength values which are in microns all units are values are in SI base units.  However for documentation some units are expressed as more common derived SI units when the values are equivalent.  For example:
- wavelengths: microns (m<sup>-6</sup>)
- conductivity: w⋅m<sup>-1</sup>⋅K<sup>-1</sup> because this is more common than m⋅kg⋅s<sup>−3</sup>⋅K<sup>−1</sup> and 1 w⋅m<sup>-1</sup>⋅K<sup>-1</sup> = 1 m⋅kg⋅s<sup>−3</sup>⋅K<sup>−1</sup>
- temperature: Kelvin
- pressure:  pascals
- thickness: meters
- width/height: meters
- etc...

### Optical Standards
Calculations can be performed using predefined optical standards in the form that is expected by [WINDOW](https://windows.lbl.gov/software/window).  The path to the base standard files is all that needs to be passed.  Any other files referenced by the standard file must be in the same directory (or specified as a relative directory from within the standard file).

Custom standards can be created by creating a new set of files following the same format.

#### Optical Standard File
Optical standards used by pywincalc are defined using a standards file and usually several related files referenced by the standards file.

For an example standards file see [W5 NFRC 2003.std](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/standards/W5_NFRC_2003.std)

Each standards file contains sections that define the optical methods provided by the standard.  In the W5 NFRC 2003 standard file the first method defined looks like this:

```
Name : SOLAR
Description : NFRC 300-2003 Solar
Source Spectrum : ASTM E891 Table 1 Direct AM1_5.ssp
Detector Spectrum : None
Wavelength Set : Source
Integration Rule : Trapezoidal
Minimum Wavelength : 0.3
Maximum Wavelength : 2.5
```
The most important part for using pywincalc is the name of the method.  Since optical standard files can set anything for a name pywincalc has one generic method for calculating optical results and two other methods to handle exceptions to the generic rule:  THERMAL IR and color calculations.  See the section on [optical calculation details](#Optical-Calculations-Details) for more on those two cases.

The choice of standards file affects what can be calculated because not all files implement all methods.  For example the [prEN_410.std](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/standards/prEN_410.std) file does not contain a definition of the THERMAL IR method.

Calculations that rely on specific methods will not work if the standard does not provide them.  Since the prEN_410.std files does not contain a definition for the thermal IR method the `pywincalc.calc_thermal_ir` function will not work. 

### Solid layers
Solid layers define the glazing or shading products that make up a glazing system.  The methods for creating solid layers currently supported are:
 
- From paths to measured data files as exported by [Optics](https://windows.lbl.gov/software/optics).  See [single_clear.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/single_clear.py) and [triple_clear.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/triple_clear.py) in the examples directory.
- From json returned by a request for a shading layer to the [IGSDB](igsdb.lbl.gov).  See [igsdb_exterior_shade_on_clear_glass.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_exterior_shade_on_clear_glass.py) in the examples directory.
- From a combination of json returned by a request for a material from the [IGSDB](igsdb.lbl.gov) and user-defined geometry.  See [igsdb_custom_perforated.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_custom_perforated.py), [igsdb_custom_venetian.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_custom_venetian.py), and [igsdb_custom_woven.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_custom_woven.py) in the examples directory.
- Shading layers that are represented by discrete BSDFs are currently a special case in the [IGSDB](igsdb.lbl.gov).  See [igsdb_interior_bsdf.py] (https://github.com/LBNL-ETA/pyWinCalc/blob/bsdf_input/examples/igsdb_interior_bsdf.py)
- From measured wavelength data from some other source and user-defined geometry.  See [custom_perforated.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/custom_perforated.py) in the examples directory.

#### Supported solid layer types
The following types of solid layers are currently supported:
- Glazings that are represented as one set of measured wavelength data.  Products that require deconstruction like some laminates and coated glass are not yet supported.
- Venetian blinds
- Woven shades
- Perforated screens
- BSDF shades

### Gaps
For systems with more than one solid layer each solid layer must be separated by a gap.  The methods for creating gaps currently supported are:

- From a selection of predefined gases.  Current predefined gases are:  Air, Argon, Krypton, Xeon.
- From a mixture of predefined gases.
- From creating a custom gas by providing molecular weight, specific heat ratio, and coefficients for specific heat at constant pressure (Cp), thermal conductivity, and viscosity.
- From a mixture of custom gases.

For examples of each see [gases.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/gases.py) in the examples directory.

### BSDF Calculations

Shading products require BSDF calculations while glazings do not.  If any layer passed to a glazing system is a shading layer the glazing system will also require a BSDF hemisphere.  For examples see any of the igsdb examples or [custom_perforated.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/custom_perforated.py) in the examples directory.

However it is possible to use BSDF calculations for a system with no shading products.  To do so pass a BSDF hemisphere as in the examples with shading systems.

If a glazing system is given a BSDF hemisphere as a parameter it will always use that for optical calculations.

### Example use cases

Since there are several ways of creating and combining layers plus different calculation options example scripts are provided in the [/example](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/) directory.  

These scripts use optical standards provided in the [/examples/standards](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/standards) directory.  Some scripts use measured data for example products provided in the [/examples/products](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/products) directory.

A minimum example might look like this
```
import pywincalc

optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

width = 1.0
height = 1.0

clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

solid_layers = [clear_3]
gaps = []

glazing_system = pywincalc.GlazingSystem(solid_layers, gaps, optical_standard, width, height)
print("Single Layer U-value: {u}".format(u=glazing_system.u()))
```

Please see the following examples which contain more information.

The examples names have the following meanings:
1. `igsdb` means the example downloads data from the [IGSDB](http://igsdb.lbl.gov)
2. `custom` means the example does not use a completely defined existing product.  This could be anything from using a pre-defined material to make a shade to using user-defined measured spectral data.

NOTE:  The igsdb examples require the python requests library and an API token for igsdb.lbl.gov.  An API token can be obtained by creating an account there.  See https://igsdb.lbl.gov/about/ for more information on creating an account.
#### Examples
- [minimum_example.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/minimum_example.py) The minimum example shown above.  Calculates the U-value for a single piece of generic clear glass.
- [single_clear.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/single_clear.py): Creates a single layer glazing system from a sample optics file.  Shows all thermal results, all optical results for a single optical method and some optical results from a second optical method.
- [triple_clear.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/triple_clear.py):  Creates a triple layer glazing system from sample optics files.  Creates two gaps, one with a single gas and one with a gas mixture.  Shows another example of optical results for each layer.
- [igsdb_double_clear_glass.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_double_clear_glass.py ) Creates a double layer glazing system from products defined in the [IGSDB](http://igsdb.lbl.gov).
- [igsdb_exterior perforated_shade_on_clear_glass.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_exterior_perforated_shade_on_clear_glass.py):  Creates a double-layer glazing system with an exterior perforated screen from products defined in the [IGSDB](http://igsdb.lbl.gov).  
- [igsdb_exterior_venetian blind_on_clear_glass.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_exterior_venetian_blind_on_clear_glass.py):  Creates a double-layer glazing systems with  an exterior Venetian blind from products defined in the [IGSDB](http://igsdb.lbl.gov). 
- [igsdb_custom_perforated.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_custom_perforated.py) Creates a double layer glazing system with an exterior perforated screen.  The perforated screen uses a material from the [IGSDB](http://igsdb.lbl.gov) and a user-defined geometry describing the perforations.  The glass layer uses data from the [IGSDB](http://igsdb.lbl.gov)
- [igsdb_custom_venetian.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_custom_venetian.py).  Creates a double layer glazing system with an exterior venetian blind.  The venetian blind uses a material from the [IGSDB](http://igsdb.lbl.gov) and a user-defined geometry describing the slats.  Also includes an example of how to change the distribution method used for calculating optical results for the shade.  The glass layer uses data from the [IGSDB](http://igsdb.lbl.gov)
- [igsdb_custom_vertical_venetian.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_custom_vertical_venetian.py).  Creates a double layer glazing system with an exterior vertical louver.  The vertical louver uses a material from the [IGSDB](http://igsdb.lbl.gov) and a user-defined geometry describing the slats.  Also includes an example of how to change the distribution method used for calculating optical results for the shade.  The glass layer uses data from the [IGSDB](http://igsdb.lbl.gov)
- [igsdb_custom_woven.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_custom_woven.py) Creates a double layer glazing system with an exterior woven shade.  The woven shade uses a material from the [IGSDB](http://igsdb.lbl.gov) and a user-defined geometry describing the thread layout.  The glass layer uses data from the [IGSDB](http://igsdb.lbl.gov)
- [custom_perforated.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/custom_perforated.py) Creates a double layer glazing system with an exterior perforated screen.  Shows an example of getting measured data from somewhere other than either the [IGSDB](http://igsdb.lbl.gov) or optics file.
- [gases.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/gases.py) Creates gases and gas mixtures from predefined gas types and custom gases created from gas properties.
- [deflection.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/deflection.py) Shows how to set and enable deflection properties and which deflection results are available.
- [cma_single_vision.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/cma_single_vision.py) Shows how to do a CMA calculation for a single-vision window and which results are available for CMA calculations.
- [cma_double_vision_horizontal.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/cma_double_vision_horizontal.py) Shows how to do a CMA calculation for a horizontal double-vision window and which results are available for CMA calculations.
- [cma_double_vision_vertical.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/cma_double_vision_vertical.py) Shows how to do a CMA calculation for a vertical double-vision window and which results are available for CMA calculations.
- [thermal_ir.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/thermal_ir.py) Shows how to calculate optical results for the thermal IR method.  Note that currently only calculations for a single solid layer are supported and these only have diffuse-diffuse transmittances and hemispherical emissivities.
- [custom_environmental_conditions.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/custom_environmental_conditions.py) Shows how to create custom environmental conditions.
- [pv_single_layer.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/pv_single_layer.py) Shows how to create a system with a single layer that has integrated PV data.  For information on creating a IGSDB v2 json file with PV data see the provided [generic_pv.json](https://github.com/LBNL-ETA/pyWinCalc/tree/main/examples/products/generic_pv.json) file and the [IGSDB v2 JSON format](#IGSDB-v2-JSON-format) section below.
#### Non-example files
These are files in the example folder that provide some functionality but are not calculation examples.
- [igsdb_interaction.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/igsdb_interaction.py) Encapsulates some basic interaction with the [IGSDB](http://igsdb.lbl.gov)
- [results_printer.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/results_printer.py) Contains some methods for displaying all available results.  The [single_clear.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/single_clear.py) example contains notes on how to calculate and access the various results.  To simplify the other examples the code to display the results has been encapsulated in this file.

If there is something you are trying to calculate that does not exist as an example yet please contact us.

### pywincalc objects

#### GlazingSystem
- Constructor:  
    - Requires parameters:  
        - optical_standard
        - solid_layers
    - Optional parameters:
        - gap_layers  Defaults to no gap layers.  If more than one solid layer is provided then len(solid_layers) - 1 gap_layers must be provided
        - width_meters  Defaults to 1.0 meters
        - height_meters  Defaults to 1.0 meters
        - environment  Defaults to NFRC U environment
        - bsdf_hemisphere  Defaults to no BSDF hemisphere. Required if any solid layers require BSDF calculations.
        - spectral_data_wavelength_range_method  Defaults to full wavelength range.
        - number_visible_bands  Defaults to 5.  Not used if spectral_data_wavelength_range_method is set to full. 
        - number_solar_bands  Defaults to 10.  Not used if spectral_data_wavelength_range_method is set to full. 
- Available calculation methods.
    - Thermal
        - u(theta=0, phi=0) Calculates the U-value for the system at incidence angle theta and phi
        - shgc(theta=0, phi=0) Calculates the SHGC value for the system at incidence angle theta and phi
        - layer_temperatures(TarcogSystemType, theta=0, phi=0)  Calculates the temperature at each layer based on the given TarcogSystemType (U or SHGC) at theta and phi incidence angle.  Returns a list of temperatures for each solid layer in K.  Note that the TarcogSystemType is specifying the calculation methodology for this calculation which is independed of the environment used to construct the GlazingSystem.  When U system is passed as a parameter the layer temperatures will be calculated for the given environments without taking solar radiation into account.  When SHGC system is passed as a parameter solar radiation is taken into account.
        - solid_layers_effective_conductivities(TarcogSystemType, theta=0, phi=0)  Calculates the effective conductivity for each solid layer based on the given TarcogSystemType (U or SHGC) at theta and phi incidence angle.  Returns a list of effective conductivities for each solid layer.  See note in layer_temperatures for the meaning of the TarcogSystemType parameter.
        - gap_layers_effective_conductivities(TarcogSystemType, theta=0, phi=0)  Calculates the effective conductivity for each gap layer based on the given TarcogSystemType (U or SHGC) at theta and phi incidence angle.  Returns a list of effective conductivities for each gap layer.  See note in layer_temperatures for the meaning of the TarcogSystemType parameter.
        - system_effective_conductivities(TarcogSystemType, theta=0, phi=0)  Calculates the effective conductivity for the entire system based on the given TarcogSystemType (U or SHGC) at theta and phi incidence angle.  Returns a single value.  See note in layer_temperatures for the meaning of the TarcogSystemType parameter.
    - Optical
        - optical_method_results(method_name, theta=0, phi=0)  Calculates all optical results for the method in the optical standard with the name of `method_name` at theta and phi incidence angle.  Returns an `OpticalResults` object containing all of the results.  See [Optical Results](Optical-Results) section below.
        - color(theta=0, phi=0) Calculates color results and theta and phi incidence angle.  Returns a ColorResults object.  See the Color Results section in Optical Results below.

##### Optical Calculations Details
Most optical results can be calculated by passing the name of the optical method to the `optical_method_results`method of the `GlazingSystem`.  However there are two exceptions:

1. Colors.  Color calculations are calculated using three tristimulus optical methods, not one.  In the [NFRC standard](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/standards/W5_NFRC_2003.std) provided these three methods are named `COLOR_TRISTIMX`, `COLOR_TRISTIMY`, and `COLOR_TRISTIMZ`.  While it is possible to calculate results for each of these methods individually the results will not give accurate color information.
2. `THERMAL IR`method.  Thermal IR optical results are only available for a single layer and cannot be calculated for a system.  These results should be calculated using the `calc_thermal_ir`function.

#### Optical Results
There are two types of optical results available: those calculated from any method that is not a color method and color results.  Color calculations are a special case and therefore have their own method used to calculate them and their own results structure.  The differences between color results and other optical results is discussed in the section below.

An `OpticalResults` object has two parts: `system_results` and `layer_results`.

`system_results` apply to the system as a whole and are objects nested as follows:  `system_results.side.transmission_type.flux_type` With the following options available for each

- side:  `front`, `back`
- transmission_type: `transmittance`, `reflectance`
- flux_type: `direct_direct`, `direct_diffuse`, `direct_hemispherical`, `diffuse_diffuse`, `matrix`
    - Note:  `direct_hemisperical` = `direct_direct` + `direct_diffuse`

E.g. the direct-diffuse front reflectance is `system_results.front.reflectance.direct_diffuse`

`layer_results` contain a list of results corresponding to each solid layer.  Results for both sides are provided for each layer.  Currently the only supported result per side is absorptance.  Absorptance is available for both direct and diffuse cases.   

As of version 2.4.0 absorptance results are available as heat and electricity.  Electricity absoprtance is only non-zero for layers with PV data.  The following results are available for each side of each layer:
`total_direct, total_diffuse, heat_direct, heat_diffuse, electricity_direct, electricity_diffuse, direct, diffuse` NOTE: direct and diffuse are deprecated and equal to total_direct and total_diffuse.  

E.g the diffuse back absorptance for the first solid layer is `layer_results[0].back.absorptance.diffuse`

##### Matrix Optical Results
Matrix results are only available for systems that have a BSDF basis.  See the section on [BSDF Calculations](#BSDF-Calculations) for information on how to create and use a BSDF basis.  For systems with a BSDF basis the matrix result is a square matrix of the same size as the number of patches in the basis.  

##### Color Results
The structure of color results is similar to, but different from, the structure of other optical results.  There are two main differences.  First individual layer results are not yet supported for colors.  And second instead of one value at each flux type (direct-direct, direct-diffuse, etc...) color results have RGB, Lab, and Trichromatic values.  Those represent the same result mapped into three common color spaces for convenience.  

So while for other results `results.front.transmittance.direct_direct` would return a single value for colors that returns an object that contains RGB, Lab, and Trichromatic objects.  E.g. to get the RGB blue value from a color result this is required: `results.front.transmittance.direct_direct.rgb.B`

##### Thermal IR Results
Thermal IR results are only available for a single layer and only have four results available.  They are:
1. `transmittance_front_diffuse_diffuse`
2. `transmittance_back_diffuse_diffuse`
3. `emissivity_front_hemispheric`
4. `emissivity_back_hemispheric`

#### Environmental Conditions
An environment consists of two parts:  the inside and outside environment.  The exterior environment will be used as the environment before the first solid layer in the system and the interior environment will be used after the last solid layer in the system.  Each contains the same fields.  To use custom values for thermal calculations create an Environments object from inside and outside Environment objects.

Environment fields:
- air_temperature
- pressure
- convection_coefficient
- coefficient_model
- radiation_temperature
- emissivity
- air_speed
- air_direction
- direct_solar_radiation

Pre-constructed NFRC U and SHGC environments are available by calling `pywincalc.nfrc_u_environments()` and `pywincalc.nfrc_shgc_environments()`

#### Gases
There are several options for gases.  Gases can be created either from pre-defined gases (e.g. Air, Argon, etc...), by supplying physical parameters to create arbitrary custom gases, or by mixtures containing either predefined or custom gases.

##### Predefined gases
Gases can be created from a `PredefinedGasType`.  Current supported predefined gas types are: AIR, ARGON, KRYPTON, and XENON.

A gap layer can be created from a predefined gas type like so:
```
gap_1 = pywincalc.Gap(pywincalc.PredefinedGasType.AIR, .0127)  # .0127 is gap thickness in meters
```

##### Custom gases
A `CustomGasData` object can be created by providing the following information:
- Name
- molecular_weight
- specific_heat_ratio
- Cp
   - Expressed as a GasCoefficients object with A, B, and C fields.
- thermal_conductivity
    - Expressed as a GasCoefficients object with A, B, and C fields.
- viscosity
   - Expressed as a GasCoefficients object with A, B, and C fields.

See [gases.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/gases.py) for more on creating custom gases.

##### Gas mixtures
Gas mixtures can be created from custom and predefined gases by specifying the percentage of each in the mixtures.  E,g,

```
# The following creates a gas that is 80% sulfur hexafluoride, 15% Argonm and 5% Air
gap_4_component_1 = pywincalc.CustomGasMixtureComponent(sulfur_hexafluoride, 0.8)
gap_4_component_2 = pywincalc.PredefinedGasMixtureComponent(pywincalc.PredefinedGasType.ARGON, .15)
gap_4_component_3 = pywincalc.PredefinedGasMixtureComponent(pywincalc.PredefinedGasType.AIR, .05)
gap_4 = pywincalc.Gap([gap_4_component_1, gap_4_component_2, gap_4_component_3], .025)  # 2.5mm thick gap
```

See [gases.py](https://github.com/LBNL-ETA/pyWinCalc/blob/main/examples/gases.py) for more on creating gas mixtures.

#### Pydoc Class Documentation
Complete class documentation generated by pydoc can be found here: https://github.com/LBNL-ETA/pyWinCalc/blob/main/pywincalc_class_documentation.html

## CMA

### Context and Background

See this paper for context and background about the CMA modeling process: [Component Modeling Methodology for Predicting Thermal Performance of Non-Residential Fenestration Systems](https://github.com/LBNL-ETA/pyWinCalc/blob/CMA/docs/Component_Modeling_Methodology.pdf)

### THERM

In THERM, when inserting a glazing system, on the first Glazing Systems dialog box, instead of clicking the "Import" button, click the "NFRC CMA..." button. This will take you to a special "Insert Glazing System" dialog box specifically for the CMA calculation. The THMX file created when this THERM file is saved has the required CMA information in it for use with the pyWinCalc code.

### CMA Calculations

The CMA calculation process can be summarized with the following steps:
1. Create frames and spacer thmx CMA files in THERM.  See previous section for the correct way to do this.
2. Parse the thmx files using pywincalc.parse_thmx_file
3. Get the effective conductivity for the spacer using pywincalc.get_spacer_keff
4. Create a CMA window.  Currently three configurations are supported: pywincalc.get_cma_window_single_vision, pywincalc.get_cma_window_double_vision_vertical, and pywincalc.get_cma_window_double_vision_horizontal.
5. Get CMA results by calling pywincalc.calc_cma with the CMA window from step 4, the glazing system U, SHGC, and visibile transmittance, and the spacer keff from step 3.  Note:  The glazing system values can be calculated using a pywincalc.GlazingSystem (see glazing system examples above) or from other sources.  However the dimensions of the glazing system used calculate those results should match the dimensions that will be used in the CMA window.  pywincalc.CMAWindow provides a glazing_system_dimensions function that will return the appropriate glazing system size.  See the cma_single_vision_igsdb_parametric.py example.

### CMA Examples
The examples folder has the following examples:

- [cma_single_vision.py](https://github.com/LBNL-ETA/pyWinCalc/blob/CMA/examples/cma_single_vision.py): Perform a CMA calculation for a single vision window using sample THERM frames and spacer thmx files and precalculated glazing system results.
- [cma_double_vision_vertical.py](https://github.com/LBNL-ETA/pyWinCalc/blob/CMA/examples/cma_double_vision_vertical.py): Perform a CMA calculation for a double vision vertical window using sample THERM frames and spacer thmx files and precalculated glazing system results.
- [cma_double_vision_horizontal.py](https://github.com/LBNL-ETA/pyWinCalc/blob/CMA/examples/cma_double_vision_horizontal.py): Perform a CMA calculation for a double vision horizontal using sample THERM frames and spacer thmx files and precalculated glazing system results.
- [cma_single_vision_igsdb_parametric.py](https://github.com/LBNL-ETA/pyWinCalc/blob/CMA/examples/cma_double_vision_horizontal.py): An example of how a parametric calculation might be performed.  Makes all possible double layer glazing systems from IGSDB glazing records with the inner layer set to generic clear 3mm glass.  Runs CMA calculations on them using sample frames and spacers.  Reports the systems with the highest and lowest U, SHGC, and visible transmittance.

## Migrating from version 1

There were several interface changes that resulted from the new functionality.  These changes are mostly contained in two places:  The GlazingSystem constructor and the results structures.  Each section will start with a guide on how to convert existing code and will follow with some rational and explination.  This conversion will convert the code in the v1 example.py file to code that will work in v2.

```python 
# Code prior to line 16 in the v1 example.py does not need to be changed

# v1 code
glazing_system_single_layer = pywincalc.Glazing_System(solid_layers, gaps, standard, width, height)
u_results = glazing_system_single_layer.u() # calculate U-value according to ISO15099
print("Single Layer U-value: {u}".format(u=u_results.result))

# v2 code
glazing_system_single_layer = pywincalc.GlazingSystem(optical_standard=optical_standard, solid_layers=solid_layers, width=width, height=height, environment=pywincalc.nfrc_u_environments())
u_result = glazing_system_single_layer.u() # calculate U-value according to ISO15099
print("Single Layer U-value: {u}".format(u=u_result))

# These results are not available in the thermal results but are available in optical results
# See the section on available optical results for how to obtain them
print("Single Layer u t_sol: {t}".format(t=u_results.t_sol))
print("Single Layer u solar absorptances per layer: {a}".format(a=u_results.layer_solar_absorptances))

#v1 code 
shgc_results = glazing_system_single_layer.shgc() # calculate SHGC according to ISO15099
print("Single Layer SHGC: {shgc}".format(shgc=shgc_results.result))

# v2 code
# Important Note:  While it is still possible to calculate the SHGC value for the 
# glazing_system_single_layer system created above it will do so using the NFRC U 
# environments.  This will not result in the same SHGC as before.  To achieve the
# same SHGC as before a glazing system with the correct environment needs to be created

glazing_system_single_layer_nfrc_shgc_env = pywincalc.GlazingSystem(optical_standard=optical_standard, solid_layers=solid_layers, width=width, height=height, environment=pywincalc.nfrc_shgc_environments())
shgc_result = glazing_system_single_layer_nfrc_shgc_env.shgc() # calculate SHGC according to ISO15099
print("Single Layer SHGC: {shgc}".format(shgc=shgc_result))

# v1 code
# These results are not available in the thermal results but are available in optical results
# See the section on available optical results for how to obtain them
print("Single Layer SHGC t_sol: {t}".format(t=shgc_results.t_sol))
print("Single Layer SHGC solar absorptances per layer: {a}".format(a=shgc_results.layer_solar_absorptances))

#v1 code
solar_optical_results_single_layer = glazing_system_single_layer.all_method_values(pywincalc.Method_Type.SOLAR)

# v2 code
solar_optical_results_single_layer = glazing_system_single_layer.optical_method_results("SOLAR")

# v1 code
print("Single Layer Solar optical transmittance front direct-direct: {r}".format(r=solar_optical_results_single_layer.direct_direct.tf))

# v2 code
print("Single Layer Solar optical transmittance front direct-direct: {r}".format(r=solar_optical_results_single_layer.system_results.front.transmittance.direct_direct))

# v1 code
gap_1 = pywincalc.Gap_Data(pywincalc.Gas_Type.AIR, .0127) # .0127 is gap thickness in meters
gap_2 = pywincalc.Gap_Data(pywincalc.Gas_Type.ARGON, .02) # .02 is gap thickness in meters

# v2 code
gap_1 = pywincalc.Gap(pywincalc.PredefinedGasType.AIR, .0127)  # .0127 is gap thickness in meters
gap_2 = pywincalc.Gap_Data(pywincalc.PredefinedGasType.ARGON, .02) # .02 is gap thickness in meters

# v1 code
tf_rgb_results_triple_layer = color_results_triple_layer.direct_direct.tf.rgb
print("Triple Layer color results transmittance front direct-direct RGB: ({r}, {g}, {b})".format(r=tf_rgb_results_triple_layer.R, g=tf_rgb_results_triple_layer.G, b=tf_rgb_results_triple_layer.B))

# v2 code
tf_rgb_results_triple_layer = color_results_triple_layer.system_results.front.transmittance.direct_direct.rgb
print("Triple Layer color results transmittance front direct-direct RGB: ({r}, {g}, {b})".format(r=tf_rgb_results_triple_layer.R, g=tf_rgb_results_triple_layer.G, b=tf_rgb_results_triple_layer.B))
```

#### Migrating Glazing_System


First Glazing_System was changed to GlazingSystem to be more in line with python's naming conventions.

Second the GlazingSystem constructor parameter order changed and there are additional paramters that can be passed in. All parameters are now able to be passed using keywords.  e.g.

`glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard, solid_layers=solid_layers)`

Finally there is a change to how environmental conditions are handled.  In v1 GlazingSystem had two built-in environments -- NFRC U and NFRC SHGC.  In v2 a GlazingSystem has one environment passed in as a parameter.  This allows for any environmental conditions to be used in thermal calculations.

For convenience there are methods to get the NFRC envionmnents, `pywincalc.nfrc_u_environments()` and `pywincalc.nfrc_shgc_environments()`  To create custom environments see the Environments section above.

However this means that some care should be taken when constructing glazing systems for thermal results.  The NFRC U and SHGC environments are simply standardized environmental conditions used by NFRC to generate their respective thermal result.  But any environmental conditions can be used to calculate both U and SHGC values.

For example, in the example.py file in v1 there is code to get U and SHGC values that looks like this 

```
u_results = glazing_system_single_layer.u() # calculate U-value according to ISO15099
shgc_results = glazing_system_single_layer.shgc() # calculate SHGC according to ISO15099
```

That behavior used to calculate U and SHGC from the respective built-in environments.  Now in order to do the equivalent two glazing systems need to be created:

```
glazing_system_nfrc_u_env = pywincalc.GlazingSystem(optical_standard=optical_standard, solid_layers=solid_layers, environment=pywincalc.nfrc_u_environments())
glazing_system_nfrc_shgc_env = pywincalc.GlazingSystem(optical_standard=optical_standard, solid_layers=solid_layers, environment=pywincalc.nfrc_shgc_environments())

nfrc_u_value = glazing_system_nfrc_u_env.u()
nfrc_shgc_value = glazing_system_nfrc_shgc_env.shgc()
```

Or one glazing system can be created with one set of environmental conditions, run calculations, and then change the environmental conditions and run different calculations:
```
glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard, solid_layers=solid_layers, environment=pywincalc.nfrc_u_environments())

nfrc_u_value = glazing_system.u()
glazing_system.environments(pywincalc.nfrc_shgc_environments())
nfrc_shgc_value = glazing_system.shgc()
```

#### Migrating Results

##### Migrating Optical Results
The `all_method_results` function has been renamed to `optical_method_results`.  It still requires an optical method but now also accepts optional theta and phi values for angular calculations.

The top level object returned by the `optical_method_results` now has two components: system\_results and layer\_results.  As the names imply system\_results contains results that apply to the system as a whole while layer\_results have results on a per-solid-layer basis.

Under `system_results` then it goes side (`front` or `back`), then `transmittance` or `reflectance`, then flux type (`direct-direct`, `direct-diffuse`, `direct-hemispherical`, `diffuse-diffuse`, or `matrix`)


##### Migrating Thermal Results

`GlazingSystem.u()` and `GlazingSystem.shgc()` now return single values
Both `u()` and `shgc()` take optional `theta` and `phi` values for angular calculations.  Both `theta` and `phi` default to zero so if neither are provided the result will be for normal incidence angle.

## IGSDB v2 JSON format
Note:  This should only be used for creating glazing layers with PV properties.  This format is not yet supported for any other solid layer types.

Please refer to the [generic_pv.json](https://github.com/LBNL-ETA/pyWinCalc/tree/main/examples/products/generic_pv.json) file provided for a working example.

### Fields:
 - id:  This field is required by the parser but not used in calculations.
	 - Required: Yes
	 - Allowed values:
		 - any int
		 - null
 - name: This field is required by the parser but not used in calculations.
	 - Required: Yes
	 - Allowed values:
		 - any string (including empty string)  
 - manufacturer: This field is required by the parser but not used in calculations.
	 - Required: Yes
	 - Allowed values:
		 - any string (including empty string)
 - type: This field is required by the parser but not used in calculations.
	 - Required: Yes
	 - Allowed values:
		 - any string (including empty string)
 - subtype: 	
	 - Required: Optional in general but likely required for any PV layers.
	 - Allowed values:
		 - A string equal to one of the following (case insensitive):
			 - "monolithic"
			 - "coated-glass"
			 - "coated"
			 - "applied-film"
			 - "applied film"
			 - "laminate" 
 - coated_side: 
	 - Required: Optional in general but likely required for any PV layers.
	 - Allowed values:
		 - A string equal to one of the following (case insensitive):
			 - "front"
			 - "back"
			 - "both"
			 - "neither"
			 - "na"
 - power_properties: These are values used for PV calculations.
	 - Required: Optional in general but required for any PV layers.
	 - type: A list of objects where each object has the following properties:
		 - temperature: In Kelvin
			 - Allowed values:
				 - A string that is convertible to a float.
		 - values: A list of objects with the following properties:
			 - jsc: short-circuit current density (Jsc) in solar cell [mA/cm2]
				 - Allowed values:
					 - A string that is convertible to a float.
			 - voc: open-circuit voltage (Voc) in solar cell [V]
				 - Allowed values:
					 - A string that is convertible to a float.
			 - ff: fill factor [-]
				 - Allowed values:
					 - A string that is convertible to a float.
	 - Note:  Currently only power properties for one temperature is supported.  If power properties for multiple temperatures are provided only the first will be used.
 - predefined_tir_front:
	 - Required: Optional in general.  Required for calculating results requiring IR values if wavelength measurements do not extend to the IR.
	 - Allowed values:
		 - non-null float
 - predefined_tir_back:
	 - Required: Optional in general.  Required for calculating results requiring IR values if wavelength measurements do not extend to the IR. 
	 - Allowed values:
		 - non-null float
 - predefined_emissivity_front:
	 - Required: Optional in general.  Required for calculating results requiring IR values if wavelength measurements do not extend to the IR.
	 - Allowed values:
		 - non-null float
 - predefined_emissivity_back:
	 - Required: Optional in general.  Required for calculating results requiring IR values if wavelength measurements do not extend to the IR.
	 - Allowed values:
		 - non-null float
 - thickness: Layer thickness in mm.
	 - Required: Optional in general but likely required for any PV layers.
	 - Allowed values:
		 - non-null float
 - conductivity:
	 - Required: Optional in general but likely required for any PV layers.
	 - Allowed values:
		 - non-null float
 - permeability_factor:
	 - Required: Optional
	 - Allowed values:
		 - null
		 - float
 - optical_properties:  
	 - Required: Yes.
	 - Allowed values:
		 - optical_data
	 - optical_data:
		 - Required: Yes.
		 - Note:  Currently only normal incidence values are supported.  If multiple lists of angle_blocks are provided only the first will be used and it will be treated as normal incidence.
		 - Allowed values:
			 - angle_blocks
		 - angle_blocks:
			 - Required: Yes.
			 - Allowed values:
				 - wavelength_data 
			 - wavelength_data:
				 - Required: Yes
				 - Allowed values:
					 - Object with these fields:
						 - wavelength:  The wavelength in microns
							 - Required: Yes
							 - Allowed values:
								 - A string that is convertible to a float. 
						 - specular: An object with these fields:
							 - Required: Optional
							 - tf: front surface transmittance
								 - Required: Yes
								 - Allowed values:
									 - A string that is convertible to a float.
							 - tb: back surface transmittance
								 - Required: Yes
								 - Allowed values:
									 - A string that is convertible to a float.
							 - rf: front surface reflectance
								 - Required: Yes
								 - Allowed values:
									 - A string that is convertible to a float.
							 - rb: back surface reflectance
								 - Required: Yes
								 - Allowed values:
									 - A string that is convertible to a float.
						 - pv: An object with these fields:
							 - Required: Optional
							 - eqef: front surface external quantum efficiency (EQE)
								 - Required: Yes
								 - Allowed values:
									 - A string that is convertible to a float.
							 - eqeb: back surface external quantum efficiency (EQE)
								 - Required: Yes
								 - Allowed values:
									 - A string that is convertible to a float.

## Changelog
### v2.4.2

- Changed the behavior of dual-band BSDF materials.  Now if there a system only has a single layer that is a dual band BSDF and the requested optical method is solar or photopic the layer is treated as a single band using the appropritate band values.  In all other cases the layer is created as a dual band layer as before.  This change is needed so that the single layer calculated solar and visible properties are derived from the values specified for those bands in the input data. 

### v.2.4.0

- Added the ability to use PV data.
	- Can now parse a modified subset of IGSDB v2 json format to create PV layers. 
- Layer absorptances now return separate heat and electricity values.
	- Available absoprtance results are now:  total_direct, total_diffuse, heat_direct, heat_diffuse, electricity_direct, electricity_diffuse, direct, diffuse.
	- Direct and diffuse are equal to total_direct and total_diffuse.  Direct and diffuse are deprecated.
