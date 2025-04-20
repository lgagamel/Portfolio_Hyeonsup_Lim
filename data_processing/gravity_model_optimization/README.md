# 🧲 Gravity Model Optimization with IPF – FAF Disaggregation Example

This project demonstrates how to estimate a disaggregated county-level OD matrix from an aggregated FAF OD matrix using a **gravity model** calibrated via **Iterative Proportional Fitting (IPF)**. Designed as an internal guide for the FAF team, the model clarifies the full disaggregation logic using simple numeric inputs, enabling team members to verify the results manually or reproduce them consistently.

---

## 📌 Summary

- **Purpose:** Help team members disaggregate FAF OD matrices to county-level with consistent logic and minimal setup
- **Method:** Use gravity-based impedance function (distance decay) and calibrate the decay factor `beta` using IPF and optimization
- **Audience:** FAF team members performing repeated OD disaggregation tasks
- **Note:** This example was developed in **one day** to quickly align disaggregation logic across the team

---

## 🧠 What is a Gravity Model?

A gravity model estimates flows between origins and destinations based on their size (e.g., production/consumption totals) and the distance between them:

$$
F_{ij} \propto \frac{O_{i} \cdot D_{j}}{d_{ij}^\beta}
$$

Where:
- $$O_{i}$$, $$D_{j}$$: total flows from origin and to destination
- $$d_{ij}$$: impedance or cost between i and j
- $$\beta$$: decay parameter to be calibrated

---

## 🔄 What is IPF?

**Iterative Proportional Fitting (IPF)** adjusts a multi-dimensional matrix (here, county OD) to satisfy marginal totals. It:
- Starts with a seed matrix (e.g., from the gravity model)
- Adjusts rows/columns to match known origin/destination and aggregated FAF totals
- Repeats until convergence

---

## 📂 Folder Structure

```
gravity_model_optimization/
├── code/
│   ├── Gravity_Model_Optimization.py     # Main script
│   ├── input/
│   │   ├── county_distance.csv
│   │   ├── county_origin_sum.csv
│   │   ├── county_destination_sum.csv
│   │   ├── faf_od_data.csv
│   │   └── county_mapping.csv
│   └── output/
│       ├── final_county_od.csv
│       ├── performance_data.csv
│       ├── performance_plot.svg
│       ├── *_check.csv
├── README.md
```

---

## ⚙️ What the Script Does

- Loads simple sample input files that can be followed and checked manually
- Defines a gravity function that includes a distance decay factor (`β`)
- Uses `scipy.optimize.minimize()` to find the `β` that minimizes error between FAF and estimated OD
- Applies IPF to estimate a county-level OD matrix that respects FAF-level totals
- Plots performance (error vs. beta) and saves final disaggregated OD results

---

## 📈 Output Highlights

- `final_county_od.csv`: Estimated OD matrix between counties
- `performance_data.csv`: Error by beta values tested
- `performance_plot.svg`: Visual error trend
- `_check.csv`: Aggregated sums for verification

---

## 💡 Why This Is Useful

- Offers a **repeatable and transparent baseline** for county-level OD disaggregation
- Reduces confusion and manual adjustment in similar FAF team tasks
- Validates logic via both **optimization** and **simple data inputs**

---

## 🚀 Usage Notes

> 🔒 The code and content in this repository are intended for review purposes only and **should not be reused or redistributed without explicit permission from the author (Hyeonsup Lim).**

---

## 📬 Contact

Created by **Hyeonsup Lim, Ph.D.**  
Email: hslim8211@gmail.com  
