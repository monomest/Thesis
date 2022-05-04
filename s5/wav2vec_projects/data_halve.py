# ---------------------------------------------------------
# data_halve.py
# Purpose: Randomly halve the amount of files in a dataset
#          for the paper.
# Author: Renee Lu, 2022
# ---------------------------------------------------------

# ------------------------------------------
#          Importing libraries
# ------------------------------------------

# For dataframes
import pandas as pd
# For printing filepath
import os

# ------------------------------------------
print('\nRunning: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#            Set data paths
# ------------------------------------------
print("\n------> Setting data paths -------------------------------------------\n")
# Datatset filepath and name
dataset_name = "myST-OGI-TLT17"
dataset_filename = "myST-OGI-TLT_data_finetune"

# Crafting filepath
dataset_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/"+dataset_name+"_local/THESIS_C/"+dataset_filename+".csv"
print("--> Dataset name:", dataset_name)
print("--> Dataset filename:", dataset_filename)
print("--> Dataset filepath:", dataset_fp)

# ------------------------------------------
#             Setting filepaths
# ------------------------------------------

# Filepath to output csv file
output_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/"+dataset_name+"_local/THESIS_C/"+dataset_filename+"_light_half.csv"

# ------------------------------------------
#           Reading in dataset
# ------------------------------------------
print("\n------> Reading in dataset... ----------------------------------------\n")
# Reading in dataset1 dataframe from csv file, as string type
# to preserve leading zeros in speaker id
dataset_og = pd.read_csv(dataset_fp, dtype=str)
dataset_og["duration"] = dataset_og["duration"].apply(pd.to_numeric)

# ------------------------------------------
#         Halve the sample
# ------------------------------------------
dataset_df = dataset_og.sample(frac = 0.50, random_state = 6)

# ------------------------------------------
#        Describe the halved sample
# ------------------------------------------
print("Old number of speech samples:", len(dataset_og.index))
print("New number of speech samples:", len(dataset_df.index))
print("New samples/old samples:", len(dataset_df.index)/len(dataset_og.index))

old_duration = dataset_og.duration.sum()/(60*60)
print("Old total duration:", old_duration)

new_duration = dataset_df.duration.sum()/(60*60)
print("New total duration", new_duration)

print("New duration/Old duration =", new_duration/old_duration)

# ------------------------------------------
#     Remove unnecessary columns
# ------------------------------------------
short_df = dataset_df[['filepath', 'transcription_clean']].copy()

# ------------------------------------------
#          Saving to csv file
# ------------------------------------------
# Save as csv file
short_df.to_csv(output_fp, index=False)
print("SUCCESS: saved new halved dataset in:",output_fp)
