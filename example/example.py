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

# Glazing_System defaults to the NFRC U environments
glazing_system_single_layer_u_env = pywincalc.Glazing_System(solid_layers, gaps, standard, width, height)
u_value = glazing_system_single_layer_u_env.u() # calculate U-value according to ISO15099
print("Single Layer U-value: {u}".format(u=u_value))

# To calculate SHGC use the NFRC SHGC environments for the glazing system instead
glazing_system_single_layer_shgc_env = pywincalc.Glazing_System(solid_layers, gaps, standard, width, height, pywincalc.nfrc_shgc_environments())
shgc_result = glazing_system_single_layer_shgc_env.shgc() # calculate SHGC according to ISO15099
print("Single Layer SHGC: {shgc}".format(shgc=shgc_result))

# It is possible to calculate U and SHGC for any environmental conditions.
# E.G. The SHGC for the NFRC U environmental conditions is
u_environment_shgc = glazing_system_single_layer_u_env.shgc()
print("SHGC for the NFRC U-value environmental conditions: {shgc}".format(shgc=u_environment_shgc))
# And the u-value for the SHGC environment is
shgc_environment_u = glazing_system_single_layer_shgc_env.u()
print("U for the NFRC SHGC environmental conditions: {u}".format(u=shgc_environment_u))

# Optical results are calculated based on methods defined by the optical standard loaded above.
# Get all solar results by
solar_results = glazing_system_single_layer_u_env.optical_method_results(pywincalc.Optical_Method_Type.SOLAR)

# Optical results have two parts, results that apply to the entire system and results for each layer.
# System results and results for each layer are then divided by side (front, back).
# then by transmission type (transmittance, reflectance) and then by ____________ (direct_direct, direct_diffuse,
# direct_hemispherical, and diffuse_diffuse).  direct_diffuse does not include the direct_direct component while
# direct_hemispherical does.  In other words direct_direct + direct_diffuse = direct_hemispherical
system_solar_results = solar_results.system_results
print("Direct-hemispheric front solar transmittance: {v}".format(v=system_solar_results.front.transmittance.direct_hemispherical))
print("Diffuse-diffuse front solar reflectance: {v}".format(v=system_solar_results.front.reflectance.diffuse_diffuse))
print("Direct-direct back solar transmittance: {v}".format(v=system_solar_results.back.transmittance.direct_direct))
#etc...

# Currently only absorptance results are provided for each layer.  Direct and diffuse absportances are
# provided for each side of each layer.
solar_results_per_layer = solar_results.layer_results
print("Layer 1 front direct solar absorptance: {v}".format(v=solar_results_per_layer[0].front.absorptance.direct))
print("Layer 1 back diffuse solar absorptance: {v}".format(v=solar_results_per_layer[0].back.absorptance.diffuse))
# etc...

# Similarly for visible results calculate using the Photopic method
visible_results = glazing_system_single_layer_u_env.optical_method_results(pywincalc.Optical_Method_Type.PHOTOPIC)
print("Direct-direct front visible transmittance: {v}".format(v=visible_results.system_results.front.transmittance.direct_direct))
print("Direct-hemispheric back visible reflectance: {v}".format(v=visible_results.system_results.back.reflectance.direct_hemispherical))
print("Layer 1 front diffuse visible absorptance: {v}".format(v=visible_results.layer_results[0].front.absorptance.diffuse))
# etc...

# If the optical standard defines color methods those have a separate results set and function call
color_results = glazing_system_single_layer_u_env.color()

# Currently color results only have system results.  Individual layer results are not yet supported.
# Color results follow the same layout as the other optical system results except each value is offered in
# the Trichromatic, Lab, and RGB color spaces.
direct_direct_front_transmittace_rgb_color = color_results.system_results.front.transmittance.direct_direct.rgb
print("Direct-direct front color transmittance in RGB: ({r}, {g}, {b})".format(r=direct_direct_front_transmittace_rgb_color.R, g=direct_direct_front_transmittace_rgb_color.G, b=direct_direct_front_transmittace_rgb_color.B))
direct_hemispherical_back_reflectance_lab_color = color_results.system_results.back.reflectance.direct_hemispherical.lab
print("Direct-hemispheric back color reflectance in Lab: ({l}, {a}, {b})".format(l=direct_hemispherical_back_reflectance_lab_color.L, a=direct_hemispherical_back_reflectance_lab_color.a, b=direct_hemispherical_back_reflectance_lab_color.b))
# etc...

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
print("Tripple Layer Photopic optical results transmittance front direct-direct: {r}".format(r=photopic_optical_results_tripple_layer.direct_direct.tf))

color_results_tripple_layer = glazing_system_tripple_layer.color()
tf_rgb_results_tripple_layer = color_results_tripple_layer.direct_direct.tf.rgb
print("Tripple Layer color results transmittance front direct-direct RGB: ({r}, {g}, {b})".format(r=tf_rgb_results_tripple_layer.R, g=tf_rgb_results_tripple_layer.G, b=tf_rgb_results_tripple_layer.B))