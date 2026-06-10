"""
Unit tests for the layers bindings (src/bindings/layers_bindings.cpp):
EffectiveMultipliers, is_closed, and the `Layers` submodule
(default_vacuum_mixture, gap, solid).

All contract/invariant checks. (CIGUSolidLayer is now registered as
IGUSolidLayer and is_closed is now re-exported in pywincalc/__init__.py -
both were previously gaps.)
"""
import math

import pywincalc


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
    def test_reexported_and_returns_bool(self):
        # is_closed is exposed on the public package and takes an
        # EffectiveMultipliers, returning bool.
        assert hasattr(pywincalc, "is_closed")
        em = pywincalc.EffectiveMultipliers(0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
        assert isinstance(pywincalc.is_closed(em), bool)


class TestLayersSubmodule:
    def test_default_vacuum_mixture_is_full_gas(self):
        vacuum = pywincalc.Layers.default_vacuum_mixture()
        assert isinstance(vacuum, pywincalc.Gas)
        assert math.isclose(vacuum.total_percent(), 1.0, abs_tol=TOL)

    def test_gap_returns_gap_layer(self):
        gap = pywincalc.Layers.gap(0.0127, True)
        assert isinstance(gap, pywincalc.IGUGapLayer)

    def test_solid_returns_solid_layer(self):
        solid = pywincalc.Layers.solid(0.003, 1.0)
        assert isinstance(solid, pywincalc.IGUSolidLayer)
