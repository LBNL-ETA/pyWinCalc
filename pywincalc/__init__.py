from pathlib import Path
import deprecation

from wincalcbindings import (
    AirHorizontalDirection, BSDF, BSDFBasisType, BSDFDirection, BSDFDirections, BSDFHemisphere,
    BSDFIntegrator, BoundaryConditionsCoefficientModelType, CMABestWorstUFactors, CMAResult, CMAWindow,
    CMAWindowDualVisionHorizontal, CMAWindowDualVisionVertical, CMAWindowSingleVision, layers, CellSpacingType, PolygonType, pillar_cell_area,
    PillarData, CylindricalPillar, SphericalPillar, RectangularPillar, TriangularPillar, PentagonPillar, HexagonPillar, LinearBearingPillar, TruncatedConePillar, Glass, PillarMeasurement,
    AnnulusCylinderPillar, CShapedCylinderPillar, UniversalSupportPillar, CylindricalPillarLayer, SphericalPillarLayer, RectangularPillarLayer,
    TriangularPillarLayer, PentagonPillarLayer, HexagonPillarLayer, LinearBearingPillarLayer, TruncatedConePillarLayer,
    AnnulusCylinderPillarLayer, CShapedCylinderPillarLayer, MeasuredPillarLayer, CoatedSide,
    ColorResult, DeflectionResults, DistributionMethodType, DualBandBSDF, EffectiveOpenness, Environment, Environments,
    FlippableSolidLayer, Gas, GasCoefficients, GasData, GlazingSystem as _GlazingSystem, GlazingSystemDimensions,
    IGUGapLayer, IntegrationRule, IntegrationRuleType, Lab, MaterialType,
    OpticalMeasurementComponent, OpticalResultAbsorptance, OpticalResultFluxType, OpticalResultFluxTypeColor,
    OpticalResultLayer, OpticalResultSide, OpticalResultSideColor, OpticalResultSide_Layer, OpticalResultTransmission,
    OpticalResultTransmissionColor, OpticalResults, OpticalResultsColor, OpticalStandard, OpticalStandardMethod,
    PVPowerProperty, PVWavelengthData, ParsedPerforatedGeometry, ParsedVenetianGeometry, ParsedWovenGeometry,
    PerforatedGeometry, PredefinedGasType, ProductComposistionData, ProductData,
    ProductDataOptical, ProductDataOpticalAndThermal, ProductDataOpticalDualBand,
    ProductDataOpticalDualBandBSDF, ProductDataOpticalDualBandHemispheric, ProductDataOpticalNBand,
    ProductDataOpticalPerforatedScreen, ProductDataOpticalVenetian, ProductDataOpticalWithMaterial,
    ProductDataOpticalWovenShade, ProductDataThermal, ProductGeometry, PropertySimple, RGB, Side,
    SpectalDataWavelengthRangeMethodType, Spectrum, SpectrumType, SquareMatrix, TarcogSystemType,
    ThermalIRResults, ThmxBoundaryCondition, ThmxBoundaryConditionPolygon, ThmxCMABestWorstOption, ThmxCMAOptions,
    ThmxFileContents, ThmxMaterial, ThmxMeshParameters, ThmxPolygon, ThmxPolygonPoint, ThmxRGB, ThmxResult,
    ThmxUFactorProjectionResult, ThmxUFactorResults, Trichromatic, VenetianGeometry, WavelengthBSDFs,
    WavelengthBoundary, WavelengthBoundaryType, WavelengthData, WavelengthSet, WavelengthSetType, WovenGeometry,
    load_standard as _load_standard, calc_cma, calc_thermal_ir, convert_to_solid_layer, convert_to_solid_layers,
    create_best_worst_u_factor_option, create_gas, create_perforated_screen, create_venetian_blind, create_woven_shade,
    get_cma_window_double_vision_horizontal, get_cma_window_double_vision_vertical, get_cma_window_single_vision,
    get_spacer_keff, nfrc_shgc_environments, nfrc_u_environments, parse_bsdf_xml_file, parse_bsdf_xml_string,
    parse_json, parse_json_file, parse_optics_file, parse_thmx_file, parse_thmx_string, IGUVentilatedGapLayer,
    forced_ventilation_gap
)

@deprecation.deprecated(deprecated_in="3.0.0", removed_in="4.0.0",
                        current_version="3.0.0",
                        details="Use pywincalc.layers.gap or pywincalc.create_gas instead")
def Gap(gas, thickness):
    converted_gas = None
    if type(gas) is list:
        # Assume it is a list of PredefinedGasMixtureComponent.
        # i.e. a list of (percent, component) tuples
        converted_gas = create_gas(gas)
    else:
        # otherwise it is just a single component and therefore 100% of the mixture
        converted_gas = create_gas([[1.0, gas]])
    return layers.gap(gas=converted_gas, thickness=thickness)


@deprecation.deprecated(deprecated_in="3.0.0", removed_in="4.0.0",
                        current_version="3.0.0",
                        details="Use pywincalc.create_gas instead")
def PredefinedGasMixtureComponent(component, percent):
    return [percent, component]


standard_path = Path(__file__).parent / "standards"


def load_standard(standard_file=standard_path / "W5_NFRC_2003.std"):
    return _load_standard(str(standard_file))


def GlazingSystem(solid_layers, gap_layers=[], optical_standard=load_standard(), width_meters=1.0,
                  height_meters=1.0, tilt_degrees=90, environment=nfrc_u_environments(), bsdf_hemisphere=None,
                  spectral_data_wavelength_range_method=SpectalDataWavelengthRangeMethodType.FULL,
                  number_visible_bands=5, number_solar_bands=10):
    return _GlazingSystem(solid_layers=solid_layers, gap_layers=gap_layers, optical_standard=optical_standard,
                          width_meters=width_meters, height_meters=height_meters,
                          tilt_degrees=tilt_degrees, environment=environment,
                          bsdf_hemisphere=bsdf_hemisphere,
                          spectral_data_wavelength_range_method=spectral_data_wavelength_range_method,
                          number_visible_bands=number_visible_bands,
                          number_solar_bands=number_solar_bands)
