import pywincalc


def print_thermal_results(glazing_system, theta=0, phi=0, leading_tabs=""):
    print("{t}U-value: {u}".format(t=leading_tabs, u=glazing_system.u(theta, phi)))
    print("{t}SHGC: {shgc}".format(t=leading_tabs, shgc=glazing_system.shgc(theta, phi)))

    print("{t}Solid layer temperatures with solar radiation: {v}".format(t=leading_tabs,
                                                                         v=glazing_system.layer_temperatures(
                                                                             pywincalc.TarcogSystemType.SHGC)))
    print("{t}Solid layer temperatures without solar radiation: {v}".format(t=leading_tabs,
                                                                            v=glazing_system.layer_temperatures(
                                                                                pywincalc.TarcogSystemType.U)))
    print("{t}Solid layer effective conductivities with solar radiation: {v}".format(t=leading_tabs,
                                                                                     v=glazing_system.solid_layers_effective_conductivities(
                                                                                         pywincalc.TarcogSystemType.SHGC)))
    print("{t}Solid layer effective conductivities without solar radiation: {v}".format(t=leading_tabs,
                                                                                        v=glazing_system.solid_layers_effective_conductivities(
                                                                                            pywincalc.TarcogSystemType.U)))

    if len(glazing_system.solid_layers()) > 1:
        print("{t}Gap layer effective conductivities with solar radiation: {v}".format(t=leading_tabs,
                                                                                       v=glazing_system.gap_layers_effective_conductivities(
                                                                                           pywincalc.TarcogSystemType.SHGC)))
        print("{t}Gap layer effective conductivities without solar radiation: {v}".format(t=leading_tabs,
                                                                                          v=glazing_system.gap_layers_effective_conductivities(
                                                                                              pywincalc.TarcogSystemType.U)))

    print("{t}System effective conductivity with solar radiation: {v}".format(t=leading_tabs,
                                                                              v=glazing_system.system_effective_conductivity(
                                                                                  pywincalc.TarcogSystemType.SHGC)))
    print("{t}System effective conductivity without solar radiation: {v}".format(t=leading_tabs,
                                                                                 v=glazing_system.system_effective_conductivity(
                                                                                     pywincalc.TarcogSystemType.U)))

    # Relative heat gain does not take a system type as a parameter
    print("{t}Relative heat gain: {v}".format(t=leading_tabs, v=glazing_system.relative_heat_gain()))


def print_system_optical_results_side(side_results, side, optical_method_name, leading_tabs=""):
    print("{t}{m} method direct-direct {s} transmittance: {v}".format(t=leading_tabs, m=optical_method_name, s=side,
                                                                      v=side_results.transmittance.direct_direct))
    print("{t}{m} method direct-diffuse {s} transmittance: {v}".format(t=leading_tabs, m=optical_method_name, s=side,
                                                                       v=side_results.transmittance.direct_direct))
    print("{t}{m} method direct-hemispherical {s} transmittance: {v}".format(t=leading_tabs, m=optical_method_name,
                                                                             s=side,
                                                                             v=side_results.transmittance.direct_hemispherical))
    print("{t}{m} method diffuse-diffuse {s} transmittance: {v}".format(t=leading_tabs, m=optical_method_name, s=side,
                                                                        v=side_results.transmittance.diffuse_diffuse))
    print("{t}{m} method direct-direct {s} reflectance: {v}".format(t=leading_tabs, m=optical_method_name, s=side,
                                                                    v=side_results.reflectance.direct_direct))
    print("{t}{m} method direct-diffuse {s} reflectance: {v}".format(t=leading_tabs, m=optical_method_name, s=side,
                                                                     v=side_results.reflectance.direct_direct))
    print("{t}{m} method direct-hemispherical {s} reflectance: {v}".format(t=leading_tabs, m=optical_method_name, s=side,
                                                                         v=side_results.reflectance.direct_hemispherical))
    print("{t}{m} method diffuse-diffuse {s} reflectance: {v}".format(t=leading_tabs, m=optical_method_name, s=side,
                                                                      v=side_results.reflectance.diffuse_diffuse))
    print("{t}{m} method {s} transmittance matrix: {v}".format(t=leading_tabs, m=optical_method_name, s=side,
                                                               v=side_results.transmittance.matrix))
    print("{t}{m} method {s} reflectance matrix: {v}".format(t=leading_tabs, m=optical_method_name, s=side,
                                                             v=side_results.reflectance.matrix))


def print_optical_method_results(glazing_system, optical_method_name, theta, phi, leading_tabs=""):
    try:
        results = glazing_system.optical_method_results(optical_method_name, theta, phi)
    except Exception as e:
        print(str(e))
        return

    system_results = results.system_results
    print_system_optical_results_side(system_results.front, "front", optical_method_name, leading_tabs)
    print_system_optical_results_side(system_results.front, "back", optical_method_name, leading_tabs)

    # Currently only absorptance results are provided for each solid layer.  Direct and diffuse absportances are
    # provided for each side of each layer.
    results_per_layer = results.layer_results
    for i in range(len(results_per_layer)):
        print("{t}{m} method layer {idx} front total direct absorptance: {v}".format(t=leading_tabs,
                                                                                     m=optical_method_name, idx=i + 1,
                                                                                     v=results_per_layer[
                                                                                         i].front.absorptance.total_direct))
        print("{t}{m} method layer {idx} front total diffuse absorptance: {v}".format(t=leading_tabs,
                                                                                      m=optical_method_name, idx=i + 1,
                                                                                      v=results_per_layer[
                                                                                          i].front.absorptance.total_diffuse))
																						  
        print("{t}{m} method layer {idx} front heat direct absorptance: {v}".format(t=leading_tabs,
                                                                                     m=optical_method_name, idx=i + 1,
                                                                                     v=results_per_layer[
                                                                                         i].front.absorptance.heat_direct))
        print("{t}{m} method layer {idx} front heat diffuse absorptance: {v}".format(t=leading_tabs,
                                                                                      m=optical_method_name, idx=i + 1,
                                                                                      v=results_per_layer[
                                                                                          i].front.absorptance.heat_diffuse))
																						  
        print("{t}{m} method layer {idx} front electricity direct absorptance: {v}".format(t=leading_tabs,
                                                                                     m=optical_method_name, idx=i + 1,
                                                                                     v=results_per_layer[
                                                                                         i].front.absorptance.electricity_direct))
        print("{t}{m} method layer {idx} front electricity diffuse absorptance: {v}".format(t=leading_tabs,
                                                                                      m=optical_method_name, idx=i + 1,
                                                                                      v=results_per_layer[
                                                                                          i].front.absorptance.electricity_diffuse))
        print(
            "{t}{m} method layer {idx} back total direct absorptance: {v}".format(t=leading_tabs, m=optical_method_name,
                                                                                  idx=i + 1,
                                                                                  v=results_per_layer[
                                                                                      i].back.absorptance.total_direct))
        print("{t}{m} method layer {idx} back total diffuse absorptance: {v}".format(t=leading_tabs,
                                                                                     m=optical_method_name, idx=i + 1,
                                                                                     v=results_per_layer[
                                                                                         i].back.absorptance.total_diffuse))
																						 
        print("{t}{m} method layer {idx} back heat direct absorptance: {v}".format(t=leading_tabs,
                                                                                     m=optical_method_name, idx=i + 1,
                                                                                     v=results_per_layer[
                                                                                         i].back.absorptance.heat_direct))
        print("{t}{m} method layer {idx} back heat diffuse absorptance: {v}".format(t=leading_tabs,
                                                                                      m=optical_method_name, idx=i + 1,
                                                                                      v=results_per_layer[
                                                                                          i].back.absorptance.heat_diffuse))
																						  
        print("{t}{m} method layer {idx} back electricity direct absorptance: {v}".format(t=leading_tabs,
                                                                                     m=optical_method_name, idx=i + 1,
                                                                                     v=results_per_layer[
                                                                                         i].back.absorptance.electricity_direct))
        print("{t}{m} method layer {idx} back electricity diffuse absorptance: {v}".format(t=leading_tabs,
                                                                                      m=optical_method_name, idx=i + 1,
                                                                                      v=results_per_layer[
                                                                                          i].back.absorptance.electricity_diffuse))


def print_color_space_results(flux_results, leading_tabs):
    rgb_color = flux_results.rgb
    print("{t}RGB: ({r}, {g}, {b})".format(t=leading_tabs, r=rgb_color.R, g=rgb_color.G, b=rgb_color.B))
    lab_color = flux_results.lab
    print("{t}Lab: ({l}, {a}, {b})".format(t=leading_tabs, l=lab_color.L, a=lab_color.a, b=lab_color.b))
    trichromatic_color = flux_results.trichromatic
    print("{t}Trichromatic: ({x}, {y}, {z})".format(t=leading_tabs, x=trichromatic_color.X, y=trichromatic_color.Y,
                                                    z=trichromatic_color.Z))


def print_color_flux_results(transmittance_reflactance_result, leading_tabs):
    color_space_leading_tabs = leading_tabs + "\t"
    print("{t}Direct-direct:".format(t=leading_tabs))
    print_color_space_results(transmittance_reflactance_result.direct_direct, color_space_leading_tabs)
    print("{t}Direct-diffuse:".format(t=leading_tabs))
    print_color_space_results(transmittance_reflactance_result.direct_diffuse, color_space_leading_tabs)
    print("{t}Diffuse-diffuse:".format(t=leading_tabs))
    print_color_space_results(transmittance_reflactance_result.diffuse_diffuse, color_space_leading_tabs)


def print_color_results(glazing_system, theta, phi, leading_tabs=""):
    # If the optical standard defines color methods those have a separate results set and function call
    color_results = glazing_system.color(theta, phi)

    # Currently color results only have system results.  Individual layer results are not yet supported.
    # Color results follow the same layout as the other optical system results except each value is offered in
    # the Trichromatic, Lab, and RGB color spaces.

    flux_leading_tabs = leading_tabs + "\t"
    print("{t}Front color transmittance:".format(t=leading_tabs))
    print_color_flux_results(color_results.system_results.front.transmittance, flux_leading_tabs)
    print("{t}Front color reflectance:".format(t=leading_tabs))
    print_color_flux_results(color_results.system_results.front.reflectance, flux_leading_tabs)
    print("{t}Back color transmittance:".format(t=leading_tabs))
    print_color_flux_results(color_results.system_results.back.transmittance, flux_leading_tabs)
    print("{t}Back color reflectance:".format(t=leading_tabs))
    print_color_flux_results(color_results.system_results.back.reflectance, flux_leading_tabs)


def print_optical_results(glazing_system, theta=0, phi=0, leading_tabs=""):
    # Optical results are calculated based on methods defined by the optical standard loaded above.
    # Methods available for calculation depend on the standard.  Not all methods may be implemented in every standard
    # Current non-color methods available for calculation (if implemented):
    # SOLAR, PHOTOPIC, THERMAL_IR, TUV, SPF, TDW, TKR)
    #
    # Calculate all optical results using the solar method:
    print_optical_method_results(glazing_system, "SOLAR", theta, phi, leading_tabs)
    print_optical_method_results(glazing_system, "PHOTOPIC", theta, phi, leading_tabs)
    print_optical_method_results(glazing_system, "TUV", theta, phi, leading_tabs)
    print_optical_method_results(glazing_system, "SPF", theta, phi, leading_tabs)
    print_optical_method_results(glazing_system, "TDW", theta, phi, leading_tabs)
    print_optical_method_results(glazing_system, "TKR", theta, phi, leading_tabs)
    print_color_results(glazing_system, theta, phi, leading_tabs)


def print_results(glazing_system_u_env, glazing_system_shgc_env):
    print("\tResults at normal incidence for system with NFRC U-Value environmental conditions")
    leading_tabs = "\t\t"
    print_optical_results(glazing_system_u_env, leading_tabs=leading_tabs)
    print_thermal_results(glazing_system_u_env, leading_tabs=leading_tabs)

    print("\tResults at normal incidence for system with NFRC SHGC environmental conditions")
    print("\tOnly printing thermal results because optical results do not change based on environmental conditions")
    leading_tabs = "\t\t"
    print_thermal_results(glazing_system_shgc_env, leading_tabs=leading_tabs)

    print("\tResults at incidence of theta = 15° and phi = 270° for system with NFRC SHGC environmental conditions")
    theta = 15
    phi = 270
    print_optical_results(glazing_system_shgc_env, theta, phi, leading_tabs=leading_tabs)
    print_thermal_results(glazing_system_shgc_env, theta, phi, leading_tabs=leading_tabs)
