import unittest
from statistics import stdev

from lod_utils import calculate_lod, prepare_measurement_data


class LodLogicTests(unittest.TestCase):
    def test_prepare_measurement_data_filters_and_converts(self):
        data = [
            {"measurement_type": "blank", "concentration": None, "signal": 0.0019},
            {"measurement_type": "blank", "concentration": None, "signal": 0.0021},
            {"measurement_type": "standard", "concentration": 1.0, "signal": 0.0195},
            {"measurement_type": "standard", "concentration": 2.0, "signal": 0.0391},
        ]

        blank_signals, calibration = prepare_measurement_data(data)

        self.assertEqual(blank_signals, [0.0019, 0.0021])
        self.assertEqual(calibration, [(1.0, 0.0195), (2.0, 0.0391)])

    def test_calculate_lod_matches_expected_formula(self):
        blank_signals = [0.0010, 0.0012, 0.0011]
        calibration = [(1.0, 0.0100), (2.0, 0.0200), (3.0, 0.0300)]

        lod = calculate_lod(blank_signals, calibration)
        expected = 3.3 * stdev(blank_signals) / 0.01

        self.assertAlmostEqual(lod, expected, places=8)


if __name__ == "__main__":
    unittest.main()
