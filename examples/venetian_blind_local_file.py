import pywincalc

# Since these products use at least one layer that requires a BSDF model a BSDF hemisphere must be
# used.  In this example a standard quarter basis is used.  Other predefined basis include Small, Half, and Full
# Custom BSDF basis is not yet supported in Python.  Please contact us if your work requires calculations with
# a custom BSDF basis.
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.FULL)

# Download some product data from the IGSDB.  This example gets a generic single clear 3mm glazing (NFRC 102),
# a venetian blind manufactured by Pella (CGDB ID 3000) and a perforated screen manufacturerd by Solar Comfort
# (CGDB ID 18000)
slim_white_pella_venetian_blind = pywincalc.parse_json_file("products/venetian_blind_CGDB_22034.json")

# Create a glazing system using the NFRC U environment in order to get NFRC U results
# U and SHGC can be caculated for any given environment but in order to get results
# The NFRC U and SHGC environments are provided as already constructed environments and Glazing_System
# defaults to using the NFRC U environments

glazing_system = pywincalc.create_glazing_system(solid_layers=[slim_white_pella_venetian_blind],
                                                 bsdf_hemisphere=bsdf_hemisphere)

u_value = glazing_system.u()
print("U-value for Venetian blind loaded from a local file: {v}".format(v=u_value))
