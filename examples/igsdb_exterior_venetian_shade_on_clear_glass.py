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

# Since these products use at least one layer that requires a BSDF model a BSDF hemisphere must be
# used.  In this example a standard quarter basis is used.  Other predefined basis include Small, Half, and Full
# Custom BSDF basis is not yet supported in Python.  Please contact us if your work requires calculations with
# a custom BSDF basis.
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.QUARTER)

# Download some product data from the IGSDB.  This example gets a generic single clear 3mm glazing (NFRC 102),
# a venetian blind manufactured by Pella (CGDB ID 3000) and a perforated screen manufacturerd by Solar Comfort
# (CGDB ID 18000)
generic_clear_3mm_glass_igsdb_id = 363
slim_white_pella_venetian_blind_igsdb_id = 14684

generic_clear_3mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_3mm_glass_igsdb_id),
                                                      headers=headers)
slim_white_pella_venetian_blind_igsdb_response = requests.get(
    url_single_product.format(id=slim_white_pella_venetian_blind_igsdb_id), headers=headers)

generic_clear_3mm_glass = pywincalc.parse_json(generic_clear_3mm_glass_igsdb_response.content)
slim_white_pella_venetian_blind = pywincalc.parse_json(slim_white_pella_venetian_blind_igsdb_response.content)

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see all_NFRC_results.py
#
# For more on environmental conditions see custom_environmental_conditions.py
glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                         solid_layers=[slim_white_pella_venetian_blind,
                                                       generic_clear_3mm_glass],
                                         gap_layers=[gap_1], width_meters=glazing_system_width,
                                         height_meters=glazing_system_height,
                                         bsdf_hemisphere=bsdf_hemisphere)

u_value = glazing_system.u()
print(
    "U-value for a double-layer system with exterior Venetian blind downloaded from igsdb.lbl.glv: {v}".format(
        v=u_value))
