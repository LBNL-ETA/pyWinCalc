import pywincalc

head_thmx_path = "./products/sample-head_CMA.thmx"
sill_thmx_path = "./products/sample-sill_CMA.thmx"
jamb_thmx_path = "./products/sample-jamb_CMA.thmx"
spacer_thmx_path = "./products/Spacer_CMA.thmx"

head_frame = pywincalc.parse_thmx_file(head_thmx_path)
sill_frame = pywincalc.parse_thmx_file(sill_thmx_path)
jamb_frame = pywincalc.parse_thmx_file(jamb_thmx_path)

window_width = 1.2
window_height = 1.5

cma_window = pywincalc.get_cma_window_single_vision(head_frame, sill_frame, jamb_frame, jamb_frame, window_width,
                                                    window_height)
													
spacer = pywincalc.parse_thmx_file(spacer_thmx_path)
spacer_keff = pywincalc.get_spacer_keff(spacer)

glazing_system_u = 1.25800
glazing_system_shgc = 0.341
glazing_system_visible_direct_hemispheric_front_transmittance = 0.53500

cma_results = pywincalc.calc_cma(cma_window, glazing_system_u, glazing_system_shgc,
                                 glazing_system_visible_direct_hemispheric_front_transmittance, spacer_keff)
								 
print("CMA Results\n\tU:\t{u}\n\tSHGC:\t{shgc}\n\tTv:\t{vt}".format(u=cma_results.u, shgc=cma_results.shgc,
                                                                    vt=cma_results.vt))
