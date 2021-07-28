# ---------------------------------------------------------
# data_getSubset.py
# Purpose: Split training dataset into 10min, 1hr and 
#          10hr subsets. 
# Requirements: Ran data_split.py
# Author: Renee Lu, 2021
# ---------------------------------------------------------

# ------------------------------------------
#          Importing libraries
# ------------------------------------------

# For dataframes
import pandas as pd
# For splitting data
from sklearn.model_selection import train_test_split
# For printing filepath
import os

# ------------------------------------------
print('Running: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#            Setting file paths
# ------------------------------------------
print("\n------> Setting file paths... ----------------------------------------\n")
# dataset_name = "myST"
#dataset_name = "OGI"
dataset_name = "myST-OGI"
print("Dataset name:", dataset_name)

# Filename of training dataframe csv file
#dataset_filename = "myST_train_15"
#dataset_filename = "OGI_scripted_train_15"
dataset_filename = "myST_OGI_train_15"
print("dataset_filename:", dataset_filename)

# Where to save 10 minute subset dataframe
#train_10min_filename = "myST_train_15_10min"
#train_10min_filename = "OGI_scripted_train_15_10min"
train_10min_filename = "myST_OGI_train_15_10min"
print("train_10min_filename:", train_10min_filename)
# Where to save 1 hour subset dataframe
#train_1h_filename = "myST_train_15_1h"
#train_1h_filename = "OGI_scripted_train_15_1h"
train_1h_filename = "myST_OGI_train_15_1h"
print("train_1h_filename:", train_1h_filename)
# Where to save 10 hour subset dataframe
#train_10h_filename = "myST_train_15_10h"
#train_10h_filename = "OGI_scripted_train_15_10h"
train_10h_filename = "myST_OGI_train_15_10h"
print("train_10h_filename:", train_10h_filename)

# Base filepath
base_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/" + dataset_name + "_local/"
print("base_fp:", base_fp)

# ------------------------------------------
#    Setting total hours in train set
# ------------------------------------------
print("\n------> Setting total hours in train set... ---------------------------\n")
# myST total hours = 85.08
# OGI total hours = 37.04
# myST-OGI total hours = 122.117
tot_hours = 122.117
print("total hours:", tot_hours)

# ------------------------------------------
#           Setting seed
# ------------------------------------------
print("\n------> Setting seed... ----------------------------------------------\n")
# Set a seed to ensure random split can be reproducible
seed = 6
print("--> Setting seed as:", seed)

# ------------------------------------------
#         Generating filepaths
# ------------------------------------------
# File path to dataframe csv file,
# generated from prep.py and/or getShortWavs.py

# Filepath to training dataframe
data_train_fp = base_fp + dataset_filename + ".csv"

# Where to save 10 minute subset
data_train_10min_fp = base_fp + train_10min_filename + ".csv"
# Where to save 1 hour subset
data_train_1h_fp = base_fp + train_1h_filename + ".csv"
# Where to save 10 hour subset
data_train_10h_fp = base_fp + train_10h_filename + ".csv"

# ------------------------------------------
#        Reading in dataframe
# ------------------------------------------
print("\n------> Reading in train dataframe... --------------------------------\n")
# Reading in data dataframe from csv file, as string type
# to preserve leading zeros in speaker id
data_train_df = pd.read_csv(data_train_fp, dtype=str)
# Converting duration column to float64
data_train_df["duration"] = data_train_df["duration"].apply(pd.to_numeric)


# ------------------------------------------
#       Getting subsets
# ------------------------------------------
print("\n------> Getting 10min, 1hr and 10hr training subsets...---------------\n")
# Convert all durations to minutes to get subset proportion
def getSubset(subset_name, subset_mins, tot_hours, data_train_df, seed):
    prop_subset = subset_mins/(tot_hours*60) # Proportion of subset compared to total
    discard, train_subset = train_test_split(data_train_df, test_size=prop_subset,
                            random_state=seed, shuffle=True)
    print("--> Speakers in", subset_name, "training subset:",
          train_subset['spkr_id'].nunique())
    print("--> Minutes in subset:", train_subset['duration'].sum()/(60))
    print("--> Hours in subset:", train_subset['duration'].sum()/(60*60))
    return train_subset
# Get 10 minute subset
subset_mins = 10
train_10min = getSubset("10 minute", subset_mins, tot_hours, data_train_df, seed)
# Get 1 hour subset
subset_mins = 1*60
train_1h = getSubset("1 hour", subset_mins, tot_hours, data_train_df, seed)
# Get 10 hour subset
subset_mins = 10*60
train_10h = getSubset("10 hour", subset_mins, tot_hours, data_train_df, seed)

# ------------------------------------------
#          Saving to csv files
# ------------------------------------------
def saveCSV(subset_name, df, fp):
    # Save spkr_id as string so leading zeros are not removed
    df['spkr_id'] = df['spkr_id'].astype('str')
    df.to_csv(fp, index=False)
    print("SUCCESS: Created", subset_name, "subset in", fp)
    print("Samples: ", len(df))
# Save to CSV file
saveCSV("10 minute", train_10min, data_train_10min_fp)
saveCSV("1 hour", train_1h, data_train_1h_fp)
saveCSV("10 hour", train_10h, data_train_10h_fp)
