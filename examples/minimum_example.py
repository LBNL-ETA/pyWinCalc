import pywincalc

clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

solid_layers = [clear_3]

glazing_system = pywincalc.create_glazing_system(solid_layers=solid_layers)
print("Single Layer U-value: {u}".format(u=glazing_system.u()))
