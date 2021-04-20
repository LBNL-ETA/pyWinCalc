import json

from pywincalc.product import Product
from pywincalc.integrated import IntegratedSpectralAveragesSummary, generate_integrated_spectral_averages_summary
from pywincalc.standard import CalculationStandardName


def test_generate_integrated_spectral_averages_summary():
    """
    Create a sample MONOLITHIC product and generate
    integrated spectral averages summary.
    :return:
    """

    with open('tests/data/sample_monolithic.json') as f:
        sample_monolithic_json = json.load(f)

    product = Product(**sample_monolithic_json)
    standard = CalculationStandardName.NFRC

    values: IntegratedSpectralAveragesSummary = generate_integrated_spectral_averages_summary(product=product,
                                                                                              standard=standard)

    assert values.standard == standard
