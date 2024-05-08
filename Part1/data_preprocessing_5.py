# -*- coding: utf-8 -*-
"""data_preprocessing_5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Qt32tiCQI97DCaUEXp2ktSn8UVIHc-Tk
"""

import pandas as pd
import numpy as np

data = pd.read_csv("test.csv")
df = pd.read_csv("res_2b.csv")
data_2 = pd.read_csv("well_and_features.csv")

# data.head()

df.columns

data.rename(columns={'well_api': 'API #', "well_name": "Well Name"}, inplace= True)
# data.head()

df_merged = pd.merge(df, data, on=['API #', "Well Name"], how='inner')
df_merged.head()

df = df_merged.drop_duplicates(subset=['API #', "Well Name"])
# df

"""# Cleaning and Modifying API #
## Only applicable to this certain condition depeding upon the API #
"""

well_no = df["API #"]
# well_no

# for i in range(len(well_no)):
  # if len(well_no[i])!=12:
    # print(well_no[i], 12-len(well_no[i]))

for i in range(len(well_no)):
  if 12-len(well_no[i])>4:
    # print(well_no[i], 12-len(well_no[i]))
    # print(well_no[i][:2]+"-"+well_no[i][-5:])
    well_no[i] = "0"+well_no[i][:2]+"-"+well_no[i][-5:]
    # print(well_no[i])

for i in range(len(well_no)):
  if 12-len(well_no[i])>3:
    # print(well_no[i], 12-len(well_no[i]))
    #print("00-0"+well_no[i][:])
    well_no[i] = "00-0"+well_no[i][:]
    # print(well_no[i])

for i in range(len(well_no)):
  if 12-len(well_no[i])>2:
    # print(well_no[i], 12-len(well_no[i]))
    #print("00-0"+well_no[i][:])
    well_no[i] = "00-"+well_no[i][:]
    # print(well_no[i])

for i in range(len(well_no)):
  if len(well_no[i])!=12:
    # print(well_no[i], 12-len(well_no[i]))
    # print(well_no[i][:2]+"-"+well_no[i][2:5]+"-"+well_no[i][-5:])
    well_no[i] = well_no[i][:2]+"-"+well_no[i][2:5]+"-"+well_no[i][-5:]
    # print(well_no[i])









"""# Extracting State code, county code and well number from API"""

Api = {
    "State":[],
    "County":[],
    "Well_no":[]
}

print(len(well_no))
for i in range(len(well_no)):
  # print(i)
  Api["State"].append(well_no[i].split("-")[0])
  Api["County"].append(well_no[i].split("-")[1])
  Api["Well_no"].append(well_no[i].split("-")[2])

# len(Api["State"])

df['State_code'] = Api["State"]
df["County_code"] = Api["County"]
df["Well_no"] = Api['Well_no']
# df.head()

df.isna().sum()

df.fillna("N/A", inplace = True)









"""# Location : County and State Division

"""

def state(x):
  County = []
  State = []
  try:
    County.append(x.split()[0])
    print(x.split()[0], x.split()[2])
    State.append(x.split()[2])
  except:
    # County.append("N/A")
    # State.append("N/A")
    pass
  return County, State

def state(x):
    try:
        county = x.split()[0]
        state = x.split()[2]
    except:
        county = "N/A"
        state = "N/A"
    return county, state

df["County"], df["State"] = zip(*df["Location"].apply(lambda x : state(x)))











"""# Data Merging
Using well file number and Api to merge 3 datasets

## Getting Well_file number
"""

def well_file(x):
  fl_name = x[1:-4]
  return fl_name

df["Well_file_no"] = df["Filename"].apply(lambda x : well_file(x))
df.drop("Filename",axis=1, inplace =True)
df.drop("Lease Name", axis =1, inplace = True)
# df.head()

data_2.rename(columns={"well_no":"Well_file_no"}, inplace = True)
data_2.drop(["well_county","state_info","well_api","operator_of_well"], axis = 1, inplace= True)
# data_2.head()

data_2["Well_file_no"] = data_2["Well_file_no"].apply(lambda x : str(x))
# data_2["Well_file_no"]

df_merged_ = pd.merge(df, data_2, on=["Well_file_no"], how='inner')

df = df_merged_.fillna("N/A")









"""# Cleaning and Type Casting

"""

df.columns

df['stimulation_date'] = pd.to_datetime(df['stimulation_date'], errors='coerce').fillna("N/A")
# df["stimulation_date"]

df['top_ft'] = pd.to_numeric(df['top_ft'], errors='coerce').fillna("N/A")
# df["top_ft"]

df['bottom_ft'] = pd.to_numeric(df['bottom_ft'], errors='coerce').fillna("N/A")
# df["bottom_ft"]

df['stages'] = pd.to_numeric(df['stages'], errors='coerce').fillna("N/A")
# df["stages"]

df['volume'] = pd.to_numeric(df['volume'], errors='coerce').fillna("N/A")
# df["volume"]

def replace_feature_value(value):
    if value == 'sand frac':
        return 'sand frac'
    else:
        return "N/A"

# Apply the function to the 'Feature' column
df['treatment_type'] = df['treatment_type'].apply(replace_feature_value)

df['lbs_prop'] = pd.to_numeric(df['lbs_prop'], errors='coerce').fillna("N/A")
# df["lbs_prop"]

df['max_psi'] = pd.to_numeric(df['max_psi'], errors='coerce').fillna("N/A")
# df["max_psi"]

df['bbls_min'] = pd.to_numeric(df['bbls_min'], errors='coerce').fillna("N/A")
# df["bbls_min"]

df.rename(columns={"Producetion_information":"Production_Info"},inplace= True)

df.drop("Location", axis = 1, inplace = True)

df.drop("well_names", axis = 1, inplace =True)

df.to_csv("final_preprocessed.csv", index =False)

print(df)

# df.head()
