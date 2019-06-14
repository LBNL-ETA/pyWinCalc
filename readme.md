Berkeley Lab WINDOW Calc Engine (CalcEngine) Copyright (c) 2016 - 2019, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Dept. of Energy).  All rights reserved.

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

### Standards
calculations can be perfromed using predefined standards in the form that is expected by [WINDOW](https://windows.lbl.gov/software/window).  The path to the base standard files is all that needs to be passed.  Any other files referenced by the standard file must be in the same directory (or specified as a relative directory from within the standard file).

### Solid layers
Solid layers can be passed by paths to measured data files as exported by [Optics](https://windows.lbl.gov/software/optics)

### Gaps
For systems with more than one solid layer each solid layer must be separated by a gap.  Currently a selection of predefined gases are supported.  Gas mixtures are not yet supported in the Python interface.

Supported gases:  Air, Argon, Krypton, Xeon

### Example use case
Assume that the measured data files are in a ./products folder and that the standards are in a ./standards directory

To calculate a system for a single layer CLEAR_3.DAT (NFRC 102) system using the NFRC 2003 standard as used in WINDOW
```
import pywincalc

width = 1.0 # width of the glazing system in meters
height = 1.0 # height of the glazing system in meters

# path to the standard file.  All other files referenced by the standard file must be in the same directory
standard_path = "standards/W5_NFRC_2003.std" 
standard = pywincalc.load_standard(standard_path)

clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

solid_layers = [clear_3]
gaps = [] # single layer does not have any gaps

glazing_system_single_layer = pywincalc.Glazing_System(solid_layers, gaps, standard, width, height)

u_results = glazing_system_single_layer.u() # calculate U-value according to ISO15099
print("Single Layer U-value: {u}".format(u=u_results.result))
print("Single Layer u t_sol: {t}".format(t=u_results.t_sol))
print("Single Layer u solar absorptances per layer: {a}".format(a=u_results.layer_solar_absorptances))

shgc_results = glazing_system_single_layer.shgc() # calculate SHGC according to ISO15099
print("Single Layer SHGC: {shgc}".format(shgc=shgc_results.result))
print("Single Layer SHGC t_sol: {t}".format(t=shgc_results.t_sol))
print("Single Layer SHGC solar absorptances per layer: {a}".format(a=shgc_results.layer_solar_absorptances))

thermal_ir_optical_results_single_layer = glazing_system_single_layer.all_method_values(pywincalc.Method_Type.SOLAR)
print("Finished single layer tir calc")
print("Single Layer Thermal IR optical transmittance front direct-direct: {r}".format(r=thermal_ir_optical_results_single_layer.tf_direct_direct))
```

For systems with more than one solid layer there must be a gap defined between each solid layer. Here is an example of how to calculate values for a tripple layer system.  In this example the first and third solid layers are CLEAR\_6 (NFRC 103) while the second solid layer is CLEAR\_3 (NFRC 102).  The first and second solid layers are separated by a 1.27cm air gap layer and the second and third layers are separated by a 2cm argon gap layer.

```
import pywincalc

width = 1.0 # width of the glazing system in meters
height = 1.0 # height of the glazing system in meters

# path to the standard file.  All other files referenced by the standard file must be in the same directory
standard_path = "standards/W5_NFRC_2003.std" 
standard = pywincalc.load_standard(standard_path)

clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

clear_6_path = "products/CLEAR_6.DAT"
clear_6 = pywincalc.parse_optics_file(clear_6_path)

solid_layers = [clear_6, clear_3, clear_6]

gap_1 = pywincalc.Gap_Data(pywincalc.Gas_Type.AIR, .0127) # .0127 is gap thickness in meters
gap_2 = pywincalc.Gap_Data(pywincalc.Gas_Type.ARGON, .02) # .02 is gap thickness in meters

gaps = [gap_1, gap_2] 

glazing_system_tripple_layer = pywincalc.Glazing_System(solid_layers, gaps, standard, width, height)

u_results = glazing_system_tripple_layer.u() # calculate U-value according to ISO15099
print("Triple Layer U-value: {u}".format(u=u_results.result))
print("Triple Layer u t_sol: {t}".format(t=u_results.t_sol))
print("Triple Layer u solar absorptances per layer: {a}".format(a=u_results.layer_solar_absorptances))

shgc_results = glazing_system_tripple_layer.shgc() # calculate SHGC according to ISO15099
print("Triple Layer SHGC: {shgc}".format(shgc=shgc_results.result))
print("Triple Layer SHGC t_sol: {t}".format(t=shgc_results.t_sol))
print("Triple Layer SHGC solar absorptances per layer: {a}".format(a=shgc_results.layer_solar_absorptances))

photopic_optical_results_tripple_layer = glazing_system_tripple_layer.all_method_values(pywincalc.Method_Type.PHOTOPIC)
print("Tripple Layer Photopic optical results: {r}".format(r=photopic_optical_results_tripple_layer))
```
### Tutorial Videos

https://youtu.be/YQzCho-Vx-k

https://youtu.be/_lfoyZ2ntkU
