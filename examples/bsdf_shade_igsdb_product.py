import pywincalc
import requests
from igsdb_interaction import url_single_product, headers, url_single_product_datafile

bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.FULL)

bsdf_igsdb_id = 14710

bsdf_igsdb_response = requests.get(url_single_product_datafile.format(id=bsdf_igsdb_id), headers=headers)

# The BSDF data is currently stored as XML on igsdb.lbl.gov.  As a result it needs to be
# parsed using the xml string parser instead of the json parser
bsdf_shade = pywincalc.parse_bsdf_xml_string(bsdf_igsdb_response.content)

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see optical_results_NFRC.py
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.create_glazing_system(solid_layers=[bsdf_shade], bsdf_hemisphere=bsdf_hemisphere)

u_value = glazing_system.u()
print("U-value for a BSDF shade downloaded from igsdb.lbl.glv: {v}".format(v=u_value))
