import pywincalc

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
gap_1 = pywincalc.Gap(pywincalc.PredefinedGasType.AIR, .0127)  # .0127 is gap thickness in meters

# 
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.FULL)

# Load solid layer measured values.  Solid layer information can come from either igsdb.lbl.gov or files generate
# by the Optics program.  Since igsdb.lbl.gov requires registration some optics files are provided for example
# purposes
clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

bsdf_path = "products/2011-SA1.XML"
bsdf_shade = pywincalc.parse_bsdf_xml_file(bsdf_path)

# The above line just returns a parsed file.
# Thermal openings are not included in the file contents (with the exception of
# permeability factor which is used for front openness).  To set other thermal
# openings the parsed object needs to be converted to a solid layer.

bsdf_shade = pywincalc.convert_to_solid_layer(bsdf_shade)

# Once there is a solid layer the thermal openings can be set in the layer's thermal_data
bsdf_shade.thermal_data.opening_top = .01  # Top opening in meters (10mm)
bsdf_shade.thermal_data.opening_bottom = .01  # Bottom opening in meters (10mm)
bsdf_shade.thermal_data.opening_left = 0
bsdf_shade.thermal_data.opening_right = 0

# Create a glazing system using the NFRC SHGC environment to calculate SHGC
# based on NFRC SHGC conditions
glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                         solid_layers=[clear_3, bsdf_shade],
                                         gap_layers=[gap_1],
                                         width_meters=glazing_system_width,
                                         height_meters=glazing_system_height,
                                         environment=pywincalc.nfrc_shgc_environments(),
                                         bsdf_hemisphere=bsdf_hemisphere)

shgc = glazing_system.shgc()
print("NFRC SHGC for top and bottom openings of 10mm: {v}".format(v=shgc))

# Set the environments to NFRC U to get a U value calculated based on NFRC U conditions
glazing_system.environments(pywincalc.nfrc_u_environments())
u_value = glazing_system.u()
print("NFRC U for top and bottom openings of 10mm: {v}".format(v=u_value))

solar_optical_results = glazing_system.optical_method_results("SOLAR")
print("Solar direct-hemispherical front transmittance: {v}".format(
    v=solar_optical_results.system_results.front.transmittance.direct_hemispherical))

visible_optical_results = glazing_system.optical_method_results("PHOTOPIC")
print("Visible direct-hemispherical front transmittance: {v}".format(
    v=visible_optical_results.system_results.front.transmittance.direct_hemispherical))
