import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =============================================================================
# 4238 value - Log-transform
# =============================================================================
filename = "output/step_7/Lasso/by_naics/value_4238_model.joblib"
loaded_model = joblib.load(filename)

x = np.linspace(0, 1, 200).reshape(-1,1) + 0.0001
x_ = np.log(x)
y = loaded_model.predict(x_)
y = np.exp(y)

y_test = np.exp(loaded_model.intercept_)*(x**(loaded_model.coef_))
y_test = y_test.reshape(1,-1)[0]

err = y - y_test
# raise()
plt.plot(x, y, 'r-.')
plt.show()







# =============================================================================
# OLS Linear Regression
# =============================================================================
filename = "output/step_7/OLS Linear Regression/by_naics/value_4238_model.joblib"
loaded_model = joblib.load(filename)

coefs = pd.DataFrame(
   loaded_model.coef_,
   columns=['Coefficients'])

# coefs.plot(kind='barh', figsize=(9, 7))
print(loaded_model.intercept_,list(loaded_model.coef_))


# =============================================================================
# Lasso
# =============================================================================
filename = "output/step_7/Lasso/by_naics/value_4238_model.joblib"
loaded_model = joblib.load(filename)

# importances  = loaded_model.feature_importances_

coefs = pd.DataFrame(
   loaded_model.coef_,
   columns=['Coefficients'])

# coefs.plot(kind='barh', figsize=(9, 7))
print(loaded_model.intercept_,list(loaded_model.coef_))


