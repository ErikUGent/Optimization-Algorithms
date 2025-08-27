# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import lime
import lime.lime_tabular
import numpy as np
import sklearn
import sklearn.ensemble
import sklearn.metrics
import matplotlib.pyplot as plt

import seaborn 
seaborn.set_context('notebook')

# Read and preview data
dataset = pd.read_csv('Tests_data_notime.csv')
X = dataset.head(1050)
print(X)

# Checks the shape of the data
X.shape

dataset_2 = pd.read_csv('Tests_target.csv')
# Gets the dependent variable (the target)
y = dataset_2['Target']
y.head(1050)
print(y)

# Split the data into train and test data:
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4)

# Build the model with Random Forest Regressor :
from sklearn.ensemble import RandomForestRegressor
#model = RandomForestRegressor(max_depth=4, random_state=0, n_estimators=10)
model = RandomForestRegressor()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, y_pred)**(0.5)
mse

# LIME has one explainer for all the models
explainer = lime.lime_tabular.LimeTabularExplainer(X_train.values, feature_names=X_train.columns.values.tolist(),
                                                  class_names=['Target'], verbose=True, mode='regression')

# Choose the 5th instance and use it to predict the results
j = 189
exp = explainer.explain_instance(X_test.values[j], model.predict, num_features=4)

exp.as_pyplot_figure()

# Show the predictions
exp.show_in_notebook(show_table=True)
exp.save_to_file('lime.html')

exp.as_list()