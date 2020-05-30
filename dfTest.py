import pandas as pd
import numpy as np
from pandas import DataFrame


data={
	'state':['Ohio','Ohio','Ohio','Nevada','Nevada'],
	'year':[2000,2001,2002,2001,2002],
	'pop':[1.5,1.7,3.6,2.4,2.9],
	'Ma5':[1,1,1,1,1],
	'Ma10':[2,2,20,2,2],
	'Ma15':[3,3,3,3,3],
	'Ma20':[4,4,4,4,4],
	}

df = DataFrame(data)
print(df)

df_diff = np.sign(df['Ma20']-df['Ma15'])+np.sign(df['Ma15']-df['Ma10'])+np.sign(df['Ma10']-df['Ma5'])
print(df_diff)

print(type(df_diff))
# df_stat = np.sign(df_diff.value<3)
# print(df_stat)
full = np.array([2.5]*5)
print(full)
res = pd.Series(full,index = [i for i in range(0,5)],dtype = str)
print(res)


list_signal = np.sign(df_diff-full)
print(list_signal)


print(df.iloc[:,0].size)