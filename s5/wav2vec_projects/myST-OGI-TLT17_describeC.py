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
#dataset = "myST"
#dataset = "OGI"
dataset = "myST-OGI-TLT17"

base = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/"
fp_all = base + dataset + "_local/THESIS_C/" + dataset + "_data_split.csv"

print("Input file:", fp_all)

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
# All data
data_df = pd.read_csv(fp_all)

# Portioned data
data_pretrain = data_df[(data_df['set'] == "pretrain")]
data_finetune = data_df[(data_df['set'] == "finetune")]
data_dev = data_df[(data_df['set'] == "dev")]
data_test = data_df[(data_df['set'] == "test")]
data_ignore = data_df[(data_df['set'] == "ignore")]

# ------------------------------------------
#     Describing datasets
# ------------------------------------------
print("\n------> Describing datasets... ---------------------------------------\n")
def describeData(df, df_all, message):
    # Print message
    print(message)
    # Find overall stats
    total_samples = len(df_all)
    # Find total samples
    samples = len(df)
    print("# Samples:", samples)
    print("Proportion of samples:", samples/total_samples)

describeData(data_df, data_df, "All data")
describeData(data_pretrain, data_df, "Pretrain data")
describeData(data_finetune, data_df, "Finetune data")
describeData(data_dev, data_df, "Development data")
describeData(data_test, data_df, "Test data")
describeData(data_ignore, data_df, "Ignored data")

print("Done!")

