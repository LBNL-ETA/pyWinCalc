from pydantic.dataclasses import dataclass
from enum import Enum
import typing
from pywincalc.standard import CalculationStandardName


class OpticalDataType(Enum):
    DISCRETE = "Discrete"
    BAND = "Band"


class AngularResolutionType(Enum):
    DIRECT = "Direct"
    DIRECT_DIFFUSE = "Direct / Diffuse"
    DIFFUSE_DIFFUSE = "Diffuse / Diffuse"
    BSDF = "BSDF"


INCIDENCE_ANGULAR_RESOLUTION_TYPES = [
    AngularResolutionType.DIRECT,
    AngularResolutionType.BSDF
]

OUTGOING_ANGULAR_RESOLUTION_TYPES = [
    AngularResolutionType.DIRECT,
    AngularResolutionType.BSDF
]


@dataclass
class OpticalProperties:
    optical_data_type: str = OpticalDataType.DISCRETE.name
    incidence_angular_resolution_type: str = AngularResolutionType.DIRECT.name
    outgoing_angular_resolution_type: str = AngularResolutionType.DIRECT.name
    optical_data: dict = None


@dataclass
class OpticalStandardMethodFluxResults:
    direct_direct: float = None
    direct_diffuse: float = None
    direct_hemispherical: float = None
    diffuse_diffuse: float = None
    matrix: typing.List[typing.List[float]] = None


@dataclass
class OpticalStandardMethodResults:
    transmittance_front: OpticalStandardMethodFluxResults = None
    transmittance_back: OpticalStandardMethodFluxResults = None
    reflectance_front: OpticalStandardMethodFluxResults = None
    reflectance_back: OpticalStandardMethodFluxResults = None
    absorptance_front_direct: float = None
    absorptance_back_direct: float = None
	absorptance_front_hemispheric: float = None
    absorptance_back_hemispheric: float = None
    error = None
	
@dataclass
class ThermalIRResults:
    transmittance_front_direct_direct: float = None
    transmittance_back_direct_direct: float = None
	absorptance_front_direct: float = None
    absorptance_back_direct: float = None
    absorptance_front_hemispheric: float = None
    absorptance_back_hemispheric: float = None
    error = None
    
    @property
    def emissivity_front_hemispheric(self):
        return self.absorptance_front_hemispheric
		
    @property
    def emissivity_back_hemispheric(self):
        return self.absorptance_back_hemispheric
		
    @property
    def emissivity_front_direct(self):
        return self.absorptance_front_direct
		
    @property
    def emissivity_back_direct(self):
        return self.absorptance_back_direct

@dataclass
class TrichromaticResult:
    x: float = None
    y: float = None
    z: float = None


@dataclass
class LabResult:
    l: float = None
    a: float = None
    b: float = None


@dataclass
class RGBResult:
    r: float = None
    g: float = None
    b: float = None


@dataclass
class OpticalColorResult:
    trichromatic: TrichromaticResult = None
    lab: LabResult = None
    rgb: RGBResult = None

@dataclass
class OpticalColorFluxResults:
    direct_direct: OpticalColorResult = None
    direct_diffuse: OpticalColorResult = None
    direct_hemispherical: OpticalColorResult = None
    diffuse_diffuse: OpticalColorResult = None

@dataclass
class OpticalColorResults:
    transmittance_front: OpticalColorFluxResults = None
    transmittance_back: OpticalColorFluxResults = None
    reflectance_front: OpticalColorFluxResults = None
    reflectance_back: OpticalColorFluxResults = None
    error = None

@dataclass
class IntegratedSpectralAveragesSummary:
    solar: OpticalStandardMethodResults = None
    photopic: OpticalStandardMethodResults = None
    thermal_ir: ThermalIRResults = None
    tuv: OpticalStandardMethodResults = None
    spf: OpticalStandardMethodResults = None
    tdw: OpticalStandardMethodResults = None
    tkr: OpticalStandardMethodResults = None
    color: OpticalColorResults = None
