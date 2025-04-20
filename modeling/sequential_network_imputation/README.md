# 🛣️ Graph-based Sequential Network Imputation Method (Submitted for Provisional Patent)

This project develops a scalable and accurate imputation framework to estimate detailed **truck class-level traffic data** for 99% of network links using less than 1% observed volume data. The method was designed for national highway networks, where vehicle-specific counts are sparsely observed (e.g., TMAS or HPMS stations).

🔬 The method was submitted for a **provisional patent** sponsored by Oak Ridge National Laboratory.  
📄 Technology disclosure: [ORNL Innovation: 202305486](https://www.ornl.gov/technology/202305486)

---

## 🧠 Problem

Most U.S. roadway links lack detailed truck volume data by vehicle class. Manual imputation is not scalable. Existing spatial interpolation methods fail to maintain network structure and can’t adapt to class-level estimation needs.

---

## 💡 Solution

Developed a **sequential, graph-based imputation approach** that propagates observed vehicle class data across the network by:
- Building a NetworkX graph of roadway links with directional information
- Identifying "nearby" links using connectivity (not just Euclidean distance)
- Iteratively updating missing values using volume-weighted local estimates
- Running separate loops for:
  - HPMS-level total truck volume
  - TMAS-level vehicle class distributions

---

## 🔁 Process Overview

1. **Network Construction & Preprocessing**
   - Merge FAF network with HPMS/TMAS where available
   - Simplify and clean link directionality and geometry

2. **HPMS Imputation (Truck Volumes)**
   - Estimate total truck volume per link using known values from HPMS
   - Use a local averaging approach weighted by neighboring volumes

3. **TMAS Imputation (Vehicle Class %)**
   - Estimate vehicle class proportions (e.g., Class 5, 6, 7, 8, etc.)
   - Normalize as ratios per link
   - Validate performance using withheld data and R² scoring

4. **Evaluation & Output**
   - Export full imputed link-level truck volume and class data
   - Generate R² box plots and QQ plots by class, year, and sample size

---

## 📂 Folder Summary

```
network_class_imputation/
├── code/
│   ├── 09_Impute_HPMS_volume.py        # Impute total truck volume using HPMS
│   ├── 10_Impute_TMAS_Data.py          # Impute class shares using TMAS (with validation)
│   └── ...                             # Preprocessing, merging, plotting, QA
├── output/
│   ├── step_9/                         # Imputed HPMS truck volumes
│   ├── step_10/                        # Imputed TMAS class distribution (with summary)
├── README.md
```

---

## 📈 Results

- **99% coverage** achieved using <1% observed TMAS station data
- **Validation via R²**, evaluated on withheld data across multiple class groups
- **Reproducible framework** with modular Python code and seed-based outputs

---

## 🔬 Innovation & Impact

- Submitted for provisional patent as an **imputation method for sparse but structured networks**
- Can scale to national freight models or regional corridor studies
- Highlights a **low-observation, high-coverage** approach using real-world networks

---

## 🚀 Usage Notes

This repository does **not include data files** due to confidentiality and size limitations.

> 🔒 The code and content in this repository are intended for review purposes only and **should not be reused or redistributed without explicit permission from the author (Hyeonsup Lim).**

---

## 📬 Contact

Developed by **Hyeonsup Lim, Ph.D.**  
Email: hslim8211@gmail.com  
