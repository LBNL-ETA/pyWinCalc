import pywincalc
import requests
from igsdb_interaction import url_single_product, headers
import json


# This example shows how to create a glass layer from user-defined thermal and n-band optical data
# and then pair it will layers from the IGSDB to create a double-layer system and calculate properties


def get_product_summary_list_from_igsdb():
    # This is a url to get the summary list of all glazing products from the IGSDB
    glazing_products_summary_url = "https://igsdb.lbl.gov/api/v1/products?type=glazing"
    igsdb_response = requests.get(glazing_products_summary_url, headers=headers)
    return json.loads(igsdb_response.content)


def filter_igsdb_product(product_summary):
    # This is an example of how to filter a product based on the summary data returned by the IGSDB.
    # It can be omitted to consider all products but if it there are some known requirements it can
    # help cut down the calculation time.
    #
    # In this case only products with a visible front transmittance >= 0.9 are considered

    # This iterates through the "integrated_results_summary" looking for the NFRC results.  This isn't strictly
    # necessary at the moment because so far only results from the NFRC standard are stored but
    # in the future there may be results from other standards stored as well so it is best to
    # make sure the results from the correct standard are used

    all_integrated_results = product_summary.get("integrated_results_summary")

    visible_transmittance = None

    for integrated_results_by_standard in all_integrated_results:
        if integrated_results_by_standard.get("calculation_standard_name") == "NFRC":
            visible_transmittance = integrated_results_by_standard.get("tfvis")
    return visible_transmittance > 0.9


def convert_wavelength_data(raw_wavelength_data):
    # Whatever format your raw wavelength data is it will need to be converted to a list of pywincalc.WavelengthData
    # For this example it is assumed that the raw measured values for each wavelength is a dict with keys
    # "wavelength_microns", "transmittance_front", "transmittance_back", "reflectance_front", and "reflectance_back"
    # See the data returned by the raw_wavelength_data function below

    # This can be done as a list comprehension but for clarity in this example it is done in a loop
    pywincalc_wavelength_measured_data = []
    for individual_wavelength_measurement in raw_wavelength_data:
        wavelength = individual_wavelength_measurement["wavelength_microns"]
        # In this case the raw data only has the direct component measured
        # Diffuse measured data is not yet supported in the calculations
        direct_component = pywincalc.OpticalMeasurementComponent(
            individual_wavelength_measurement["transmittance_front"],
            individual_wavelength_measurement["transmittance_back"],
            individual_wavelength_measurement["reflectance_front"],
            individual_wavelength_measurement["reflectance_back"])
        pywincalc_wavelength_measured_data.append(pywincalc.WavelengthData(wavelength, direct_component))

    return pywincalc_wavelength_measured_data


def raw_glazing_wavelength_data():
    # This format is for example purposes only.
    return [{"wavelength_microns": 0.300, "transmittance_front": 0.0020, "transmittance_back": 0.0020,
             "reflectance_front": 0.0470, "reflectance_back": 0.0480},
            {"wavelength_microns": 0.305, "transmittance_front": 0.0030, "transmittance_back": 0.0030,
             "reflectance_front": 0.0470, "reflectance_back": 0.0480},
            {"wavelength_microns": 0.310, "transmittance_front": 0.0090, "transmittance_back": 0.0090,
             "reflectance_front": 0.0470, "reflectance_back": 0.0480},
            {"wavelength_microns": 0.315, "transmittance_front": 0.0350, "transmittance_back": 0.0350,
             "reflectance_front": 0.0470, "reflectance_back": 0.0480},
            {"wavelength_microns": 0.320, "transmittance_front": 0.1000, "transmittance_back": 0.1000,
             "reflectance_front": 0.0470, "reflectance_back": 0.0480},
            {"wavelength_microns": 0.325, "transmittance_front": 0.2180, "transmittance_back": 0.2180,
             "reflectance_front": 0.0490, "reflectance_back": 0.0500},
            {"wavelength_microns": 0.330, "transmittance_front": 0.3560, "transmittance_back": 0.3560,
             "reflectance_front": 0.0530, "reflectance_back": 0.0540},
            {"wavelength_microns": 0.335, "transmittance_front": 0.4980, "transmittance_back": 0.4980,
             "reflectance_front": 0.0600, "reflectance_back": 0.0610},
            {"wavelength_microns": 0.340, "transmittance_front": 0.6160, "transmittance_back": 0.6160,
             "reflectance_front": 0.0670, "reflectance_back": 0.0670},
            {"wavelength_microns": 0.345, "transmittance_front": 0.7090, "transmittance_back": 0.7090,
             "reflectance_front": 0.0730, "reflectance_back": 0.0740},
            {"wavelength_microns": 0.350, "transmittance_front": 0.7740, "transmittance_back": 0.7740,
             "reflectance_front": 0.0780, "reflectance_back": 0.0790},
            {"wavelength_microns": 0.355, "transmittance_front": 0.8180, "transmittance_back": 0.8180,
             "reflectance_front": 0.0820, "reflectance_back": 0.0820},
            {"wavelength_microns": 0.360, "transmittance_front": 0.8470, "transmittance_back": 0.8470,
             "reflectance_front": 0.0840, "reflectance_back": 0.0840},
            {"wavelength_microns": 0.365, "transmittance_front": 0.8630, "transmittance_back": 0.8630,
             "reflectance_front": 0.0850, "reflectance_back": 0.0850},
            {"wavelength_microns": 0.370, "transmittance_front": 0.8690, "transmittance_back": 0.8690,
             "reflectance_front": 0.0850, "reflectance_back": 0.0860},
            {"wavelength_microns": 0.375, "transmittance_front": 0.8610, "transmittance_back": 0.8610,
             "reflectance_front": 0.0850, "reflectance_back": 0.0850},
            {"wavelength_microns": 0.380, "transmittance_front": 0.8560, "transmittance_back": 0.8560,
             "reflectance_front": 0.0840, "reflectance_back": 0.0840},
            {"wavelength_microns": 0.385, "transmittance_front": 0.8660, "transmittance_back": 0.8660,
             "reflectance_front": 0.0850, "reflectance_back": 0.0850},
            {"wavelength_microns": 0.390, "transmittance_front": 0.8810, "transmittance_back": 0.8810,
             "reflectance_front": 0.0860, "reflectance_back": 0.0860},
            {"wavelength_microns": 0.395, "transmittance_front": 0.8890, "transmittance_back": 0.8890,
             "reflectance_front": 0.0860, "reflectance_back": 0.0860},
            {"wavelength_microns": 0.400, "transmittance_front": 0.8930, "transmittance_back": 0.8930,
             "reflectance_front": 0.0860, "reflectance_back": 0.0860},
            {"wavelength_microns": 0.410, "transmittance_front": 0.8930, "transmittance_back": 0.8930,
             "reflectance_front": 0.0860, "reflectance_back": 0.0860},
            {"wavelength_microns": 0.420, "transmittance_front": 0.8920, "transmittance_back": 0.8920,
             "reflectance_front": 0.0860, "reflectance_back": 0.0860},
            {"wavelength_microns": 0.430, "transmittance_front": 0.8920, "transmittance_back": 0.8920,
             "reflectance_front": 0.0850, "reflectance_back": 0.0850},
            {"wavelength_microns": 0.440, "transmittance_front": 0.8920, "transmittance_back": 0.8920,
             "reflectance_front": 0.0850, "reflectance_back": 0.0850},
            {"wavelength_microns": 0.450, "transmittance_front": 0.8960, "transmittance_back": 0.8960,
             "reflectance_front": 0.0850, "reflectance_back": 0.0850},
            {"wavelength_microns": 0.460, "transmittance_front": 0.9000, "transmittance_back": 0.9000,
             "reflectance_front": 0.0850, "reflectance_back": 0.0850},
            {"wavelength_microns": 0.470, "transmittance_front": 0.9020, "transmittance_back": 0.9020,
             "reflectance_front": 0.0840, "reflectance_back": 0.0840},
            {"wavelength_microns": 0.480, "transmittance_front": 0.9030, "transmittance_back": 0.9030,
             "reflectance_front": 0.0840, "reflectance_back": 0.0840},
            {"wavelength_microns": 0.490, "transmittance_front": 0.9040, "transmittance_back": 0.9040,
             "reflectance_front": 0.0850, "reflectance_back": 0.0850},
            {"wavelength_microns": 0.500, "transmittance_front": 0.9050, "transmittance_back": 0.9050,
             "reflectance_front": 0.0840, "reflectance_back": 0.0840},
            {"wavelength_microns": 0.510, "transmittance_front": 0.9050, "transmittance_back": 0.9050,
             "reflectance_front": 0.0840, "reflectance_back": 0.0840},
            {"wavelength_microns": 0.520, "transmittance_front": 0.9050, "transmittance_back": 0.9050,
             "reflectance_front": 0.0840, "reflectance_back": 0.0840},
            {"wavelength_microns": 0.530, "transmittance_front": 0.9040, "transmittance_back": 0.9040,
             "reflectance_front": 0.0840, "reflectance_back": 0.0840},
            {"wavelength_microns": 0.540, "transmittance_front": 0.9040, "transmittance_back": 0.9040,
             "reflectance_front": 0.0830, "reflectance_back": 0.0830},
            {"wavelength_microns": 0.550, "transmittance_front": 0.9030, "transmittance_back": 0.9030,
             "reflectance_front": 0.0830, "reflectance_back": 0.0830},
            {"wavelength_microns": 0.560, "transmittance_front": 0.9020, "transmittance_back": 0.9020,
             "reflectance_front": 0.0830, "reflectance_back": 0.0830},
            {"wavelength_microns": 0.570, "transmittance_front": 0.9000, "transmittance_back": 0.9000,
             "reflectance_front": 0.0820, "reflectance_back": 0.0820},
            {"wavelength_microns": 0.580, "transmittance_front": 0.8980, "transmittance_back": 0.8980,
             "reflectance_front": 0.0820, "reflectance_back": 0.0820},
            {"wavelength_microns": 0.590, "transmittance_front": 0.8960, "transmittance_back": 0.8960,
             "reflectance_front": 0.0810, "reflectance_back": 0.0810},
            {"wavelength_microns": 0.600, "transmittance_front": 0.8930, "transmittance_back": 0.8930,
             "reflectance_front": 0.0810, "reflectance_back": 0.0810},
            {"wavelength_microns": 0.610, "transmittance_front": 0.8900, "transmittance_back": 0.8900,
             "reflectance_front": 0.0810, "reflectance_back": 0.0810},
            {"wavelength_microns": 0.620, "transmittance_front": 0.8860, "transmittance_back": 0.8860,
             "reflectance_front": 0.0800, "reflectance_back": 0.0800},
            {"wavelength_microns": 0.630, "transmittance_front": 0.8830, "transmittance_back": 0.8830,
             "reflectance_front": 0.0800, "reflectance_back": 0.0800},
            {"wavelength_microns": 0.640, "transmittance_front": 0.8790, "transmittance_back": 0.8790,
             "reflectance_front": 0.0790, "reflectance_back": 0.0790},
            {"wavelength_microns": 0.650, "transmittance_front": 0.8750, "transmittance_back": 0.8750,
             "reflectance_front": 0.0790, "reflectance_back": 0.0790},
            {"wavelength_microns": 0.660, "transmittance_front": 0.8720, "transmittance_back": 0.8720,
             "reflectance_front": 0.0790, "reflectance_back": 0.0790},
            {"wavelength_microns": 0.670, "transmittance_front": 0.8680, "transmittance_back": 0.8680,
             "reflectance_front": 0.0780, "reflectance_back": 0.0780},
            {"wavelength_microns": 0.680, "transmittance_front": 0.8630, "transmittance_back": 0.8630,
             "reflectance_front": 0.0780, "reflectance_back": 0.0780},
            {"wavelength_microns": 0.690, "transmittance_front": 0.8590, "transmittance_back": 0.8590,
             "reflectance_front": 0.0770, "reflectance_back": 0.0770},
            {"wavelength_microns": 0.700, "transmittance_front": 0.8540, "transmittance_back": 0.8540,
             "reflectance_front": 0.0760, "reflectance_back": 0.0770},
            {"wavelength_microns": 0.710, "transmittance_front": 0.8500, "transmittance_back": 0.8500,
             "reflectance_front": 0.0760, "reflectance_back": 0.0760},
            {"wavelength_microns": 0.720, "transmittance_front": 0.8450, "transmittance_back": 0.8450,
             "reflectance_front": 0.0750, "reflectance_back": 0.0760},
            {"wavelength_microns": 0.730, "transmittance_front": 0.8400, "transmittance_back": 0.8400,
             "reflectance_front": 0.0750, "reflectance_back": 0.0750},
            {"wavelength_microns": 0.740, "transmittance_front": 0.8350, "transmittance_back": 0.8350,
             "reflectance_front": 0.0750, "reflectance_back": 0.0750},
            {"wavelength_microns": 0.750, "transmittance_front": 0.8310, "transmittance_back": 0.8310,
             "reflectance_front": 0.0740, "reflectance_back": 0.0740},
            {"wavelength_microns": 0.760, "transmittance_front": 0.8260, "transmittance_back": 0.8260,
             "reflectance_front": 0.0740, "reflectance_back": 0.0740},
            {"wavelength_microns": 0.770, "transmittance_front": 0.8210, "transmittance_back": 0.8210,
             "reflectance_front": 0.0740, "reflectance_back": 0.0740},
            {"wavelength_microns": 0.780, "transmittance_front": 0.8160, "transmittance_back": 0.8160,
             "reflectance_front": 0.0730, "reflectance_back": 0.0730},
            {"wavelength_microns": 0.790, "transmittance_front": 0.8120, "transmittance_back": 0.8120,
             "reflectance_front": 0.0730, "reflectance_back": 0.0730},
            {"wavelength_microns": 0.800, "transmittance_front": 0.8080, "transmittance_back": 0.8080,
             "reflectance_front": 0.0720, "reflectance_back": 0.0720},
            {"wavelength_microns": 0.810, "transmittance_front": 0.8030, "transmittance_back": 0.8030,
             "reflectance_front": 0.0720, "reflectance_back": 0.0720},
            {"wavelength_microns": 0.820, "transmittance_front": 0.8000, "transmittance_back": 0.8000,
             "reflectance_front": 0.0720, "reflectance_back": 0.0720},
            {"wavelength_microns": 0.830, "transmittance_front": 0.7960, "transmittance_back": 0.7960,
             "reflectance_front": 0.0710, "reflectance_back": 0.0710},
            {"wavelength_microns": 0.840, "transmittance_front": 0.7930, "transmittance_back": 0.7930,
             "reflectance_front": 0.0700, "reflectance_back": 0.0710},
            {"wavelength_microns": 0.850, "transmittance_front": 0.7880, "transmittance_back": 0.7880,
             "reflectance_front": 0.0700, "reflectance_back": 0.0710},
            {"wavelength_microns": 0.860, "transmittance_front": 0.7860, "transmittance_back": 0.7860,
             "reflectance_front": 0.0700, "reflectance_back": 0.0700},
            {"wavelength_microns": 0.870, "transmittance_front": 0.7820, "transmittance_back": 0.7820,
             "reflectance_front": 0.0740, "reflectance_back": 0.0740},
            {"wavelength_microns": 0.880, "transmittance_front": 0.7800, "transmittance_back": 0.7800,
             "reflectance_front": 0.0720, "reflectance_back": 0.0720},
            {"wavelength_microns": 0.890, "transmittance_front": 0.7770, "transmittance_back": 0.7770,
             "reflectance_front": 0.0730, "reflectance_back": 0.0740},
            {"wavelength_microns": 0.900, "transmittance_front": 0.7760, "transmittance_back": 0.7760,
             "reflectance_front": 0.0720, "reflectance_back": 0.0720},
            {"wavelength_microns": 0.910, "transmittance_front": 0.7730, "transmittance_back": 0.7730,
             "reflectance_front": 0.0720, "reflectance_back": 0.0720},
            {"wavelength_microns": 0.920, "transmittance_front": 0.7710, "transmittance_back": 0.7710,
             "reflectance_front": 0.0710, "reflectance_back": 0.0710},
            {"wavelength_microns": 0.930, "transmittance_front": 0.7700, "transmittance_back": 0.7700,
             "reflectance_front": 0.0700, "reflectance_back": 0.0700},
            {"wavelength_microns": 0.940, "transmittance_front": 0.7680, "transmittance_back": 0.7680,
             "reflectance_front": 0.0690, "reflectance_back": 0.0690},
            {"wavelength_microns": 0.950, "transmittance_front": 0.7660, "transmittance_back": 0.7660,
             "reflectance_front": 0.0680, "reflectance_back": 0.0680},
            {"wavelength_microns": 0.960, "transmittance_front": 0.7660, "transmittance_back": 0.7660,
             "reflectance_front": 0.0670, "reflectance_back": 0.0680},
            {"wavelength_microns": 0.970, "transmittance_front": 0.7640, "transmittance_back": 0.7640,
             "reflectance_front": 0.0680, "reflectance_back": 0.0680},
            {"wavelength_microns": 0.980, "transmittance_front": 0.7630, "transmittance_back": 0.7630,
             "reflectance_front": 0.0680, "reflectance_back": 0.0680},
            {"wavelength_microns": 0.990, "transmittance_front": 0.7620, "transmittance_back": 0.7620,
             "reflectance_front": 0.0670, "reflectance_back": 0.0670},
            {"wavelength_microns": 1.000, "transmittance_front": 0.7620, "transmittance_back": 0.7620,
             "reflectance_front": 0.0660, "reflectance_back": 0.0670},
            {"wavelength_microns": 1.050, "transmittance_front": 0.7600, "transmittance_back": 0.7600,
             "reflectance_front": 0.0660, "reflectance_back": 0.0660},
            {"wavelength_microns": 1.100, "transmittance_front": 0.7590, "transmittance_back": 0.7590,
             "reflectance_front": 0.0660, "reflectance_back": 0.0660},
            {"wavelength_microns": 1.150, "transmittance_front": 0.7610, "transmittance_back": 0.7610,
             "reflectance_front": 0.0660, "reflectance_back": 0.0660},
            {"wavelength_microns": 1.200, "transmittance_front": 0.7650, "transmittance_back": 0.7650,
             "reflectance_front": 0.0660, "reflectance_back": 0.0660},
            {"wavelength_microns": 1.250, "transmittance_front": 0.7700, "transmittance_back": 0.7700,
             "reflectance_front": 0.0650, "reflectance_back": 0.0650},
            {"wavelength_microns": 1.300, "transmittance_front": 0.7770, "transmittance_back": 0.7770,
             "reflectance_front": 0.0670, "reflectance_back": 0.0670},
            {"wavelength_microns": 1.350, "transmittance_front": 0.7860, "transmittance_back": 0.7860,
             "reflectance_front": 0.0660, "reflectance_back": 0.0670},
            {"wavelength_microns": 1.400, "transmittance_front": 0.7950, "transmittance_back": 0.7950,
             "reflectance_front": 0.0670, "reflectance_back": 0.0680},
            {"wavelength_microns": 1.450, "transmittance_front": 0.8080, "transmittance_back": 0.8080,
             "reflectance_front": 0.0670, "reflectance_back": 0.0670},
            {"wavelength_microns": 1.500, "transmittance_front": 0.8190, "transmittance_back": 0.8190,
             "reflectance_front": 0.0690, "reflectance_back": 0.0690},
            {"wavelength_microns": 1.550, "transmittance_front": 0.8290, "transmittance_back": 0.8290,
             "reflectance_front": 0.0690, "reflectance_back": 0.0690},
            {"wavelength_microns": 1.600, "transmittance_front": 0.8360, "transmittance_back": 0.8360,
             "reflectance_front": 0.0700, "reflectance_back": 0.0700},
            {"wavelength_microns": 1.650, "transmittance_front": 0.8400, "transmittance_back": 0.8400,
             "reflectance_front": 0.0700, "reflectance_back": 0.0700},
            {"wavelength_microns": 1.700, "transmittance_front": 0.8420, "transmittance_back": 0.8420,
             "reflectance_front": 0.0690, "reflectance_back": 0.0700},
            {"wavelength_microns": 1.750, "transmittance_front": 0.8420, "transmittance_back": 0.8420,
             "reflectance_front": 0.0690, "reflectance_back": 0.0700},
            {"wavelength_microns": 1.800, "transmittance_front": 0.8410, "transmittance_back": 0.8410,
             "reflectance_front": 0.0700, "reflectance_back": 0.0700},
            {"wavelength_microns": 1.850, "transmittance_front": 0.8400, "transmittance_back": 0.8400,
             "reflectance_front": 0.0690, "reflectance_back": 0.0690},
            {"wavelength_microns": 1.900, "transmittance_front": 0.8390, "transmittance_back": 0.8390,
             "reflectance_front": 0.0680, "reflectance_back": 0.0680},
            {"wavelength_microns": 1.950, "transmittance_front": 0.8390, "transmittance_back": 0.8390,
             "reflectance_front": 0.0710, "reflectance_back": 0.0710},
            {"wavelength_microns": 2.000, "transmittance_front": 0.8390, "transmittance_back": 0.8390,
             "reflectance_front": 0.0690, "reflectance_back": 0.0690},
            {"wavelength_microns": 2.050, "transmittance_front": 0.8400, "transmittance_back": 0.8400,
             "reflectance_front": 0.0680, "reflectance_back": 0.0680},
            {"wavelength_microns": 2.100, "transmittance_front": 0.8410, "transmittance_back": 0.8410,
             "reflectance_front": 0.0680, "reflectance_back": 0.0680},
            {"wavelength_microns": 2.150, "transmittance_front": 0.8390, "transmittance_back": 0.8390,
             "reflectance_front": 0.0690, "reflectance_back": 0.0690},
            {"wavelength_microns": 2.200, "transmittance_front": 0.8300, "transmittance_back": 0.8300,
             "reflectance_front": 0.0700, "reflectance_back": 0.0700},
            {"wavelength_microns": 2.250, "transmittance_front": 0.8300, "transmittance_back": 0.8300,
             "reflectance_front": 0.0700, "reflectance_back": 0.0700},
            {"wavelength_microns": 2.300, "transmittance_front": 0.8320, "transmittance_back": 0.8320,
             "reflectance_front": 0.0690, "reflectance_back": 0.0690},
            {"wavelength_microns": 2.350, "transmittance_front": 0.8320, "transmittance_back": 0.8320,
             "reflectance_front": 0.0690, "reflectance_back": 0.0700},
            {"wavelength_microns": 2.400, "transmittance_front": 0.8320, "transmittance_back": 0.8320,
             "reflectance_front": 0.0700, "reflectance_back": 0.0700},
            {"wavelength_microns": 2.450, "transmittance_front": 0.8260, "transmittance_back": 0.8260,
             "reflectance_front": 0.0690, "reflectance_back": 0.0690},
            {"wavelength_microns": 2.500, "transmittance_front": 0.8220, "transmittance_back": 0.8220,
             "reflectance_front": 0.0680, "reflectance_back": 0.0680}]


def create_user_defined_layer():
    # Create optical data for the glass layer

    # Make sure to select the appropriate material type for the layer.
    # Current supported options are:
    # APPLIED_FILM, COATED, ELECTROCHROMIC, FILM, INTERLAYER, LAMINATE, MONOLITHIC, THERMOCHROMIC
    glass_material_type = pywincalc.MaterialType.MONOLITHIC
    glass_material_thickness = .003048  # 3.048mm thick
    glass_wavelength_measurements = convert_wavelength_data(raw_glazing_wavelength_data())
    # Since the measurements do not extend to the IR range emissivity and IR transmittances should be provided
    # If there are measurements that extend to the IR range these values can be provided but result calculated
    # from the measurements will be used
    glass_emissivity_front = .84
    glass_emissivity_back = .84
    glass_ir_transmittance_front = 0
    glass_ir_transmittance_back = 0
    glass_coated_side = pywincalc.CoatedSide.NEITHER
    glass_permeability_factor = 0
    flipped = False

    glass_n_band_optical_data = pywincalc.ProductDataOpticalNBand(material_type=glass_material_type,
                                                                  thickness_meters=glass_material_thickness,
                                                                  wavelength_data=glass_wavelength_measurements,
                                                                  coated_side=glass_coated_side,
                                                                  ir_transmittance_front=glass_ir_transmittance_front,
                                                                  ir_transmittance_back=glass_ir_transmittance_back,
                                                                  emissivity_front=glass_emissivity_front,
                                                                  emissivity_back=glass_emissivity_back,
                                                                  permeability_factor=glass_permeability_factor,
                                                                  flipped=flipped)

    # Next create the thermal data for the glass layer
    glass_conductivity = 1
    # Since thermal openings in this case are all zero they can be omitted.  They are included he for example purposes.
    glass_opening_top = 0
    glass_opening_bottom = 0
    glass_opening_left = 0
    glass_opening_right = 0
    glass_opening_front = 0

    glass_thermal = pywincalc.ProductDataThermal(conductivity=glass_conductivity,
                                                 thickness_meters=glass_material_thickness,
                                                 flipped=flipped,
                                                 opening_top=glass_opening_top,
                                                 opening_bottom=glass_opening_bottom,
                                                 opening_left=glass_opening_left,
                                                 opening_right=glass_opening_right,
                                                 opening_front=glass_opening_front)

    # Create a glass layer from both the optical and thermal data
    glass_layer = pywincalc.ProductDataOpticalAndThermal(glass_n_band_optical_data,
                                                         glass_thermal)
    return glass_layer


# A simple function to save some typing when caching results
def cache_results(current, field, value, product_id):
    if value < current[field]["min"]["value"]:
        current[field]["min"]["value"] = value
        current[field]["min"]["product_id"] = igsdb_product_id

    if value > current[field]["max"]["value"]:
        current[field]["max"]["value"] = value
        current[field]["max"]["product_id"] = igsdb_product_id

    return current


# Define the gap between the two layers.  In this case use a default air gap
# that is 12.7mm thick.  For more on creating gases and gaps see the gaps_and_gases.py example
gap_1 = pywincalc.Layers.gap(thickness=.0127)

# Get the user-defined layer
user_defiled_layer = create_user_defined_layer()

# Get the product summary list from igsdb.lbl.gov
all_igsdb_glazing_prodcts = get_product_summary_list_from_igsdb()

# This is just a very basic example to keep track of the min and max values for some properties.
# In this case it will keep track of the min and max values (and the corresponding IGSDB product_id)
# of NFRC U, NRFC SHGC, TVis and direct-hemispheric front visible and solar transmittances
min_and_max_results = {
    "NFRC U": {"min": {"value": 1e100, "product_id": None}, "max": {"value": -1, "product_id": None}},
    "NFRC SHGC": {"min": {"value": 1e100, "product_id": None}, "max": {"value": -1, "product_id": None}},
    "direct-hemispheric front visible transmittance": {"min": {"value": 1e100, "product_id": None},
                                                       "max": {"value": -1, "product_id": None}},
    "direct-hemispheric front solar transmittance": {"min": {"value": 1e100, "product_id": None},
                                                     "max": {"value": -1, "product_id": None}}}

# Iterate through all of the products in the IGSDB summary list
for igsdb_product_summary in all_igsdb_glazing_prodcts:
    # Only consider products that meet some already-known filtering criteria.  Omit this to consider all products
    if filter_igsdb_product(igsdb_product_summary):
        # Get the IGSDB product_id from the product summary
        igsdb_product_id = igsdb_product_summary.get("product_id")
        print(f"Calculating results for system with IGSDB product_id: {igsdb_product_id}")

        # Query igsdb.lbl.gov for the detailed product data.  If multiple runs are needed it may be more
        # efficient to download each product once and save it to disk and then use that.
        igsdb_response = requests.get(url_single_product.format(id=igsdb_product_id), headers=headers)

        # Convert the json returned from igsdb.lbl.gov into a pywincalc layer
        # If using IGSDB product data that has been saved to disk instead of pywincalc.parse_json use
        # pywincalc.parse_json_file(path_to_file) instead
        igsdb_product = pywincalc.parse_json(igsdb_response.content)

        # Create a double-layerd glazing system with the IGSDB product on the exterior and the user-defined
        # layer on the interior using the gap defined above
        glazing_system = pywincalc.GlazingSystem(solid_layers=[igsdb_product, user_defiled_layer],
                                                 gap_layers=[gap_1])

        # Get all optical solar results
        solar_results = glazing_system.optical_method_results("SOLAR")
        # Get the direct_hemispherical front transmittance from the solar results
        tsol = solar_results.system_results.front.transmittance.direct_hemispherical

        # Get all optical visible results
        visible_results = glazing_system.optical_method_results("PHOTOPIC")
        # Get the direct_hemispherical front transmittance from the solar results
        tvis = visible_results.system_results.front.transmittance.direct_hemispherical

        # Calculate NFRC U
        u = glazing_system.u()

        # Calculate NFRC SHGC.  Note that the glazing system defaults to NFRC U-value (winter) environmental conditions
        # To calculate NFRC SHGC the NFRC SHGC (summer) environmental conditions are needed
        glazing_system.environments(pywincalc.nfrc_shgc_environments())
        shgc = glazing_system.shgc()

        # Store the results if they are larger/smaller than previously calculated results
        min_and_max_results = cache_results(min_and_max_results, "NFRC U", u, igsdb_product_id)
        min_and_max_results = cache_results(min_and_max_results, "NFRC SHGC", shgc, igsdb_product_id)
        min_and_max_results = cache_results(min_and_max_results, "direct-hemispheric front visible transmittance", tvis,
                                            igsdb_product_id)
        min_and_max_results = cache_results(min_and_max_results, "direct-hemispheric front solar transmittance", tsol,
                                            igsdb_product_id)

print("Finished calculating.  Here are the min and max values found:")
print(min_and_max_results)
