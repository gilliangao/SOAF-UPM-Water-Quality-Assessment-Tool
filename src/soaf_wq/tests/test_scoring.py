from soaf_wq.scoring import (
    SampleMetrics,
    assess_reach_impact,
    classify_impact,
    score_sample,
)
from soaf_wq.standards import get_thresholds


def test_score_sample_flags_failures_correctly():
    thresholds = get_thresholds("good", "salmonid")
    sample = SampleMetrics(
        bod_99p_mg_l=5.1,
        total_ammonia_99p_mg_l=0.4,
        dissolved_oxygen_min_mg_l=4.8,
        unionised_ammonia_max_mg_l=0.03,
    )

    score = score_sample(sample, thresholds)

    assert score.bod_fail == 1
    assert score.total_ammonia_fail == 0
    assert score.dissolved_oxygen_fail == 1
    assert score.unionised_ammonia_fail == 1
    assert score.total == 3


def test_classify_impact_boundaries():
    assert classify_impact(1, 1) == "no_deterioration"
    assert classify_impact(1, 2) == "minor_impact"
    assert classify_impact(1, 3) == "moderate_impact"
    assert classify_impact(1, 4) == "major_impact"


def test_assess_reach_impact_returns_expected_bundle():
    thresholds = get_thresholds("good", "salmonid")
    upstream = SampleMetrics(3.0, 0.2, 6.0, 0.01)
    downstream = SampleMetrics(5.0, 0.8, 4.8, 0.03)

    result = assess_reach_impact(upstream, downstream, thresholds)

    assert result["upstream_total"] == 0
    assert result["downstream_total"] == 4
    assert result["delta"] == 4
    assert result["impact_classification"] == "major_impact"
