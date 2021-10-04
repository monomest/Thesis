# myST_splitC.py
# Purpose: Split the transcribed myST data 
#          for Thesis C
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
# Setting maximum seconds duration
# ------------------------------------------
print("\n------> Setting duration limit... ------------------------------------ \n")
# Maximum seconds
limit = 15
print("--> Fine-tuning files limited to less than or equal to", limit, "seconds.")

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
# Dataframe in csv containing all the data information
fp_all = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data.csv"
fp_dev = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_dev_wav.csv"
fp_test = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_test_wav.csv"

print("Input files...")
fp_list = [fp_all, fp_dev, fp_test]
for fp in fp_list:
    print(fp)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_split.csv"
pretrain_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_pretrain.csv"
finetune_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_finetune.csv"
dev_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_dev.csv"
test_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_test.csv"
ignore_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_ignore.csv"

output_fp = [out_fp, pretrain_fp, finetune_fp, dev_fp, test_fp, ignore_fp]

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

# All data
myST_df = readCSV(fp_all)
# Development set
myST_dev = readCSV(fp_dev)
filepath_dev = myST_dev['filepath'].tolist()
# Test set
myST_test = readCSV(fp_test)
filepath_test = myST_test['filepath'].tolist()

# ------------------------------------------
#       Split into portions
# ------------------------------------------
print("\n------> Splitting into ignore, test, dev, finetune, pretrain... ------\n")
myST_df['set'] = np.nan

# ignore: 
# if usable = False
myST_df.loc[myST_df.usable == False, 'set'] = "ignore"

# test: 
# if filepath in filepath_test AND usable == True AND set == NaN
myST_df['set'] = np.where((myST_df['filepath'].isin(filepath_test)) & 
                          (myST_df['usable'] == True) &
                          (myST_df['set'] != myST_df['set']),
                           "test", myST_df['set'])

# dev: if filepath in filepath_dev AND usable == True AND set == NaN
myST_df['set'] = np.where((myST_df['filepath'].isin(filepath_dev)) &
                          (myST_df['usable'] == True) &
                          (myST_df['set'] != myST_df['set']),
                           "dev", myST_df['set'])

# finetune: 
# if duration <= limit AND transcribed == True AND usable == True AND set == NaN
myST_df['set'] = np.where((myST_df['duration'] <= limit) &
                          (myST_df['transcribed'] == True) &
                          (myST_df['usable'] == True) &
                          (myST_df['set'] != myST_df['set']),
                           "finetune", myST_df['set'])

# pretrain:
# if transcribed != True AND usable == True AND set == NaN OR
# if transcribed == True AND duration > limit AND usable == True and set == NaN
myST_df['set'] = np.where((myST_df['transcribed'] != True) &
                          (myST_df['usable'] == True) &
                          (myST_df['set'] != myST_df['set']),
                          "pretrain", myST_df['set'])
myST_df['set'] = np.where((myST_df['transcribed'] == True) &
                          (myST_df['duration'] > limit) &
                          (myST_df['usable'] == True) &
                          (myST_df['set'] != myST_df['set']),
                           "pretrain", myST_df['set'])

print("Checking if there's any null values in 'set' column:")
print(myST_df['set'].isnull().values.any())
print("Unique values in 'set' column:")
print(myST_df['set'].unique())

# Creating set dataframes
myST_pretrain = myST_df[(myST_df['set'] == "pretrain")]
myST_finetune = myST_df[(myST_df['set'] == "finetune")]
myST_dev = myST_df[(myST_df['set'] == "dev")]
myST_test = myST_df[(myST_df['set'] == "test")]
myST_ignore = myST_df[(myST_df['set'] == "ignore")]

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
myST_df.to_csv(out_fp,index=False)
myST_pretrain.to_csv(pretrain_fp, index=False)
myST_finetune.to_csv(finetune_fp, index=False)
myST_dev.to_csv(dev_fp, index=False)
myST_test.to_csv(test_fp, index=False)
myST_ignore.to_csv(ignore_fp, index=False)

for fp in output_fp:
    print("Saved:", fp)

print("Done!")

