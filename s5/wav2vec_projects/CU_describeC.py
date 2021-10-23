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
print('\nRunning: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
# Input file
dataset = "CU"

base = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/"
fp_all = base + dataset + "_local/THESIS_C/" + "CU_data_split.csv"

print("Input file:", fp_all)

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
def readCSV(fp):
    # Read the csv file as dataframe, and as string type 
    df = pd.read_csv(fp)
    # Convert duration column to float64
    df["duration"] = df["duration"].apply(pd.to_numeric)
    return df

# All data
data_df = readCSV(fp_all)

# Portioned data
data_pretrain = data_df[((data_df['set'] == "short") | (data_df['set'] == "long"))]
data_ignore = data_df[(data_df['set'] == "ignore")]

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
describeData(data_pretrain, data_df, "Pretrain data")
describeData(data_ignore, data_df, "Ignored data")

print("Done!")

