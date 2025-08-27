
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

dataset = pd.read_csv('Data_Tests_VShape_Perc_zh.csv')
#x = dataset['Number of Birds']
#x = dataset['Wind Speed']
#x = dataset['Angle']
x = dataset['CW']
#x = dataset['Surface']
#x = dataset[['Number of Birds','Wind Speed','Angle','CW','Surface']]
x.head()
print(x)

y = dataset['Target']
y.head()
print(y)

#create basic scatterplot 
#plt.plot(x, y, 'o') 
 
#obtain m (slope) and b(intercept) of linear regression line 
m, b = np.polyfit(x, y, 1) 
print(m)
print(b) 
#add linear regression line to scatterplot  
#plt.plot(x, m*x+b)