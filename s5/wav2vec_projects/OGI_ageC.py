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
out_K = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_ageK.csv"
out_1 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age1.csv"
out_2 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age2.csv"
out_3 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age3.csv"
out_4 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age4.csv"
out_5 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age5.csv"
out_6 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age6.csv"
out_7 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age7.csv"
out_8 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age8.csv"
out_9 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age9.csv"
out_10 = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age10.csv"
out_list = [out_K, out_1, out_2, out_3, out_4, out_5, out_6, out_7, out_8, out_9, out_10]

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
id_to_age = [['0','b'], ['1','c'], ['2','d'], ['3','e'], ['4','f'], ['5','g'],
             ['6', 'h'], ['7', 'i'], ['8', 'j'], ['9', 'k'], ['a', 'l']]
df['age'] = [fp[2] for fp in df['spkr_id']]
# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
df.to_csv(out_fp,index=False)
print("Saved:", out_fp)
i = 0
for age in id_to_age:
    new_df = df[(df['age']==age[0]) | (df['age']==age[1])]
    new_df = new_df[["filepath", "transcription_clean"]]
    print("Samples for grade", i, ":", len(new_df))
    output_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age" + str(i) + ".csv"
    new_df.to_csv(output_fp, index=False)
    print("Saved:", output_fp)
    i += 1

print("Done!")



