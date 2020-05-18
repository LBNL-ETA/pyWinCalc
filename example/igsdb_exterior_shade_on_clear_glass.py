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

# Since these products use at least one layer that requires a BSDF model a BSDF hemisphere must be
# used.  In this example a standard quarter basis is used.  Other predefined basis include Small, Half, and Full
# Custom BSDF basis is not yet supported in Python.  Please contact us if your work requires calculations with
# a custom BSDF basis.
bsdf_hemisphere = pywincalc.BSDF_Hemisphere.create(pywincalc.BSDF_Basis.Quarter)

# Download some product data from the IGSDB.  This example gets a generic single clear 3mm glazing (NFRC 102),
# a venetian blind manufactured by Pella (CGDB ID 3000) and a perforated screen manufacturerd by Solar Comfort
# (CGDB ID 18000)
# For more information on getting data from the igsdb please see igsdb.lbl.gov/openapi
igsdb_api_token = "INSERT_YOUR_TOKEN_HERE"
url_single_product = "https://igsdb-development.herokumapp.com/api/v1/products/{id}"  # Template URL for single product

headers = {"Authorization": "Token {token}".format(token=igsdb_api_token)}  # Token authorization headers

generic_clear_3mm_glass_igsdb_id = 363
slim_white_pella_venetian_blind_igsdb_id = 12149
solar_comfort_radiant_barrier_perforated_screen_igsdb_id = 12295

generic_clear_3mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_3mm_glass_igsdb_id),
                                                      headers=headers)
slim_white_pella_venetian_blind_igsdb_response = requests.get(
    url_single_product.format(id=slim_white_pella_venetian_blind_igsdb_id), headers=headers)
solar_comfort_radiant_barrier_perforated_screen_igsdb_response = requests.get(
    url_single_product.format(id=solar_comfort_radiant_barrier_perforated_screen_igsdb_id), headers=headers)

generic_clear_3mm_glass = pywincalc.parse_json(generic_clear_3mm_glass_igsdb_response.content)
# NOTE:  By default venetian blinds are set to have a slat tilt of zero degrees
slim_white_pella_venetian_blind = pywincalc.parse_json(slim_white_pella_venetian_blind_igsdb_response.content)
# To change the slat tilt change the slat_tilt value in the geometry section of the product_composition information
# slim_white_pella_venetian_blind.composition_information.geometry.slat_tilt = 15
solar_comfort_radiant_barrier_perforated_screen = pywincalc.parse_json(
    solar_comfort_radiant_barrier_perforated_screen_igsdb_response.content)

# Create a glazing system using the NFRC U environment in order to get NFRC U results
# U and SHGC can be caculated for any given environment but in order to get results
# The NFRC U and SHGC environments are provided as already constructed environments and Glazing_System
# defaults to using the NFRC U environments
exterior_venetian_u_environment = pywincalc.Glazing_System([slim_white_pella_venetian_blind, generic_clear_3mm_glass],
                                                           [gap_1],
                                                           optical_standard, glazing_system_width,
                                                           glazing_system_height,
                                                           pywincalc.nfrc_u_environments(), bsdf_hemisphere)

exterior_venetian_shgc_environment = pywincalc.Glazing_System(
    [slim_white_pella_venetian_blind, generic_clear_3mm_glass], [gap_1],
    optical_standard, glazing_system_width, glazing_system_height,
    pywincalc.nfrc_shgc_environments(), bsdf_hemisphere)

exterior_perforated_u_environment = pywincalc.Glazing_System(
    [solar_comfort_radiant_barrier_perforated_screen, generic_clear_3mm_glass], [gap_1],
    optical_standard, glazing_system_width, glazing_system_height,
    pywincalc.nfrc_u_environments(), bsdf_hemisphere)

exterior_perforated_shgc_environment = pywincalc.Glazing_System(
    [solar_comfort_radiant_barrier_perforated_screen, generic_clear_3mm_glass], [gap_1],
    optical_standard, glazing_system_width, glazing_system_height,
    pywincalc.nfrc_shgc_environments(), bsdf_hemisphere)

exterior_venetian_u = exterior_venetian_u_environment.u()
print("Exterior venetian U: {v}".format(v=exterior_venetian_u))
exterior_venetian_shgc = exterior_venetian_shgc_environment.shgc()
print("Exterior venetian SHGC: {v}".format(v=exterior_venetian_shgc))

exterior_perforated_u = exterior_perforated_u_environment.u()
print("Exterior perforated screen U: {v}".format(v=exterior_perforated_u))
exterior_perforated_shgc = exterior_perforated_shgc_environment.shgc()
print("Exterior perforated screen SHGC: {v}".format(v=exterior_perforated_shgc))
