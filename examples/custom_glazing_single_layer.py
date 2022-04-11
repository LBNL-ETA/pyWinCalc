import pywincalc
import results_printer


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

# Path to the optical standard file.  All other files referenced by the standard file must be in the same directory
# Note:  While all optical standards packaged with WINDOW should work with optical calculations care should be
# taken to use NFRC standards if NFRC thermal results are desired.  This is because for thermal calculations currently
# only ISO 15099 is supported.  While it is possible to use EN optical standards and create thermal results
# those results will not be based on EN 673
optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

glazing_system_width = 1.0  # width of the glazing system in meters
glazing_system_height = 1.0  # height of the glazing system in meters


# Create optical data for the glass layer

# Make sure to select the approriate material type for the layer.
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
flipped = False

glass_n_band_optical_data = pywincalc.ProductDataOpticalNBand(glass_material_type,
                                                              glass_material_thickness,
                                                              glass_wavelength_measurements,
                                                              glass_coated_side,
                                                              glass_emissivity_front,
                                                              glass_emissivity_back,
                                                              glass_ir_transmittance_front,
                                                              glass_ir_transmittance_back,
                                                              flipped)

# Next create the thermal data for the glass layer
glass_conductivity = 1
# Since thermal openings in this case are all zero they can be omitted.  They are included he for example purposes.
glass_opening_top = 0
glass_opening_bottom = 0
glass_opening_left = 0
glass_opening_right = 0

glass_thermal = pywincalc.ProductDataThermal(glass_conductivity, glass_material_thickness, flipped, glass_opening_top,
                                             glass_opening_bottom, glass_opening_left, glass_opening_right)

# Create a glass layer from both the optical and thermal data
glass_layer = pywincalc.ProductDataOpticalAndThermal(glass_n_band_optical_data, glass_thermal)

# Create a glazing system using the NFRC U environment in order to get NFRC U results
# U and SHGC can be caculated for any given environment but in order to get results
# The NFRC U and SHGC environments are provided as already constructed environments and Glazing_System
# defaults to using the NFRC U environments
glazing_system_u_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                       solid_layers=[glass_layer],
                                                       width_meters=glazing_system_width,
                                                       height_meters=glazing_system_height,
                                                       environment=pywincalc.nfrc_u_environments())

# In order to get NFRC SHGC results the NFRC SHGC environment should be used when creating the glazing system
glazing_system_shgc_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                          solid_layers=[glass_layer],
                                                          width_meters=glazing_system_width,
                                                          height_meters=glazing_system_height,
                                                          environment=pywincalc.nfrc_shgc_environments())

results_name = "Results for a single-layer system with a single glazing layer made from user-defined spectral data."
print("*" * len(results_name))
print(results_name)
print("*" * len(results_name))
results_printer.print_results(glazing_system_u_environment, glazing_system_shgc_environment)
