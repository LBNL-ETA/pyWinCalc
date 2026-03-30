import pywincalc

# Create a BSDF hemisphere for the optical calculations
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.SMALL)

# Load a BSDF shade and a clear glass
bsdf_path = "products/2011-SA1.XML"
bsdf_shade = pywincalc.parse_bsdf_xml_file(bsdf_path)

clear_glass_path = "products/CLEAR_3.DAT"
clear_glass = pywincalc.parse_optics_file(clear_glass_path)

# Create a double-layer glazing system: clear glass + BSDF shade
gap = pywincalc.Layers.gap(thickness=0.0127)
glazing_system = pywincalc.GlazingSystem(
    solid_layers=[clear_glass, bsdf_shade],
    gap_layers=[gap],
    bsdf_hemisphere=bsdf_hemisphere
)


def print_matrix(matrix, indent="    "):
    data = matrix.get_matrix()
    for row in data:
        print(indent + "  ".join(f"{val:10.6f}" for val in row))


def print_wavelength_matrices(label, matrices):
    if matrices is None:
        return
    print(f"\n  {label}: {len(matrices)} wavelength matrices")
    for mat_at_wl in matrices:
        size = mat_at_wl.matrix.size()
        print(f"\n    wavelength = {mat_at_wl.wavelength:.4f} um, matrix {size}x{size}:")
        print_matrix(mat_at_wl.matrix)


# Get standard optical results (fast)
method_name = "SOLAR"
optical_results = glazing_system.optical_method_results(method_name)

print("System transmittance (direct-direct):",
      optical_results.system_results.front.transmittance.direct_direct)
print("System reflectance (direct-direct):",
      optical_results.system_results.front.reflectance.direct_direct)

# Print system-level wavelength matrices
print("\n=== System wavelength matrices ===")
sys_front = optical_results.system_results.front
if sys_front.transmittance.wavelength_matrices is not None:
    print_wavelength_matrices("System front transmittance",
                              sys_front.transmittance.wavelength_matrices)
if sys_front.reflectance.wavelength_matrices is not None:
    print_wavelength_matrices("System front reflectance",
                              sys_front.reflectance.wavelength_matrices)

# Compute per-layer wavelength matrices on demand (expensive)
glazing_system.populate_layer_wavelength_matrices(optical_results, method_name)

# Print per-layer wavelength matrices
print("\n=== Per-layer wavelength matrices ===")
for idx, layer_result in enumerate(optical_results.layer_results):
    print(f"\nLayer {idx}:")
    print_wavelength_matrices("Front transmittance",
                              layer_result.front.transmittance_wavelength_matrices)
    print_wavelength_matrices("Front reflectance",
                              layer_result.front.reflectance_wavelength_matrices)
    print_wavelength_matrices("Back transmittance",
                              layer_result.back.transmittance_wavelength_matrices)
    print_wavelength_matrices("Back reflectance",
                              layer_result.back.reflectance_wavelength_matrices)
