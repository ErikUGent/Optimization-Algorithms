import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error 
import seaborn as sns


plt.style.use('default')

dataset = pd.read_csv('Tests_w_target_mean.csv')
X = dataset[['Target','Pop Size','r2','r1']].values
y = dataset['Iterations'].values

# Fitting Polynomial Regression to the dataset
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.01)

poly = PolynomialFeatures(degree=4)
X_poly = poly.fit_transform(X_train)

lin2 = LinearRegression()
lin2.fit(X_poly, y_train)
#lin2.predict(X_poly)

lin_reg_rmse = np.sqrt(mean_squared_error(y_test, lin2.predict(poly.fit_transform(X_test))))
print(lin_reg_rmse)
#print(lin2.coef_)

fig, ax = plt.subplots(figsize=(8,6))

#y_plot = lin2.predict(poly.fit_transform(X_test))
#plt.scatter(X_test[:, 1], lin2.predict(poly.fit_transform(X_test)), color = 'green')
#plt.plot(X_test[:, 1], y_plot)
##plt.show()

#X_new = [y, X_test, lin2.predict(poly.fit_transform(X_test))]
#sns.regplot(data=X, x=X_test, y=lin2.predict(poly.fit_transform(X_test)), order=5)
sns.regplot(data=X_test, x=X_test[:, 0], y=lin2.predict(poly.fit_transform(X_test)), order=2)
#sns.regplot(data=X_test, x=X_test[:, 3], y=lin2.predict(poly.fit_transform(X_test)), order=2)
ax.set_xlabel( "r1" , size = 10)
ax.set_ylabel( "Target (min)" , size = 10)
plt.legend()
# Predicting a new result with Polynomial Regression
# after converting predict variable to 2D array

new_data = np.array([[1519,500,15,5]])  # Example values for median income, house age, and average rooms
new_data_poly = poly.fit_transform(new_data)

w = lin2.predict(new_data_poly)
print(w)
