import pywincalc

# This example shows how to create a Venetian blind from user-defined dual-band shade
# # material data and user-defined Venetian blind geometry.

# Create dual-band optical data for the material.  All numbers are for example purposes only
shade_material_optical = pywincalc.ProductDataOpticalDualBandHemispheric(solar_transmittance_front=0,
                                                                         solar_transmittance_back=0,
                                                                         solar_reflectance_front=0.7,
                                                                         solar_reflectance_back=0.7,
                                                                         visible_transmittance_front=0,
                                                                         visible_transmittance_back=0,
                                                                         visible_reflectance_front=0.7,
                                                                         visible_reflectance_back=0.7,
                                                                         thickness_meters=0.001,
                                                                         ir_transmittance_front=0,
                                                                         ir_transmittance_back=0,
                                                                         emissivity_front=0.8,
                                                                         emissivity_back=0.8,
                                                                         flipped=False)

# Venetian blinds need a Venetian_Geometry.
slat_width = .020  # width of 20 mm
slat_spacing = .050  # spacing of 50 mm
slat_curvature = .025  # curvature of 25 mm
slat_tilt = 15  # 15 degree tilt
# distribution_method can be omitted and defaults to directional diffuse.  Uniform diffuse is also supported
distribution_method = pywincalc.DistributionMethodType.UNIFORM_DIFFUSE
# number_slat_segments can be omitted and defaults to 5.  Do not change unless there is a reason to.
# Included here only for completeness purposes
number_slat_segments = 5
geometry = pywincalc.VenetianGeometry(slat_width_meters=slat_width,
                                      slat_spacing_meters=slat_spacing,
                                      slat_curvature_meters=slat_curvature,
                                      slat_tilt_degrees=slat_tilt,
                                      number_slat_segments=number_slat_segments,
                                      distribution_method=distribution_method,
                                      is_horizontal=True)

# Create a venetian layer from the geometry and material data.
# NOTE:  Since this example only calculates an optical result thermal data can be omitted
# To calculate thermal results product_data_thermal must also be supplied.
# See perforated_screen_user_defined_geometry_and_user_defined_nband_material.py for an example
# of creating thermal data for shade materials
venetian_layer = pywincalc.create_venetian_blind(geometry=geometry,
                                                 material_data_optical=shade_material_optical,
                                                 material_data_thermal=None)

# A woven shade requires a BSDF hemisphere.  Create one based on a standard quarter basis for this test
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.FULL)

# Create a glazing system
glazing_system = pywincalc.GlazingSystem(solid_layers=[venetian_layer], bsdf_hemisphere=bsdf_hemisphere)

solar_results = glazing_system.optical_method_results("SOLAR")
tf_sol_hemispheric = solar_results.system_results.front.transmittance.direct_hemispherical
print("Front hemispheric transmittance for solar: {v}".format(v=tf_sol_hemispheric))
