import pywincalc

# Load solid layer measured values.  Solid layer information can come from either igsdb.lbl.gov or files generate
# by the Optics program.  Since igsdb.lbl.gov requires registration some optics files are provided for example
# purposes
clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

solid_layers = [clear_3]

# Using a small basis here to make printing out the matrix results managable
# Small should probably not be used for actual simulation
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.SMALL)

# By default a glazing system is created using the environmental conditions defined by
# the NFRC U-value calculations
glazing_system_u_environment = pywincalc.create_glazing_system(solid_layers=solid_layers,
                                                               bsdf_hemisphere=bsdf_hemisphere)

# To calculate SHGC use the NFRC SHGC environments for the glazing system instead.
# These are provided by calling pywincalc.nfrc_shgc_environments().
# U-value conditions are also available with pywincalc.nfrc_u_environments().
glazing_system_shgc_environment = pywincalc.create_glazing_system(solid_layers=solid_layers,
                                                                  environment=pywincalc.nfrc_shgc_environments(),
                                                                  bsdf_hemisphere=bsdf_hemisphere)

# In general there are two types of results: optical and thermal.  Here optical and thermal
# refer to the calculation methods and not the wavelengths.  Environmental conditions can only affect thermal results.
#
# All calculations default to calculating results from radiation at a normal angle of incidence but
# support off-normal calculations by allowing users to pass theta and phi values.
#
# So any result can be calculated for any incidence angle this way.
# e.g. to calculate SHGC results at incidence angle theta = 15 and phi = 25 call
# glazing_system.shgc(theta=15, phi=25)
#
# ------------------------------------Thermal Results--------------------------------------------
# Since thermal results depend on environmental conditions the below examples will show
# results for the two most common values (U and SHGC) using both sets of standard NFRC environmental conditions
# to demonstrate the difference environmental conditions can make
#
# However any system created with any environmental conditions has all results available to it.
# For more on creating user-defined environmental conditions see environmental_conditions_user_defined.py

u_value_NFRC_u_conditions = glazing_system_u_environment.u()
u_value_NFRC_shgc_conditions = glazing_system_shgc_environment.u()
print(
    "U-Value.  Based on NFRC U-value environmental conditions: {u}.  Based on NFRC SHGC environmnetal conditions: {shgc}".format(
        u=u_value_NFRC_u_conditions, shgc=u_value_NFRC_shgc_conditions))

shgc_NFRC_u_conditions = glazing_system_u_environment.shgc()
shgc_NFRC_shgc_conditions = glazing_system_shgc_environment.shgc()
print(
    "SHGC.  Based on NFRC U-value environmental conditions: {u}.  Based on NFRC SHGC environmnetal conditions: {shgc}".format(
        u=shgc_NFRC_u_conditions, shgc=shgc_NFRC_shgc_conditions))

# ----------------------------Other thermal results-----------------------------
# Most other thermal can be calculated for two cases for each environment.  When U system is passed as a parameter
# the layer temperatures will be calculated for the given environments without taking solar radiation into account.
# When SHGC system is passed as a parameter solar ration is taken into account
#
# The exception is relative_heat_gain which does not take a system type.
#
# Since the NFRC U-value conditions have 0 solar radiation the below will all use the SHGC conditions
# as examples.
shgc_layer_temperatures_with_solar_radiation = glazing_system_shgc_environment.layer_temperatures(
    pywincalc.TarcogSystemType.SHGC)
print("Layer temperatures in SHGC environment with solar radiation: {v}".format(
    v=shgc_layer_temperatures_with_solar_radiation))
shgc_layer_temperatures_without_solar_radiation = glazing_system_shgc_environment.layer_temperatures(
    pywincalc.TarcogSystemType.U)
print("Layer temperatures in SHGC environment without solar radiation: {v}".format(
    v=shgc_layer_temperatures_without_solar_radiation))

shgc_environment_solid_layer_effective_conductivities_with_solar_radiation = glazing_system_shgc_environment.solid_layers_effective_conductivities(
    (pywincalc.TarcogSystemType.SHGC))
print("Solid layer effective conductivities in SHGC environment with solar radiation: {v}".format(
    v=shgc_environment_solid_layer_effective_conductivities_with_solar_radiation))
shgc_environment_solid_layer_effective_conductivities_without_solar_radiation = glazing_system_shgc_environment.solid_layers_effective_conductivities(
    (pywincalc.TarcogSystemType.U))
print("Solid layer effective conductivities in SHGC environment without solar radiation: {v}".format(
    v=shgc_environment_solid_layer_effective_conductivities_without_solar_radiation))

shgc_environment_gap_layer_effective_conductivities_with_solar_radiation = glazing_system_shgc_environment.gap_layers_effective_conductivities(
    (pywincalc.TarcogSystemType.SHGC))
print("Gap layer effective conductivities in SHGC environment with solar radiation: {v}".format(
    v=shgc_environment_gap_layer_effective_conductivities_with_solar_radiation))
shgc_environment_gap_layer_effective_conductivities_without_solar_radiation = glazing_system_shgc_environment.gap_layers_effective_conductivities(
    (pywincalc.TarcogSystemType.U))
print("Gap layer effective conductivities in SHGC environment without solar radiation: {v}".format(
    v=shgc_environment_gap_layer_effective_conductivities_without_solar_radiation))

system_effective_conductivity_with_solar_radiation = glazing_system_shgc_environment.system_effective_conductivity(
    pywincalc.TarcogSystemType.SHGC)
print("System effective conductivity with solar radiation: {v}".format(
    v=system_effective_conductivity_with_solar_radiation))
system_effective_conductivity_without_solar_radiation = glazing_system_shgc_environment.system_effective_conductivity(
    pywincalc.TarcogSystemType.U)
print("System effective conductivity without solar radiation: {v}".format(
    v=system_effective_conductivity_without_solar_radiation))

# Relative heat gain is an exception and does not take a system type as a parameter
relative_heat_gain = glazing_system_shgc_environment.relative_heat_gain()
print("Relative heat gain: {v}".format(v=relative_heat_gain))

