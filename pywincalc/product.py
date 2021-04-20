from pydantic.dataclasses import dataclass
from enum import Enum
from typing import List, Dict
from decimal import *
from pydantic.dataclasses import dataclass

from pywincalc.material import MaterialBulkProperties
from pywincalc.optical import OpticalProperties, IntegratedSpectralAveragesSummary


class TokenType(Enum):
    PUBLISHED = "PUBLISHED"
    UNDEFINED = "UNDEFINED"
    PROPOSED = "PROPOSED"
    INTRAGROUP = "INTRAGROUP"


class ProductType(Enum):
    GLAZING = "GLAZING"
    SHADING = "SHADING"
    MATERIAL = "MATERIAL"


class ProductSubtype(Enum):
    # glazing types
    MONOLITHIC = "MONOLITHIC"
    LAMINATE = "LAMINATE"
    INTERLAYER = "INTERLAYER"
    EMBEDDED_COATING = "EMBEDDED_COATING"
    COATED = "COATED"
    COATING = "COATING"
    APPLIED_FILM = "APPLIED_FILM"
    FILM = "FILM"
    FRITTED_GLASS = "FRITTED_GLASS"
    CHROMOGENIC = "CHROMOGENIC"

    # shading and material types
    VENETIAN_BLIND = "VENETIAN_BLIND"
    DIFFUSING_SHADE = "DIFFUSING_SHADE"
    WOVEN_SHADE = "WOVEN_SHADE"
    VERTICAL_LOUVER = "VERTICAL_LOUVER"
    PERFORATED_SCREEN = "PERFORATED_SCREEN"
    CELLULAR_SHADE = "CELLULAR_SHADE"

    # other
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"


@dataclass
class PhysicalProperties:
    thickness: float = None
    tir_front: float = None
    tir_back: float = 0.0
    emissivity_front: float = None
    emissivity_back: float = None
    permeability_factor: float = None
    optical_openness: float = None
    bulk_properties_override: dict = None
    is_specular: bool = True
    optical_properties: OpticalProperties = None


@dataclass
class Product:
    type: ProductType
    subtype: ProductSubtype
    product_id: int = None
    token: str = None
    token_type: TokenType = None
    data_file_name: str = None
    data_file_type: str = None
    # This product can be decomposed into parts
    deconstructable: bool = False
    # This product is a 'reference' product, meaning it's sole purpose is
    # to get a child product into the IGSDB using reference substrates.
    # This is method of submittal is  only valid for APPLIED_FILM and LAMINATE products.
    reference: bool = False
    igsdb_version: str = None
    coated_side: str = None
    coating_name: str = None
    owner: str = None
    manufacturer: str = None
    coating_id: int = None
    product_description: Dict = None
    igsdb_checksum: int = None
    material: str = None
    published_date: str = None
    hidden: bool = None
    active: bool = True
    appearance: str = None
    acceptance: str = None
    nfrc_id: str = None
    composition: list = None
    material_bulk_properties: MaterialBulkProperties = None
    integrated_spectral_averages_summaries: List[IntegratedSpectralAveragesSummary] = None
    physical_properties: PhysicalProperties = None
    extra_data: dict = None
    created_at: str = None
    updated_at: str = None
