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

# Define the gap between the shade and the glazing
gap_1 = pywincalc.Gap(pywincalc.PredefinedGasType.AIR, .0127)  # .0127 is gap thickness in meters

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
thermeshade_perforated_screen_igsdb_id = 14990

generic_clear_3mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_3mm_glass_igsdb_id),
                                                      headers=headers)
thermeshade_perforated_screen_igsdb_response = requests.get(
    url_single_product.format(id=thermeshade_perforated_screen_igsdb_id), headers=headers)

generic_clear_3mm_glass = pywincalc.parse_json(generic_clear_3mm_glass_igsdb_response.content)
thermeshade_perforated_screen = pywincalc.parse_json(
    thermeshade_perforated_screen_igsdb_response.content)

# Create a glazing system using the NFRC U environment in order to get NFRC U results
# U and SHGC can be caculated for any given environment but in order to get results
# The NFRC U and SHGC environments are provided as already constructed environments and Glazing_System
# defaults to using the NFRC U environments

glazing_system_u_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                       solid_layers=[thermeshade_perforated_screen,
                                                                     generic_clear_3mm_glass],
                                                       gap_layers=[gap_1], width_meters=glazing_system_width,
                                                       height_meters=glazing_system_height,
                                                       environment=pywincalc.nfrc_u_environments(),
                                                       bsdf_hemisphere=bsdf_hemisphere)

glazing_system_shgc_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                          solid_layers=[thermeshade_perforated_screen,
                                                                        generic_clear_3mm_glass],
                                                          gap_layers=[gap_1], width_meters=glazing_system_width,
                                                          height_meters=glazing_system_height,
                                                          environment=pywincalc.nfrc_shgc_environments(),
                                                          bsdf_hemisphere=bsdf_hemisphere)

results_name = "Results for a double-layer system with exterior perforated screen downloaded from the IGSDB"
print("*" * len(results_name))
print(results_name)
print("*" * len(results_name))
results_printer.print_results(glazing_system_u_environment, glazing_system_shgc_environment)
