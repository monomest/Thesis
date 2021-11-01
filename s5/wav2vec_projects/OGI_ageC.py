# OGI_ageC.py
# Purpose: Get the age of each speaker 
#          for Thesis C
# Author: Renee Lu, 2021

# ------------------------------------------
#            Information
# ------------------------------------------
#The verification codes:
#1 Good: Only the target word is said.
#2 Maybe: Target word is present, but there's other junk in the file.
#3 Bad: Target word is not said.
#4 Puff: Same as good, but w/ an air puff.

#The naming convention:
#ks000820 --> ks[1gradeid][2spkcode][2uttid]0
#gradeid: K --> 0,b 
#         1 --> 1,c 
#         2 --> 2,d 
#         3 --> 3,e 
#         4 --> 4,f 
#         5 --> 5,g 
#         6 --> 6,h 
#         7 --> 7,i 
#         8 --> 8,j 
#         9 --> 9,k 
#         10 --> a,l 
#Uttid 2 digits, check docs/all.map for scripted
#Uttid is xx for spontaneous speech

# ------------------------------------------
#         Importing libraries
# ------------------------------------------
# For dataframes
import pandas as pd
import numpy as np
# For printing filepath
import os
# For reading files
from pathlib import Path
# For regex
import re
# For dealing with audio files
import soundfile as sf
# For dealing with NaN
import math

# ------------------------------------------
print('\nRunning: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
# Dataframe in csv containing all the data information
fp_test = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test.csv"
print("Input file:", fp_test)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age.csv"

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
def readCSV(fp):
    # Read the csv file as dataframe, and as string type 
    # so that speaker IDs retain leading zeros
    df = pd.read_csv(fp, dtype={'spkr_id': object})
    # Convert duration column to float64
    df["duration"] = df["duration"].apply(pd.to_numeric)
    return df

# Get the dataframes of files that will be used
df = readCSV(fp_test)

# ------------------------------------------
#             Get speaker age
# ------------------------------------------
# ------------v
# spkr_id = ksb0p
#gradeid: K --> 0,b 
#         1 --> 1,c 
#         2 --> 2,d 
#         3 --> 3,e 
#         4 --> 4,f 
#         5 --> 5,g 
#         6 --> 6,h 
#         7 --> 7,i 
#         8 --> 8,j 
#         9 --> 9,k 
#         10 --> a,l 
df['age'] = [fp[2] for fp in df['spkr_id']]

num_K = len(df[(df['age']=="0") | (df['age']=="b")])
num_1 = len(df[(df['age']=="1") | (df['age']=="c")])
num_2 = len(df[(df['age']=="2") | (df['age']=="d")])
num_3 = len(df[(df['age']=="3") | (df['age']=="e")])
num_4 = len(df[(df['age']=="4") | (df['age']=="f")])
num_5 = len(df[(df['age']=="5") | (df['age']=="g")])
num_6 = len(df[(df['age']=="6") | (df['age']=="h")])
num_7 = len(df[(df['age']=="7") | (df['age']=="i")])
num_8 = len(df[(df['age']=="8") | (df['age']=="j")])
num_9 = len(df[(df['age']=="9") | (df['age']=="k")])
num_10 = len(df[(df['age']=="a") | (df['age']=="l")])

age_list = [num_K, num_1, num_2, num_3, num_4, num_5, num_6, num_7, num_8, num_9, num_10]
index = 0
print("\n------> Number of samples per age group:")
for age in age_list:
    print(index, ":", age)
    index += 1

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
df.to_csv(out_fp,index=False)
print("Saved:", out_fp)

print("Done!")



