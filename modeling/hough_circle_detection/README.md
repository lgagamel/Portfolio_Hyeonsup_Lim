# ⛽ Estimating Petroleum Product Consumption at Terminals using Hough Circle Detection and Weighted Voronoi Diagrams

This project develops a spatial modeling pipeline to estimate **petroleum product consumption** at terminal locations, despite the lack of granular consumption data. By integrating **remote sensing**, **Voronoi diagrams**, and **vehicle miles traveled (VMT)**, it delivers refined regional estimates of light-duty and truck fuel use, validated against state-level benchmarks.

---

## 🧠 Motivation

Public data sources (e.g., EIA) only provide aggregated state-level petroleum product consumption. However, understanding **local terminal-level** demand is critical for modeling logistics, energy resilience, and emissions. This project addresses this gap with:

- Satellite imagery for estimating **terminal tank capacity**
- Voronoi diagrams (weighted by estimated capacity) to define **service areas**
- Disaggregated **fuel use** using FAF and HPMS VMT data
- Validation and calibration using **state-level EIA data**

---

## 🧩 Process Workflow

### 1. Terminal Capacity Estimation using Satellite Image Processing and Hough Circle Detection 
- Extract tank locations and radii using **Hough Circle Transform**
- Estimate capacity as a function of radius:  
  `capacity ∝ Σ r^α`, where α is empirically calibrated between 2–3

### 2. Define Service Areas using Weighted Voronoi Diagrams
- Generate Voronoi diagrams around terminal locations
- Weights derived from estimated capacities:  
  `weight ∝ capacity^β`

### 3. Calculate Total VMT within Coverage
- Combine FAF and HPMS to split truck/light-duty VMT
- Overlay Voronoi zones to sum VMT within each terminal service area

### 4. Estimate Consumption
- Estimate terminal-level consumption using:  
  `Fuel = VMT × Avg Fuel Consumption Rate`

### 5. Validation and Calibration
- Compare state-level estimated totals vs EIA benchmarks
- Calibrate Voronoi weighting exponent β based on R² performance

### 6. Final Adjustment (Scaling)
- Scale each terminal’s consumption to ensure state-level totals match EIA  
  `ŷ_i* = ŷ_i × (Y / Σŷ_i)`

---

## 📦 Folder Structure

```
petroleum_consumption_model/
├── code/
│   ├── step0-1, 0-2/: Input data processing
│   ├── step2-1, 2-2/: Voronoi weighting + generation
│   ├── step3-1/: Spatial VMT intersection
│   ├── step4-1, 4-2, 4-3/: Fuel estimation & visualization
│   ├── step5-1/: Final state-level calibration and shapefile export
├── presentation/
│   └── Estimating Petroleum Product Consumption - Hyeonsup Lim.pdf
```

---

## 📈 Results

- 📍 Terminal-level estimates of both light-duty and truck fuel consumption
- 🗺️ Interactive visualization maps
- 🧪 R²-based model selection for Voronoi exponent β
- ✅ Final output calibrated to match **EIA state totals exactly**

📄 **Presentation**:  
[2019 International Visualization in Transportation Symposium (PDF)](presentation/Estimating_Petroleum_Product_Consumption.pdf)

---

## 🛠 Tools Used

- Python: `GeoPandas`, `Shapely`, `OGR`, `Plotly`
- Remote sensing: Hough Transform (via OpenCV, preprocessed)
- GIS operations: spatial join, buffer, area-weighted aggregation

---

## 🚀 Usage Notes

This repository does **not include data files** due to confidentiality and size limitations.

> 🔒 The code and content in this repository are intended for review purposes only and **should not be reused or redistributed without explicit permission from the author (Hyeonsup Lim).**

---

## 📬 Contact

Developed by **Hyeonsup Lim, Ph.D.**  
Email: hslim8211@gmail.com  
