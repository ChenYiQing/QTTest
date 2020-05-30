from pandas import *
from random import *
df = DataFrame(columns=('lib', 'qty1', 'qty2'))  # 生成空的pandas表
for i in range(6):  # 插入一行
    df.loc[i] = [randint(-1, 1) for n in range(3)]
df.loc[6] = [2,1,3]
df.loc[7] = [2,1,3]

print(df)
