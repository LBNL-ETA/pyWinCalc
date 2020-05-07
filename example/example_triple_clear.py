import pywincalc

# Path to the optical standard file.  All other files referenced by the standard file must be in the same directory
# Note:  While all optical standards packaged with WINDOW should work with optical calculations care should be
# taken to use NFRC standards if thermal results are desired.  This is because for thermal calculations currently
# only ISO 15099 is supported.  So while it is possible to use EN optical standards and create thermal results
# those results will not be based on EN 673
optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

width = 1.0  # width of the glazing system in meters
height = 1.0  # height of the glazing system in meters

# Load solid layer measured values.  Solid layer information can come from either igsdb.lbl.gov or files generate
# by the Optics program.  Since igsdb.lbl.gov requires registration some optics files are provided for example
# purposes
clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

clear_6_path = "products/CLEAR_6.DAT"
clear_6 = pywincalc.parse_optics_file(clear_6_path)

# Create a list of solid layers in order from outside to inside
# This is a triple glazing where the outside and inside are the glass
# that was just loaded and the middle is the same glass as the single clear example above
solid_layers = [clear_6, clear_3, clear_6]

# Solid layers must be separated by gap layers
# Currently there are four pre-defined gases available: Air, Argon, Krypton, and Xenon
# Vacuum gaps are not yet supported
# To create a gap with 100% of a predefined gas create a Gap_Data object with the gas type
# and thickness in meters
gap_1 = pywincalc.Gap_Data(pywincalc.Predefined_Gas_Type.AIR, .0127)  # .0127 is gap thickness in meters

# To create a mixture of predefined gases first create the components with the gas type and portion of the mixture
# The following creates a gas that is 70% Krypton and 30% Xenon and 2cm thick
gap_2_component_1 = pywincalc.Predefined_Gas_Mixture_Component(pywincalc.Predefined_Gas_Type.KRYPTON, .7)
gap_2_component_2 = pywincalc.Predefined_Gas_Mixture_Component(pywincalc.Predefined_Gas_Type.XENON, .3)
gap_2 = pywincalc.Gap_Data([gap_2_component_1, gap_2_component_2], .02)  # .02 is gap thickness in meters

# Put all gaps into a list ordered from outside to inside
# Note:  This is only specifying gaps between solid layers
# Gases on the interior and exterior of the glazing system are more fixed and only subject to
# change based on the properties in the environmental conditions
gaps = [gap_1, gap_2]

# Create a triple layer glazing system
glazing_system_triple_layer_u_environment = pywincalc.Glazing_System(solid_layers, gaps, optical_standard, width,
                                                                     height)
print("U-value: {u}".format(u=glazing_system_triple_layer_u_environment.u()))
# If SHGC results for the NFRC SHGC environment are needed create a glazing system with that environment
glazing_system_triple_layer_shgc_environment = pywincalc.Glazing_System(solid_layers, gaps, optical_standard, width,
                                                                        height,
                                                                        pywincalc.nfrc_shgc_environments())
print("SHGC: {shgc}".format(shgc=glazing_system_triple_layer_shgc_environment.shgc()))

# Get the results the same way as in example_single_clear.py.
# The only difference is in this case since there are multiple layers there are
# multiple layer results for optical methods
solar_results = glazing_system_triple_layer_u_environment.optical_method_results(pywincalc.Optical_Method_Type.SOLAR)
# In this case since there are multiple layers there are multiple layer results
solar_results_per_layer = solar_results.layer_results
# Print some of the layer solar absorptances
print("Triple clear layer 1 front direct solar absorptance: {v}".format(
    v=solar_results_per_layer[0].front.absorptance.direct))
print("Triple clear layer 1 back diffuse solar absorptance: {v}".format(
    v=solar_results_per_layer[0].back.absorptance.diffuse))
print("Triple clear layer 2 front direct solar absorptance: {v}".format(
    v=solar_results_per_layer[1].front.absorptance.direct))
print("Triple clear layer 2 back diffuse solar absorptance: {v}".format(
    v=solar_results_per_layer[1].back.absorptance.diffuse))
print("Triple clear layer 3 front direct solar absorptance: {v}".format(
    v=solar_results_per_layer[2].front.absorptance.direct))
print("Triple clear layer 3 back diffuse solar absorptance: {v}".format(
    v=solar_results_per_layer[2].back.absorptance.diffuse))
# etc...

# Custom gases are also available.  Mixing custom gases and predefined gases is not yet supported
# TODO Create example using custom gases
