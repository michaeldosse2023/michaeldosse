from multiprocessing.reduction import duplicate

import pandas as pd
import numpy as np
from future.backports.datetime import timedelta
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from datetime import datetime
#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import mean_squared_error
import random
from scipy import stats

n = 100
# 1. Generate Age with Nulls
age = np.random.normal(30, 10, n)
age[np.random.randint(0, n, 10)] = np.nan

# 2. Generate Income with extreme outliers
income = np.random.normal(50000, 15000, n)
income[np.random.randint(0, n, 5)] *= 10

# 3. Generate Cities with None/Nulls
cities = np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston'], n)
cities = cities.astype(object) # Ensure it can hold 'None'
cities[np.random.randint(0, n, 8)] = None

# 4. Generate Dates (Fixed the Null logic)
dates = [datetime.today() - timedelta(days=random.randint(0, 365)) for _ in range(n)]
for idx in np.random.randint(0, n, 5):
    dates[idx] = pd.NaT  # Use NaT (Not a Time) for proper pandas date nulls

# 5. Build the DataFrame
df = pd.DataFrame({
    "age": age,
    "income": income,
    "city": cities,
    "joined": dates
})

# 6. Add the Duplicates row
duplicate_idx = 20
duplicated_row = df.iloc[[duplicate_idx]] # Easier way to grab the whole row
df = pd.concat([df, duplicated_row], ignore_index=True)

# 7. Categorical Notes (Fixed '1' to 'i')
df['notes'] = [
    'good customer' if i % 3 == 0 else 'slow-payer' if i % 4 == 0 else 'frequent complaints'
    for i in range(len(df))
]

df.head()

# *****************************************************************************************************

class DeepClean:
    def __init__(self, df):
        self.df = df.copy()
        self.report = {}

    def remove_duplicates(self):
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        after = len(self.df)
        self.report["duplicates_removed"] = before - after
