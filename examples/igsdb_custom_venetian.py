import pywincalc
import requests
from igsdb_interaction import url_single_product, headers

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

# This is the same material used in the venetian in the igsdb_exterior_shade_on_cleara_glass.py example
# but could be any material in the igsdb
shade_material_igsdb_id = 14477

shade_material_igsdb_response = requests.get(
    url_single_product.format(id=shade_material_igsdb_id), headers=headers)

shade_material = pywincalc.parse_json(shade_material_igsdb_response.content)

# Venetian blinds need a Venetian_Geometry.
slat_width = .020  # width of 20 mm
slat_spacing = .050  # spacing of 50 mm
slat_curvature = .025  # curvature of 25 mm
slat_tilt = 15  # 15 degree tilt
number_segments = 5  # The default is 5.  Do not change unless there is a reason to.
# Currently the only modeling parameter for venetian layers is the distribution method.
# That defaults to directional diffuse but can be changed to uniform-diffuse on a per-layer basis
distribution_method = pywincalc.DistributionMethodType.UNIFORM_DIFFUSE
geometry = pywincalc.VenetianGeometry(slat_width_meters=slat_width,
                                      slat_spacing_meters=slat_spacing,
                                      slat_curvature_meters=slat_curvature,
                                      slat_tilt_degrees=slat_tilt,
                                      number_slat_segments=number_segments,
                                      distribution_method=distribution_method)

# Create a layer from the geometry and material
venetian_layer = pywincalc.create_venetian_blind(geometry=geometry, material=shade_material)

# If there are any side gaps in the shade those can be set in the thermal part of the solid layer.
# In this case the left and right openings would apply if the length of the slats was less than the width
# of the glazing system and the top and bottom openings would apply if the top and bottom slats did not
# sit flush with the top and bottom of the glazing system when the slats are closed.
# Do not take slat angle into account for these values.
# These values are for example purposes only
venetian_layer.thermal_data.opening_top = .01  # 10mm top gap
venetian_layer.thermal_data.opening_bottom = .01  # 10mm bottom gap
venetian_layer.thermal_data.opening_left = .02  # 20mm left gap
venetian_layer.thermal_data.opening_right = .02  # 20mm right gap

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see all_NFRC_results.py
#
# For more on environmental conditions see custom_environmental_conditions.py
glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                         solid_layers=[venetian_layer],
                                         gap_layers=[],
                                         width_meters=glazing_system_width,
                                         height_meters=glazing_system_height,
                                         bsdf_hemisphere=bsdf_hemisphere)

u_value = glazing_system.u()
print(
    "U-value for a custom Venetian blind made from a material downloaded from igsdb.lbl.glv: {v}".format(v=u_value))
