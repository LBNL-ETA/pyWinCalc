import pywincalc
import requests

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
gap_1 = pywincalc.Gap_Data(pywincalc.Predefined_Gas_Type.AIR, .0127)  # .0127 is gap thickness in meters

# A woven shade requires a BSDF hemisphere.  Create one based on a standard quarter basis for this test
bsdf_hemisphere = pywincalc.BSDF_Hemisphere.create(pywincalc.BSDF_Basis.Quarter)

# Download some product data from the IGSDB.  This example gets a generic single clear 3mm glazing (NFRC 102),
# and a material to use as part of the woven shade.
# For more information on getting data from the igsdb please see igsdb.lbl.gov/openapi
igsdb_api_token = "INSERT_YOUR_TOKEN_HERE"
url_single_product = "https://igsdb-development.herokuapp.com/api/v1/products/{id}"  # Template URL for single product

headers = {"Authorization": "Token {token}".format(token=igsdb_api_token)}  # Token authorization headers

generic_clear_3mm_glass_igsdb_id = 363

# This is the same material used in the venetian in the igsdb_exterior_shade_on_cleara_glass.py example
# but could be any material in the igsdb
shade_material_igsdb_id = 12852

generic_clear_3mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_3mm_glass_igsdb_id),
                                                      headers=headers)
shade_material_igsdb_response = requests.get(
    url_single_product.format(id=shade_material_igsdb_id), headers=headers)

generic_clear_3mm_glass = pywincalc.parse_json(generic_clear_3mm_glass_igsdb_response.content)

shade_material = pywincalc.parse_json(shade_material_igsdb_response.content)

# Ventian blinds need a Venetian_Geometry.
slat_width = .020  # width of 20 mm
slat_spacing = .050  # spacing of 50 mm
slat_curvature = .025  # curvature of 25 mm
slat_tilt = 15  # 15 degree tilt
number_segments = 7  # Not sure what to say here.  The default is 5 but I do not know what impact changing this has
geometry = pywincalc.Venetian_Geometry(slat_width, slat_spacing, slat_curvature, slat_tilt, number_segments)

# combine the shade_material and the geometry together into a Product_Composistion_Data
composition_data = pywincalc.Product_Composistion_Data(shade_material, geometry)
venetian_layer = pywincalc.Composed_Product_Data(composition_data)

# At this point the layer is only using measured value and any modeling parameters.
# To change modeling parameters from their default the measured data must first be converted to
# a solid layer.
venetian_solid_layer = pywincalc.convert_to_solid_layer(venetian_layer)

# Currently the only modeling parameter for venetian layers is the distribution method.
# That defaults to directional diffuse but can be changed to uniform-diffuse on a per-layer basis
venetian_solid_layer.optical_data.distribution_method = pywincalc.Distribution_Method.Uniform_Diffuse

# Create a glazing system using the NFRC U environment in order to get NFRC U results
# U and SHGC can be caculated for any given environment but in order to get results
# The NFRC U and SHGC environments are provided as already constructed environments and Glazing_System
# defaults to using the NFRC U environments
exterior_venetian_nfrc_u_environment = pywincalc.Glazing_System([venetian_solid_layer, generic_clear_3mm_glass],
                                                                [gap_1],
                                                                optical_standard, glazing_system_width,
                                                                glazing_system_height,
                                                                pywincalc.nfrc_u_environments(), bsdf_hemisphere)

exterior_venetian_nfrc_shgc_environment = pywincalc.Glazing_System(
    [venetian_solid_layer, generic_clear_3mm_glass], [gap_1],
    optical_standard, glazing_system_width, glazing_system_height,
    pywincalc.nfrc_shgc_environments(), bsdf_hemisphere)

exterior_venetian_nfrc_u = exterior_venetian_nfrc_u_environment.u()
print("Exterior venetian NFRC U: {v}".format(v=exterior_venetian_nfrc_u))
exterior_venetian_nfrc_shgc = exterior_venetian_nfrc_shgc_environment.shgc()
print("Exterior venetian NFRC SHGC: {v}".format(v=exterior_venetian_nfrc_shgc))
