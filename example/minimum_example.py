import pywincalc

optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

width = 1.0
height = 1.0

clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

solid_layers = [clear_3]
gaps = []

glazing_system = pywincalc.GlazingSystem(solid_layers, gaps, optical_standard, width, height)
print("Single Layer U-value: {u}".format(u=glazing_system.u()))
