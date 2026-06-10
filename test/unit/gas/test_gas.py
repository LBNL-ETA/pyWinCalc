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
        # fractions reflect the requested mixture and sum to the whole
        assert math.isclose(sum(item.fraction() for item in items), 1.0, abs_tol=TOL)
        assert all(isinstance(item.name(), str) for item in items)
        # each item exposes its underlying GasData
        assert all(item.gas_data().get_molecular_weight() > 0 for item in items)


class TestGasProperties:
    def test_get_simple_gas_properties_are_physical(self):
        gas = pywincalc.create_gas([[1.0, pywincalc.PredefinedGasType.AIR]])
        props = gas.get_simple_gas_properties(273.15, 101325.0)
        # all transport properties of air at STP are finite and positive
        assert props.thermal_conductivity > 0
        assert props.viscosity > 0
        assert props.specific_heat > 0
        assert props.density > 0
        assert props.molecular_weight > 0

    def test_get_gas_properties_returns_properties(self):
        gas = pywincalc.create_gas([[1.0, pywincalc.PredefinedGasType.AIR]])
        props = gas.get_gas_properties(273.15, 101325.0)
        assert props.thermal_conductivity > 0
        assert props.molecular_weight > 0
