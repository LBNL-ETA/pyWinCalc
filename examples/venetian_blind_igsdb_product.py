import pywincalc
import requests
from igsdb_interaction import url_single_product, headers

# Since these products use at least one layer that requires a BSDF model a BSDF hemisphere must be
# used.  In this example a standard quarter basis is used.  Other predefined basis include Small, Half, and Full
# Custom BSDF basis is not yet supported in Python.  Please contact us if your work requires calculations with
# a custom BSDF basis.
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.QUARTER)

# Download a venetian blind from the igsdb.lbl.gov.
slim_white_pella_venetian_blind_igsdb_id = 17186

slim_white_pella_venetian_blind_igsdb_response = requests.get(
    url_single_product.format(id=slim_white_pella_venetian_blind_igsdb_id), headers=headers)

slim_white_pella_venetian_blind = pywincalc.parse_json(slim_white_pella_venetian_blind_igsdb_response.content)

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see optical_results_NFRC.py
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.GlazingSystem(solid_layers=[slim_white_pella_venetian_blind],
                                                 bsdf_hemisphere=bsdf_hemisphere)

u_value = glazing_system.u()
print("U-value for a Venetian blind downloaded from igsdb.lbl.glv: {v}".format(v=u_value))
