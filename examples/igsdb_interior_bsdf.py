import pywincalc
import requests
from igsdb_interaction import url_single_product, headers, url_single_product_datafile
import results_printer

# Path to the optical standard file.  All other files referenced by the standard file must be in the same directory
# Note:  While all optical standards packaged with WINDOW should work with optical calculations care should be
# taken to use NFRC standards if NFRC thermal results are desired.  This is because for thermal calculations currently
# only ISO 15099 is supported.  While it is possible to use EN optical standards and create thermal results
# those results will not be based on EN 673
optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

glazing_system_width = 1.0  # width of the glazing system in meters
glazing_system_height = 1.0  # height of the glazing system in meters

# Define the gap between the shade and the glazing.  In this case use a default air gap
# that is 12.7mm thick.  For more on creating gases and gaps see the gases.py example
gap_1 = pywincalc.Layers.gap(thickness=.0127)

bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.FULL)

generic_clear_3mm_glass_igsdb_id = 363
bsdf_igsdb_id = 14710

generic_clear_3mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_3mm_glass_igsdb_id),
                                                      headers=headers)

bsdf_igsdb_response = requests.get(
    url_single_product_datafile.format(id=bsdf_igsdb_id), headers=headers)

clear_3 = pywincalc.parse_json(generic_clear_3mm_glass_igsdb_response.content)

# The BSDF data is currently stored as XML on igsdb.lbl.gov.  As a result it needs to be
# parsed using the xml string parser instead of the json parser
bsdf_shade = pywincalc.parse_bsdf_xml_string(bsdf_igsdb_response.content)

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see all_NFRC_results.py
#
# For more on environmental conditions see custom_environmental_conditions.py
glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                         solid_layers=[clear_3, bsdf_shade],
                                         gap_layers=[gap_1],
                                         width_meters=glazing_system_width,
                                         height_meters=glazing_system_height,
                                         bsdf_hemisphere=bsdf_hemisphere)

u_value = glazing_system.u()
print(
    "U-value for a double-layer system with exterior interior BSDF shade downloaded from igsdb.lbl.glv: {v}".format(
        v=u_value))
