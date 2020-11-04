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
gap_1 = pywincalc.Gap(pywincalc.PredefinedGasType.AIR, .0127)  # .0127 is gap thickness in meters

# 
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.FULL)

igsdb_api_token = "2aad63e52070a0cc92568d6e2b4e2d86f996595b"  # "INSERT_YOUR_TOKEN_HERE"
url_single_product = "https://igsdb-staging.herokuapp.com/api/v1/products/{id}"
# BSDF shade measured data is currently stored behind a "datafile" API endpoint
# on igsdb.lbl.gov.
url_single_product_datafile = "https://igsdb-staging.herokuapp.com/api/v1/products/{id}/datafile"  # Template URL for getting data file for a product

headers = {"Authorization": "Token {token}".format(token=igsdb_api_token)}  # Token authorization headers

generic_clear_3mm_glass_igsdb_id = 363
bsdf_igsdb_id = 12165

generic_clear_3mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_3mm_glass_igsdb_id),
                                                      headers=headers)

bsdf_igsdb_response = requests.get(
    url_single_product_datafile.format(id=bsdf_igsdb_id), headers=headers)

clear_3 = pywincalc.parse_json(generic_clear_3mm_glass_igsdb_response.content)

# The BSDF data is currently stored as XML on igsdb.lbl.gov.  As a result it needs to be
# parsed using the xml string parser instead of the json parser
bsdf_shade = pywincalc.parse_bsdf_xml_string(bsdf_igsdb_response.content)

# Create a glazing system using the NFRC U environment in order to get NFRC U results
# U and SHGC can be caculated for any given environment but in order to get results
# The NFRC U and SHGC environments are provided as already constructed environments and Glazing_System
# defaults to using the NFRC U environments
glazing_system_u_environment = pywincalc.GlazingSystem(optical_standard,
                                                       [clear_3, bsdf_shade],
                                                       [gap_1],
                                                       glazing_system_width,
                                                       glazing_system_height,
                                                       pywincalc.nfrc_u_environments(), bsdf_hemisphere)

glazing_system_shgc_environment = pywincalc.GlazingSystem(optical_standard,
                                                          [clear_3, bsdf_shade], [gap_1],
                                                          glazing_system_width, glazing_system_height,
                                                          pywincalc.nfrc_shgc_environments(), bsdf_hemisphere)

u = glazing_system_u_environment.u()
print("Exterior venetian U: {u}".format(u=u))
shgc = glazing_system_shgc_environment.shgc()
print("Exterior venetian SHGC: {shgc}".format(shgc=shgc))
