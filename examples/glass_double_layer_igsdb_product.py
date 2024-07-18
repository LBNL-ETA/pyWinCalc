import pywincalc
import requests
from igsdb_interaction import url_single_product, headers

# Define the gap between the shade and the glazing.  In this case use a default air gap
# that is 12.7mm thick.  For more on creating gases and gaps see the gaps_and_gases.py example
gap_1 = pywincalc.layers.gap(thickness=.0127)

# Download some product data from the IGSDB.  This example gets a generic single clear 3mm glazing (NFRC 102),
# and a generic single clear 6mm glazing (NFRC 103)
generic_clear_3mm_glass_igsdb_id = 363
generic_clear_6mm_glass_igsdb_id = 362

generic_clear_3mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_3mm_glass_igsdb_id),
                                                      headers=headers)
generic_clear_6mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_6mm_glass_igsdb_id),
                                                      headers=headers)

generic_clear_3mm_glass = pywincalc.parse_json(generic_clear_3mm_glass_igsdb_response.content)
generic_clear_6mm_glass = pywincalc.parse_json(generic_clear_6mm_glass_igsdb_response.content)

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see optical_results_NFRC.py
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.GlazingSystem(solid_layers=[generic_clear_6mm_glass, generic_clear_3mm_glass],
                                                 gap_layers=[gap_1])

u_value = glazing_system.u()
print("U-value for a double-layer system with glass downloaded from igsdb.lbl.glv: {v}".format(v=u_value))
