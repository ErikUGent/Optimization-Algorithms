import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('default')

from sklearn.metrics import roc_curve
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import mean_absolute_error as MAE
from sklearn.metrics import r2_score as R2
from scipy.special import softmax

import shap

def print_feature_importances_random_forest(random_forest_model):
    
    '''
    Prints the feature importances of a Random Forest model in an ordered way.
    random_forest_model -> The sklearn.ensemble.RandomForestRegressor or RandomForestClassifier trained model
    '''
    
    # Fetch the feature importances and feature names
    importances = random_forest_model.feature_importances_
    features = random_forest_model.feature_names_in_
    
    # Organize them in a dictionary
    feature_importances = {fea: imp for imp, fea in zip(importances, features)}
    
    # Sorts the dictionary
    feature_importances = {k: v for k, v in sorted(feature_importances.items(), key=lambda item: item[1], reverse = True)}
    
    # Prints the feature importances
    for k, v in feature_importances.items():
        print(f"{k} -> {v:.4f}")


def print_feature_importances_shap_values(shap_values, features):    
    '''
    Prints the feature importances based on SHAP values in an ordered way
    shap_values -> The SHAP values calculated from a shap.Explainer object
    features -> The name of the features, on the order presented to the explainer
    '''

    # Calculates the feature importance (mean absolute shap value) for each feature
    importances = []
    for i in range(shap_values.values.shape[1]):
        importances.append(np.mean(np.abs(shap_values.values[:, i])))
        
    # Calculates the normalized version
    importances_norm = softmax(importances)

    # Organize the importances and columns in a dictionary
    feature_importances = {fea: imp for imp, fea in zip(importances, features)}
    feature_importances_norm = {fea: imp for imp, fea in zip(importances_norm, features)}

    # Sorts the dictionary
    feature_importances = {k: v for k, v in sorted(feature_importances.items(), key=lambda item: item[1], reverse = True)}
    feature_importances_norm= {k: v for k, v in sorted(feature_importances_norm.items(), key=lambda item: item[1], reverse = True)}

    # Prints the feature importances
    for k, v in feature_importances.items():
        print(f"{k} -> {v:.4f} (softmax = {feature_importances_norm[k]:.4f})")

def evaluate_regression(y, y_pred):
    
    '''
    Prints the most common evaluation metrics for regression
    '''
    
    mae = MAE(y, y_pred)
    mse = MSE(y, y_pred)
    rmse = mse ** (1/2)
    r2 = R2(y, y_pred)
    
    print('Regression result')
    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2: {r2:.2f}")

 #   roc_curve(X_test, y_test)

#from sklearn.datasets import fetch_california_housing
#dataset = fetch_california_housing(as_frame = True)

#dataset = pd.read_csv('Tests_data.csv')

#dataset = pd.read_csv('Tests_data_notime.csv')
#X = dataset.head(1050)
dataset = pd.read_csv('Tests_Nurse_CSV.csv')
X = dataset[['Route','Capacity','Depot_1','Depot_2','Depot_1_2','VP']]
print(X)
#print(dataset['DESCR'])

# Gets the independent variables
#X = dataset['data']
#print (X)
#X.head(5)

# Checks the shape of the data
X.shape

dataset_2 = pd.read_csv('Tests_Nurse_CSV.csv')
# Gets the dependent variable (the target)
y = dataset_2['Time']
y.head(5)
print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

# Prepares a default instance of the random forest regressor
model = RandomForestRegressor()

# Fits the model on the data
model.fit(X_train, y_train)

# Evaluates the model
y_pred = model.predict(X_test)
evaluate_regression(y_test, y_pred)

# Prints the feature importances
print_feature_importances_random_forest(model)

# Fits the explainer
explainer = shap.Explainer(model.predict, X_test)
n_explainer = shap.TreeExplainer(model)

# Calculates the SHAP values - It takes some time
shap_values = explainer(X_test)
shap_values

shap_interaction_values = n_explainer.shap_interaction_values(X_test)
#print(np.shape(shap_interaction_values))

# Plots this view
shap.plots.bar(shap_values)

# Plots the beeswarm
shap.plots.beeswarm(shap_values.sample(50))

shap.summary_plot(shap_interaction_values, X_test)
shap.dependence_plot("Route", shap_values[0], X_test, interaction_index="Capacity")

# Violin plot
#shap.summary_plot(shap_interaction_values, plot_type='violin')

# Prints the SHAP feature importances
print_feature_importances_shap_values(shap_values, X_test.columns)
