import pandas as pd

df = pd.read_csv('dataframe.csv', sep=',')

words = ['sea', 'thieves']

df["penalty"] = 0

for i in range(len(df)):
    
    q = df["question"][i].lower()
    # q = ''.join(ch for ch in q if not ch.isupper())
    
    for word in words:
        # print(word, q)
        if word in q:
            print(q, 'contains', word)
            df["penalty"][i] += 1

print(df)