import pywincalc

bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.FULL)

bsdf_path = "products/2011-SA1.XML"
bsdf_shade = pywincalc.parse_bsdf_xml_file(bsdf_path)

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see optical_results_NFRC.py
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.GlazingSystem(solid_layers=[bsdf_shade], bsdf_hemisphere=bsdf_hemisphere)

u_value = glazing_system.u()
print("U-value for a BSDF shade created from a local file: {v}".format(v=u_value))
