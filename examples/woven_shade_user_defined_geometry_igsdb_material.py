import pywincalc
import requests
from igsdb_interaction import url_single_product, headers

# This is the same material used in the venetian example but could be any material in the igsdb
shade_material_igsdb_id = 17935

shade_material_igsdb_response = requests.get(
    url_single_product.format(id=shade_material_igsdb_id), headers=headers)

shade_material = pywincalc.parse_json(shade_material_igsdb_response.content)

# Woven shades need Woven_Geometry.
thread_diameter = 0.002  # 2mm diameter
thread_spacing = 0.003  # 3mm spacing
shade_thickness = 0.002  # 2mm shade thickness
geometry = pywincalc.WovenGeometry(thread_diameter, thread_spacing, shade_thickness)

# Convert the parsed shade material data into a solid layer.  Without doing
# anything else this would be treated as a solid sheet of the material.
woven_layer = pywincalc.convert_to_solid_layer(
    shade_material)  # The easiest way to transform it into a Venetian blind is to replace the optical portion
# with a ProductDataOpticalWovenShade object made from the material's optical data
# and the user-defined geometry created above.
woven_layer.optical_data = pywincalc.ProductDataOpticalWovenShade(woven_layer.optical_data, geometry)

# If there are any side gaps in the shade those can be set in the thermal part of the solid layer
# These values are for example purposes only
woven_layer.thermal_data.opening_top = .01  # 10mm top gap
woven_layer.thermal_data.opening_bottom = .01  # 10mm bottom gap
woven_layer.thermal_data.opening_left = .02  # 20mm left gap
woven_layer.thermal_data.opening_right = .02  # 20mm right gap

# A woven shade requires a BSDF hemisphere.  Create one based on a standard quarter basis for this example
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.QUARTER)

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see optical_results_NFRC.py
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.GlazingSystem(solid_layers=[woven_layer],
                                                 bsdf_hemisphere=bsdf_hemisphere)

u_value = glazing_system.u()
print(
    "U-value for a woven shade made from a user-defined geometry and material downloaded from igsdb.lbl.glv: {v}".format(
        v=u_value))
