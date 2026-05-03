# SOAF-UPM-Water-Quality-Assessment-Tool

Initial modularization scaffold for a SOAF Stage 2c Level 1 + UPM water-quality tool.

## Proposed folder structure

```text
.
├── README.md
├── pyproject.toml
└── src/
    └── soaf_wq/
        ├── __init__.py
        ├── standards.py         # River type + fishery type threshold selection
        ├── scoring.py           # SOAF scoring and impact classification logic
        └── tests/
            ├── __init__.py
            ├── test_standards.py
            └── test_scoring.py
```

## Notes

- Existing repo had no implemented calculation code, so this scaffold introduces baseline module boundaries.
- Threshold and classification values include TODO markers where methodology sign-off is needed.
- Preserve/port any existing spreadsheet calculations into `standards.py` and `scoring.py` as the next step.
