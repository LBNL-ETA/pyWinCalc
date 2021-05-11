from pywincalc.optical import IntegratedSpectralAveragesSummary
from pywincalc.product import Product
from pywincalc.standard import CalculationStandardName


def generate_integrated_spectral_averages_summary(product: Product,
                                                  standard: CalculationStandardName) \
        -> IntegratedSpectralAveragesSummary:
    """
    Generate integrated spectral averages summary for a given product and standard.

    :param product:
    :param standard:
    :return:
    """

    # TODO: Business logic that generates integrated spectral averages summary
    # TODO: for the given product and calculation standard.

    values: IntegratedSpectralAveragesSummary = IntegratedSpectralAveragesSummary(standard=standard)
    values.standard = standard
    values.tf_sol = 0.123

    return values
