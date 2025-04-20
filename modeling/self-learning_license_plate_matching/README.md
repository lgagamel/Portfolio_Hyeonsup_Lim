# 🔍 License Plate Matching Using Self-Learning and Derived Association Matrices

This project implements and evaluates a self-learning license plate matching algorithm using edit distance techniques, association matrix estimation, and a novel matrix derivation method. It improves the robustness of license plate recognition (LPR) under poor OCR performance or limited matched samples.

---

## 📌 Project Summary

- **Goal**: Improve post-processing license plate matching between two LPR stations using self-learning and derived association matrices.
- **Approach**: Develop a framework using edit distance and empirical association matrices, enhanced by a third station to derive a matrix between sparse station pairs.
- **Key Innovation**: Introduction of a **derived association matrix** using matrix multiplication to supplement weak station links.
- **Result**: Achieved significantly higher matching accuracy with fewer samples than traditional learned matrices.
- **Data**: Simulated LPR data using empirically derived association matrices based on OCR character confusion.

---

## 📂 Repository Structure

```
license_plate_self_learning/
├── code/                        # MATLAB code files by functional modules
│   ├── Edit Distance/           # Functions for generalized edit distance calculations
│   ├── Main/                    # Master script to run end-to-end experiments
│   ├── Matching/                # License plate string matching using edit distance + association matrix
│   ├── Matrix_Comparison/       # Evaluation and visualization of matrix similarity and closeness
│   └── Self Learning/           # Core module: iterative self-learning of association matrices
├── paper/
│   └── 16-6478.docx             # Reference manuscript for TRB paper
├── README.md
```

---

## 🧠 Code Overview

| Folder | Description |
|--------|-------------|
| `Edit Distance/` | Functions for calculating weighted edit distance, including empirical character similarity |
| `Main/` | Main script to run the complete simulation or matching pipeline |
| `Matching/` | Performs LPR string matching using learned or derived association matrices |
| `Matrix_Comparison/` | Evaluates matrix closeness (e.g., against ideal) and visualizes learning progress |
| `Self Learning/` | Contains the iterative learning routine that updates the association matrix using empirical matching results |

---

## 🧪 Methods & Logic

- **Weighted Edit Distance**: Modified Levenshtein distance, where weights are based on learned association matrix of OCR misreads
- **Association Matrix**:
  - Learned directly from matched OCR character strings between two stations
  - Derived by multiplying two station-pair matrices that share a common station
- **Self-Learning**: Algorithm repeatedly improves the association matrix as more characters are matched
- **Matrix Evaluation**: Compares closeness to an "ideal" association matrix using statistical metrics

---

## 📊 Highlights

- Enhanced Oliveira-Neto et al.’s self-learning algorithm with a derived matrix concept
- Proposed method reduces required samples by **up to 75%** to achieve **90%+ matching rate**
- Real-world scenarios simulated with poor read accuracy and sparse travel time overlaps
- Suitable for sparse LPR networks with minimal overlapping traffic

📘 **Paper**:  
[TRR Journal Link](https://doi.org/10.3141/2594-09)  
> 🎓 Co-author (2nd author) of the paper , but **led the development and implementation** of the self-learning algorithm, derived matrix logic, and most of the MATLAB modules in this repository.

---

## 🛠️ Tools Used

- MATLAB (.m)
- Edit Distance Heuristics
- Self-Learning Algorithms
- Monte Carlo Simulation
- Matrix Multiplication for Probability Estimation

---

## 🚀 Usage Notes

This repository does **not include data files** due to confidentiality and size limitations.

> 🔒 The code and content in this repository are intended for review purposes only and **should not be reused or redistributed without explicit permission from the author (Hyeonsup Lim).**

---

## 📬 Contact

Created by **Hyeonsup Lim, Ph.D.**  
Email: hslim8211@gmail.com

