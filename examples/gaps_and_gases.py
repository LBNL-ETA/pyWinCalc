import pywincalc

# The default way to create a gap.  Creates a gap containing air with a given thickness
# at a default pressure of 101325
gap_1 = pywincalc.Layers.gap(thickness=.0127)  # .0127 is gap thickness in meters

# Currently there are four pre-defined gases available: Air, Argon, Krypton, and Xenon
# A gas object is created from a list of pairs where the first item is the percentage
# and the second item is either one of the predefined gas types or a user-defined GasData object

# Here a gas consisting of 100% Argon is created
gas_2 = pywincalc.create_gas([[1.0, pywincalc.PredefinedGasType.ARGON]])
# Create a gap from this gas by passing it to the gap function.
# In this case the gap is given a different pressure as well
gap_2 = pywincalc.Layers.gap(thickness=.0127, gas=gas_2, pressure=101300)

# Gaps may also contain a mixture of gases.
# Here is a gas that is 70% Krypton and 30% Xenon
gas_3 = pywincalc.create_gas([[0.7, pywincalc.PredefinedGasType.KRYPTON], [0.3, pywincalc.PredefinedGasType.XENON]])
# Create a gap from this gas the same as above.  Here the pressure is omitted so it uses the default 101325
gap_3 = pywincalc.Layers.gap(thickness=.0127, gas=gas_3)

# Custom gases can be created from properties.  The following creates sulfur hexafluoride as distributed with WINDOW 7
sulfur_hexafluoride_conductivity_a = 0.013
sulfur_hexafluoride_conductivity_b = 0
sulfur_hexafluoride_conductivity_c = 0
sulfur_hexafluoride_conductivity_coefficients = pywincalc.GasCoefficients(sulfur_hexafluoride_conductivity_a,
                                                                          sulfur_hexafluoride_conductivity_b,
                                                                          sulfur_hexafluoride_conductivity_c)
sulfur_hexafluoride_viscosity_a = 7.214E-7
sulfur_hexafluoride_viscosity_b = 4.928E-8
sulfur_hexafluoride_viscosity_c = 0
sulfur_hexafluoride_viscosity_coefficients = pywincalc.GasCoefficients(sulfur_hexafluoride_viscosity_a,
                                                                       sulfur_hexafluoride_viscosity_b,
                                                                       sulfur_hexafluoride_viscosity_c)
sulfur_hexafluoride_Cp_a = 418.6
sulfur_hexafluoride_Cp_b = 0
sulfur_hexafluoride_Cp_c = 0
sulfur_hexafluoride_Cp_coefficients = pywincalc.GasCoefficients(sulfur_hexafluoride_Cp_a,
                                                                sulfur_hexafluoride_Cp_b,
                                                                sulfur_hexafluoride_Cp_c)
sulfur_hexafluoride_molecular_weight = 146.1
sulfur_hexafluoride_specific_heat_ratio = 1

sulfur_hexafluoride = pywincalc.GasData("sulfur_hexafluoride",
                                        molecular_weight=sulfur_hexafluoride_molecular_weight,
                                        specific_heat_ratio=sulfur_hexafluoride_specific_heat_ratio,
                                        Cp=sulfur_hexafluoride_Cp_coefficients,
                                        thermal_conductivity=sulfur_hexafluoride_conductivity_coefficients,
                                        viscosity=sulfur_hexafluoride_viscosity_coefficients)

# Once a custom gas is created it can either be used by itself
gas_4 = pywincalc.create_gas([[1.0, sulfur_hexafluoride]])
gap_4 = pywincalc.Layers.gap(thickness=.003, gas=gas_4)  # 3mm thick gap filled with sulfur hexafluoride

# Or it can be mixed with either other predefined or custom gases
# The following creates a gas that is 80% sulfur hexafluoride, 15% Argon, and 5% Air
gas_5 = pywincalc.create_gas(
    [[0.8, sulfur_hexafluoride],
     [0.15, pywincalc.PredefinedGasType.ARGON],
     [0.05, pywincalc.PredefinedGasType.AIR]])
# And uses it it a 2.5mm thick gap at pressure = 101500
gap_5 = pywincalc.Layers.gap(thickness=.0025, gas=gas_5, pressure=101500)

gaps = [gap_1, gap_2, gap_3, gap_4, gap_5]

clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)
solid_layers = [clear_3] * 6

# Create a glazing system.  This only shows an example of getting one result from a glazing system
# created using default environmental conditions.
#
# For more possible results see optical_results_NFRC.py
#
# For more on environmental conditions see environmental_conditions_user_defined.py
glazing_system = pywincalc.create_glazing_system(solid_layers=solid_layers, gap_layers=gaps)
u_value = glazing_system.u()
print("U-value for six-layer system of various gases: {v}".format(v=u_value))
