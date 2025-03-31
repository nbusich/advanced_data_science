import pandas as pd
import warnings
from Functions import viz as v

# Suppressing Unwanted warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

# Specifying the file path
file_path = 'artists.json'

# Reading the JSON file into a DataFrame, removing unwanted columns (axis is 1 for columns)
df = pd.read_json(file_path)
df = df.drop(df.columns[[0,1,2,6,7,8]], axis=1)

# Making the birth year into birth decade
df['BeginDate'][df['BeginDate'] % 10 != 0] = df['BeginDate'] - (df['BeginDate'] % 10)
v.lowercase(df)
df = df.dropna()

# Removing unwanted values
df = v.keep_rows(df, 'Nationality', '!=', 'nationality unknown')
df = v.keep_rows(df, 'BeginDate', '!=', 0)
df = v.keep_rows(df, 'Gender', '!=', 'gender unknown')

# Making the sankey diagrams
v.make_sankey(df,50, 'Nationality, Birthdate', 'Nationality', 'BeginDate')
v.make_sankey(df, 60, 'Nationality, Gender', 'Nationality', 'Gender')
v.make_sankey(df, 40, 'Nationality, Gender, Birthdate', 'Nationality', 'Gender', 'BeginDate')
v.make_sankey(df,60, 'Gender, Birthdate', 'Gender', 'BeginDate')



