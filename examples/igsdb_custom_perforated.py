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
# For an example where the data is completely custom generated see custom_perforated.py
# Create perforated geometry 
perforation_type = pywincalc.PerforatedGeometry.Type.RECTANGULAR
spacing_x = .02  # 20mm horizontal spacing
spacing_y = .03  # 30mm vertical spacing
dimension_x = .001  # 1mm perforation in the horizontal direction
dimension_y = .003  # 3mm perforation in the vertical direction
geometry = pywincalc.PerforatedGeometry(spacing_x, spacing_y, dimension_x, dimension_y, perforation_type)

# Convert the parsed shade material data into a solid layer.  Without doing
# anything else this would be treated as a solid sheet of the material.
perforated_layer = pywincalc.convert_to_solid_layer(shade_material)
# The easiest way to transform it into a perforated screen is to replace the optical portion
# with a ProductDataOpticalPerforatedScreen object made from the material's optical data
# and the user-defined geometry created above.
perforated_layer.optical_data = pywincalc.ProductDataOpticalPerforatedScreen(perforated_layer.optical_data, geometry)

# If there are any side gaps in the shade those can be set in the thermal part of the solid layer
# These are gaps in addition to any perforations.  If the shade is flush with the sides of the
# glazing system disregarding any perforations this step can be omitted.
# These values are for example purposes only.
perforated_layer.thermal_data.opening_top = .01  # 10mm top gap
perforated_layer.thermal_data.opening_bottom = .01  # 10mm bottom gap
perforated_layer.thermal_data.opening_left = .02  # 20mm left gap
perforated_layer.thermal_data.opening_right = .02  # 20mm right gap

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see all_NFRC_results.py
#
# For more on environmental conditions see custom_environmental_conditions.py
glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                         solid_layers=[perforated_layer],
                                         gap_layers=[],
                                         width_meters=glazing_system_width,
                                         height_meters=glazing_system_height,
                                         bsdf_hemisphere=bsdf_hemisphere)

u_value = glazing_system.u()
print(
    "U-value for a custom perforated screen made from a material downloaded from igsdb.lbl.glv: {v}".format(v=u_value))
