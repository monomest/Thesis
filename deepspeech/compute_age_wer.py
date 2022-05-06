#----------------------------------------------------------
# compute__age_wer.py
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
# Age:
# K  1  2  3  4  5  6  7  8  9  10
# 0  1  2  3  4  5  6  7  8  9  10
age = "10"

# Results fp
result_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/20211015-base-OGI-eval-age_OGI_test_results"+age+".csv" 

# Reference fp
reference_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_age"+age+".csv"

print("--> Age:", age)
print("--> Result filepath:", result_fp)

# ------------------------------------------
#           Reading in dataset
# ------------------------------------------
print("\n------> Reading in dataset... ----------------------------------------\n")
# Read in reference
reference_df = pd.read_csv(reference_fp, dtype=str)
# Convert all to string
reference_df['transcription_clean'] = reference_df['transcription_clean'].astype(str)

# Read in result
result_df = pd.read_csv(result_fp, dtype=str)
# Convert all to string
result_df['pred_str'] = result_df['pred_str'].astype(str)

# ------------------------------------------
#            Computing WER
# ------------------------------------------

# Put result predictions into reference dataframe
reference_df['pred_str']= result_df['pred_str']
reference_df['pred_str'] = reference_df['pred_str'].astype(str)

# Lowercase transcription and predictions
reference_df['pred_str'] = reference_df['pred_str'].str.lower()
reference_df['transcription_clean'] = reference_df['transcription_clean'].str.lower()

# Split into scripted and spontaneous
scripted_df = reference_df[reference_df['filepath'].str.contains("scripted")]
spontaneous_df = reference_df[reference_df['filepath'].str.contains("spontaneous")]

wer = load_metric("wer")
wer_scripted = wer.compute(predictions=scripted_df['pred_str'], references=scripted_df['transcription_clean'])
wer_spontaneous = wer.compute(predictions=spontaneous_df['pred_str'], references=spontaneous_df['transcription_clean'])

print("Scripted WER:", wer_scripted)
print("Spontaneous WER:", wer_spontaneous)

