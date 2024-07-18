import pywincalc

pillar = pywincalc.LinearBearingPillar(height=0.002, material_conductivity=20,
                                       cell_area=pywincalc.pillar_cell_area(pywincalc.CellSpacingType.SQUARE, 0.03),
                                       length=0.25e-3, width=0.01e-3)
gap = pywincalc.layers.create_pillar(pillar=pillar, pressure=0.1333)

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
