import lightgbm as lgb
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv('Tests_Nurse_CSV.csv')

X = dataset[['Route','Capacity','Depot1','Depot2','Depot12','VP']]
y = dataset['Target'].values

# Load dataset and split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.60)

# Train a LightGBM model
model = lgb.LGBMRegressor(importance_type='gain',num_leaves=1000, learning_rate=0.05, n_estimators=60, num_iterations=100)
model.fit(X_train, y_train)

# Obtain gain feature importance
gain_importance = model.feature_importances_

# Display feature importance with feature names
feature_names = X_test.columns.values.tolist()
gain_importance_df = pd.DataFrame({'Feature': feature_names, 'Gain': gain_importance})
print(gain_importance_df.sort_values(by='Gain', ascending=False))

# Train a LightGBM model
model = lgb.LGBMRegressor(importance_type='split', num_leaves=30, learning_rate=0.03, n_estimators=60, num_iterations=100)
model.fit(X_train, y_train)

# Obtain split feature importance
split_importance = model.feature_importances_

# Display feature importance with feature names
feature_names = X_test.columns.values.tolist()
split_importance_df = pd.DataFrame({'Feature': feature_names, 'Split': split_importance})
print(split_importance_df.sort_values(by='Split', ascending=False))


def plot_feature_importance(importance_values, feature_names, title):
    # Create a DataFrame with feature names and importance values
    importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': gain_importance})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    
    # Plot the feature importances
    #plt.fig(figsize=(10, 6))
    plt.bar(importance_df['Feature'], importance_df['Importance'])
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.show()

# Plot Gain feature importance
plot_feature_importance(gain_importance, feature_names, 'Gain Feature Importance')

def plot_split_importance(importance_values, feature_names, title):
    # Create a DataFrame with feature names and importance values
    importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': split_importance})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)
    
    # Plot the feature importances
    #plt.fig(figsize=(10, 6))
    plt.bar(importance_df['Feature'], importance_df['Importance'])
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.show()

# Plot Split feature importance
plot_split_importance(split_importance, feature_names, 'Split Feature Importance')