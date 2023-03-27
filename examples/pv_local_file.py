import pywincalc

# Layers with PV data can be created using a subset of the IGSDB v2 json structure. For an example see the
# generic_pv.json file in the examples/products directory.
# Note:  This format should only be used for creating json files for layers with PV data.  Other layer types are not
# supported yet with this format and should use one of the other available input types as shown in the other examples.
pv_path = "products/generic_pv.json"
pv = pywincalc.parse_json_file(pv_path)

# Create a list of solid layers in order from outside to inside
solid_layers = [pv]

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see optical_results_NFRC.py
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.create_glazing_system(solid_layers=solid_layers)

u_value = glazing_system.u()
print("U-value for a single layer system with integrated PV: {v}".format(v=u_value))
