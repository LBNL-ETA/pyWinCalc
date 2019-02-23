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

### Windows
Wheels have been provided for 32 and 64 bit versions of Python 2.7 and 3.7.  To insall

```
git clone https://bitbucket.org/StephenCzarnecki/pywincalc.git
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

To calculate a system for a single layer CLEAR\_3.DAT (NFRC 102) system using the NFRC 2003 standard as used in WINDOW
```
import pywincalc

standard = "standards/W5\_NFRC\_2003.std" # path to the standard file.  All other files referenced by the standard file must be in the same directory

width = 1.0 # width of the glazing system in meters
height = 1.0 # height of the glazing system in meters

solid\_layers = ["products/CLEAR\_3.DAT"]
gaps = [] # single layer does not have any gaps

u\_results = pywincalc.calc\_u(solid\_layers, gaps, standard, width, height) # calculate U-value according to ISO15099
print("Single Layer U-value: {u}".format(u=u\_results.result))
print("Single Layer u t\_sol: {t}".format(t=u\_results.t\_sol))
print("Single Layer u solar absorptances per layer: {a}".format(a=u\_results.layer\_solar\_absorptances))

shgc\_results = pywincalc.calc\_shgc(solid\_layers, gaps, standard, width, height) # calculate SHGC according to ISO15099
print("Single Layer SHGC: {shgc}".format(shgc=shgc\_results.result))
print("Single Layer SHGC t\_sol: {t}".format(t=shgc\_results.t\_sol))
print("Single Layer SHGC solar absorptances per layer: {a}".format(a=shgc\_results.layer\_solar\_absorptances))
```

For systems with more than one solid layer there must be a gap defined between each solid layer. Here is an example of how to calculate values for a tripple layer system.  In this example the first and third solid layers are CLEAR\_6 (NFRC 103) while the second solid layer is CLEAR\_3 (NFRC 102).  The first and second solid layers are separated by a 1.27cm air gap layer and the second and third layers are separated by a 2cm argon gap layer.

```
import pywincalc

standard = "standards/W5\_NFRC\_2003.std" # path to the standard file.  All other files referenced by the standard file must be in the same directory

width = 1.0 # width of the glazing system in meters
height = 1.0 # height of the glazing system in meters

solid\_layer\_1  = "products/CLEAR\_6.DAT"
solid\_layer\_2  = "products/CLEAR\_3.DAT"
solid\_layer\_3  = "products/CLEAR\_6.DAT"

solid\_layers = [solid\_layer\_1, solid\_layer\_2, solid\_layer\_3]

gap\_1 = pywincalc.Gap\_Data(pywincalc.Gas\_Type.AIR, .0127) # .0127 is gap thickness in meters
gap\_2 = pywincalc.Gap\_Data(pywincalc.Gas\_Type.ARGON, .02) # .02 is gap thickness in meters

gaps = [gap\_1, gap\_2] 

u\_results = pywincalc.calc\_u(solid\_layers, gaps, standard, width, height) # calculate U-value according to ISO15099
print("Triple Layer U-value: {u}".format(u=u\_results.result))
print("Triple Layer u t\_sol: {t}".format(t=u\_results.t\_sol))
print("Triple Layer u solar absorptances per layer: {a}".format(a=u\_results.layer\_solar\_absorptances))


shgc\_results = pywincalc.calc\_shgc(solid\_layers, gaps, standard, width, height) # calculate SHGC according to ISO15099
print("Triple Layer SHGC: {shgc}".format(shgc=shgc\_results.result))
print("Triple Layer SHGC t\_sol: {t}".format(t=shgc\_results.t\_sol))
print("Triple Layer SHGC solar absorptances per layer: {a}".format(a=shgc\_results.layer\_solar\_absorptances))
```
