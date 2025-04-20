# 🚗 Multi-Stop Route Optimization with Dynamic PDF & Google Maps QR Link (Personal Project)

This is a personal project built to optimize real-world multi-stop travel routes. Users input a list of locations, and the backend computes an efficient visiting order using TSP algorithms and returns an interactive PDF that includes a Google Maps route link **and a QR code** for quick mobile access. This project highlights the intersection of geospatial routing, automation, and user-friendly delivery.

> 🛠 Built completely independently — not affiliated with any employer or sponsor.  
> ❤️ A passion project to explore implementable, real-world logistics solutions.

---

## 🧠 Key Features

- **Automated Multi-Stop Routing** using the Traveling Salesman Problem (TSP)
- **Interactive Output PDF** including:
  - Route table with lat/lon and original input
  - Google Maps link to visualize the optimal path
  - QR Code linking directly to the route
- **Web-connected Pipeline**:
  - ASP.NET handles user queries and logs
  - Python backend performs routing, optimization, and PDF generation

---

## 📦 Folder Structure

```
multi_stop_route_optimizer/
├── code/
│   ├── asp.net/                 # Frontend (not detailed here)
│   └── python/                 # Backend core logic
│       ├── 00_Initiate_Output_Folders.py
│       ├── 01_Get_Coordinate.py
│       ├── 02_Update_Graph.py
│       ├── 03_Calculate_Distance.py
│       ├── 04_Run_TSP.py
│       ├── 05_Output.py
│       ├── Application.py
├── example_input/
│   └── address.txt             # Sample input with user address list
├── example_output/
│   ├── suggested_route.pdf     # Auto-generated route summary PDF
│   └── final.txt               # Google Maps route links
├── README.md
```

---

## 🔧 How It Works (Python Backend)

1. **Geocode Input Locations**  
   → Using Nominatim, retrieves lat/lon from free-text addresses  
2. **Download/Update Street Network**  
   → Downloads necessary OSM network data near input coordinates  
3. **Build Distance Matrix**  
   → Computes shortest travel times or fallback to distance estimates  
4. **Solve TSP**  
   → Uses `mlrose` optimization to find efficient stop order  
5. **Output**  
   → Generates a PDF with a QR code + Google Maps route links and sends it to the user

---

## 📥 Input Format (Simple and Flexible)

A plain text list of addresses or coordinates, e.g.:

```
123 Main St, Atlanta, GA
100 5th Ave, New York, NY
33.7756 -84.3963
```

---

## 📤 Output Example

- ✅ `suggested_route.pdf`:  
  Interactive PDF showing the route order + QR code to launch on mobile

- ✅ `final.txt`:  
  Google Maps links for immediate navigation

---

## 💡 Why This Matters

This project bridges real-time user interaction, geospatial computation, and clear output delivery in a reusable framework. It's an example of how backend logic can be applied practically to make logistics problems easy and approachable for everyday users.

---

## 🚀 Usage Notes

This repository does **not include data files** due to confidentiality and size limitations.

> 🔒 The code and content in this repository are intended for review purposes only and **should not be reused or redistributed without explicit permission from the author (Hyeonsup Lim).**

---

## 📬 Contact

Created by **Hyeonsup Lim, Ph.D.**  
Email: hslim8211@gmail.com 

> 💬 This is a personal side project — a testament to building practical tools with real-world impact.
