# 🧭 Bayesian Data Fusion to Estimate Error Distribution of Position and Distance Measurements for Connected Vehicles

This project proposes a self-learning, Bayesian data fusion model to improve the **raw accuracy of position and distance measurements** in connected vehicle (CV) environments. By estimating the true error distribution of each data source (e.g., GPS, distance sensors) and continuously updating them as new data arrives, the model enhances overall positioning and inter-vehicle measurement reliability.

---

## 📌 Project Summary

- **Goal**: Enhance raw GPS and distance sensor measurements for connected vehicles by estimating their error distributions.
- **Approach**: Use Bayesian estimation to infer and update the error distribution of each sensor in real-time using surrounding vehicle data.
- **Innovation**: The model incorporates a **self-evaluation mechanism** to determine when sufficient new data justifies updating the distribution.
- **Result**: Achieved **Over 98% of R-squared** in bias estimation of position and distance measurements.
- **Data**: `highD` dataset (Germany), with synthetic sensor errors applied to simulate real-world CV conditions.

---

## 📂 Repository Structure

```
bayesian_data_fusion_cav/
├── code/                                      # Python code for each step of simulation and model estimation
│   ├── Step_00_Reorganize_HighD.py              # Preprocess highD vehicle trajectory data
│   ├── Step_01_Read_HighD.py                    # Compute relative distances and relationships between vehicles
│   ├── Step_02_Generate_Error.py                # Simulate sensor error distributions (bias, covariance)
│   ├── Step_03_Generate_Observed_Measures.py    # Apply noise to simulate raw measurements
│   └── Step_04_Estimates.py                     # Core model: estimate true position, update error distributions
├── presentation/
│   └── 2021_IEEE_Bayesian_Approach_Error_Distribution_Estimation.pdf  # IEEE conference slides
├── README.md
```

---

## 🧠 Code Workflow

1. **Step0**: Split and reorganize highD trajectory files by lane and frame.
2. **Step1**: Match each vehicle with its preceding and following vehicles and calculate true distances.
3. **Step2**: Generate synthetic bias and variance values for each sensor (GPS and distance).
4. **Step3**: Apply generated errors to simulate observed noisy measurements.
5. **Step4**: Estimate true positions using Bayesian log-likelihood over grid candidates and update error distributions if learning criteria are met.

---

## 🔍 Methodology

- **Bayesian Estimation**: Used to compute and update the likelihood-based error distributions of GPS and distance sensors.
- **Multi-source Fusion**: Observed measurements from preceding and following vehicles are used in combination.
- **Grid Search**: A local likelihood optimization technique estimates the most probable true position.
- **Self-Learning Trigger**: Error distributions are only updated when new observations improve overall log-likelihood, avoiding noisy overfitting.
- **Performance Evaluation**: Accuracy is measured over 100 iterations of learning using mean absolute error (MAE) against known ground truth.

---

## 📊 Highlights

- Improved accuracy of both GPS and distance measurements even when true error distributions were unknown.
- Capable of real-time updates as new vehicle trajectory data becomes available.
- Robust across 9 different sensor error scenarios (varying bias and variance levels).
- Position estimation R² exceeded 0.98 after sufficient learning iterations.

📘 **Paper**:  
[2021 IFIP/IEEE Paper PDF](https://ieeexplore.ieee.org/document/9464040)

📄 **Presentation**:  
[2021 IEEE Poster PDF](presentation/2021_IEEE_Bayesian_Approach_Error_Distribution_Estimation.pdf)

---

## 🛠️ Tools Used

- Python (pandas, NumPy, SciPy, matplotlib)
- Multivariate normal distributions
- Likelihood maximization
- Synthetic data simulation
- Iterative learning & error correction

---

## 🚀 Usage Notes

This repository does **not include data files** due to confidentiality and size limitations.

> 🔒 The code and content in this repository are intended for review purposes only and **should not be reused or redistributed without explicit permission from the author (Hyeonsup Lim).**

---

## 📬 Contact

Created by **Hyeonsup Lim, Ph.D.**  
Email: hslim8211@gmail.com
