"""SOAF water quality impact scoring logic.

Preserves a simple additive scoring shape: each failed standard contributes one
impact point, compared upstream vs downstream.

TODO: Review whether parameter weights should be non-uniform in your official method.
"""

from __future__ import annotations

from dataclasses import dataclass

from .standards import RiverThresholds


@dataclass(frozen=True)
class SampleMetrics:
    """Observed concentrations/statistics for a location (upstream/downstream)."""

    bod_99p_mg_l: float
    total_ammonia_99p_mg_l: float
    dissolved_oxygen_min_mg_l: float
    unionised_ammonia_max_mg_l: float


@dataclass(frozen=True)
class ScoreBreakdown:
    """Detailed binary failures and total score for a sample against thresholds."""

    bod_fail: int
    total_ammonia_fail: int
    dissolved_oxygen_fail: int
    unionised_ammonia_fail: int

    @property
    def total(self) -> int:
        return self.bod_fail + self.total_ammonia_fail + self.dissolved_oxygen_fail + self.unionised_ammonia_fail


def score_sample(sample: SampleMetrics, thresholds: RiverThresholds) -> ScoreBreakdown:
    """Score a sample against standards (1 point per exceedance/non-compliance)."""

    return ScoreBreakdown(
        bod_fail=int(sample.bod_99p_mg_l > thresholds.bod_99p_mg_l),
        total_ammonia_fail=int(sample.total_ammonia_99p_mg_l > thresholds.total_ammonia_99p_mg_l),
        dissolved_oxygen_fail=int(sample.dissolved_oxygen_min_mg_l < thresholds.dissolved_oxygen_fis_mg_l),
        unionised_ammonia_fail=int(sample.unionised_ammonia_max_mg_l > thresholds.unionised_ammonia_fis_mg_l),
    )


def classify_impact(upstream_score: int, downstream_score: int) -> str:
    """Classify CSO impact from upstream-vs-downstream score delta.

    TODO: Confirm class boundaries against the currently accepted UPM scoring table.
    """

    delta = downstream_score - upstream_score
    if delta <= 0:
        return "no_deterioration"
    if delta == 1:
        return "minor_impact"
    if delta == 2:
        return "moderate_impact"
    return "major_impact"


def assess_reach_impact(
    upstream: SampleMetrics,
    downstream: SampleMetrics,
    thresholds: RiverThresholds,
) -> dict:
    """End-to-end assessment bundle for one reach."""

    up = score_sample(upstream, thresholds)
    down = score_sample(downstream, thresholds)
    impact_class = classify_impact(up.total, down.total)

    return {
        "upstream": up,
        "downstream": down,
        "upstream_total": up.total,
        "downstream_total": down.total,
        "delta": down.total - up.total,
        "impact_classification": impact_class,
    }
