import json

from pywincalc.product import Product
from pywincalc.integrated import generate_integrated_spectral_averages_summary
from pywincalc.standard import CalculationStandardName
import pywincalc
import pywincalc.optical
import os

OPTICAL_STANDARD_PATH_NFRC = os.path.join(os.path.dirname(__file__), "../example/standards/W5_NFRC_2003.std")


def test_generate_integrated_spectral_averages_summary():
    """
    Create a sample MONOLITHIC product and generate
    integrated spectral averages summary.
    :return:
    """

    optical_standard = pywincalc.load_standard(OPTICAL_STANDARD_PATH_NFRC)
    sample_monolithic_path = os.path.join(os.path.dirname(__file__), "./data/sample_monolithic.json")
    with open(sample_monolithic_path) as f:
        sample_monolithic_json = json.load(f)

    product = Product(**sample_monolithic_json)
    
    values: pywincalc.optical.IntegratedSpectralAveragesSummary = generate_integrated_spectral_averages_summary(
        product=product,
        optical_standard=optical_standard)        
    assert values.solar.transmittance_front.direct_hemispherical == 0.847468218237298
    assert values.thermal_ir.absorptance_front_hemispheric == 0.839999974
    assert values.thermal_ir.absorptance_back_hemispheric == 0.839999974
    assert values.thermal_ir.emissivity_front_hemispheric == values.thermal_ir.absorptance_front_hemispheric
    assert values.thermal_ir.emissivity_back_hemispheric == values.thermal_ir.absorptance_back_hemispheric
    assert values.thermal_ir.transmittance_front_diffuse_diffuse == 0
    assert values.thermal_ir.transmittance_back_diffuse_diffuse == 0
    

def test_calculate_emissivity_from_wavelengths():
    """
    Create a sample product with measurements into the IR range and generate
    integrated spectral averages summary.
    :return:
    """

    optical_standard = pywincalc.load_standard(OPTICAL_STANDARD_PATH_NFRC)
    sample_path = os.path.join(os.path.dirname(__file__), "./data/sample_with_measured_ir.json")
    with open(sample_path) as f:
        sample_json = json.load(f)

    product = Product(**sample_json)
    
    values: pywincalc.optical.IntegratedSpectralAveragesSummary = generate_integrated_spectral_averages_summary(
        product=product,
        optical_standard=optical_standard)        
    assert values.thermal_ir.absorptance_front_hemispheric == 0.8402627824166977
    assert values.thermal_ir.absorptance_back_hemispheric == 0.0077240385089490824
    assert values.thermal_ir.emissivity_front_hemispheric == values.thermal_ir.absorptance_front_hemispheric
    assert values.thermal_ir.emissivity_back_hemispheric == values.thermal_ir.absorptance_back_hemispheric
    assert values.thermal_ir.transmittance_front_diffuse_diffuse == 0
    assert values.thermal_ir.transmittance_back_diffuse_diffuse == 0
    


if __name__ == "__main__":
    test_generate_integrated_spectral_averages_summary()
    test_calculate_emissivity_from_wavelengths()
