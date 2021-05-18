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


if __name__ == "__main__":
    test_generate_integrated_spectral_averages_summary()
