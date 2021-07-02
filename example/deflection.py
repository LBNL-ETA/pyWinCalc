import pywincalc

# Path to the optical standard file.  All other files referenced by the standard file must be in the same directory
# Note:  While all optical standards packaged with WINDOW should work with optical calculations care should be
# taken to use NFRC standards if NFRC thermal results are desired.  This is because for thermal calculations currently
# only ISO 15099 is supported.  While it is possible to use EN optical standards and create thermal results
# those results will not be based on EN 673
optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

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
gap_1 = pywincalc.Gap(pywincalc.PredefinedGasType.AIR, .0127)  # .0127 is gap thickness in meters

# To create a mixture of predefined gases first create the components with the gas type and portion of the mixture
# The following creates a gas that is 70% Krypton and 30% Xenon and 2cm thick
gap_2_component_1 = pywincalc.PredefinedGasMixtureComponent(pywincalc.PredefinedGasType.KRYPTON, .7)
gap_2_component_2 = pywincalc.PredefinedGasMixtureComponent(pywincalc.PredefinedGasType.XENON, .3)
gap_2 = pywincalc.Gap([gap_2_component_1, gap_2_component_2], .02)  # .02 is gap thickness in meters

# Put all gaps into a list ordered from outside to inside
# Note:  This is only specifying gaps between solid layers
# Gases on the interior and exterior of the glazing system are more fixed and only subject to
# change based on the properties in the environmental conditions
gaps = [gap_1, gap_2]

width = 1.0  # width of the glazing system in meters
height = 1.0  # height of the glazing system in meters
tilt = 90  # glazing system tilt in degrees

glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard, solid_layers=solid_layers, gap_layers=gaps,
                                         width_meters=width, height_meters=height, tilt_degrees=tilt,
                                         environment=pywincalc.nfrc_u_environments())
# Deflection calcs currently need to be specifically enabled
glazing_system.enable_deflection(True)

# Set initial temperature and pressure.  Values just chosen for example purposes
glazing_system.set_deflection_properties(temperature_initial=273, pressure_initial=1013200)

# Density can be calculated using either U or SHGC TARCOG system types.  Just using SHGC for this
# example for simplicity.
deflection_results = glazing_system.calc_deflection_properties(pywincalc.TarcogSystemType.SHGC)
print("Initial results")
print("\tdeflection max: {val}".format(val=deflection_results.deflection_max))
print("\tdeflection mean: {val}".format(val=deflection_results.deflection_mean))
print("\tpanes load: {val}".format(val=deflection_results.panes_load))
print("\tU: {val}".format(val=glazing_system.u()))
print("\tSHGC: {val}".format(val=glazing_system.shgc()))
print("\tLayer temperatures (U): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.U)))
print("\tLayer temperatures (SHGC): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.SHGC)))
visible_results = glazing_system.optical_method_results("PHOTOPIC")
print("\tVT: {val}".format(val=visible_results.system_results.front.transmittance.direct_hemispherical))


# Change initial temperature and pressure.  Values just chosen for example purposes
glazing_system.set_deflection_properties(temperature_initial=290, pressure_initial=1014500)
print("")
print("Changed initial temperature and pressure")
print("\tdeflection max: {val}".format(val=deflection_results.deflection_max))
print("\tdeflection mean: {val}".format(val=deflection_results.deflection_mean))
print("\tpanes load: {val}".format(val=deflection_results.panes_load))
print("\tU: {val}".format(val=glazing_system.u()))
print("\tSHGC: {val}".format(val=glazing_system.shgc()))
print("\tLayer temperatures (U): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.U)))
print("\tLayer temperatures (SHGC): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.SHGC)))
visible_results = glazing_system.optical_method_results("PHOTOPIC")
print("\tVT: {val}".format(val=visible_results.system_results.front.transmittance.direct_hemispherical))
# Change tilt
glazing_system.set_tilt(50)
deflection_results = glazing_system.calc_deflection_properties(pywincalc.TarcogSystemType.SHGC)

print("")
print("Set tilt")
print("\tdeflection max: {val}".format(val=deflection_results.deflection_max))
print("\tdeflection mean: {val}".format(val=deflection_results.deflection_mean))
print("\tpanes load: {val}".format(val=deflection_results.panes_load))
print("\tU: {val}".format(val=glazing_system.u()))
print("\tSHGC: {val}".format(val=glazing_system.shgc()))
print("\tLayer temperatures (U): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.U)))
print("\tLayer temperatures (SHGC): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.SHGC)))
visible_results = glazing_system.optical_method_results("PHOTOPIC")
print("\tVT: {val}".format(val=visible_results.system_results.front.transmittance.direct_hemispherical))

# Set pane loads.  Note:  These numbers are just randomly chosen for example purposes
pane_loads = [25, 5, 50]
glazing_system.set_applied_loads(pane_loads)
deflection_results = glazing_system.calc_deflection_properties(pywincalc.TarcogSystemType.SHGC)

print("")
print("Set applied loads")
print("\tdeflection max: {val}".format(val=deflection_results.deflection_max))
print("\tdeflection mean: {val}".format(val=deflection_results.deflection_mean))
print("\tpanes load: {val}".format(val=deflection_results.panes_load))
print("\tU: {val}".format(val=glazing_system.u()))
print("\tSHGC: {val}".format(val=glazing_system.shgc()))
print("\tLayer temperatures (U): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.U)))
print("\tLayer temperatures (SHGC): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.SHGC)))
visible_results = glazing_system.optical_method_results("PHOTOPIC")
print("\tVT: {val}".format(val=visible_results.system_results.front.transmittance.direct_hemispherical))

# create and use custom environmental conditions
# This creates environmental conditions that are the same as the NFRC SHCG environment
# Note:  These conditions are also available with the pywincalc.nfrc_shgc_environments() function
air_direction_inside = pywincalc.AirHorizontalDirection.NONE
air_speed_inside = 0
air_temperature_inside = 297.15
coefficient_model_inside = pywincalc.BoundaryConditionsCoefficientModelType.CALCULATED_H
convection_coefficient_inside = 0
direct_solar_radiation_inside = 0
emissivity_inside = 1
pressure_inside = 101325
radiation_temperature_inside = 297.15

air_direction_outside = pywincalc.AirHorizontalDirection.WINDWARD
air_speed_outside = 2.75
air_temperature_outside = 305.15
coefficient_model_outside = pywincalc.BoundaryConditionsCoefficientModelType.CALCULATED_H
convection_coefficient_outside = 15
direct_solar_radiation_outside = 783
emissivity_outside = 1
pressure_outside = 101325
radiation_temperature_outside = 297.15

custom_inside_env = pywincalc.Environment(air_temperature=air_temperature_inside,
                                          pressure=pressure_inside,
                                          convection_coefficient=convection_coefficient_inside,
                                          coefficient_model=coefficient_model_inside,
                                          radiation_temperature=radiation_temperature_inside,
                                          emissivity=emissivity_inside,
                                          air_speed=air_speed_inside,
                                          air_direction=air_direction_inside,
                                          direct_solar_radiation=direct_solar_radiation_inside)

custom_outside_env = pywincalc.Environment(air_temperature=air_temperature_outside,
                                           pressure=pressure_outside,
                                           convection_coefficient=convection_coefficient_outside,
                                           coefficient_model=coefficient_model_outside,
                                           radiation_temperature=radiation_temperature_outside,
                                           emissivity=emissivity_outside,
                                           air_speed=air_speed_outside,
                                           air_direction=air_direction_outside,
                                           direct_solar_radiation=direct_solar_radiation_outside)

custom_env = pywincalc.Environments(outside=custom_outside_env, inside=custom_inside_env)

# changing environmental conditions currently requires creating a new glazing system
# note:  this resets any changes made such as if deflection is enabled or applied load is set.
# if this is a problem or you think it would be better to be able to change environmental conditions
# like tilt and load let us know.

glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard, solid_layers=solid_layers, gap_layers=gaps,
                                         width_meters=width, height_meters=height, tilt_degrees=tilt,
                                         environment=custom_env)

glazing_system.enable_deflection(True)
glazing_system.set_deflection_properties(temperature_initial=273, pressure_initial=1013200)
deflection_results = glazing_system.calc_deflection_properties(pywincalc.TarcogSystemType.SHGC)

print("")
print("Set custom environmental conditions 1")
print("\tdeflection max: {val}".format(val=deflection_results.deflection_max))
print("\tdeflection mean: {val}".format(val=deflection_results.deflection_mean))
print("\tpanes load: {val}".format(val=deflection_results.panes_load))
print("\tU: {val}".format(val=glazing_system.u()))
print("\tSHGC: {val}".format(val=glazing_system.shgc()))
print("\tLayer temperatures (U): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.U)))
print("\tLayer temperatures (SHGC): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.SHGC)))
visible_results = glazing_system.optical_method_results("PHOTOPIC")
print("\tVT: {val}".format(val=visible_results.system_results.front.transmittance.direct_hemispherical))

# Rather than setting all the parameters for a custom environment it may be easier to start with
# an existing environment and only change what is needed

# Start from the NFRC SHGC environment and add 500 pascals to the outside pressure
# and subtract 200 from the inside pressure
custom_env_2 = pywincalc.nfrc_shgc_environments()
custom_env_2.outside.pressure += 500
custom_env_2.inside.pressure -= 200

glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard, solid_layers=solid_layers, gap_layers=gaps,
                                         width_meters=width, height_meters=height, tilt_degrees=tilt,
                                         environment=custom_env_2)

glazing_system.enable_deflection(True)
glazing_system.set_deflection_properties(temperature_initial=273, pressure_initial=1013200)
deflection_results = glazing_system.calc_deflection_properties(pywincalc.TarcogSystemType.SHGC)

print("")
print("Set custom environmental conditions 2")
print("\tdeflection max: {val}".format(val=deflection_results.deflection_max))
print("\tdeflection mean: {val}".format(val=deflection_results.deflection_mean))
print("\tpanes load: {val}".format(val=deflection_results.panes_load))
print("\tU: {val}".format(val=glazing_system.u()))
print("\tSHGC: {val}".format(val=glazing_system.shgc()))
print("\tLayer temperatures (U): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.U)))
print("\tLayer temperatures (SHGC): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.SHGC)))
visible_results = glazing_system.optical_method_results("PHOTOPIC")
print("\tVT: {val}".format(val=visible_results.system_results.front.transmittance.direct_hemispherical))

# Density and Young's Modulus are set on the solid layers.  Changing them also involves re-creating the
# glazing system.  Again let us know if you would like a mechanism for being able to change them
# on a glazing system that has already been created

# Change the density of the clear_6 glass and the Young's Modulus of the clear_3
clear_6.density = 2000
clear_3.youngs_modulus = 7e10;

solid_layers = [clear_6, clear_3, clear_6]

glazing_system = pywincalc.GlazingSystem(optical_standard=optical_standard, solid_layers=solid_layers,
                                         gap_layers=gaps, width_meters=width, height_meters=height, tilt_degrees=tilt,
                                         environment=custom_env_2)

glazing_system.enable_deflection(True)
glazing_system.set_deflection_properties(temperature_initial=273, pressure_initial=1013200)
deflection_results = glazing_system.calc_deflection_properties(pywincalc.TarcogSystemType.SHGC)

print("")
print("Set density and youngs modulus")
print("\tdeflection max: {val}".format(val=deflection_results.deflection_max))
print("\tdeflection mean: {val}".format(val=deflection_results.deflection_mean))
print("\tpanes load: {val}".format(val=deflection_results.panes_load))
print("\tU: {val}".format(val=glazing_system.u()))
print("\tSHGC: {val}".format(val=glazing_system.shgc()))
print("\tLayer temperatures (U): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.U)))
print("\tLayer temperatures (SHGC): {val}".format(val=glazing_system.layer_temperatures(pywincalc.TarcogSystemType.SHGC)))
visible_results = glazing_system.optical_method_results("PHOTOPIC")
print("\tVT: {val}".format(val=visible_results.system_results.front.transmittance.direct_hemispherical))