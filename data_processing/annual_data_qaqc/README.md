# 🛠️ Automated QA/QC Example for FAF5 Annual Data

This project demonstrates one of the many automated QA/QC modules developed for the **[Freight Analysis Framework (FAF5)](https://faf.ornl.gov/faf5/)** project. These tools perform large-scale consistency and validation checks across multiple freight flow datasets before public release.

🧠 This example, combined with other validation scripts not included here, has reduced manual QA/QC processing time by **around 80%**, streamlining one of the most time-consuming parts of the FAF data release cycle.

---

## 🧾 Summary of QA/QC Checks Performed

Each module below targets a specific class of data anomalies across freight measures (`tons`, `value`, `tmiles`, `v2w`) using a flexible threshold-driven logic.

| Script | Purpose |
|--------|---------|
| `00_create_folders.py` | Prepares output directories for flagged and full results |
| `01_data_format_check.py` | Detects nulls, infinite values, and unexpected attribute patterns |
| `02_trend_over_years.py` | Flags abnormal year-to-year trends using thresholds per group and measure |
| `03_changes_from_previous_version.py` | Compares current and previous data versions to flag unusual changes |
| `04_v2w_over_years.py` | Analyzes value-to-weight ratio (`v2w`) over time for outliers |
| `05_change_of_shares.py` | Checks for major changes in modal or commodity share composition |
| `99_summary.py` | Aggregates flagged record counts by type, dimension, and measure into an Excel report |
| `_FAF5_QAQC_Run_All_.py` | Batch runner that executes all the above scripts in sequence |

---

## 🧩 Features

- **Fully Modular**: Each validation rule runs independently with configurable thresholds via Excel inputs
- **Threshold-Driven**: Analysts can adjust tolerances per commodity group, mode, or geography
- **Flagged Outputs**: Results separated into "all records" and "only flagged" folders
- **Automated Summary**: Excel file summarizes issue counts by dimension and check type
- **Scalable**: Designed to handle millions of records across multiple years and versions

---

## 🔄 Example Workflow

To run the entire QA/QC suite:

```bash
python _FAF5_QAQC_Run_All_.py
```

This script will:
- Clear and recreate output folders
- Run six independent validation checks
- Export detailed and flagged results to Excel
- Create a summary file `summary.xlsx` in `output/`

---

## 📂 Folder Structure

```
automated_qaqc_faf/
├── code/
│   ├── 00_create_folders.py
│   ├── 01_data_format_check.py
│   ├── 02_trend_over_years.py
│   ├── 03_changes_from_previous_version.py
│   ├── 04_v2w_over_years.py
│   ├── 05_change_of_shares.py
│   ├── 99_summary.py
│   └── _FAF5_QAQC_Run_All_.py
├── input/                    # Excel threshold files (not included here)
├── output/                   # Generated QA/QC reports
│   ├── all/
│   └── only_flagged/
├── README.md
```

---

## 🚀 Usage Notes

This repository does **not include data files** due to confidentiality and size limitations.

> 🔒 The code and content in this repository are intended for review purposes only and **should not be reused or redistributed without explicit permission from the author (Hyeonsup Lim).**

---

## 📬 Contact

Created by **Hyeonsup Lim, Ph.D.**  
Email: hslim8211@gmail.com  
