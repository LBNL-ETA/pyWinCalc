"""
Unit tests for the SquareMatrix binding (src/bindings/bsdf_bindings.cpp).

Pure contract/invariant tests on the exposed matrix interface - no golden data.
Mutating methods (set_zeros, set_identity, set_diagonal) modify in place and
return None; inverse() returns a new SquareMatrix.
"""
import math

import pywincalc


TOL = 1e-9


def _approx_equal(lhs, rhs, tol=TOL):
    """Element-wise approximate equality of two 2D lists."""
    if len(lhs) != len(rhs):
        return False
    return all(
        len(row_l) == len(row_r)
        and all(math.isclose(a, b, abs_tol=tol) for a, b in zip(row_l, row_r))
        for row_l, row_r in zip(lhs, rhs)
    )


class TestSquareMatrix:
    def test_construction_and_roundtrip(self):
        values = [[1.0, 2.0], [3.0, 4.0]]
        mat = pywincalc.SquareMatrix(values)
        assert mat.size() == 2
        assert mat.get_matrix() == values

    def test_size_matches_dimension(self):
        mat = pywincalc.SquareMatrix([[0.0] * 3 for _ in range(3)])
        assert mat.size() == 3

    def test_set_zeros_mutates_in_place(self):
        mat = pywincalc.SquareMatrix([[1.0, 2.0], [3.0, 4.0]])
        assert mat.set_zeros() is None
        assert mat.get_matrix() == [[0.0, 0.0], [0.0, 0.0]]

    def test_set_identity_mutates_in_place(self):
        mat = pywincalc.SquareMatrix([[5.0, 5.0], [5.0, 5.0]])
        assert mat.set_identity() is None
        assert mat.get_matrix() == [[1.0, 0.0], [0.0, 1.0]]

    def test_set_diagonal(self):
        mat = pywincalc.SquareMatrix([[0.0, 0.0], [0.0, 0.0]])
        assert mat.set_diagonal([5.0, 9.0]) is None
        assert mat.get_matrix() == [[5.0, 0.0], [0.0, 9.0]]

    def test_inverse_returns_new_matrix(self):
        mat = pywincalc.SquareMatrix([[4.0, 7.0], [2.0, 6.0]])
        inv = mat.inverse()
        assert isinstance(inv, pywincalc.SquareMatrix)
        # original is untouched (inverse does not mutate)
        assert mat.get_matrix() == [[4.0, 7.0], [2.0, 6.0]]

    def test_inverse_known_value(self):
        mat = pywincalc.SquareMatrix([[4.0, 7.0], [2.0, 6.0]])
        # closed-form inverse: 1/det * [[d,-b],[-c,a]], det = 24-14 = 10
        expected = [[0.6, -0.7], [-0.2, 0.4]]
        assert _approx_equal(mat.inverse().get_matrix(), expected)

    def test_inverse_of_identity_is_identity(self):
        mat = pywincalc.SquareMatrix([[1.0, 0.0], [0.0, 1.0]])
        assert _approx_equal(mat.inverse().get_matrix(), [[1.0, 0.0], [0.0, 1.0]])

    def test_double_inverse_roundtrips(self):
        values = [[4.0, 7.0], [2.0, 6.0]]
        mat = pywincalc.SquareMatrix(values)
        assert _approx_equal(mat.inverse().inverse().get_matrix(), values)
