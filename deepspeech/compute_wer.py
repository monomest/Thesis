#----------------------------------------------------------
# compute_wer.py
# Purpose: Compute WER given a dataframe of transcriptions
#          and predictions
# Based on source:
# https://github.com/huggingface/datasets/tree/master/metrics/wer
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
# output195.txt = OGI test set
# output196.txt = TLT17 test set 
# output197.txt = MyST test set
dataset_name = "output197.csv"

# Crafting filepath
dataset_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/wav2vec_projects/output/"+dataset_name
print("--> Dataset name:", dataset_name)
print("--> Dataset filepath:", dataset_fp)

# ------------------------------------------
#           Reading in dataset
# ------------------------------------------
print("\n------> Reading in dataset... ----------------------------------------\n")
df = pd.read_csv(dataset_fp, dtype=str)
# Convert all to string
df['transcription_clean'] = df['transcription_clean'].astype(str)
df['prediction'] = df['prediction'].astype(str)

# ------------------------------------------
#            Computing WER
# ------------------------------------------
wer = load_metric("wer")
#predictions = df['prediction'].tolist()
#references = df['transcription_clean'].tolist()
wer_score = wer.compute(predictions=df['prediction'], references=df['transcription_clean'])

print("WER:", wer_score)

