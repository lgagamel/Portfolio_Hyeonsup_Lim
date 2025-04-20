# 🏭 Freight Generation Modeling Using Machine Learning

This project compares traditional regression and modern machine learning algorithms for industry-specific freight generation estimation. It demonstrates a statistically rigorous model selection process using a range of regression techniques to improve estimation accuracy by industry.

---

## 📌 Project Summary

- **Goal**: Predict freight generation (tonnage and value) by industry using U.S. CFS data and county-level business statistics.
- **Approach**: Evaluate OLS and seven alternative ML algorithms across 45 NAICS industry codes.
- **Key Result**: Over 80% of industry-specific models showed statistically significant improvement in RMSE using ML vs. OLS.
- **Performance Boost**: Up to **30% RMSE reduction** for certain industries.
- **Data**: 2017 Commodity Flow Survey (CFS), County Business Patterns (CBP), and Economic Census (EC).

---

## 📂 Repository Structure

```
freight_generation_model/
├── code/                         # Python scripts for data processing and modeling
├── poster/
│   └── 2022_TRB_Freight_Generation.pdf  # TRB poster summarizing findings
├── README.md                     # Project overview (this file)
```

---

## 🧠 Code Overview

The `code/` directory contains the following Python scripts:

- **`Step_00 ~ Step_06`**: Handles data cleaning, merging datasets, and preparing features for modeling.
- **`Step_07_1 ~ Step_07_8`**: Implements training various regression models, including OLS, Lasso, Decision Tree, Random Forest, Gradient Boosting, SVR, GPR, and MLP.
- **`Step_08 ~ Step_09`**: Contains functions to evaluate model performance using metrics like RMSE and conducts statistical significance testing.

---

## 📈 Methods and Algorithms

This study tested the following regression methods:

- **OLS** (baseline)
- **Lasso Regression**
- **Decision Tree**
- **Random Forest**
- **Gradient Boosting**
- **Support Vector Regression (SVR)**
- **Gaussian Process Regression (GPR)**
- **Multi-Layer Perceptron (MLP)**

Each model was tuned per-industry using:

- Evaluation of all possible variable combinations among 3~4 independent variables.
- Log vs. non-log transformations
- Hyperparameter grid search
- Statistical validation using 4-fold cross-validation repeated 25 times
- Model selection based on RMSE and significance tests (T-test, Wilcoxon)

---

## 📊 Highlights

- Developed a rigorous model selection pipeline for freight generation modeling
- Introduced per-industry model decisions — simpler OLS for some industries and advanced ML where statistically justified
- Visualization and benchmarking available in the TRB poster below

📁 **Code**:  
[GitHub code folder](code/)

📄 **Poster**:  
[2022 TRB Poster – Freight Generation Model (PDF)](poster/2022_TRB_Freight_Generation.pdf)

📘 **Paper**:  
[Sustainability Journal (Open Access)](https://doi.org/10.3390/su142215367)

---

## 🛠️ Tools Used

- Python (pandas, NumPy, scikit-learn)
- Statistical testing (SciPy)
- Hyperparameter tuning (GridSearchCV)
- Cross-validation and visualizations

---

## 🚀 Usage Notes

This repository does **not include data files** due to confidentiality and size limitations.

> 🔒 The code and content in this repository are intended for review purposes only and **should not be reused or redistributed without explicit permission from the author (Hyeonsup Lim).**

---

## 📬 Contact

Created by **Hyeonsup Lim, Ph.D.**  
Email: hslim8211@gmail.com  
