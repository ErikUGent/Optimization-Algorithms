import numpy as np
import pandas as pd

data = [[30, 40], [37, 52], [49, 49], [52, 64], [20, 26], [40, 30], [21, 47], [17, 63], [31, 62], [52, 33], [51, 21], [42, 41], [31, 32], [5, 25], [12, 42], [36, 16], [52, 41], [27, 23], [17, 33], [13, 13], [57, 58], [62, 42], [42, 57], [16, 57], [8, 52], [7, 38], [27, 68], [30, 48], [43, 67], [58, 48], [58, 27], [37, 69], [38, 46], [46, 10], [61, 33], [62, 63], [63, 69], [32, 22], [45, 35], [59, 15], [5, 6], [10, 17], [21, 10], [5, 64], [30, 15]]
df = pd.DataFrame(data, columns=['xcord', 'ycord'], dtype='int16')


n_df=(df.values)

(df.values).shape

matrix=np.zeros(((df.values).shape[0],(df.values).shape[0]))

for i in range((df.values).shape[0]):
    for j in range((df.values).shape[0]):
        matrix[i,j]=round(float(np.sqrt(np.sum((n_df[i]-n_df[j])**2))), 0)

np.set_printoptions(threshold=np.inf)
print(matrix, file=open('output.txt', 'a'))
print(matrix)