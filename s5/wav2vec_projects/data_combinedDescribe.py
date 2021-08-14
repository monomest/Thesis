# data_combinedDescribe.py
# Purpose: Decribe myST-OGI combined dataset
# Author: Renee Lu, 2021

# ------------------------------------------
#         Importing libraries
# ------------------------------------------
# For dataframes
import pandas as pd
# For printing filepath
import os

# ------------------------------------------
print('Running: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
# Dataframe in csv containing all the OGI information
# For 10mins, 1h, 10h and all 120hrs
fp_10m = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI_local/myST_OGI_train_15_10min.csv"
fp_1h = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI_local/myST_OGI_train_15_1h.csv"
fp_10h = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI_local/myST_OGI_train_15_10h.csv"
fp_all = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI_local/myST_OGI_train_15.csv"

fp_list = [fp_10m, fp_1h, fp_10h, fp_all]

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
def readCSV(fp):
    # Read the OGI csv file as dataframe, and as string type
    df = pd.read_csv(fp, dtype=str)
    # Convert duration column to float64
    df["duration"] = df["duration"].apply(pd.to_numeric)
    return df
# ------------------------------------------
#   Describe portion of OGI and myST
# ------------------------------------------
def filterData(df):    
    df_OGI = df[df['filepath'].str.contains("/srv/scratch/chacmod/OGI")]
    df_myST = df[df['filepath'].str.contains("/srv/scratch/chacmod/MyST/")]
    return df_OGI, df_myST

def describeData(df, total_hours, total_samples, total_spkrs):
    # Find total duration
    hours = df.duration.sum()/(60*60)
    print("# Hours:", hours)
    print("Proportion of hours:", hours/total_hours)
    # Find total samples
    samples = len(df)
    print("# Samples:", samples)
    print("Proportion of samples:", samples/total_samples)
    # Find total speakers
    # Group by speaker id, and then sum the durations for each speaker id
    spkrs = len(df.groupby(["spkr_id"]).duration.sum().reset_index())
    print("# Speakers:", spkrs)
    print("Proportion of speakers:", spkrs/total_spkrs)

for fp in fp_list:
    print("------>", fp)
    df = readCSV(fp)
    total_hours = df.duration.sum()/(60*60)
    total_samples = len(df)
    total_spkrs = len(df.groupby(["spkr_id"]).duration.sum().reset_index())
    df_OGI, df_myST = filterData(df)
    print("------> OGI portion...")
    describeData(df_OGI, total_hours, total_samples, total_spkrs)
    print("------> myST portion...")
    describeData(df_myST, total_hours, total_samples, total_spkrs)

print("SUCCESS: Data set described.")
