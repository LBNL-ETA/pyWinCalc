"""
Unit tests for the gas bindings (src/bindings/gas_bindings.cpp).

Covers the working surface (PredefinedGasType, create_gas, GasData,
GasCoefficients) with contract/invariant checks. Two methods currently return
C++ types that are NOT registered with pybind11 (Gases::GasProperties,
Gases::CGasItem), so they raise on return conversion - those are tracked here
as strict xfail and should flip to failures (prompting marker removal) once the
return types are bound.
"""
import math

import pytest
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


class TestKnownBindingGaps:
    """Methods whose C++ return types are not registered with pybind11.

    These raise TypeError on return-value conversion. Marked strict xfail so the
    day the return types get bound, the test xpasses -> fails -> marker removed.
    """

    @pytest.mark.xfail(
        reason="Gases::CGasItem not registered in bindings",
        raises=TypeError, strict=True,
    )
    def test_gas_items_converts(self):
        gas = pywincalc.create_gas([[1.0, pywincalc.PredefinedGasType.AIR]])
        gas.gas_items()

    @pytest.mark.xfail(
        reason="Gases::GasProperties not registered in bindings",
        raises=TypeError, strict=True,
    )
    def test_get_simple_gas_properties_converts(self):
        gas = pywincalc.create_gas([[1.0, pywincalc.PredefinedGasType.AIR]])
        gas.get_simple_gas_properties(273.15, 101325.0)

    @pytest.mark.xfail(
        reason="Gases::GasProperties not registered in bindings",
        raises=TypeError, strict=True,
    )
    def test_get_gas_properties_converts(self):
        gas = pywincalc.create_gas([[1.0, pywincalc.PredefinedGasType.AIR]])
        gas.get_gas_properties(273.15, 101325.0)
