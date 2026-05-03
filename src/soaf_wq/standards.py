"""Standards and threshold-selection logic for SOAF Stage 2c Level 1 + UPM usage.

This module centralizes river-type and fishery-type dependent thresholds used in
water quality impact checks:
- 99th percentile standards for BOD and total ammonia
- Fundamental Intermittent Standards (FIS) for dissolved oxygen and un-ionised ammonia

TODO: Verify each threshold value against the latest agreed SOAF/UPM methodology pack.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiverThresholds:
    """Threshold values selected for a specific river + fishery context."""

    bod_99p_mg_l: float
    total_ammonia_99p_mg_l: float
    dissolved_oxygen_fis_mg_l: float
    unionised_ammonia_fis_mg_l: float


# NOTE: Placeholder defaults are based on common UK river quality framing.
# TODO: Confirm exact class names and values used by your existing spreadsheets/tooling.
RIVER_99P_STANDARDS = {
    "high": {"bod_99p_mg_l": 3.0, "total_ammonia_99p_mg_l": 0.25},
    "good": {"bod_99p_mg_l": 4.0, "total_ammonia_99p_mg_l": 0.60},
    "moderate": {"bod_99p_mg_l": 6.0, "total_ammonia_99p_mg_l": 1.20},
    "poor": {"bod_99p_mg_l": 8.0, "total_ammonia_99p_mg_l": 2.50},
}

FISHERY_FIS_STANDARDS = {
    "salmonid": {"dissolved_oxygen_fis_mg_l": 5.0, "unionised_ammonia_fis_mg_l": 0.021},
    "cyprinid": {"dissolved_oxygen_fis_mg_l": 4.0, "unionised_ammonia_fis_mg_l": 0.025},
}


def get_thresholds(river_type: str, fishery_type: str) -> RiverThresholds:
    """Return thresholds for the selected river/fishery type.

    Args:
        river_type: River class key (e.g. ``high``, ``good``, ``moderate``, ``poor``).
        fishery_type: Fishery class key (e.g. ``salmonid``, ``cyprinid``).
    """

    river_key = river_type.strip().lower()
    fishery_key = fishery_type.strip().lower()

    if river_key not in RIVER_99P_STANDARDS:
        valid = ", ".join(sorted(RIVER_99P_STANDARDS))
        raise ValueError(f"Unknown river_type='{river_type}'. Expected one of: {valid}")

    if fishery_key not in FISHERY_FIS_STANDARDS:
        valid = ", ".join(sorted(FISHERY_FIS_STANDARDS))
        raise ValueError(f"Unknown fishery_type='{fishery_type}'. Expected one of: {valid}")

    river_vals = RIVER_99P_STANDARDS[river_key]
    fishery_vals = FISHERY_FIS_STANDARDS[fishery_key]

    return RiverThresholds(
        bod_99p_mg_l=river_vals["bod_99p_mg_l"],
        total_ammonia_99p_mg_l=river_vals["total_ammonia_99p_mg_l"],
        dissolved_oxygen_fis_mg_l=fishery_vals["dissolved_oxygen_fis_mg_l"],
        unionised_ammonia_fis_mg_l=fishery_vals["unionised_ammonia_fis_mg_l"],
    )
