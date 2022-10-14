#importing required modules
import pandas as pd
import numpy as np
from scipy import stats
 
#importing dataset
df = pd.read_csv('data.csv')
ser = df['gender'].isna()
dropped = 0
drop_row = []

for elm in df.index:
    if elm == 0:
        continue

    if ser[elm] == True:
        dropped += 1
        drop_row.append(elm)
        continue

    if df['gender'][elm] != 'male' and df['gender'][elm] != 'female':
        dropped += 1
        drop_row.append(elm)

df = df.drop(drop_row)


print(dropped)
df.to_csv('data.csv')