import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataset = pd.read_csv('Data_Tests_VShape.csv')
X = dataset[['Number of Birds','Wind Speed','Angle','CW','Surface']]
y = dataset['Target']

#dataframe = pd.DataFrame(data = dataset, columns = X)
matrix = dataset.corr()
print(matrix)
#print(X)
#corr_matrix = X_scaled.corr()
sns.heatmap(matrix, cmap="coolwarm", fmt=".1f", vmin=-1, vmax=1,annot=True)
plt.title("Correlation Matrix of Input Variables")
plt.show()
