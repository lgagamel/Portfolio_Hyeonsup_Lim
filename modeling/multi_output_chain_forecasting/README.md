# 🔗 Multi-Output Chaining for Time Series Forecasting of U.S. Imports/Exports

This project introduces a novel time series modeling approach that applies **multi-output chaining** to forecast U.S. import and export values by commodity. The method accounts for cross-correlations across commodities and estimates how the disruption caused by Russia’s invasion of Ukraine propagates through supply chains.

---

## 📌 Project Summary

- **Goal**: Estimate the cascading impact of the Ukraine war on U.S. trade by forecasting import/export values using chained multi-output time series modeling.
- **Approach**: Use SARIMAX models enhanced by a chained multi-output structure to capture upstream/downstream dependencies across over 1,000 commodities.
- **Key Result**: Proposed model reduced **MAE by 36%** and **RMSE by 26%** compared to baseline SARIMAX without chaining.
- **Data**: USA Trade Online (USATO) data, Jan 2002 – Sep 2022, covering over 99% of U.S. imports and exports by value.

---

## 📂 Repository Structure

```
multi_output_chain_forecasting/
├── code/                                          # Python scripts for data processing and forecasting
├── poster/
│   └── 2023_TRB_Multi_Output_Chain_Forecasting.pdf  # TRB poster summarizing findings
├── README.md                                      # Project overview (this file)
```

---

## 🧠 Code Overview

The `code/` directory includes the following components:

- **`Step00 ~ Step03`**: Data loading, cleaning, and preprocessing from USATO trade data.
- **`Step04`**: Baseline time series model using simple SARIMAX for each commodity.
- **`Step05`**: Proposed model implementation using chained multi-output SARIMAX, where upstream-downstream relations are derived from lagged cross-correlations.
- **`Step06`**: Model fitting for each chain structure.
- **`Step07`**: Forecast future import/export values under multiple disruption scenarios (e.g., invasion ending in different months).
- **`Step08 ~ Step10`**: Evaluate forecasts (MAE, RMSE) and visualize scenario-based impact on U.S. trade.

---

## 📈 Methods and Modeling Approach

- **SARIMAX**: Seasonal ARIMA with exogenous regressors (used as the base model)
- **Multi-Output Chaining**:
  - Identifies high cross-correlated commodity pairs (lags only)
  - Chains forecasts in sequence (e.g., upstream HS codes help predict downstream ones)
- **Scenario Modeling**:
  - Five different scenarios of the war ending: Jan, Mar, Jun, Sep, and Dec 2023
  - Model updates input forecasts month-by-month for chained dependencies
- **Evaluation**: MAE, RMSE, and relative change in predicted values for top commodity groups

---

## 📊 Highlights

- Developed scalable chaining framework to forecast over 2,000 time series (imports and exports by HS code)
- Proposed approach outperformed standard SARIMAX in predictive accuracy
- Offers early-warning capability by detecting commodities impacted first and most

📁 **Code**:  
[GitHub code folder](code/)

📄 **Poster**:  
[2023 TRB Poster – Multi-Output Forecasting (PDF)](poster/2023_TRB_Multi_Output_Chain_Forecasting.pdf)

---

## 🛠️ Tools Used

- Python (pandas, NumPy, statsmodels, SciPy, pmdarima)
- SARIMAX (seasonal auto-regressive model with exogenous variables)
- Scenario-based time series forecasting
- Multi-output chaining (custom implementation)

---

## 🚀 Usage Notes

This repository does **not include data files** due to confidentiality and size limitations.

> 🔒 The code and content in this repository are intended for review purposes only and **should not be reused or redistributed without explicit permission from the author (Hyeonsup Lim).**

---

## 📬 Contact

Created by **Hyeonsup Lim, Ph.D.**  
Email: hslim8211@gmail.com  
