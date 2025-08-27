import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataset = pd.read_csv('Tests_w_target.csv')
X = dataset[['Iterations','Pop Size','r1','r2']]
y = dataset['Target']

matrix = dataset.corr()

sns.heatmap(matrix, cmap="coolwarm", fmt=".1f", vmin=-1, vmax=1,annot=True)
plt.title("Correlation Matrix of Input Variables")
plt.show()
