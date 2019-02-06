import pywincalc

standard = "standards/W5_NFRC_2003.std" # path to the standard file.  All other files referenced by the standard file must be in the same directory

width = 1.0 # width of the glazing system in meters
height = 1.0 # height of the glazing system in meters

solid_layers = ["products/CLEAR_3.DAT"]
gaps = [] # single layer does not have any gaps

u = pywincalc.calc_u(products, gaps, standard, width, height) # calculate U-value according to ISO15099
print("Single Layer U-value: {u}".format(u=u))

shgc = pywincalc.calc_shgc(products, gaps, standard, width, height) # calculate U-value according to ISO15099
print("Single Layer SHGC: {shgc}".format(shgc=shgc))

solid_layer_1  = "products/CLEAR_6.DAT"
solid_layer_2  = "products/CLEAR_3.DAT"
solid_layer_3  = "products/CLEAR_6.DAT"

solid_layers = [solid_layer_1, solid_layer_2, solid_layer_3]

gap_1 = pywincalc.Gap_Data("Air", .0127) # .0127 is gap thickness in meters
gap_2 = pywincalc.Gap_Data("Argon", .02) # .02 is gap thickness in meters

gaps = [gap_1, gap_2] 

u = pywincalc.calc_u(products, gaps, standard, width, height) # calculate U-value according to ISO15099
print("Double Layer U-value: {u}".format(u=u))

shgc = pywincalc.calc_shgc(products, gaps, standard, width, height) # calculate U-value according to ISO15099
print("Double Layer SHGC: {shgc}".format(shgc=shgc))