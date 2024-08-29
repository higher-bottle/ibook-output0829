import pandas as pd
#%%
a = [(1, 2, 3), (4, 5, 6)]
test_df = pd.DataFrame(a)
print(test_df)
#%%
for row in test_df.values:
    print(row)
