import pywincalc

# Load solid layer measured values.  Solid layer information can come from either igsdb.lbl.gov or files generate
# by the Optics program.  Since igsdb.lbl.gov requires registration some optics files are provided for example
# purposes
product_path = "products/sample_dir_dif.txt"
product = pywincalc.parse_optics_file(product_path)

solid_layers = [product]

bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.FULL)

glazing_system = pywincalc.GlazingSystem(solid_layers=solid_layers, bsdf_hemisphere=bsdf_hemisphere)

solar_results = glazing_system.optical_method_results("SOLAR")

print("System solar front transmittance direct-direct: {v}".format(
    v=solar_results.system_results.front.transmittance.direct_direct))
print("System solar front transmittance direct-diffuse: {v}".format(
    v=solar_results.system_results.front.transmittance.direct_diffuse))
print("System solar front transmittance direct-hemispherical: {v}".format(
    v=solar_results.system_results.front.transmittance.direct_hemispherical))