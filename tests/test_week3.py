"""Constructed tests for Days 15-21 yield, capability, association and PCA."""

import unittest

import numpy as np
import pandas as pd

from src.association import benjamini_hochberg, compare_pass_fail
from src.multivariate import fit_pca_monitor, score_pca_monitor
from src.quality import capability_summary, summarize_yield


class YieldAndCapabilityTests(unittest.TestCase):
    def test_yield_counts_and_wilson_interval(self):
        result = summarize_yield([-1] * 90 + [1] * 10)
        self.assertEqual((result.pass_count, result.fail_count, result.total), (90, 10, 100))
        self.assertAlmostEqual(result.yield_fraction, 0.9)
        self.assertLess(result.ci_low, result.yield_fraction)
        self.assertGreater(result.ci_high, result.yield_fraction)

    def test_yield_rejects_unknown_labels(self):
        with self.assertRaises(ValueError):
            summarize_yield([-1, 0, 1])

    def test_capability_uses_declared_specs_and_sample_sigma(self):
        result = capability_summary([9.8, 10.0, 10.2, 10.1, 9.9], 9.0, 11.0)
        self.assertEqual(result.sample_size, 5)
        self.assertAlmostEqual(result.process_mean, 10.0)
        self.assertAlmostEqual(result.cp, 2.0 / (6 * np.std([9.8, 10, 10.2, 10.1, 9.9], ddof=1)))
        self.assertAlmostEqual(result.cpk, result.cp)

    def test_capability_rejects_invalid_specs(self):
        with self.assertRaises(ValueError):
            capability_summary([1, 2, 3], 4, 2)


class AssociationTests(unittest.TestCase):
    def test_bh_adjustment_preserves_order_and_nan(self):
        result = benjamini_hochberg(np.array([0.01, 0.04, 0.03, np.nan]))
        self.assertTrue(np.isnan(result[3]))
        self.assertAlmostEqual(result[0], 0.03)
        self.assertAlmostEqual(result[1], 0.04)
        self.assertAlmostEqual(result[2], 0.04)

    def test_pass_fail_comparison_reports_effect_and_adjusted_p(self):
        features = pd.DataFrame({"shifted": [1, 2, 1.1, 2.1, 1.2, 2.2]})
        labels = pd.Series([-1, -1, -1, 1, 1, 1])
        result = compare_pass_fail(features, labels, minimum_per_class=3)
        self.assertGreater(result.loc["shifted", "hedges_g_fail_minus_pass"], 0)
        self.assertLessEqual(result.loc["shifted", "q_value_bh"], 1)


class PcaMonitoringTests(unittest.TestCase):
    def test_fit_on_baseline_and_score_flags_later_outlier(self):
        rng = np.random.default_rng(27)
        baseline = pd.DataFrame(rng.normal(size=(80, 4)), columns=list("abcd"))
        later = pd.DataFrame(rng.normal(size=(10, 4)), columns=list("abcd"))
        later.loc[0, "a"] = 12.0
        monitor = fit_pca_monitor(baseline, variance_retained=0.9, threshold_quantile=0.95)
        scored = score_pca_monitor(monitor, later)
        self.assertEqual(scored.shape[0], 10)
        self.assertTrue(scored.loc[0, "investigate"])

    def test_pca_rejects_empty_feature_selection(self):
        constant = pd.DataFrame({"constant": [1.0] * 12})
        with self.assertRaises(ValueError):
            fit_pca_monitor(constant)


if __name__ == "__main__":
    unittest.main()
