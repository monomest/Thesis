# ---------------------------------------------------------
# remove_spkr_col.py
# Purpose: Remove the spkr_id column from a dataset.
#          Addressed pyarrow error when trying to convert
#          string spkr id into an integer.
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
# Datatset filepath and name
#dataset_name = "myST-OGI"
#dataset_name = "myST"
dataset_name = "OGI"
dataset_filename = "OGI_data_test"

# Crafting filepath
dataset_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/"+dataset_name+"_local/THESIS_C/"+dataset_filename+".csv"
print("--> Dataset name:", dataset_name)
print("--> Dataset filename:", dataset_filename)
print("--> Dataset filepath:", dataset_fp)

# ------------------------------------------
#             Setting filepaths
# ------------------------------------------

# Filepath to output csv file
output_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/"+dataset_name+"_local/THESIS_C/"+dataset_filename+"_noSpkrCol.csv"

# ------------------------------------------
#           Reading in dataset
# ------------------------------------------
print("\n------> Reading in dataset... ----------------------------------------\n")
# Reading in dataset1 dataframe from csv file, as string type
# to preserve leading zeros in speaker id
dataset_df = pd.read_csv(dataset_fp, dtype=str)
# Converting duration column to float64
dataset_df["duration"] = dataset_df["duration"].apply(pd.to_numeric)

# ------------------------------------------
#         Dropping spkr_id column
# ------------------------------------------
dataset_df.drop(columns=['spkr_id'], inplace=True)

# ------------------------------------------
#          Saving to csv file
# ------------------------------------------
# Save as csv file
dataset_df.to_csv(output_fp, index=False)
print("SUCCESS: Dropped spkr_id column and saved in:",output_fp)
