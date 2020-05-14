Berkeley Lab WINDOW Calc Engine (CalcEngine) Copyright (c) 2016 - 2020, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Dept. of Energy).  All rights reserved.

If you have questions about your rights to use or distribute this software, please contact Berkeley Lab's Innovation & Partnerships Office at IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department of Energy and the U.S. Government consequently retains certain rights.  As such, the U.S. Government has been granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the Software to reproduce, distribute copies to the public, prepare derivative works, and perform publicly and display publicly, and to permit other to do so.


# pywincalc

This module provides a simplified method for calculating various thermal and optical properties of glazing systems.


### Requirements
[Git](https://git-scm.com/)

[CMake](https://cmake.org/) - Not required for installing from wheel files on Windows.

## Install

### Linux
Once the requirementes have been installed this can be installed with pip by doing

` pip install git+https://github.com/LBNL-ETA/pyWinCalc.git `

### Mac
Once the requirementes have been installed this can be installed with pip by doing

` pip install git+https://github.com/LBNL-ETA/pyWinCalc.git `

### Windows
Wheels have been provided for 32 and 64 bit versions of Python 2.7 and 3.7.  To insall

```
git clone https://github.com/LBNL-ETA/pyWinCalc.git
cd pywincalc\wheels
pip install pywincalc-0.0.1-your-version-of-python.whl
```

For other versions of Python the correct C++ compiler first needs to be installed as well as CMake.  Once that has been installed pyWinCalc can be built following the Linux build steps.

## Use
Calculations can be performed with either a single solid layer or multiple solid layers separated by gaps.

A folder with example calculation script, products and standards is provided under the example directory.

### Units

With the exception of wavelength values which are in microns all units are values are in SI base units.  However for documenentation some units are expressed as more common derived SI units when the values are equivalent.  For example:
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

### Solid layers
Solid layers define the glazing or shading products that make up a glazing system.  The methods for creating solid layers currently supported are:
 
- From paths to measured data files as exported by [Optics](https://windows.lbl.gov/software/optics).  See [single_clear.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/single_clear.py) and [triple_clear.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/triple_clear.py) in the examples directory.
- From json returned by a request for a shading layer to the [IGSDB](igsdb.lbl.gov).  See [igsdb_exterior_shade_on_clear_glass.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/igsdb_exterior_shade_on_clear_glass.py) in the examples directory.
- From a combination of json returned by a request for a material from the [IGSDB](igsdb.lbl.gov) and user-defined geometry.  See [igsdb_custom_perforated.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/igsdb_custom_perforated.py), [igsdb_custom_venetian.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/igsdb_custom_venetian.py), and [igsdb_custom_woven.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/igsdb_custom_woven.py) in the examples directory.
- From measured wavelength data from some other source and user-defined geometry.  See [custom_perforated.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/custom_perforated.py) in the examples directory.

#### Supported solid layer types
The following types of solid layers are currently supported:
- Glazings that are represented as one set of measured wavelength data.  Products that require deconstruction like some laminates and coated glass are not yet supported.
- Venetian blinds
- Woven shades
- Perforated screens

### Gaps
For systems with more than one solid layer each solid layer must be separated by a gap.  The methods for creating gaps currently supported are:

- From a selection of predefined gases.  Current predefined gases are:  Air, Argon, Krypton, Xeon.  See gap_1 in [triple_clear.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/triple_clear.py)
- From a mixture of predefined gases.  See gap_2 in [triple_clear.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/triple_clear.py)
- From creating a custom gas by providing molecular weight, specific heat ratio, and coefficients for specific heat at constant pressure (Cp), thermal conductivity, and viscosity.  No example yet.
- From a mixture of custom gases.  No example yet.

### BSDF Calculations

Shading products require BSDF calculations while glazings do not.  If any layer passed to a glazing system is a shading layer the glazing system will also require a BSDF hemisphere.  For examples see any of the igsdb examples or [custom_perforated.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/custom_perforated.py) in the examples directory.

However it is possible to use BSDF calculations for a system with no shading products.  To do so pass a BSDF hemisphere as in the examples with shading systems.

If a glazing system is given a BSDF hemisphere as a parameter it will always use that for optical calculations.

### Example use cases

Since there are several ways of creating and combining layers plus different calculation options example scripts are provided in the [/example](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/) directory.  

These scripts use optical standards provided in the [/example/standards](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/standards) directory.  Some scripts use measured data for example products provided in the [/example/products](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/products) directory.

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

glazing_system = pywincalc.Glazing_System(solid_layers, gaps, optical_standard, width, height)
print("Single Layer U-value: {u}".format(u=glazing_system.u()))
```

Please see the following examples which contain more information.
- [single_clear.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/single_clear.py): Creates a single layer glazing system from a sample optics file.  Shows all thermal results, all optical results for a single optical method and some optical results from a second optical method.
- [triple_clear.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/triple_clear.py):  Creates a triple layer glazing system from sample optics files.  Creates two gaps, one with a single gas and one with a gas mixture.  Shows another example of optical results for each layer.
- [igsdb_exterior_shade_on_clear_glass.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/igsdb_exterior_shade_on_clear_glass.py):  Creates two double-layer glazing systems with exterior shading products (Venetian blind and perforated screen).  Uses shading layers and glass from the [IGSDB](http://igsdb.lbl.gov).  
- [igsdb_custom_perforated.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/igsdb_custom_perforated.py) Creates a double layer glazing system with an exterior perforated screen.  The perforated screen uses a material from the [IGSDB](http://igsdb.lbl.gov) and a user-defined geometry describing the perforations.  The glass layer uses data from the [IGSDB](http://igsdb.lbl.gov)
- [igsdb_custom_venetian.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/igsdb_custom_venetian.py).  Creates a double layer glazing system with an exterior venetian blind.  The venetian blind uses a material from the [IGSDB](http://igsdb.lbl.gov) and a user-defined geometry describing the slats.  Also includes an example of how to change the distribution method used for calculating optical results for the shade.  The glass layer uses data from the [IGSDB](http://igsdb.lbl.gov)
- [igsdb_custom_woven.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/igsdb_custom_woven.py) Creates a double layer glazing system with an exterior woven shade.  The woven shade uses a material from the [IGSDB](http://igsdb.lbl.gov) and a user-defined geometry describing the thread layout.  The glass layer uses data from the [IGSDB](http://igsdb.lbl.gov)
- [custom_perforated.py](https://github.com/LBNL-ETA/pyWinCalc/blob/shading_calcs/example/custom_perforated.py) Creates a double layer glazing system with an exterior perforated screen.  Shows an example of getting measured data from somewhere other than either the [IGSDB](http://igsdb.lbl.gov) or optics file.

If there is something you are trying to calculate that does not exist as an example yet please contact us.

### Tutorial Videos

https://youtu.be/YQzCho-Vx-k

https://youtu.be/_lfoyZ2ntkU
