import pywincalc

optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

solid_layers = [clear_3]

glazing_system = pywincalc.GlazingSystem( optical_standard, solid_layers)
print("Single Layer U-value: {u}".format(u=glazing_system.u()))
