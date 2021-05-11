from pydantic.dataclasses import dataclass
from enum import Enum

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
class IntegratedSpectralAveragesSummary:
    standard: CalculationStandardName

    tf_sol: float = 0
    tb_sol: float = 0
    rf_sol: float = 0
    rb_sol: float = 0

    tf_vis: float = 0
    tb_vis: float = 0
    rf_vis: float = 0
    rb_vis: float = 0

    tf_tdw: float = 0
    tf_tuv: float = 0
    tf_spf: float = 0
    tf_tkr: float = 0

    tf_ciex: float = 0
    tf_ciey: float = 0
    tf_ciez: float = 0
    tf_r: float = 0
    tf_g: float = 0
    tf_b: float = 0

    rf_ciex: float = 0
    rf_ciey: float = 0
    rf_ciez: float = 0
    rf_r: float = 0
    rf_g: float = 0
    rf_b: float = 0

    rb_ciex: float = 0
    rb_ciey: float = 0
    rb_ciez: float = 0
    rb_r: float = 0
    rb_g: float = 0
    rb_b: float = 0
