import pywincalc
import results_printer

# Currently there are four pre-defined gases available: Air, Argon, Krypton, and Xenon
# Vacuum gaps are not yet supported
# To create a gap with 100% of a predefined gas create a Gap_Data object with the gas type
# and thickness in meters
gap_1 = pywincalc.Gap(pywincalc.PredefinedGasType.AIR, .0127)  # .0127 is gap thickness in meters

# Gaps may also contain a mixture of gases.  # To create a mixture of predefined gases first create the
# components with the gas type and portion of the mixture.
# The following creates a gas that is 70% Krypton and 30% Xenon and 2cm thick
gap_2_component_1 = pywincalc.PredefinedGasMixtureComponent(pywincalc.PredefinedGasType.KRYPTON, .7)
gap_2_component_2 = pywincalc.PredefinedGasMixtureComponent(pywincalc.PredefinedGasType.XENON, .3)
gap_2 = pywincalc.Gap([gap_2_component_1, gap_2_component_2], .02)  # .02 is gap thickness in meters

# Custom gases can be created from properties.  The following creates sulfur hexafluoride as distributed with WINDOW 7
sulfur_hexafluoride_conductivity_a = 0.0130000002682209
sulfur_hexafluoride_conductivity_b = 0
sulfur_hexafluoride_conductivity_c = 0
sulfur_hexafluoride_conductivity_coefficients = pywincalc.GasCoefficients(sulfur_hexafluoride_conductivity_a,
                                                                          sulfur_hexafluoride_conductivity_b,
                                                                          sulfur_hexafluoride_conductivity_c)
sulfur_hexafluoride_viscosity_a = 7.21399999292771E-7
sulfur_hexafluoride_viscosity_b = 4.92800005247318E-8
sulfur_hexafluoride_viscosity_c = 0
sulfur_hexafluoride_viscosity_coefficients = pywincalc.GasCoefficients(sulfur_hexafluoride_viscosity_a,
                                                                       sulfur_hexafluoride_viscosity_b,
                                                                       sulfur_hexafluoride_viscosity_c)
sulfur_hexafluoride_Cp_a = 418.600006103516
sulfur_hexafluoride_Cp_b = 0
sulfur_hexafluoride_Cp_c = 0
sulfur_hexafluoride_Cp_coefficients = pywincalc.GasCoefficients(sulfur_hexafluoride_Cp_a,
                                                                sulfur_hexafluoride_Cp_b,
                                                                sulfur_hexafluoride_Cp_c)
sulfur_hexafluoride_molecular_weight = 146.100006103516
sulfur_hexafluoride_specific_heat_ratio = 1

sulfur_hexafluoride = pywincalc.CustomGasData("sulfur_hexafluoride",
                                              molecular_weight=sulfur_hexafluoride_molecular_weight,
                                              specific_heat_ratio=sulfur_hexafluoride_specific_heat_ratio,
                                              Cp=sulfur_hexafluoride_Cp_coefficients,
                                              thermal_conductivity=sulfur_hexafluoride_conductivity_coefficients,
                                              viscosity=sulfur_hexafluoride_viscosity_coefficients)

# Once a custom gas is created it can either be used by itself to create a layer
gap_3 = pywincalc.Gap(sulfur_hexafluoride, .003)  # 3mm thick gap filled with sulfur hexafluoride

# Or it can be mixed with either other predefined or custom gases
# The following creates a gas that is 80% sulfur hexafluoride, 15% Argonm and 5% Air
gap_4_component_1 = pywincalc.CustomGasMixtureComponent(sulfur_hexafluoride, 0.8)
gap_4_component_2 = pywincalc.PredefinedGasMixtureComponent(pywincalc.PredefinedGasType.ARGON, .15)
gap_4_component_3 = pywincalc.PredefinedGasMixtureComponent(pywincalc.PredefinedGasType.AIR, .05)
gap_4 = pywincalc.Gap([gap_4_component_1, gap_4_component_2, gap_4_component_3], .025)  # 2.5mm thick gap

gaps = [gap_1, gap_2, gap_3, gap_4]

# Next load the other things required to create a glazing system.  Since this example is just for how to create gaps
# it will use the included generic clear 3 glass and NFRC optical standards to make a five layer system.  Five
# solid layer to accomidate the 4 gases created above
optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

width = 1.0  # width of the glazing system in meters
height = 1.0  # height of the glazing system in meters

clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)
solid_layers = [clear_3] * 5
glazing_system_u_environment = pywincalc.GlazingSystem(optical_standard, solid_layers, gaps, width, height)

glazing_system_shgc_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                          solid_layers=solid_layers,
                                                          gap_layers=gaps,
                                                          width_meters=width,
                                                          height_meters=height,
                                                          environment=pywincalc.nfrc_shgc_environments())

results_name = "Results for a 5-layer system with varying gases"
print("*" * len(results_name))
print(results_name)
print("*" * len(results_name))
results_printer.print_results(glazing_system_u_environment, glazing_system_shgc_environment)
