"""
Test utility functions for pywincalc tests.

Provides functions for:
- Loading and saving expected results
- Comparing thermal and optical results
- Converting pywincalc results to comparable dictionaries
"""
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pywincalc

# Import from conftest
from conftest import TEST_DIR, TEST_TOLERANCE


def get_expected_results_path(
    test_name: str,
    results_name: str,
    spectrum: str = "condensed_spectrum",
    theta: float = 0,
    phi: float = 0
) -> Path:
    """
    Get the path to an expected results file.

    Args:
        test_name: Test case name (e.g., "1_layer/nfrc_102/default")
        results_name: Result file name without extension (e.g., "thermal_U_Environment")
        spectrum: Spectrum type ("condensed_spectrum" or "full_spectrum")
        theta: Incidence angle theta
        phi: Incidence angle phi

    Returns:
        Path to the expected results JSON file
    """
    angle_dir = f"theta={int(theta)}_phi={int(phi)}"
    return TEST_DIR / "expected_results" / test_name / spectrum / angle_dir / f"{results_name}.json"


def load_expected_results(
    test_name: str,
    results_name: str,
    spectrum: str = "condensed_spectrum",
    theta: float = 0,
    phi: float = 0
) -> Optional[Dict[str, Any]]:
    """
    Load expected results from a JSON file.

    Returns None if the file doesn't exist.
    """
    path = get_expected_results_path(test_name, results_name, spectrum, theta, phi)
    if not path.exists():
        return None

    with open(path, 'r') as file:
        return json.load(file)


def save_expected_results(
    test_name: str,
    results_name: str,
    results: Dict[str, Any],
    spectrum: str = "condensed_spectrum",
    theta: float = 0,
    phi: float = 0
) -> None:
    """
    Save results to an expected results JSON file.

    Creates directories if they don't exist.
    """
    path = get_expected_results_path(test_name, results_name, spectrum, theta, phi)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w') as file:
        json.dump(results, file, indent=4, default=_json_serializer)


def _json_serializer(obj: Any) -> Any:
    """Custom JSON serializer for special float values."""
    if isinstance(obj, float):
        if math.isnan(obj):
            return None
        if math.isinf(obj):
            return None
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def compare_values(
    actual: Union[float, int],
    expected: Union[float, int, None],
    name: str,
    tolerance: float = TEST_TOLERANCE
) -> List[str]:
    """
    Compare two numeric values with tolerance.

    Returns a list of error messages (empty if values match).
    """
    errors = []

    # Handle None (represents NaN/inf in expected results)
    if expected is None:
        if actual is not None and not (math.isnan(actual) if isinstance(actual, float) else False):
            errors.append(f"{name}: expected None/NaN, got {actual}")
        return errors

    if actual is None:
        errors.append(f"{name}: expected {expected}, got None")
        return errors

    # Handle NaN
    if isinstance(expected, float) and math.isnan(expected):
        if not (isinstance(actual, float) and math.isnan(actual)):
            errors.append(f"{name}: expected NaN, got {actual}")
        return errors

    # Compare with tolerance
    if abs(actual - expected) > tolerance:
        errors.append(f"{name}: expected {expected}, got {actual}, diff={abs(actual - expected)}")

    return errors


def compare_lists(
    actual: List[float],
    expected: List[float],
    name: str,
    tolerance: float = TEST_TOLERANCE
) -> List[str]:
    """
    Compare two lists of numeric values.

    Returns a list of error messages.
    """
    errors = []

    if len(actual) != len(expected):
        errors.append(f"{name}: length mismatch, expected {len(expected)}, got {len(actual)}")
        return errors

    for idx, (act, exp) in enumerate(zip(actual, expected)):
        errors.extend(compare_values(act, exp, f"{name}[{idx}]", tolerance))

    return errors


def get_thermal_results(
    glazing_system: pywincalc.GlazingSystem,
    theta: float = 0,
    phi: float = 0
) -> Dict[str, Any]:
    """
    Extract thermal results from a glazing system.

    Returns a dictionary with all thermal metrics.
    """
    results = {}

    # U-value and SHGC
    results["U"] = glazing_system.u(theta, phi)
    results["SHGC"] = glazing_system.shgc(theta, phi)

    # Relative heat gain
    results["relative_heat_gain"] = glazing_system.relative_heat_gain(theta, phi)

    # Layer temperatures
    results["layer_temperatures_u"] = glazing_system.layer_temperatures(
        pywincalc.TarcogSystemType.U, theta, phi
    )
    results["layer_temperatures_shgc"] = glazing_system.layer_temperatures(
        pywincalc.TarcogSystemType.SHGC, theta, phi
    )

    # Effective conductivities
    results["solid_layer_effective_conductivities_u"] = glazing_system.solid_layers_effective_conductivities(
        pywincalc.TarcogSystemType.U, theta, phi
    )
    results["solid_layer_effective_conductivities_shgc"] = glazing_system.solid_layers_effective_conductivities(
        pywincalc.TarcogSystemType.SHGC, theta, phi
    )
    results["gap_layer_effective_conductivities_u"] = glazing_system.gap_layers_effective_conductivities(
        pywincalc.TarcogSystemType.U, theta, phi
    )
    results["gap_layer_effective_conductivities_shgc"] = glazing_system.gap_layers_effective_conductivities(
        pywincalc.TarcogSystemType.SHGC, theta, phi
    )
    results["system_effective_conductivity_u"] = glazing_system.system_effective_conductivity(
        pywincalc.TarcogSystemType.U, theta, phi
    )
    results["system_effective_conductivity_shgc"] = glazing_system.system_effective_conductivity(
        pywincalc.TarcogSystemType.SHGC, theta, phi
    )

    # Heat flow
    results["heat_flow_u_indoor"] = glazing_system.heat_flow(
        pywincalc.TarcogSystemType.U, pywincalc.TarcogEnvironmentType.Indoor, theta, phi
    )
    results["heat_flow_u_outdoor"] = glazing_system.heat_flow(
        pywincalc.TarcogSystemType.U, pywincalc.TarcogEnvironmentType.Outdoor, theta, phi
    )
    results["heat_flow_shgc_indoor"] = glazing_system.heat_flow(
        pywincalc.TarcogSystemType.SHGC, pywincalc.TarcogEnvironmentType.Indoor, theta, phi
    )
    results["heat_flow_shgc_outdoor"] = glazing_system.heat_flow(
        pywincalc.TarcogSystemType.SHGC, pywincalc.TarcogEnvironmentType.Outdoor, theta, phi
    )

    # H values (convection coefficients)
    results["H_u_indoor"] = glazing_system.h(
        pywincalc.TarcogSystemType.U, pywincalc.TarcogEnvironmentType.Indoor, theta, phi
    )
    results["H_u_outdoor"] = glazing_system.h(
        pywincalc.TarcogSystemType.U, pywincalc.TarcogEnvironmentType.Outdoor, theta, phi
    )
    results["H_shgc_indoor"] = glazing_system.h(
        pywincalc.TarcogSystemType.SHGC, pywincalc.TarcogEnvironmentType.Indoor, theta, phi
    )
    results["H_shgc_outdoor"] = glazing_system.h(
        pywincalc.TarcogSystemType.SHGC, pywincalc.TarcogEnvironmentType.Outdoor, theta, phi
    )

    # Radiosities
    results["radiosities_u"] = glazing_system.radiosities(
        pywincalc.TarcogSystemType.U, theta, phi
    )
    results["radiosities_shgc"] = glazing_system.radiosities(
        pywincalc.TarcogSystemType.SHGC, theta, phi
    )

    return results


def get_optical_results(
    glazing_system: pywincalc.GlazingSystem,
    method_name: str,
    theta: float = 0,
    phi: float = 0
) -> Dict[str, Any]:
    """
    Extract optical results for a specific method from a glazing system.

    Args:
        glazing_system: The glazing system to test
        method_name: Optical method name (e.g., "SOLAR", "PHOTOPIC")
        theta: Incidence angle theta
        phi: Incidence angle phi

    Returns a dictionary with optical results.
    """
    optical = glazing_system.optical_method_results(method_name, theta, phi)

    results = {
        "system_results": {
            "front": {
                "transmittance": {
                    "direct_direct": optical.system_results.front.transmittance.direct_direct,
                    "direct_diffuse": optical.system_results.front.transmittance.direct_diffuse,
                    "direct_hemispherical": optical.system_results.front.transmittance.direct_hemispherical,
                    "diffuse_diffuse": optical.system_results.front.transmittance.diffuse_diffuse,
                },
                "reflectance": {
                    "direct_direct": optical.system_results.front.reflectance.direct_direct,
                    "direct_diffuse": optical.system_results.front.reflectance.direct_diffuse,
                    "direct_hemispherical": optical.system_results.front.reflectance.direct_hemispherical,
                    "diffuse_diffuse": optical.system_results.front.reflectance.diffuse_diffuse,
                },
            },
            "back": {
                "transmittance": {
                    "direct_direct": optical.system_results.back.transmittance.direct_direct,
                    "direct_diffuse": optical.system_results.back.transmittance.direct_diffuse,
                    "direct_hemispherical": optical.system_results.back.transmittance.direct_hemispherical,
                    "diffuse_diffuse": optical.system_results.back.transmittance.diffuse_diffuse,
                },
                "reflectance": {
                    "direct_direct": optical.system_results.back.reflectance.direct_direct,
                    "direct_diffuse": optical.system_results.back.reflectance.direct_diffuse,
                    "direct_hemispherical": optical.system_results.back.reflectance.direct_hemispherical,
                    "diffuse_diffuse": optical.system_results.back.reflectance.diffuse_diffuse,
                },
            },
        },
        "layer_results": {},
    }

    # Add layer results
    for idx, layer in enumerate(optical.layer_results):
        layer_key = f"layer {idx}"
        results["layer_results"][layer_key] = {
            "front": {
                "absorptance": {
                    "total_direct": layer.front.absorptance.total_direct,
                    "total_diffuse": layer.front.absorptance.total_diffuse,
                    "heat_direct": layer.front.absorptance.heat_direct,
                    "heat_diffuse": layer.front.absorptance.heat_diffuse,
                    "electricity_direct": layer.front.absorptance.electricity_direct,
                    "electricity_diffuse": layer.front.absorptance.electricity_diffuse,
                },
            },
            "back": {
                "absorptance": {
                    "total_direct": layer.back.absorptance.total_direct,
                    "total_diffuse": layer.back.absorptance.total_diffuse,
                    "heat_direct": layer.back.absorptance.heat_direct,
                    "heat_diffuse": layer.back.absorptance.heat_diffuse,
                    "electricity_direct": layer.back.absorptance.electricity_direct,
                    "electricity_diffuse": layer.back.absorptance.electricity_diffuse,
                },
            },
        }

    # Add empty attachment placeholders (matching WinCalc format)
    results["layer_results"]["noncoplanar_attachment_exterior"] = {}
    results["layer_results"]["noncoplanar_attachment_interior"] = {}

    return results


def compare_thermal_results(
    actual: Dict[str, Any],
    expected: Dict[str, Any],
    tolerance: float = TEST_TOLERANCE
) -> List[str]:
    """
    Compare thermal results dictionaries.

    Returns a list of error messages (empty if all values match).
    """
    errors = []

    # Compare scalar values
    scalar_keys = [
        "U", "SHGC", "relative_heat_gain",
        "system_effective_conductivity_u", "system_effective_conductivity_shgc",
        "heat_flow_u_indoor", "heat_flow_u_outdoor",
        "heat_flow_shgc_indoor", "heat_flow_shgc_outdoor",
        "H_u_indoor", "H_u_outdoor", "H_shgc_indoor", "H_shgc_outdoor",
    ]

    for key in scalar_keys:
        if key in expected:
            errors.extend(compare_values(actual.get(key), expected.get(key), key, tolerance))

    # Compare list values
    list_keys = [
        "layer_temperatures_u", "layer_temperatures_shgc",
        "solid_layer_effective_conductivities_u", "solid_layer_effective_conductivities_shgc",
        "gap_layer_effective_conductivities_u", "gap_layer_effective_conductivities_shgc",
        "radiosities_u", "radiosities_shgc",
    ]

    for key in list_keys:
        if key in expected:
            errors.extend(compare_lists(actual.get(key, []), expected.get(key, []), key, tolerance))

    return errors


def compare_optical_results(
    actual: Dict[str, Any],
    expected: Dict[str, Any],
    tolerance: float = TEST_TOLERANCE
) -> List[str]:
    """
    Compare optical results dictionaries.

    Returns a list of error messages (empty if all values match).
    """
    errors = []

    # Compare system results
    for side in ["front", "back"]:
        for prop_type in ["transmittance", "reflectance"]:
            for flux_type in ["direct_direct", "direct_diffuse", "direct_hemispherical", "diffuse_diffuse"]:
                key_path = f"system_results.{side}.{prop_type}.{flux_type}"
                actual_val = actual.get("system_results", {}).get(side, {}).get(prop_type, {}).get(flux_type)
                expected_val = expected.get("system_results", {}).get(side, {}).get(prop_type, {}).get(flux_type)
                if expected_val is not None:
                    errors.extend(compare_values(actual_val, expected_val, key_path, tolerance))

    # Compare layer results
    for layer_key in expected.get("layer_results", {}):
        if layer_key.startswith("layer "):
            for side in ["front", "back"]:
                for absorb_type in ["total_direct", "total_diffuse", "heat_direct", "heat_diffuse",
                                     "electricity_direct", "electricity_diffuse"]:
                    key_path = f"layer_results.{layer_key}.{side}.absorptance.{absorb_type}"
                    actual_val = (actual.get("layer_results", {}).get(layer_key, {})
                                  .get(side, {}).get("absorptance", {}).get(absorb_type))
                    expected_val = (expected.get("layer_results", {}).get(layer_key, {})
                                    .get(side, {}).get("absorptance", {}).get(absorb_type))
                    if expected_val is not None:
                        errors.extend(compare_values(actual_val, expected_val, key_path, tolerance))

    return errors


def check_thermal_results(
    test_name: str,
    results_name: str,
    glazing_system: pywincalc.GlazingSystem,
    update_results: bool = False,
    theta: float = 0,
    phi: float = 0,
    spectrum: str = "condensed_spectrum"
) -> None:
    """
    Check thermal results against expected values.

    If update_results is True, saves current results as expected values.
    Otherwise, compares and raises AssertionError on mismatch.
    """
    actual = get_thermal_results(glazing_system, theta, phi)

    if update_results:
        save_expected_results(test_name, results_name, actual, spectrum, theta, phi)
        return

    expected = load_expected_results(test_name, results_name, spectrum, theta, phi)
    if expected is None:
        raise FileNotFoundError(
            f"Expected results not found: {get_expected_results_path(test_name, results_name, spectrum, theta, phi)}"
        )

    errors = compare_thermal_results(actual, expected)
    if errors:
        raise AssertionError(f"Thermal results mismatch:\n" + "\n".join(errors))


def check_optical_results(
    test_name: str,
    method_name: str,
    glazing_system: pywincalc.GlazingSystem,
    update_results: bool = False,
    theta: float = 0,
    phi: float = 0,
    spectrum: str = "condensed_spectrum"
) -> None:
    """
    Check optical results for a specific method against expected values.

    If update_results is True, saves current results as expected values.
    Otherwise, compares and raises AssertionError on mismatch.
    """
    actual = get_optical_results(glazing_system, method_name, theta, phi)
    results_file_name = method_name.lower()

    if update_results:
        save_expected_results(test_name, results_file_name, actual, spectrum, theta, phi)
        return

    expected = load_expected_results(test_name, results_file_name, spectrum, theta, phi)
    if expected is None:
        raise FileNotFoundError(
            f"Expected results not found: {get_expected_results_path(test_name, results_file_name, spectrum, theta, phi)}"
        )

    errors = compare_optical_results(actual, expected)
    if errors:
        raise AssertionError(f"Optical results mismatch for {method_name}:\n" + "\n".join(errors))
