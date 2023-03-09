import pywincalc
import results_printer

# Path to the optical standard file.  All other files referenced by the standard file must be in the same directory
# Note:  While all optical standards packaged with WINDOW should work with optical calculations care should be
# taken to use NFRC standards if NFRC thermal results are desired.  This is because for thermal calculations currently
# only ISO 15099 is supported.  While it is possible to use EN optical standards and create thermal results
# those results will not be based on EN 673
optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

width = 1.0  # width of the glazing system in meters
height = 1.0  # height of the glazing system in meters

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
# For more possible results see all_NFRC_results.py
#
# For more on environmental conditions see custom_environmental_conditions.py
glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                         solid_layers=solid_layers,
                                         width_meters=width,
                                         height_meters=height)

u_value = glazing_system.u()
print("U-value for a single layer system with integrated PV: {v}".format(v=u_value))
