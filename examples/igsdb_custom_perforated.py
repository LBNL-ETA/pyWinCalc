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

# A woven shade requires a BSDF hemisphere.  Create one based on a standard quarter basis for this test
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.QUARTER)

# This is the same material used in the venetian example but could be any material in the igsdb
shade_material_igsdb_id = 14477

shade_material_igsdb_response = requests.get(
    url_single_product.format(id=shade_material_igsdb_id), headers=headers)

shade_material = pywincalc.parse_json(shade_material_igsdb_response.content)

# Perforated screens need Perforated_Geometry.
# Make a rectangular perforation here.  Other options include circular and square
# Note: While using a string for perforation type is not ideal it is used here because this
# example is mostly using data from the IGSDB for the material and only adding a custom geometry
# For an example where the data is completely custom generated see custom_perforated.py
perforation_type = pywincalc.PerforatedGeometry.Type.RECTANGULAR
spacing_x = 0.01  # 10mm horizontal spacing
spacing_y = 0.02  # 20mm vertical spacing
dimension_x = 0.002  # 2mm perforation in the horizontal direction
dimension_y = 0.003  # 3mm perforation in the vertical direction
geometry = pywincalc.PerforatedGeometry(spacing_x, spacing_y, dimension_x, dimension_y, perforation_type)

# Create a layer from the geometry and parsed shade material data using pywincalc.create_perforated_screen
perforated_shade_layer = pywincalc.create_perforated_screen(geometry=geometry, parsed_material=shade_material)

# Create a glazing system using the NFRC U environment in order to get NFRC U results
# U and SHGC can be caculated for any given environment but in order to get results
# The NFRC U and SHGC environments are provided as already constructed environments and Glazing_System
# defaults to using the NFRC U environments
glazing_system_u_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                       solid_layers=[perforated_shade_layer],
                                                       width_meters=glazing_system_width,
                                                       height_meters=glazing_system_height,
                                                       environment=pywincalc.nfrc_u_environments(),
                                                       bsdf_hemisphere=bsdf_hemisphere)

glazing_system_shgc_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                          solid_layers=[perforated_shade_layer],
                                                          width_meters=glazing_system_width,
                                                          height_meters=glazing_system_height,
                                                          environment=pywincalc.nfrc_shgc_environments(),
                                                          bsdf_hemisphere=bsdf_hemisphere)

results_name = "Results for a single-layer system with a custom perforated screen made from a material downloaded from the IGSDB and a user-defined geometry."
print("*" * len(results_name))
print(results_name)
print("*" * len(results_name))
results_printer.print_results(glazing_system_u_environment, glazing_system_shgc_environment)
