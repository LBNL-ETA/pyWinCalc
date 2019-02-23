import pywincalc

standard = "standards/W5_NFRC_2003.std" # path to the standard file.  All other files referenced by the standard file must be in the same directory

width = 1.0 # width of the glazing system in meters
height = 1.0 # height of the glazing system in meters

solid_layers = ["products/CLEAR_3.DAT"]
gaps = [] # single layer does not have any gaps

u_results = pywincalc.calc_u(solid_layers, gaps, standard, width, height) # calculate U-value according to ISO15099
print("Single Layer U-value: {u}".format(u=u_results.result))
print("Single Layer u t_sol: {t}".format(t=u_results.t_sol))
print("Single Layer u solar absorptances per layer: {a}".format(a=u_results.layer_solar_absorptances))

shgc_results = pywincalc.calc_shgc(solid_layers, gaps, standard, width, height) # calculate U-value according to ISO15099
print("Single Layer SHGC: {shgc}".format(shgc=shgc_results.result))
print("Single Layer SHGC t_sol: {t}".format(t=shgc_results.t_sol))
print("Single Layer SHGC solar absorptances per layer: {a}".format(a=shgc_results.layer_solar_absorptances))


solid_layer_1  = "products/CLEAR_6.DAT"
solid_layer_2  = "products/CLEAR_3.DAT"
solid_layer_3  = "products/CLEAR_6.DAT"

solid_layers = [solid_layer_1, solid_layer_2, solid_layer_3]

gap_1 = pywincalc.Gap_Data(pywincalc.Gas_Type.AIR, .0127) # .0127 is gap thickness in meters
gap_2 = pywincalc.Gap_Data(pywincalc.Gas_Type.ARGON, .02) # .02 is gap thickness in meters

gaps = [gap_1, gap_2] 

u_results = pywincalc.calc_u(solid_layers, gaps, standard, width, height) # calculate U-value according to ISO15099
print("Triple Layer U-value: {u}".format(u=u_results.result))
print("Triple Layer u t_sol: {t}".format(t=u_results.t_sol))
print("Triple Layer u solar absorptances per layer: {a}".format(a=u_results.layer_solar_absorptances))


shgc_results = pywincalc.calc_shgc(solid_layers, gaps, standard, width, height) # calculate U-value according to ISO15099
print("Triple Layer SHGC: {shgc}".format(shgc=shgc_results.result))
print("Triple Layer SHGC t_sol: {t}".format(t=shgc_results.t_sol))
print("Triple Layer SHGC solar absorptances per layer: {a}".format(a=shgc_results.layer_solar_absorptances))
