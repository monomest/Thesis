# ---------------------------------------------------------
# remove_cols.py
# Purpose: Remove all columns from a dataset except
#          filepath and transcription.
#          Addressed pyarrow error when it automatically
#          converts types.
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
print('\nRunning: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#            Set data paths
# ------------------------------------------
print("\n------> Setting data paths -------------------------------------------\n")
# Datatset filepath and name
#dataset_name = "myST-OGI"
dataset_name = "myST-OGI-TLT17"
#dataset_name = "myST"
#dataset_name = "OGI"
#dataset_name = "TLT"
dataset_filename = "myST-OGI-TLT17_data_pretrain"

# Crafting filepath
dataset_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/"+dataset_name+"_local/THESIS_C/"+dataset_filename+".csv"
print("--> Dataset name:", dataset_name)
print("--> Dataset filename:", dataset_filename)
print("--> Dataset filepath:", dataset_fp)

# ------------------------------------------
#             Setting filepaths
# ------------------------------------------

# Filepath to output csv file
output_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/"+dataset_name+"_local/THESIS_C/"+dataset_filename+"_light.csv"

# ------------------------------------------
#           Reading in dataset
# ------------------------------------------
print("\n------> Reading in dataset... ----------------------------------------\n")
# Reading in dataset1 dataframe from csv file, as string type
# to preserve leading zeros in speaker id
dataset_og = pd.read_csv(dataset_fp, dtype=str)

# ------------------------------------------
#         Dropping spkr_id column
# ------------------------------------------
#dataset_df = dataset_og[['filepath', 'transcription_clean']].copy()
dataset_df = dataset_og[['filepath', 'duration']].copy()

# ------------------------------------------
#          Saving to csv file
# ------------------------------------------
# Save as csv file
dataset_df.to_csv(output_fp, index=False)
print("SUCCESS: Dropped unused columns and saved in:",output_fp)
