# compute_wer.py
# Purpose: Compute WER of DeepSpeech inferences
# Author: Renee Lu, 2022

# ------------------------------------------
#          Importing libraries
# ------------------------------------------

# For WER
from jiwer import wer

# For printing filepath
import os
# ------------------------------------------
print('Running: ', os.path.abspath(__file__))
# ------------------------------------------
# For accessing date and time
from datetime import date
from datetime import datetime
now = datetime.now()
# Print out dd/mm/YY H:M:S
# ------------------------------------------
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Started:", dt_string)
# ------------------------------------------ 
print("\n------> IMPORTING PACKAGES.... ---------------------------------------\n")
print("-->Importing datasets...")
# Import datasets and evaluation metric
from datasets import load_dataset, load_metric, ClassLabel
# Convert pandas dataframe to DatasetDict
from datasets import Dataset
# Generate random numbers
print("-->Importing random...")
import random
# Manipulate dataframes and numbers
print("-->Importing pandas & numpy...")
import pandas as pd
import numpy as np
# Use regex
print("-->Importing re...")
import re
# Read, Write, Open json files
print("-->Importing json...")
import json
# Use models and tokenizers
print("-->Importing Wav2VecCTC...")
from transformers import Wav2Vec2CTCTokenizer
from transformers import Wav2Vec2ForCTC
from transformers import Wav2Vec2FeatureExtractor
from transformers import Wav2Vec2Processor
# Loading audio files
print("-->Importing soundfile...")
import soundfile as sf
# For training
print("-->Importing torch, dataclasses & typing...")
import torch
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
print("-->Importing from transformers for training...")
from transformers import TrainingArguments
from transformers import Trainer
print("-->Importing pyarrow for loading dataset...")
import pyarrow as pa
import pyarrow.csv as csv
print("-->SUCCESS! All packages imported.")

# ------------------------------------------
print('\nRunning: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#            Set data paths
# ------------------------------------------
print("\n------> Setting data paths -------------------------------------------\n")
# Datatset filepath and name
# OGI test set
dataset_name = "output195.csv"
# TLT17 test set
#dataset_name = "output196.csv"
# MyST test set
#dataset_name = "output197.csv"

# Crafting filepath
dataset_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/wav2vec_projects/output/"+dataset_name
print("--> Dataset name:", dataset_name)
print("--> Dataset filepath:", dataset_fp)

# ------------------------------------------
#           Reading in dataset
# ------------------------------------------
print("\n------> Reading in dataset... ----------------------------------------\n")
# Reading in dataset1 dataframe from csv file, as string type
# to preserve leading zeros in speaker id
df = pd.read_csv(dataset_fp, dtype=str)

# Get the ground truth transcription and DeepSpeech hypothesis
ground_truth = df['transcription_clean'].tolist()
hypothesis = df['prediction'].tolist()

#error = wer(ground_truth[:50], hypothesis[:50])

wer = pywer.wer(references, hypotheses)
cer = pywer.cer(references, hypotheses)

print(wer)
'''
wer_metric = load_metric("wer")
def compute_metrics(pred):
    pred_logits = pred.predictions
    pred_ids = np.argmax(pred_logits, axis=-1)

    pred.label_ids[pred.label_ids == -100] = processor.tokenizer.pad_token_id

    pred_str = processor.batch_decode(pred_ids)
    # we do not want to group tokens when computing the metrics
    label_str = processor.batch_decode(pred.label_ids, group_tokens=False)

    wer = wer_metric.compute(predictions=pred_str, references=label_str)

    return {"wer": wer}
print("SUCCESS: Defined WER evaluation metric.")
'''
