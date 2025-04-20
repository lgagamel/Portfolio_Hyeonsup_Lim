import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ['emp_324', 'ap_324', 'est_324', 'rcptot_324']

fig, ax = plt.subplots(1,2,figsize=(16,5))

# =============================================================================
# Random forest
# =============================================================================
filename = "output/step_10/Random Forest/by_naics/tons_4245_model.joblib"
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

ax[0].barh(range(len(importances)), importances[indices])
ax[0].set_yticks(range(len(importances)))
_ = ax[0].set_yticklabels(y_label)



# =============================================================================
# Random forest
# =============================================================================
filename = "output/step_7/Random Forest/by_naics/tons_4245_model.joblib"
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

plt.savefig("output/step_9/test2.png",dpi=500)


# df = pd.DataFrame({"DTR":importances_DTR,"GBR":importances_GBR,"RFR":importances_RFR},index=['EMP', 'PAYANN', 'ESTAB', 'RCPTOT'])

