

# %%
import pandas as pd
import numpy as np

url = "https://raw.githubusercontent.com/Rose-Petals/TOL-1B/main/TOLCC%20Break%20Through%20Tech%20Dataset_2.csv"

df2 = pd.read_csv(url)

print(df2.head())

# %%
df2.columns = df2.columns.str.strip().str.lower().str.replace(" ", "_")
df2.rename(columns={'if_talk_therapy,_specifically_what_type?': 'talk_therapy_type', 'unnamed:_1' : 'referer'}, inplace=True)
df2.drop(columns= {"please_be_specific_on_who_sent_you_our_way,_we'd_like_to_thank_them.", "unnamed:_10", "unnamed:_11"}, inplace=True)

df2['talk_therapy_type'].unique()
df2['talk_therapy_type'].value_counts()

df2['talk_therapy_type'] = df2['talk_therapy_type'].replace('\u200b', np.nan)
df2['talk_therapy_type'] = df2['talk_therapy_type'].replace('Individual (minor)', 'Individual')
df2['talk_therapy_type'] = df2['talk_therapy_type'].replace('Individual (adult)', 'Individual')
df2['talk_therapy_type'].value_counts()

# %%
def average_age(cell):
    if pd.isna(cell):
        return np.nan
    values = str(cell).replace('-', ',').split(',')
    nums = []
    for val in values:
        val = val.strip()
        try:
            nums.append(float(val))
        except ValueError:
            continue
    if not nums:
        return np.nan
    return sum(nums) / len(nums)
df2['age'] = df2['age'].apply(average_age)
print(df2['age'])

# %%
df2.head()

# %%
df2['appointment_time'].value_counts()
df2['appointment_time'] = df2['appointment_time'].replace('Evening (4-8)' , 'Evening')
df2['appointment_time'] = df2['appointment_time'].replace('Afternoon (12-4)' , 'Afternoon')
df2['appointment_time'] = df2['appointment_time'].replace('Morning (9-12)' , 'Morning')
df2['appointment_time'].value_counts()


# %%
df2['insurance_carrier'].unique()


# %%
df2['insurance_carrier'].value_counts()


# %%
sum(df2['insurance_carrier'].isnull())

# %%
df2.isnull().sum()

# %%
df2.dropna(subset = ['appointment_time'], inplace = True)

# %%
df2.isnull().sum()

# %%
df2.fillna({'age': df2['age'].mean(), 'referer' : 'Unknown', 'town' : 'Unknown'}, inplace=True)


# %%
df2.isnull().sum()

# %%
df2['talk_therapy_type'].unique()

# %%
df2['talk_therapy_type'] = df2['talk_therapy_type'].fillna('ignore')
therapy_dummies = pd.get_dummies(df2['talk_therapy_type'], prefix = 'therapy')
therapy_dummies = therapy_dummies[['therapy_Individual', 'therapy_Family', 'therapy_Couples', 'therapy_Bariatric Evaluation']].reindex(df2.index,fill_value = 0)
df2['Medication Management'] = (df2['appointment_type'] == 'Medication Management').astype(int)
df2 = pd.concat([df2, therapy_dummies], axis = 1)
therapy_columns = ['therapy_Individual', 'therapy_Family', 'therapy_Couples', 'therapy_Bariatric Evaluation']
df2[therapy_columns] = df2[therapy_columns].astype(int)
df2.drop(['appointment_type', 'talk_therapy_type'], axis = 1, inplace = True)

# %%
df2.head()

# %%
df2.head()

# %%
df2.isnull().sum()


