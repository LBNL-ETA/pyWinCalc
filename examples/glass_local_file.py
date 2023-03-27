import pywincalc

# Load solid layer measured values.  Solid layer information can come from either igsdb.lbl.gov or files generate
# by the Optics program.  Since igsdb.lbl.gov requires registration some optics files are provided for example
# purposes
clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

solid_layers = [clear_3]

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see optical_results_NFRC.py
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.create_glazing_system(solid_layers=solid_layers)

u_value = glazing_system.u()
print("U-value for a single-layer system with generic clear glass: {v}".format(v=u_value))
