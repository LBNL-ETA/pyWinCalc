import pywincalc
import requests
from igsdb_interaction import url_single_product, headers
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

# Download some product data from the IGSDB.  This example gets a generic single clear 3mm glazing (NFRC 102),
# and a generic single clear 6mm glazing (NFRC 103)
generic_clear_3mm_glass_igsdb_id = 363
generic_clear_6mm_glass_igsdb_id = 362

generic_clear_3mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_3mm_glass_igsdb_id),
                                                      headers=headers)
generic_clear_6mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_6mm_glass_igsdb_id),
                                                      headers=headers)

generic_clear_3mm_glass = pywincalc.parse_json(generic_clear_3mm_glass_igsdb_response.content)
generic_clear_6mm_glass = pywincalc.parse_json(generic_clear_6mm_glass_igsdb_response.content)

# Create a glazing system using the NFRC U environment in order to get NFRC U results
# U and SHGC can be caculated for any given environment.  In order to get NFRC U and SHGC results the systems must
# use the standard NFRC U and SHGC environments
# The NFRC U and SHGC environments are provided as already constructed environments.
# Glazing_System defaults to using the NFRC U environment
glazing_system_u_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                     solid_layers=[generic_clear_6mm_glass, generic_clear_3mm_glass],
                                                     gap_layers=[gap_1],
                                                     width_meters=glazing_system_width,
                                                     height_meters=glazing_system_height,
                                                     environment=pywincalc.nfrc_u_environments())

glazing_system_shgc_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                        solid_layers=[generic_clear_6mm_glass, generic_clear_3mm_glass],
                                                        gap_layers=[gap_1],
                                                        width_meters=glazing_system_width,
                                                        height_meters=glazing_system_height,
                                                        environment=pywincalc.nfrc_shgc_environments())

results_name = "Results for a double-layer system of clear glass downloaded from the IGSDB"
print("*" * len(results_name))
print(results_name)
print("*" * len(results_name))
results_printer.print_results(glazing_system_u_environment, glazing_system_shgc_environment)
