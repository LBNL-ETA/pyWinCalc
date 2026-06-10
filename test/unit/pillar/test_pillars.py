"""
Unit tests for the pillar bindings (src/bindings/pillar_bindings.cpp).

Construction + attribute round-trips for the pillar geometry data classes, the
cell-spacing/polygon enums, pillar_cell_area, and Glass. Pure data, no system.
"""
import math

import pywincalc


class TestEnums:
    def test_cell_spacing_values(self):
        for name in ("SQUARE", "SHIFTEDSQUARE", "SHIFTEDROTATEDSQUARE"):
            assert hasattr(pywincalc.CellSpacingType, name)

    def test_polygon_values(self):
        for name in ("TRIANGLE", "PENTAGON", "HEXAGON"):
            assert hasattr(pywincalc.PolygonType, name)


class TestPillarData:
    def test_attributes(self):
        pillar = pywincalc.PillarData(0.2, 20.0, 1e-4)
        assert pillar.height == 0.2
        assert pillar.material_conductivity == 20.0
        assert pillar.cell_area == 1e-4


class TestPillarShapes:
    def test_cylindrical(self):
        pillar = pywincalc.CylindricalPillar(0.2, 20.0, 1e-4, 5e-4)
        assert pillar.radius == 5e-4
        # inherited PillarData fields
        assert pillar.height == 0.2
        assert pillar.material_conductivity == 20.0
        assert pillar.cell_area == 1e-4

    def test_spherical(self):
        pillar = pywincalc.SphericalPillar(0.2, 20.0, 1e-4, 5e-4)
        assert pillar.radius_of_contact == 5e-4

    def test_rectangular(self):
        pillar = pywincalc.RectangularPillar(0.2, 20.0, 1e-4, 1e-3, 2e-3)
        assert pillar.length == 1e-3
        assert pillar.width == 2e-3


class TestPillarCellArea:
    def test_square_spacing_is_spacing_squared(self):
        # SQUARE spacing of sp -> cell area = sp^2
        area = pywincalc.pillar_cell_area(pywincalc.CellSpacingType.SQUARE, 0.001)
        assert math.isclose(area, 1e-6, rel_tol=1e-9)


class TestGlass:
    def test_attributes(self):
        glass = pywincalc.Glass(0.003, 1.0, 0.84)
        assert glass.thickness == 0.003
        assert glass.conductivity == 1.0
        assert glass.emissivity == 0.84
