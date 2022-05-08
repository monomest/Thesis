#----------------------------------------------------------
# make_files.py
# Purpose: Make train.csv and dev.csv files for training
#          with DeepSpeech
# Author: Renee Lu, 2022
#----------------------------------------------------------


# ------------------------------------------
#          Importing libraries
# ------------------------------------------
# For WER
from datasets import load_metric
import pandas as pd
# For printing filepath
import os
# For accessing date and time
from datetime import date
from datetime import datetime
now = datetime.now()

# Print out dd/mm/YY H:M:S and own filepath
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Started:", dt_string)
print('\nRunning:', os.path.abspath(__file__))

# ------------------------------------------
#            Set data paths
# ------------------------------------------
print("\n------> Setting data paths -------------------------------------------\n")
#dataset_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_finetune_unk_5h_light.csv"
dataset_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_dev_unk_light.csv"
print("--> Dataset filepath:", dataset_fp)

out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/deepspeech/dev_5h.csv"
print("--> Output filepath:", out_fp)

# ------------------------------------------
#           Reading in dataset
# ------------------------------------------
print("\n------> Reading in dataset... ----------------------------------------\n")
df = pd.read_csv(dataset_fp, dtype=str)
# Convert all to string
df['transcription_clean'] = df['transcription_clean'].astype(str)
df['filepath'] = df['filepath'].astype(str)

# ------------------------------------------
#            Creating file
# ------------------------------------------
def get_bytes (row):
    return os.path.getsize(row['filepath'])

df['wav_filesize'] = df.apply (lambda row: get_bytes(row), axis=1)

# Get bytes in a speech sample
print("\n------> Getting bytes in a speech sample ... -------------------------\n")

# Re-format dataframe to conform with DeepSpeech requirements
df.rename(columns = {'filepath':'wav_filename', 'transcription_clean':'transcript'}, inplace = True)
df = df[["wav_filename", "wav_filesize", "transcript"]]

# ------------------------------------------
#    Saving file to output
# ------------------------------------------
df.to_csv(out_fp, index=False)
print("SUCCESS: saved file in:", out_fp)

