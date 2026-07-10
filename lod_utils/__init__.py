from __future__ import annotations

from statistics import mean, pstdev, stdev
from typing import Iterable, List, Sequence, Tuple


def prepare_measurement_data(records: Sequence[dict]) -> Tuple[List[float], List[Tuple[float, float]]]:
    blank_signals: List[float] = []
    calibration: List[Tuple[float, float]] = []
    # Helfer: sichere Float-Konvertierung (auch Dezimalkomma)
    def _to_float(x):
        if x is None:
            return None
        try:
            s = str(x).strip()
            if s == '':
                return None
            s = s.replace(',', '.')
            return float(s)
        except Exception:
            return None

    # Sammle alle Schlüssel (erwartet: bereits normalisierte Spaltennamen)
    keys = set()
    for r in records:
        keys.update(k for k in r.keys())

    # Erkenne, ob eine eigene Spalte für Blindwerte existiert (z.B. 'blank')
    blank_field_candidates = {
        'blank', 'blank_value', 'blank_wert', 'blankwert', 'blank_signal', 'blanksignal', 'blank_value'
    }
    blank_field = None
    for cand in blank_field_candidates:
        if cand in keys:
            blank_field = cand
            break

    # Wenn eine Blank-Spalte vorhanden ist, nutze deren Werte nur für Zeilen mit measurement_type == 'blank'
    if blank_field:
        has_measurement_type = 'measurement_type' in keys
        for record in records:
            if has_measurement_type:
                measurement_type = str(record.get("measurement_type", "")).strip().lower()
                if measurement_type != "blank":
                    continue
            val = _to_float(record.get(blank_field))
            if val is not None:
                blank_signals.append(val)
    else:
        # Fallback: nutze rows mit measurement_type == 'blank'
        for record in records:
            measurement_type = str(record.get("measurement_type", "")).strip().lower()
            signal = _to_float(record.get("signal"))
            if measurement_type == "blank":
                if signal is None:
                    continue
                blank_signals.append(signal)

    # Kalibrierpunkte: sichere Konvertierung und akzeptiere gängige Bezeichnungen
    for record in records:
        measurement_type = str(record.get("measurement_type", "")).strip().lower()
        signal = _to_float(record.get("signal"))
        concentration = _to_float(record.get("concentration"))

        if measurement_type in {"standard", "calibration", "std", "cal" , "kalibrierung", "kalibration"}:
            if signal is None or concentration is None:
                continue
            calibration.append((concentration, signal))

    return blank_signals, calibration


def calculate_lod(blank_signals: Sequence[float], calibration: Sequence[Tuple[float, float]], ddof: int = 1) -> float:
    if len(blank_signals) < 2:
        raise ValueError("Mindestens zwei Blindwerte werden benötigt.")
    if len(calibration) < 2:
        raise ValueError("Mindestens zwei Kalibrierpunkte werden benötigt.")

    slope = _calculate_slope(calibration)
    if slope == 0:
        raise ValueError("Die Kalibriergerade hat eine Steigung von 0.")

    blank_sd = stdev(blank_signals) if ddof == 1 else pstdev(blank_signals) if ddof == 1 else pstdev(blank_signals)
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
