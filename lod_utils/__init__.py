from __future__ import annotations

from statistics import mean, stdev
from typing import Iterable, List, Sequence, Tuple


def prepare_measurement_data(records: Sequence[dict]) -> Tuple[List[float], List[Tuple[float, float]]]:
    blank_signals: List[float] = []
    calibration: List[Tuple[float, float]] = []

    for record in records:
        measurement_type = str(record.get("measurement_type", "")).strip().lower()
        signal = record.get("signal")
        concentration = record.get("concentration")

        if measurement_type == "blank":
            if signal is None:
                continue
            blank_signals.append(float(signal))
        elif measurement_type == "standard":
            if signal is None or concentration is None:
                continue
            calibration.append((float(concentration), float(signal)))

    return blank_signals, calibration


def calculate_lod(blank_signals: Sequence[float], calibration: Sequence[Tuple[float, float]]) -> float:
    if len(blank_signals) < 2:
        raise ValueError("Mindestens zwei Blindwerte werden benötigt.")
    if len(calibration) < 2:
        raise ValueError("Mindestens zwei Kalibrierpunkte werden benötigt.")

    slope = _calculate_slope(calibration)
    if slope == 0:
        raise ValueError("Die Kalibriergerade hat eine Steigung von 0.")

    blank_sd = stdev(blank_signals)
    return 3.3 * blank_sd / slope


def _calculate_slope(calibration: Sequence[Tuple[float, float]]) -> float:
    x_values = [x for x, _ in calibration]
    y_values = [y for _, y in calibration]
    x_mean = mean(x_values)
    y_mean = mean(y_values)

    numerator = sum((x - x_mean) * (y - y_mean) for x, y in calibration)
    denominator = sum((x - x_mean) ** 2 for x, _ in calibration)

    if denominator == 0:
        return 0.0

    return numerator / denominator
