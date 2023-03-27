from pathlib import Path
from wincalcbindings import *
from wincalcbindings import _load_standard
import deprecation

@deprecation.deprecated(deprecated_in="2.5", removed_in="3",
                        current_version="2.5",
                        details="Use pywincalc.Layers.gap instead")
def Gap(gas, thickness):
    converted_gas = None
    if type(gas) is list:
        # Assume it is a list of PredefinedGasMixtureComponent.
        # i.e. a list of (percent, component) tuples
        converted_gas = create_gas(gas)
    else:
        # otherwise it is just a single component and therefore 100% of the mixture
        converted_gas = create_gas([[1.0, gas]])
    return Layers.gap(gas=converted_gas, thickness=thickness)

@deprecation.deprecated(deprecated_in="2.5", removed_in="3",
                        current_version="2.5",
                        details="Use pywincalc.Layers.gap instead")
def PredefinedGasMixtureComponent(component, percent):
    return [percent, component]

standard_path = Path(__file__).parent / "standards"

def load_standard(standard_file=standard_path / "W5_NFRC_2003.std"):
    return _load_standard(str(standard_file))


def create_glazing_system(solid_layers, gap_layers=[], optical_standard=load_standard(), width_meters=1.0,
                          height_meters=1.0, tilt_degrees=90, environment=nfrc_u_environments(), bsdf_hemisphere=None,
                          spectral_data_wavelength_range_method=SpectalDataWavelengthRangeMethodType.FULL,
                          number_visible_bands=5, number_solar_bands=10):
    return GlazingSystem(solid_layers=solid_layers, gap_layers=gap_layers, optical_standard=optical_standard,
                         width_meters=width_meters, height_meters=height_meters,
                         tilt_degrees=tilt_degrees, environment=environment,
                         bsdf_hemisphere=bsdf_hemisphere,
                         spectral_data_wavelength_range_method=spectral_data_wavelength_range_method,
                         number_visible_bands=number_visible_bands,
                         number_solar_bands=number_solar_bands)


__all__ = (
    'load_standard',
    'standard_path',
)
