from pydantic.dataclasses import dataclass
from enum import Enum


class MaterialType(Enum):
    UNKNOWN = "Unknown"
    NA = "Not applicable"
    GLASS = "glass"
    PVB = "PVB"
    POLYCARBONATE = "polycarbonate"
    ACRYLIC = "acrylic"
    PET = "PET"


material_type_lookup = {
    1: "UNKNOWN",
    2: "NA",
    3: "GLASS",
    4: "PVB",
    5: "POLYCARBONATE",
    6: "ACRYLIC",
    7: "PET"
}


@dataclass
class MaterialBulkProperties:
    name: str
    display_name: str
    version: str
    conductivity: float
    youngs_modulus: float
    poissons_ratio: float
    elasticity: float
    moisture_properties: dict
