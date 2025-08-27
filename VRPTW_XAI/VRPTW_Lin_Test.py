
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

dataset = pd.read_csv('Tests_Nurse_Route_1_2_Perc.csv')
x = dataset['VP']
x.head()
print(x)

dataset_2 = pd.read_csv('Tests_Nurse_Route_1_2_Perc.csv')
# Gets the dependent variable (the target)
y = dataset_2['Time']
y.head()
print(y)

#create basic scatterplot 
plt.scatter(x, y, 'o') 
 
#obtain m (slope) and b(intercept) of linear regression line 
m, b = np.polyfit(x, y, 1) 
print(m)
print(b) 
#add linear regression line to scatterplot  
plt.plot(x, m*x+b)