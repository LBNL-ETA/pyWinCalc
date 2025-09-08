import pywincalc

# Load solid layer measured values.  Solid layer information can come from either igsdb.lbl.gov or files generate
# by the Optics program.  Since igsdb.lbl.gov requires registration some optics files are provided for example
# purposes
product_path = "products/sample_dir_dif.txt"
product = pywincalc.parse_optics_file(product_path)

solid_layers = [product]

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see optical_results_NFRC.py
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.GlazingSystem(solid_layers=solid_layers)

u_value = glazing_system.u()
print("U-value for a single-layer system with a direct-diffuse layer: {v}".format(v=u_value))
