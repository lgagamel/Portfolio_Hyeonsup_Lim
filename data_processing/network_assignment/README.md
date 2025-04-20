# 🌊 Multi-Modal Network Assignment Pipeline (Example for Water Shipments)

This ongoing project focuses on automating data workflows to assign domestic and foreign water shipments to a multi-modal network—including truck, water, and intermodal links—supporting the **Freight Analysis Framework (FAF)**. The pipeline integrates diverse data sources and introduces new geospatial features such as **dummy links** for node transitions, facilitating accurate water-to-land freight routing.

---

## 📌 Project Summary

- **Goal:** Build a scalable and automated pipeline to support water shipment assignments as part of a larger multimodal freight network.
- **Approach:** Combine geospatial preprocessing, port-to-port skims, origin-to-port assignments, and OD construction with enhanced routing logic.
- **Status:** This is a **work in progress**, with new updates expected.
- **Impact:** Reduces manual geoprocessing and validation efforts; supports future MNL model development and FAF toolchain integration.

---

## 📂 Project Structure

```
network_assignment_water/
├── code/
├── README.md
```

---

## 🧩 Processing Workflow

### 🗂 1. Data Preprocessing & Projection (Steps 01–02)
- Reprocess water and truck links
- Reproject input networks to EPSG:5070
- Clean and harmonize node/link attributes

### 📍 2. Port Mapping & Feasibility (Steps 03–08)
- Map water ports to truck network nodes
- Identify feasible ports for truck centroids
- Add dummy ports for centroids with no viable links

### 🔗 3. Dummy Link Generation
- Add dummy links where neighboring links change type (e.g., ocean ↔ inland) to preserve connectivity
- Apply configurable penalty weights to control flow patterns

### 🔄 4. Skim Creation & OD Construction (Steps 09–13)
- Perform skims: truck to port, port to port, and foreign port access
- Match US/foreign ports by ID, name, and predefined zones
- Generate domestic and foreign county/region-level OD files

### 🛰 5. AIS Data Integration & OD Calibration (Steps 16–17)
- Unzip, filter, and process AIS data by MMSI
- Generate foreign OD estimations and identify top OD flows

### 🧪 6. Evaluation (Steps 14–15, 20+)
- Validate connectivity and route plausibility
- Compare estimated vs. actual tonnage (USACE link tons, port throughput)
- Visualize assigned routes and output skims

---

## ✨ Key Innovations

- **Dummy Links for Mode Shifts:** Geospatial engineering technique to simulate water segment changes (e.g., ocean ↔ inland).
- **Foreign Port OD Matching:** Hybrid approach using IDs, names, and manual validation to link global trade flows.
- **Skim Optimization:** Truck centroids are pre-filtered to reduce redundant calculations.
- **Scalable & Modular:** Designed to expand with AIS calibration, MNL chain modeling, and port-level capacity constraints.

---

## 🚀 Usage Notes

This repository does **not include data files** due to confidentiality and size limitations.

> 🔒 The code and content in this repository are intended for review purposes only and **should not be reused or redistributed without explicit permission from the author (Hyeonsup Lim).**

---

## 📬 Contact

Created by **Hyeonsup Lim, Ph.D.**  
Email: hslim8211@gmail.com  
