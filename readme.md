# pywincalc

This module provides a simplified method for calculating various thermal and optical properties of glazing systems.

## Install

This can be installed with pip by doing

` pip install git+https://bitbucket.org/StephenCzarnecki/pywincalc.git `

## Use
Calculations can be performed with either a single solid layer or multiple solid layers separated by gaps.  And calculations can be perfromed using predefined standards in the form that is expected by [WINDOW](https://windows.lbl.gov/software/window).

### Solid layers
Solid layers can be passed by filename to measured data files as exported by [Optics](https://windows.lbl.gov/software/optics)

### Gaps
For systems with more than one solid layer each solid layer must be separated by a gap.  Currently a selection of predefined gases are supported.  Gas mixtures are not yet supported in the Python interface.

Supported gases:  Air, Argon, Krypton, Xeon

### Example use case
Assume that the measured data files are in a ./products folder and that the standards are in a ./standards directory

To calculate a system for a single layer CLEAR_3.DAT (NFRC 102) system using the NFRC 2003 standard as used in WINDOW
```
import pywincalc

standard = "standards/W5_NFRC_2003.std" # path to the standard file.  All other files referenced by the standard file must be in the same directory

solid_layers = ["products/CLEAR_3.DAT]
gaps = [] # single layer does not have any gaps

width = 1.0 # width of the glazing system in meters
height = 1.0 # height of the glazing system in meters

u = pywincalc.calc_u(products, gaps, standard, width, height) # calculate U-value according to ISO15099

shgc = pywincalc.calc_shgc(products, gaps, standard, width, height) # calculate U-value according to ISO15099
```

For systems with more than one layer there must be a gap defined between each layer. Here is an example of how to calculate values for a tripple layer system.  In this example the first and third layers are CLEAR\_6 (NFRC 103) while the second layer is CLEAR\_3 (NFRC 102).  And where the first and second layers are separated by a 1.27cm air gap while the second and third layers are separated by a 2cm argon gap.

```
import pywincalc

standard = "standards/W5_NFRC_2003.std" # path to the standard file.  All other files referenced by the standard file must be in the same directory

solid_layer_1  = "products/CLEAR_3.DAT"
solid_layer_2  = "products/CLEAR_6.DAT"
solid_layer_3  = "products/CLEAR_3.DAT"

solid_layers = [solid_layer_1, solid_layer_2, solid_layer_3]

gap_1 = pywincalc.Gap_Data("Air", .0127) # .0127 is gap thickness in meters
gap_2 = pywincalc.Gap_Data("Argon", .02) # .02 is gap thickness in meters

gaps = [gap_1, gap_2] 

width = 1.0 # width of the glazing system in meters
height = 1.0 # height of the glazing system in meters

u = pywincalc.calc_u(products, gaps, standard, width, height) # calculate U-value according to ISO15099

shgc = pywincalc.calc_shgc(products, gaps, standard, width, height) # calculate U-value according to ISO15099
```
