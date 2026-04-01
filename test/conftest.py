"""
Pytest configuration and fixtures for pywincalc tests.
"""
import gc
import os
import pytest
from pathlib import Path

# Global test directory path
TEST_DIR = Path(__file__).parent.absolute()

# Tolerance for floating point comparisons
TEST_TOLERANCE = 1e-6


def pytest_addoption(parser):
    """Add command line options for test configuration."""
    parser.addoption(
        "--update-results",
        action="store_true",
        default=False,
        help="Update expected results files instead of comparing"
    )


@pytest.fixture(scope="session")
def test_dir():
    """Return the test directory path."""
    return TEST_DIR


@pytest.fixture(scope="session")
def products_dir(test_dir):
    """Return the products directory path."""
    return test_dir / "products"


@pytest.fixture(scope="session")
def standards_dir(test_dir):
    """Return the standards directory path."""
    return test_dir / "standards"


@pytest.fixture(scope="session")
def expected_results_dir(test_dir):
    """Return the expected results directory path."""
    return test_dir / "expected_results"


@pytest.fixture(scope="session")
def update_results(request):
    """Return whether to update expected results."""
    return request.config.getoption("--update-results")


@pytest.fixture(scope="session")
def standard_path(standards_dir):
    """Return the path to the NFRC standard file."""
    return standards_dir / "W5_NFRC_2003.std"


def pytest_runtest_teardown(item, nextitem):
    """Clear test instance attributes after each test to free C++ objects.

    Pytest keeps test class instances alive for the entire session.
    Without this, every GlazingSystem created in setup fixtures stays
    in memory until the session ends.
    """
    instance = getattr(item, "instance", None)
    if instance is not None:
        for attr in list(vars(instance)):
            try:
                delattr(instance, attr)
            except (AttributeError, TypeError):
                pass
    gc.collect()
