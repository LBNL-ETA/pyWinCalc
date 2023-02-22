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

# A woven shade requires a BSDF hemisphere.  Create one based on a standard quarter basis for this test
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.QUARTER)

# Download some product data from the IGSDB.  This example gets a generic single clear 3mm glazing (NFRC 102),
# and a material to use as part of the woven shade.
generic_clear_3mm_glass_igsdb_id = 363

# This is the same material used in the venetian example but could be any material in the igsdb
shade_material_igsdb_id = 14477

generic_clear_3mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_3mm_glass_igsdb_id),
                                                      headers=headers)
shade_material_igsdb_response = requests.get(
    url_single_product.format(id=shade_material_igsdb_id), headers=headers)

generic_clear_3mm_glass = pywincalc.parse_json(generic_clear_3mm_glass_igsdb_response.content)

shade_material = pywincalc.parse_json(shade_material_igsdb_response.content)

# Woven shades need Woven_Geometry.
thread_diameter = 0.002  # 2mm diameter
thread_spacing = 0.003  # 3mm spacing
shade_thickness = 0.002  # 2mm shade thickness
geometry = pywincalc.WovenGeometry(thread_diameter, thread_spacing, shade_thickness)

# Convert the parsed shade data into a solid layer and then replace the optical portion 
# with a ProductDataOpticalWovenShade object made from the material's optical data and geometry.
woven_layer = pywincalc.convert_to_solid_layer(shade_material)
woven_layer.optical_data = pywincalc.ProductDataOpticalWovenShade(woven_layer.optical_data, geometry)

# If there are any side gaps in the shade those can be set in the thermal part of the solid layer
# These values are for example purposes only
woven_layer.thermal_data.opening_bottom = .01 # 10mm bottom gap
woven_layer.thermal_data.opening_left = .02 # 20mm left gap
woven_layer.thermal_data.opening_right = .02 # 20mm right gap

# Create a glazing system using the NFRC U environment in order to get NFRC U results
# U and SHGC can be caculated for any given environment but in order to get results
# The NFRC U and SHGC environments are provided as already constructed environments and Glazing_System
# defaults to using the NFRC U environments
glazing_system_u_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                       solid_layers=[woven_layer, generic_clear_3mm_glass],
                                                       gap_layers=[gap_1],
                                                       width_meters=glazing_system_width,
                                                       height_meters=glazing_system_height,
                                                       environment=pywincalc.nfrc_u_environments(),
                                                       bsdf_hemisphere=bsdf_hemisphere)

glazing_system_shgc_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                          solid_layers=[woven_layer, generic_clear_3mm_glass],
                                                          gap_layers=[gap_1],
                                                          width_meters=glazing_system_width,
                                                          height_meters=glazing_system_height,
                                                          environment=pywincalc.nfrc_shgc_environments(),
                                                          bsdf_hemisphere=bsdf_hemisphere)

results_name = "Results for a double-layer system with a custom exterior woven shade made from a material downloaded from the IGSDB"
print("*" * len(results_name))
print(results_name)
print("*" * len(results_name))
results_printer.print_results(glazing_system_u_environment, glazing_system_shgc_environment)
