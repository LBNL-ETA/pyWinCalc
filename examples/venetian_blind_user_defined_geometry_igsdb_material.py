import pywincalc
import requests
from igsdb_interaction import url_single_product, headers

# This example shows how to create a Venetian blind from a user-defined Venetian geometry
# and shade material data download from igsdb.lbl.gov

# This is the same material used in the venetian in the igsdb_exterior_shade_on_cleara_glass.py example
# but could be any material in the igsdb
shade_material_igsdb_id = 14477

shade_material_igsdb_response = requests.get(url_single_product.format(id=shade_material_igsdb_id), headers=headers)

shade_material = pywincalc.parse_json(shade_material_igsdb_response.content)

# Venetian blinds need a Venetian_Geometry.
slat_width = .020  # width of 20 mm
slat_spacing = .050  # spacing of 50 mm
slat_curvature = .025  # curvature of 25 mm
slat_tilt = 15  # 15 degree tilt
# distribution_method can be omitted and defaults to directional diffuse.  Uniform diffuse is also supported
distribution_method = pywincalc.DistributionMethodType.UNIFORM_DIFFUSE
# number_slat_segments can be omitted and defaults to 5.  Do not change unless there is a reason to.
# Included here only for completeness purposes
number_slat_segments = 5
geometry = pywincalc.VenetianGeometry(slat_width_meters=slat_width,
                                      slat_spacing_meters=slat_spacing,
                                      slat_curvature_meters=slat_curvature,
                                      slat_tilt_degrees=slat_tilt,
                                      number_slat_segments=number_slat_segments,
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

# A Venetian blind requires a BSDF hemisphere.  Create one based on a standard quarter basis for this example
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.QUARTER)

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see optical_results_NFRC.py
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.GlazingSystem(solid_layers=[venetian_layer], bsdf_hemisphere=bsdf_hemisphere)

u_value = glazing_system.u()
print(
    "U-value for a custom Venetian blind made from a material downloaded from igsdb.lbl.glv: {v}".format(v=u_value))
