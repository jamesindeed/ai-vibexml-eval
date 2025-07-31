#!/usr/bin/env python3
"""
Statistical Analysis Module for LLML Evaluation

Provides objective statistical analysis for LLM evaluation research,
including effect sizes, significance testing, and descriptive statistics.
"""

from typing import Dict, List

import numpy as np
from scipy import stats


class StatisticalAnalyzer:
    """Statistical analysis utilities for academic rigor."""

    @staticmethod
    def calculate_effect_size(group1: List[float], group2: List[float]) -> Dict:
        """Calculate Cohen's d and other effect size metrics."""
        mean1, mean2 = np.mean(group1), np.mean(group2)
        std1, std2 = np.std(group1, ddof=1), np.std(group2, ddof=1)

        # Pooled standard deviation
        pooled_std = np.sqrt(
            ((len(group1) - 1) * std1**2 + (len(group2) - 1) * std2**2)
            / (len(group1) + len(group2) - 2)
        )

        # Handle division by zero (when both groups have identical scores)
        if pooled_std == 0:
            cohens_d = 0.0  # No effect when there's no variation
        else:
            cohens_d = (mean2 - mean1) / pooled_std

        return {
            "cohens_d": cohens_d,
            "effect_size_interpretation": StatisticalAnalyzer._interpret_effect_size(
                cohens_d
            ),
            "mean_difference": mean2 - mean1,
            "pooled_std": pooled_std,
        }

    @staticmethod
    def _interpret_effect_size(d: float) -> str:
        """Interpret Cohen's d effect size."""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"

    @staticmethod
    def paired_t_test(scores_a: List[float], scores_b: List[float]) -> Dict:
        """Perform paired t-test for significance testing."""
        if len(scores_a) != len(scores_b):
            raise ValueError("Score lists must have equal length")

        differences = np.array(scores_b) - np.array(scores_a)
        t_stat, p_value = stats.ttest_1samp(differences, 0)

        return {
            "t_statistic": t_stat,
            "p_value": p_value,
            "significant": p_value < 0.05,
            "degrees_freedom": len(differences) - 1,
            "mean_difference": np.mean(differences),
            "confidence_interval": stats.t.interval(
                0.95,
                len(differences) - 1,
                loc=np.mean(differences),
                scale=stats.sem(differences),
            ),
        }


class MultiJudgeValidator:
    """Utilities for multiple judge validation and consensus."""

    @staticmethod
    def calculate_inter_rater_reliability(judgments_matrix: np.ndarray) -> Dict:
        """
        Calculate inter-rater reliability metrics.

        Args:
            judgments_matrix: (n_cases, n_judges) matrix of numeric scores
        """
        # Krippendorff's Alpha approximation using Pearson correlation
        correlations = []
        n_judges = judgments_matrix.shape[1]

        for i in range(n_judges):
            for j in range(i + 1, n_judges):
                corr, _ = stats.pearsonr(judgments_matrix[:, i], judgments_matrix[:, j])
                if not np.isnan(corr):
                    correlations.append(corr)

        avg_correlation = np.mean(correlations) if correlations else 0

        return {
            "average_pairwise_correlation": avg_correlation,
            "reliability_interpretation": MultiJudgeValidator._interpret_reliability(
                avg_correlation
            ),
            "individual_correlations": correlations,
            "n_judges": n_judges,
            "n_cases": judgments_matrix.shape[0],
        }

    @staticmethod
    def _interpret_reliability(correlation: float) -> str:
        """Interpret reliability correlation."""
        if correlation >= 0.9:
            return "excellent"
        elif correlation >= 0.8:
            return "good"
        elif correlation >= 0.7:
            return "acceptable"
        elif correlation >= 0.6:
            return "questionable"
        else:
            return "poor"


class StatisticalAnalysisReporter:
    """Generate objective statistical analysis for research evaluation."""

    def __init__(self, results: Dict):
        self.results = results
        self.stats_analyzer = StatisticalAnalyzer()
        self.validator = MultiJudgeValidator()

    def generate_statistical_summary(self) -> Dict:
        """Generate comprehensive statistical analysis summary."""
        judgments = self.results["judgments"]

        # Extract scores
        raw_scores = [j.raw_text_score for j in judgments]
        vibexml_scores = [j.vibexml_score for j in judgments]

        # Statistical analysis
        effect_size = self.stats_analyzer.calculate_effect_size(
            raw_scores, vibexml_scores
        )
        significance = self.stats_analyzer.paired_t_test(raw_scores, vibexml_scores)

        # Win rate analysis
        vibexml_wins = sum(1 for j in judgments if j.winner == "vibexml")
        raw_text_wins = sum(1 for j in judgments if j.winner == "raw_text")
        ties = sum(1 for j in judgments if j.winner == "tie")
        total_cases = len(judgments)

        # Power analysis (post-hoc)
        observed_effect = effect_size["cohens_d"]
        power_analysis = self._calculate_power_analysis(total_cases, observed_effect)

        return {
            "study_design": {
                "method": "LLM-as-a-judge evaluation",
                "comparison": "Structured (VibeXML) vs Unstructured (Raw Text)",
                "design_type": "within-subjects comparison",
                "sample_size": total_cases,
                "evaluation_criteria": 5,
                "random_seed_used": True,
                "blind_evaluation": True,
            },
            "descriptive_statistics": {
                "raw_text": {
                    "mean": np.mean(raw_scores),
                    "std": np.std(raw_scores, ddof=1),
                    "median": np.median(raw_scores),
                    "min": np.min(raw_scores),
                    "max": np.max(raw_scores),
                },
                "vibexml": {
                    "mean": np.mean(vibexml_scores),
                    "std": np.std(vibexml_scores, ddof=1),
                    "median": np.median(vibexml_scores),
                    "min": np.min(vibexml_scores),
                    "max": np.max(vibexml_scores),
                },
                "difference": {
                    "mean": np.mean(vibexml_scores) - np.mean(raw_scores),
                    "std": np.std(
                        np.array(vibexml_scores) - np.array(raw_scores), ddof=1
                    ),
                },
            },
            "inferential_statistics": {
                "paired_t_test": significance,
                "effect_size": effect_size,
                "power_analysis": power_analysis,
            },
            "categorical_outcomes": {
                "vibexml_wins": vibexml_wins,
                "raw_text_wins": raw_text_wins,
                "ties": ties,
                "total_cases": total_cases,
                "vibexml_win_rate": vibexml_wins / total_cases,
                "raw_text_win_rate": raw_text_wins / total_cases,
                "tie_rate": ties / total_cases,
                "binomial_test": {
                    "p_value": stats.binomtest(vibexml_wins, total_cases, 0.5).pvalue,
                    "statistically_significant": stats.binomtest(
                        vibexml_wins, total_cases, 0.5
                    ).pvalue
                    < 0.05,
                    "null_hypothesis": "Equal probability of winning (p = 0.5)",
                },
            },
        }

    def _calculate_power_analysis(self, sample_size: int, effect_size: float) -> Dict:
        """Calculate post-hoc power analysis for the observed effect."""
        # Using Cohen's conventions for power analysis
        # Power = 1 - β (probability of correctly rejecting false null hypothesis)

        try:
            # Calculate observed power (post-hoc)
            import math

            # Critical t-value for alpha = 0.05, two-tailed
            critical_t = stats.t.ppf(0.975, sample_size - 1)

            # Non-centrality parameter
            ncp = effect_size * math.sqrt(sample_size)

            # Power calculation (simplified)
            power = 1 - stats.t.cdf(critical_t, sample_size - 1, loc=ncp)

            return {
                "observed_power": power,
                "effect_size_used": effect_size,
                "alpha_level": 0.05,
                "sample_size": sample_size,
                "critical_t_value": critical_t,
                "non_centrality_parameter": ncp,
            }
        except Exception:
            # Fallback for power analysis
            return {
                "observed_power": None,
                "effect_size_used": effect_size,
                "alpha_level": 0.05,
                "sample_size": sample_size,
                "note": "Power calculation unavailable",
            }


# Example usage for statistical analysis
if __name__ == "__main__":
    print("Statistical Analysis Module for LLML Evaluation")
    print("Provides objective statistical analysis for LLM evaluation research.")
