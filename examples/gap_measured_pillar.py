import pywincalc

glass_1 = pywincalc.Glass(thickness=0.05, conductivity=1, emissivity=0.8)
glass_2 = pywincalc.Glass(thickness=0.05, conductivity=1, emissivity=0.8)
measured_pillar = pywincalc.PillarMeasurement(total_thickness=0.12, conductivity=0.3, temperature_surface_1=295,
                                              temperature_surface_4=305, glass_1=glass_1, glass_2=glass_2)

gap = pywincalc.layers.create_pillar(pillar=measured_pillar)

gaps = [gap]

clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)
solid_layers = [clear_3, clear_3]

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see optical_results_NFRC.py
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.GlazingSystem(solid_layers=solid_layers, gap_layers=gaps)
u_value = glazing_system.u()
print(f"U-value for the system: {u_value}")
