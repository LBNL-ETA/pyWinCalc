"""
Unit tests for the gas bindings (src/bindings/gas_bindings.cpp).

Covers PredefinedGasType, create_gas, GasData, GasCoefficients, GasItem
(formerly Gases::CGasItem) and GasProperties (formerly Gases::GasProperties)
with contract/invariant checks. GasProperties and GasItem are now registered
(they previously raised on return conversion).
"""
import math

import pywincalc


TOL = 1e-9


class TestPredefinedGasType:
    def test_expected_values_present(self):
        for name in ("AIR", "ARGON", "KRYPTON", "XENON"):
            assert hasattr(pywincalc.PredefinedGasType, name)


class TestCreateGas:
    def test_single_component_total_percent(self):
        gas = pywincalc.create_gas([[1.0, pywincalc.PredefinedGasType.AIR]])
        assert math.isclose(gas.total_percent(), 1.0, abs_tol=TOL)

    def test_multi_component_total_percent(self):
        gas = pywincalc.create_gas(
            [
                [0.9, pywincalc.PredefinedGasType.ARGON],
                [0.1, pywincalc.PredefinedGasType.AIR],
            ]
        )
        assert math.isclose(gas.total_percent(), 1.0, abs_tol=TOL)

    def test_create_from_custom_gas_data(self):
        argon = pywincalc.GasData(
            "Argon", 39.948, 1.67,
            pywincalc.GasCoefficients(1.0, 2.0, 3.0),
            pywincalc.GasCoefficients(1.0, 2.0, 3.0),
            pywincalc.GasCoefficients(1.0, 2.0, 3.0),
        )
        gas = pywincalc.create_gas([[1.0, argon]])
        assert math.isclose(gas.total_percent(), 1.0, abs_tol=TOL)


class TestGasData:
    def test_roundtrip(self):
        gd = pywincalc.GasData(
            "Argon", 39.948, 1.67,
            pywincalc.GasCoefficients(1.0, 2.0, 3.0),
            pywincalc.GasCoefficients(1.0, 2.0, 3.0),
            pywincalc.GasCoefficients(1.0, 2.0, 3.0),
        )
        assert gd.name() == "Argon"
        assert math.isclose(gd.get_molecular_weight(), 39.948, abs_tol=TOL)
        assert math.isclose(gd.get_specific_heat_ratio(), 1.67, abs_tol=TOL)


class TestGasItems:
    def test_gas_items_returns_components(self):
        gas = pywincalc.create_gas(
            [
                [0.9, pywincalc.PredefinedGasType.ARGON],
                [0.1, pywincalc.PredefinedGasType.AIR],
            ]
        )
        items = gas.gas_items()
        assert len(items) == 2
        # exact fractions and molecular weights, keyed by component name
        by_name = {
            item.name(): (item.fraction(), item.gas_data().get_molecular_weight())
            for item in items
        }
        assert math.isclose(by_name["Argon"][0], 0.9, abs_tol=TOL)
        assert math.isclose(by_name["Argon"][1], 39.948, rel_tol=1e-9)  # argon MW
        assert math.isclose(by_name["Air"][0], 0.1, abs_tol=TOL)
        assert math.isclose(by_name["Air"][1], 28.97, rel_tol=1e-9)     # dry-air MW


class TestGasProperties:
    # Reference values for air at 273.15 K, 101325 Pa (ISO 15099 gas model).
    # These are physically correct, not just current model output:
    #   - molecular_weight = 28.97 g/mol (standard dry air)
    #   - density = P*M/(R*T) = 101325*0.02897/(8.31446*273.15) = 1.29250 kg/m3
    #   - k ~ 0.0241 W/mK, mu ~ 1.72e-5 Pa.s, cp ~ 1006 J/kgK, Pr ~ 0.72 (textbook air at 0 C)
    AIR_STP = dict(
        thermal_conductivity=0.02406974,
        viscosity=1.721691e-05,
        specific_heat=1006.1033006,
        density=1.2924975866,
        molecular_weight=28.97,
        prandl_number=0.7196583751,
    )

    def _assert_air_stp(self, props):
        assert math.isclose(props.thermal_conductivity,
                            self.AIR_STP["thermal_conductivity"], rel_tol=1e-5)
        assert math.isclose(props.viscosity, self.AIR_STP["viscosity"], rel_tol=1e-5)
        assert math.isclose(props.specific_heat, self.AIR_STP["specific_heat"], rel_tol=1e-5)
        assert math.isclose(props.density, self.AIR_STP["density"], rel_tol=1e-5)
        assert math.isclose(props.molecular_weight, self.AIR_STP["molecular_weight"], rel_tol=1e-9)
        assert math.isclose(props.prandl_number, self.AIR_STP["prandl_number"], rel_tol=1e-5)

    def test_simple_gas_properties_air_stp(self):
        gas = pywincalc.create_gas([[1.0, pywincalc.PredefinedGasType.AIR]])
        self._assert_air_stp(gas.get_simple_gas_properties(273.15, 101325.0))

    def test_full_gas_properties_air_stp(self):
        # for a single-component gas the full model equals the simple model
        gas = pywincalc.create_gas([[1.0, pywincalc.PredefinedGasType.AIR]])
        self._assert_air_stp(gas.get_gas_properties(273.15, 101325.0))

    def test_density_obeys_ideal_gas_law(self):
        # independent cross-check: rho = P*M/(R*T) with M in kg/mol
        gas = pywincalc.create_gas([[1.0, pywincalc.PredefinedGasType.AIR]])
        props = gas.get_simple_gas_properties(273.15, 101325.0)
        expected = 101325.0 * (props.molecular_weight / 1000.0) / (8.314462618 * 273.15)
        assert math.isclose(props.density, expected, rel_tol=1e-5)
