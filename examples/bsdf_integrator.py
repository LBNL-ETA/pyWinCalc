import pywincalc

bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.FULL)

bsdf_path = "products/2011-SA1.XML"
bsdf_shade = pywincalc.parse_bsdf_xml_file(bsdf_path)

front_transmittance_matrix = pywincalc.SquareMatrix(bsdf_shade.measurements.solar.transmittance_front.data)
front_reflectance_matrix = pywincalc.SquareMatrix(bsdf_shade.measurements.solar.reflectance_front.data)

integrator = pywincalc.BSDFIntegrator(bsdf_hemisphere.get_directions(pywincalc.BSDFDirection.Incoming))
integrator.set_matrices(front_transmittance_matrix, front_reflectance_matrix, pywincalc.Side.Front)

front_hemispheric_transmittances = integrator.direct_hemispheric(pywincalc.Side.Front, pywincalc.PropertySimple.T)
front_hemispheric_reflectances = integrator.direct_hemispheric(pywincalc.Side.Front, pywincalc.PropertySimple.R)

print("Front hemipsheric transmittances for each incoming angle: {v}".format(v=front_hemispheric_transmittances))
print("Front hemipsheric reflectances for each incoming angle: {v}".format(v=front_hemispheric_reflectances))
