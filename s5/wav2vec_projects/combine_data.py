# ---------------------------------------------------------
# combine_data.py
# Purpose: Combines datasets together.
# Requirements: Prepared datasets ready to feed into a run.py script
# Author: Renee Lu, 2021
# ---------------------------------------------------------

# ------------------------------------------
#          Importing libraries
# ------------------------------------------

# For dataframes
import pandas as pd
# For printing filepath
import os

# ------------------------------------------
print('Running: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#            Set data paths
# ------------------------------------------
print("\n------> Setting data paths -------------------------------------------\n")
# Datatset 1 filepath and name
dataset1_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_train_15.csv"
dataset1_name = "OGI-subset"
# Dataset 2 filepath and name
dataset2_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_train_15_subset_2.csv"
dataset2_name = "myST-subset"
print("--> Dataset1:", dataset1_fp)
print("--> Dataset2:", dataset2_fp)

# ------------------------------------------
#             Setting filepaths
# ------------------------------------------

# Filepath to output combined csv file
combined_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/wav2vec_local/"+dataset1_name+"_"+dataset2_name+".csv"

# ------------------------------------------
#        Combining dataset
# ------------------------------------------
print("\n------> Combining dataset... -------------------------------------\n")
# Reading in dataset1 dataframe from csv file, as string type
# to preserve leading zeros in speaker id
dataset1_df = pd.read_csv(dataset1_fp, dtype=str)
# Converting duration column to float64
dataset1_df["duration"] = dataset1_df["duration"].apply(pd.to_numeric)

# Reading in datatset2 dataframe from csv file, as string type
# to preserve leading zeros in speaker id
dataset2_df = pd.read_csv(dataset2_fp, dtype=str)
# Converting duration column to float64
dataset2_df["duration"] = dataset2_df["duration"].apply(pd.to_numeric)

# Combine datasets
combined_df = dataset1_df.append(dataset2_df, ignore_index=True)

# ------------------------------------------
#          Saving to csv file
# ------------------------------------------
# Save spkr_id as string so leading zeros are not removed
combined_df['spkr_id'] = combined_df['spkr_id'].astype('str')
# Save as csv file
combined_df.to_csv(combined_fp, index=False)
print("SUCCESS: Combined datasets and saved in:",combined_fp)
print("Number of utterances:", len(combined_df))
print("Total hours:", combined_df['duration'].sum()/(60*60))
print("Description of duration in seconds:")
print(combined_df.duration.describe())
