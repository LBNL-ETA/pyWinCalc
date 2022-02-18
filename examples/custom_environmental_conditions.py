import pywincalc

optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

solid_layers = [clear_3]

inside_air_temperature = 294.15
inside_air_pressure = 101325.0
inside_convection_coefficient = 0.0
inside_coefficient_model = pywincalc.BoundaryConditionsCoefficientModelType.CALCULATED_H
inside_radiation_temperature = 294.15
inside_emissivity = 1.0
inside_air_speed = 0.0
inside_air_direction = pywincalc.AirHorizontalDirection.NONE
inside_direct_solar_radiation = 0.0

outside_air_temperature = 255.15
outside_air_pressure = 101325.0
outside_convection_coefficient = 26.0
outside_coefficient_model = pywincalc.BoundaryConditionsCoefficientModelType.CALCULATED_H
outside_radiation_temperature = 255.15
outside_emissivity = 1.0
outside_air_speed = 5.0
outside_air_direction = pywincalc.AirHorizontalDirection.WINDWARD
outside_direct_solar_radiation = 0.0

inside_environment = pywincalc.Environment(air_temperature=inside_air_temperature, pressure=inside_air_pressure,
                                           convection_coefficient=inside_convection_coefficient,
                                           coefficient_model=inside_coefficient_model,
                                           radiation_temperature=inside_radiation_temperature,
                                           emissivity=inside_emissivity, air_speed=inside_air_speed,
                                           air_direction=inside_air_direction,
                                           direct_solar_radiation=inside_direct_solar_radiation)

outside_environment = pywincalc.Environment(air_temperature=outside_air_temperature, pressure=outside_air_pressure,
                                           convection_coefficient=outside_convection_coefficient,
                                           coefficient_model=outside_coefficient_model,
                                           radiation_temperature=outside_radiation_temperature,
                                           emissivity=outside_emissivity, air_speed=outside_air_speed,
                                           air_direction=outside_air_direction,
                                           direct_solar_radiation=outside_direct_solar_radiation)

environmental_conditions = pywincalc.Environments(outside_environment, inside_environment)
glazing_system = pywincalc.GlazingSystem(optical_standard, solid_layers, environment=environmental_conditions)
print("U-value for a single-clear system with custom environmental conditions: {u}".format(u=glazing_system.u()))
