import pywincalc
import requests
from igsdb_interaction import url_single_product, headers

# This shows an example of how to create a perforated screen using shade material data download from
# igsdb.lbl.gov and user-defined perforated geometry.

# This is the same material used in the venetian example but could be any material in the igsdb
shade_material_igsdb_id = 17935

shade_material_igsdb_response = requests.get(
    url_single_product.format(id=shade_material_igsdb_id), headers=headers)

shade_material = pywincalc.parse_json(shade_material_igsdb_response.content)

# Perforated screens need Perforated_Geometry.
# Make a rectangular perforation here.  Other options include circular and square
# For an example where the data is completely custom generated see perforated_screen_user_defined_geometry_and_user_defined_nband_material.py
# Create perforated geometry 
perforation_type = pywincalc.PerforatedGeometry.Type.RECTANGULAR
spacing_x = .02  # 20mm horizontal spacing
spacing_y = .03  # 30mm vertical spacing
dimension_x = .001  # 1mm perforation in the horizontal direction
dimension_y = .003  # 3mm perforation in the vertical direction
geometry = pywincalc.PerforatedGeometry(spacing_x, spacing_y, dimension_x, dimension_y, perforation_type)

# Create a perforated layer from the geometry and matrial data
perforated_layer = pywincalc.create_perforated_screen(geometry=geometry, material=shade_material)

# If there are any side gaps in the shade those can be set in the thermal part of the solid layer
# These are gaps in addition to any perforations.  If the shade is flush with the sides of the
# glazing system disregarding any perforations this step can be omitted.
# These values are for example purposes only.
perforated_layer.thermal_data.opening_top = .01  # 10mm top gap
perforated_layer.thermal_data.opening_bottom = .01  # 10mm bottom gap
perforated_layer.thermal_data.opening_left = .02  # 20mm left gap
perforated_layer.thermal_data.opening_right = .02  # 20mm right gap

# A perforated shade requires a BSDF hemisphere.  Create one based on a standard quarter basis for this example
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.QUARTER)

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default NFRC standard and environmental conditions.
#
# For more possible results see:
# - optical_results_NFRC.py for all optical results available in the default NFRC optical standard
# - thermal_results_ISO_15099.py for all thermal results available.
# - deflection.py for additional results when deflection calculations are enabled
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.GlazingSystem(solid_layers=[perforated_layer], bsdf_hemisphere=bsdf_hemisphere)

u_value = glazing_system.u()
print(
    "U-value for a perforated screen made from user-defined geometry and a material downloaded from igsdb.lbl.glv: {v}".format(
        v=u_value))
