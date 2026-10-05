"""Constructed examples for the I-MR calculations and Western Electric rules."""

import unittest

from src.spc import compute_imr_limits, western_electric_signals


class ImrLimitTests(unittest.TestCase):
    def test_limits_use_adjacent_absolute_differences(self):
        result = compute_imr_limits([10, 12, 11, 15])
        self.assertEqual(result.moving_ranges, (2.0, 1.0, 4.0))
        self.assertAlmostEqual(result.moving_range_center, 7 / 3)
        self.assertAlmostEqual(result.individuals_center, 12.0)
        self.assertAlmostEqual(result.individuals_ucl, 12 + 3 * (7 / 3) / 1.128)
        self.assertAlmostEqual(result.moving_range_ucl, 3.267 * (7 / 3))
        self.assertEqual(result.moving_range_lcl, 0.0)

    def test_rejects_too_few_or_nonfinite_points(self):
        with self.assertRaises(ValueError):
            compute_imr_limits([2])
        with self.assertRaises(ValueError):
            compute_imr_limits([2, float("nan")])


class WesternElectricRuleTests(unittest.TestCase):
    def test_rule_1_flags_a_point_beyond_three_sigma(self):
        signals = western_electric_signals([0, 3.1], center_line=0, sigma=1)
        self.assertIn((1, 1, 1, "above"), [(s.rule, s.start_index, s.end_index, s.direction) for s in signals])

    def test_rule_2_flags_two_of_three_beyond_two_sigma_on_same_side(self):
        signals = western_electric_signals([2.1, 0.5, 2.2], center_line=0, sigma=1)
        self.assertIn((2, 0, 2, "above"), [(s.rule, s.start_index, s.end_index, s.direction) for s in signals])

    def test_rule_3_flags_four_of_five_beyond_one_sigma_on_same_side(self):
        signals = western_electric_signals([1.1, 1.2, 0.2, 1.3, 1.4], center_line=0, sigma=1)
        self.assertIn((3, 0, 4, "above"), [(s.rule, s.start_index, s.end_index, s.direction) for s in signals])

    def test_rule_4_flags_eight_consecutive_points_on_one_side(self):
        signals = western_electric_signals([0.5] * 8, center_line=0, sigma=1)
        self.assertIn((4, 0, 7, "above"), [(s.rule, s.start_index, s.end_index, s.direction) for s in signals])

    def test_zone_boundaries_are_strict(self):
        signals = western_electric_signals([3.0, 2.0, 0.0], center_line=0, sigma=1)
        self.assertEqual(signals, ())

    def test_rejects_zero_sigma(self):
        with self.assertRaises(ValueError):
            western_electric_signals([1], center_line=0, sigma=0)


if __name__ == "__main__":
    unittest.main()
