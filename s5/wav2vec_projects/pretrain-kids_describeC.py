# data_describeC.py
# Purpose: Describe the data for Thesis C
# Author: Renee Lu, 2021

# ------------------------------------------
#         Importing libraries
# ------------------------------------------
# For dataframes
import pandas as pd
import numpy as np
# For printing filepath
import os

# ------------------------------------------
print('Running: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
# Input file

fp_all = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI-TLT-CU_local/THESIS_C/myST-OGI-TLT-CU_pretrain_manifest.csv"

print("Input file:", fp_all)

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
def readCSV(fp):
    # Read the csv file as dataframe, and as string type 
    # so that speaker IDs retain leading zeros
    df = pd.read_csv(fp)
    # Convert duration column to float64
    df["duration"] = df["duration"].apply(pd.to_numeric)
    return df

# All data
data_df = readCSV(fp_all)

# Portioned data
data_myST = data_df[(data_df['dataset'] == "myST")]
data_OGI = data_df[(data_df['dataset'] == "OGI")]
data_TLT = data_df[(data_df['dataset'] == "TLT")]
data_CU = data_df[(data_df['dataset'] == "CU")]
data_native = data_df[(data_df['dataset'] != "TLT")]

# ------------------------------------------
#     Describing datasets
# ------------------------------------------
print("\n------> Describing datasets... ---------------------------------------\n")
def describeData(df, df_all, message):
    # Print message
    print(message)
    # Find overall stats
    total_hours = df_all.duration.sum()/(60*60)
    total_samples = len(df_all)
    # Find total duration
    hours = df.duration.sum()/(60*60)
    print("# Hours:", hours)
    print("Proportion of hours:", hours/total_hours)
    # Find total samples
    samples = len(df)
    print("# Samples:", samples)
    print("Proportion of samples:", samples/total_samples)
    # Find distribution of duration 
    print("Distribution of audio durations:")
    print(df.duration.describe())

describeData(data_df, data_df, "All data")
describeData(data_myST, data_df, "myST data")
describeData(data_OGI, data_df, "OGI data")
describeData(data_CU, data_df, "CU data")
describeData(data_TLT, data_df, "TLT data")
describeData(data_native, data_df, "Native data")

print("Done!")

