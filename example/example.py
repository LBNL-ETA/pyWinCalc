import pywincalc

# path to the standard file.  All other files referenced by the standard file must be in the same directory
standard_path = "standards/W5_NFRC_2003.std" 
standard = pywincalc.load_standard(standard_path)

width = 1.0 # width of the glazing system in meters
height = 1.0 # height of the glazing system in meters

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

color_results_single_layer = glazing_system_single_layer.color()
print("Single Layer color results: {r}".format(r=thermal_ir_optical_results_single_layer))

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

color_results_tripple_layer = glazing_system_tripple_layer.color()
print("Tripple Layer color results: {r}".format(r=thermal_ir_optical_results_tripple_layer))