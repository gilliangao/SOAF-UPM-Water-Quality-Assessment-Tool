import pytest

from soaf_wq.standards import get_thresholds


def test_get_thresholds_selects_expected_values():
    thresholds = get_thresholds("good", "salmonid")

    assert thresholds.bod_99p_mg_l == 4.0
    assert thresholds.total_ammonia_99p_mg_l == 0.60
    assert thresholds.dissolved_oxygen_fis_mg_l == 5.0
    assert thresholds.unionised_ammonia_fis_mg_l == 0.021


def test_get_thresholds_accepts_mixed_case_and_spaces():
    thresholds = get_thresholds("  MODERATE  ", "Cyprinid")

    assert thresholds.bod_99p_mg_l == 6.0
    assert thresholds.dissolved_oxygen_fis_mg_l == 4.0


def test_get_thresholds_rejects_unknown_river_type():
    with pytest.raises(ValueError, match="Unknown river_type"):
        get_thresholds("unknown", "salmonid")


def test_get_thresholds_rejects_unknown_fishery_type():
    with pytest.raises(ValueError, match="Unknown fishery_type"):
        get_thresholds("good", "unknown")
