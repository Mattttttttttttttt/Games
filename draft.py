import pandas as pd
import cross_zeros

df = cross_zeros.create_field()
c = 0
for i in range(3):
    for j in range(3):
        c+=1
        df.iloc[i][j] = c

cross_zeros.save(df, 'admin')