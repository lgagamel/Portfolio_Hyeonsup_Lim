import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ['emp_324', 'ap_324', 'est_324', 'rcptot_324']

fig, ax = plt.subplots(1,3,figsize=(16,5))

# =============================================================================
# Decision Tree
# =============================================================================
filename = "output/step_10/Decision Tree/by_naics/value_324_model.joblib"
loaded_model = joblib.load(filename)

importances  = loaded_model.feature_importances_
print(importances)
importances_DTR = importances

indices = np.argsort(importances)
y_label = ['EMP', 'PAYANN', 'ESTAB', 'RCPTOT']
y_label = ["$\it{" + x + "}$" for x in y_label]
y_label = np.array(y_label)
y_label = y_label[indices]

ax[0].barh(range(len(importances)), importances[indices])
ax[0].set_yticks(range(len(importances)))
_ = ax[0].set_yticklabels(y_label)



# =============================================================================
# Random forest
# =============================================================================
filename = "output/step_10/Random Forest/by_naics/value_324_model.joblib"
loaded_model = joblib.load(filename)

importances  = loaded_model.feature_importances_
std = np.std([tree.feature_importances_ for tree in loaded_model.estimators_], axis=0)
print(importances)
importances_RFR = importances

indices = np.argsort(importances)
y_label = ['EMP', 'PAYANN', 'ESTAB', 'RCPTOT']
y_label = ["$\it{" + x + "}$" for x in y_label]
y_label = np.array(y_label)
y_label = y_label[indices]

ax[1].barh(range(len(importances)), importances[indices])
ax[1].set_yticks(range(len(importances)))
_ = ax[1].set_yticklabels(y_label)



# =============================================================================
# Gradient Boosting
# =============================================================================
filename = "output/step_10/Gradient Boosting/by_naics/value_324_model.joblib"
loaded_model = joblib.load(filename)

importances  = loaded_model.feature_importances_
# std = np.std([tree.feature_importances_ for tree in loaded_model.estimators_], axis=0)
print(importances)
importances_GBR = importances

indices = np.argsort(importances)
y_label = ['EMP', 'PAYANN', 'ESTAB', 'RCPTOT']
y_label = ["$\it{" + x + "}$" for x in y_label]
y_label = np.array(y_label)
y_label = y_label[indices]

ax[2].barh(range(len(importances)), importances[indices])
ax[2].set_yticks(range(len(importances)))
_ = ax[2].set_yticklabels(y_label)

plt.savefig("output/step_9/test.png",dpi=500)


# df = pd.DataFrame({"DTR":importances_DTR,"GBR":importances_GBR,"RFR":importances_RFR},index=['EMP', 'PAYANN', 'ESTAB', 'RCPTOT'])


# =============================================================================
# Lasso
# =============================================================================
filename = "output/step_10/Lasso/by_naics/value_324_model.joblib"
loaded_model = joblib.load(filename)

# importances  = loaded_model.feature_importances_

coefs = pd.DataFrame(
   loaded_model.coef_,
   columns=['Coefficients'])

# coefs.plot(kind='barh', figsize=(9, 7))
print(list(loaded_model.coef_))


# =============================================================================
# OLS Linear Regression
# =============================================================================
filename = "output/step_10/OLS Linear Regression/by_naics/value_324_model.joblib"
loaded_model = joblib.load(filename)

coefs = pd.DataFrame(
   loaded_model.coef_,
   columns=['Coefficients'])

# coefs.plot(kind='barh', figsize=(9, 7))
print(list(loaded_model.coef_))



raise()








# =============================================================================
# Support Vector Regression - NOT WORKING
# =============================================================================
filename = "output/step_7/Support Vector Regression/by_naics/value_324_model.joblib"
loaded_model = joblib.load(filename)

importances  = loaded_model.feature_importances_





# =============================================================================
# MLP - NOT WORKING
# =============================================================================
filename = "output/step_7/Multilayer Perceptron/by_naics/value_324_model.joblib"
loaded_model = joblib.load(filename)

importances  = loaded_model.feature_importances_



# =============================================================================
# Gaussian Process - NOT WORKING
# =============================================================================
filename = "output/step_7/Gaussian Process/by_naics/value_324_model.joblib"
loaded_model = joblib.load(filename)

importances  = loaded_model.feature_importances_
