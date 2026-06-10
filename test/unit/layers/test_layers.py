"""
Unit tests for the layers bindings (src/bindings/layers_bindings.cpp):
EffectiveMultipliers, is_closed, and the `Layers` submodule
(default_vacuum_mixture, gap, solid).

Working surface gets contract/invariant checks. Two gaps are tracked as strict
xfail:
  * Layers.solid() returns Tarcog::ISO15099::CIGUSolidLayer, which is not
    registered with pybind11 -> raises on return conversion.
  * is_closed is bound on wincalcbindings but NOT re-exported in
    pywincalc/__init__.py, so it is missing from the public package API.
"""
import math

import pytest
import pywincalc
import wincalcbindings


TOL = 1e-12


class TestEffectiveMultipliers:
    def test_construction_and_attributes(self):
        # ctor order: front, left, right, top, bot, permeability_factor
        em = pywincalc.EffectiveMultipliers(0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
        assert em.front == 0.1
        assert em.left == 0.2
        assert em.right == 0.3
        assert em.top == 0.4
        assert em.bot == 0.5
        assert em.permeability_factor == 0.6


class TestIsClosed:
    def test_returns_bool(self):
        # bound on wincalcbindings (see TestKnownBindingGaps for the missing
        # pywincalc re-export); takes an EffectiveMultipliers, returns bool.
        em = pywincalc.EffectiveMultipliers(0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
        assert isinstance(wincalcbindings.is_closed(em), bool)


class TestLayersSubmodule:
    def test_default_vacuum_mixture_is_full_gas(self):
        vacuum = pywincalc.Layers.default_vacuum_mixture()
        assert isinstance(vacuum, pywincalc.Gas)
        assert math.isclose(vacuum.total_percent(), 1.0, abs_tol=TOL)

    def test_gap_returns_gap_layer(self):
        gap = pywincalc.Layers.gap(0.0127, True)
        assert isinstance(gap, pywincalc.IGUGapLayer)


class TestKnownBindingGaps:
    @pytest.mark.xfail(
        reason="Tarcog::ISO15099::CIGUSolidLayer not registered in bindings",
        raises=TypeError, strict=True,
    )
    def test_layers_solid_converts(self):
        pywincalc.Layers.solid(0.003, 1.0)

    @pytest.mark.xfail(
        reason="is_closed bound on wincalcbindings but not re-exported in pywincalc/__init__.py",
        raises=AssertionError, strict=True,
    )
    def test_is_closed_reexported_in_pywincalc(self):
        assert hasattr(pywincalc, "is_closed")
