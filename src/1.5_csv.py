import os
import pandas as pd

path = "data/snippets/CSV"
for file in os.listdir(path):
    try:
        df = pd.read_csv(f"{path}/{file}")
        print("GOOD", f"{path}/{file}")
    except:
        print("BAD", f"{path}/{file}")
        os.remove(f"{path}/{file}")
