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

dataset = pd.read_csv('Data_tests_VShape_zh.csv')
X = dataset[['Number of Birds','Wind Speed','Angle','CW','Surface']]
y = dataset['Target']

'''
# Read and preview data
X = pd.read_csv('Results_V-Shape_Param.csv')
#X = dataset
print(X)

#X.shape

y = pd.read_csv('Results_V-Shape_Target.csv')
#y = dataset_2
print(y)
'''
# Split the data into train and test data:
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4)

# Build the model with Random Forest Regressor :
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV
#model = RidgeCV()
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
j = 79
exp = explainer.explain_instance(X_test.values[j], model.predict, num_features=5)

exp.as_pyplot_figure()

# Show the predictions
exp.show_in_notebook(show_table=True)
exp.save_to_file('lime.html')

exp.as_list()