import pywincalc

optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)
clear_3 = pywincalc.convert_to_solid_layer(clear_3)

thermal_ir_results = pywincalc.calc_thermal_ir(optical_standard, clear_3)

print("Diffuse-diffuse front transmittance: {v}".format(v=thermal_ir_results.transmittance_front_diffuse_diffuse))
print("Diffuse-diffuse back transmittance: {v}".format(v=thermal_ir_results.transmittance_back_diffuse_diffuse))
print("Hemispheric front emissivity: {v}".format(v=thermal_ir_results.emissivity_front_hemispheric))
print("Hemispheric back emissivity: {v}".format(v=thermal_ir_results.emissivity_back_hemispheric))
