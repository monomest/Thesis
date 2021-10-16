#----------------------------------------------------------
# run_finetune_kids.py
# Purpose: Uses wav2vec2 to fine tune for kids speech
#          with children's speech corpus.
# Based on source:
# https://colab.research.google.com/github/patrickvonplaten/notebooks/blob/master/Fine_tuning_Wav2Vec2_for_English_ASR.ipynb
# Author: Renee Lu, 2021
#----------------------------------------------------------

# ------------------------------------------
#      Install packages if needed
# ------------------------------------------
#pip install datasets==1.8.0
#pip install transformers
#pip install soundfile
#pip install jiwer
print("------------------------------------------------------------------------")
print("                 run_finetune_kids.py                                   ")
print("------------------------------------------------------------------------")
# ------------------------------------------
#       Import required packages
# ------------------------------------------
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
#      Setting experiment arguments
# ------------------------------------------
print("\n------> EXPERIMENT ARGUMENTS ----------------------------------------- \n")

# Perform Training (True/False)
# If false, this will go straight to model evaluation 
training = True
print("training:", training)

# Experiment ID
# For 1) naming vocab.json file and
#     2) naming model output directory
#     3) naming results file
experiment_id = "20211015-base-myST-OGI"
print("experiment_id:", experiment_id)

# DatasetDict Id
# For 1) naming cache directory and 
#     2) saving the DatasetDict object
datasetdict_id = "myST-OGI-finetune"
print("datasetdict_id:", datasetdict_id)

# Base filepath
# For setting the base filepath to direct output to
base_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/"
print("base_fp:", base_fp)

# Base cache directory filepath
# For setting directory for cache files
base_cache_fp = "/srv/scratch/chacmod/.cache/huggingface/datasets/"

# Training dataset name and filename
# Dataset name and filename of the csv file containing the training data
# For generating filepath to file location
train_name = "myST-OGI"
train_filename = "THESIS_C/myST-OGI_data_finetune"
print("train_name:", train_name)
print("train_filename:", train_filename)

# Evaluation dataset name and filename
# Dataset name and filename of the csv file containing the evaluation data
# For generating filepath to file location
evaluation_name = "myST-OGI"
evaluation_filename = "THESIS_C/myST-OGI_data_dev"
print("evaluation_name:", evaluation_name)
print("evaluation_filename:", evaluation_filename)

# Resume training from/ use checkpoint (True/False)
# Set to True for:
# 1) resuming from a saved checkpoint if training stopped midway through
# 2) for using an existing finetuned model for evaluation 
# If 2), then must also set eval_pretrained = True
use_checkpoint = False
print("use_checkpoint:", use_checkpoint)
# Set checkpoint if resuming from/using checkpoint
checkpoint = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST-OGI_local/20210819-OGI-myST-120h"
if use_checkpoint:
    print("checkpoint:", checkpoint)

# Use a pretrained tokenizer (True/False)
#     True: Use existing tokenizer (if custom dataset has same vocab)
#     False: Use custom tokenizer (if custom dataset has different vocab)
use_pretrained_tokenizer = True
print("use_pretrained_tokenizer:", use_pretrained_tokenizer)
# Set tokenizer
pretrained_tokenizer = "facebook/wav2vec2-base-960h"
if use_pretrained_tokenizer:
    print("pretrained_tokenizer:", pretrained_tokenizer)

# Evaluate existing model instead of newly trained model (True/False)
#     True: use the model in the filepath set by 'eval_model' for eval
#     False: use the model trained from this script for eval
eval_pretrained = False
print("eval_pretrained:", eval_pretrained)
# Set existing model to evaluate, if evaluating on existing model
eval_model = checkpoint
if eval_pretrained:
    print("eval_model:", eval_model)

# Baseline model for evaluating baseline metric
# This model will be evaluated at the end for the baseline WER
baseline_model = "facebook/wav2vec2-base-960h"
print("baseline_model:", baseline_model)

# Evalulate the baseline model or not (True/False)
#   True: evaluate baseline model on test set
#   False: do not evaluate baseline model on test set
eval_baseline = False

print("\n------> MODEL ARGUMENTS... -------------------------------------------\n")
# For setting model = Wav2Vec2ForCTC.from_pretrained()

set_hidden_dropout = 0.1                    # Default = 0.1
print("hidden_dropout:", set_hidden_dropout)
set_activation_dropout = 0.1                # Default = 0.1
print("activation_dropout:", set_activation_dropout)
set_attention_dropout = 0.1                 # Default = 0.1
print("attention_dropoutput:", set_attention_dropout)
set_feat_proj_dropout = 0.0                 # Default = 0.1
print("feat_proj_dropout:", set_feat_proj_dropout)
set_layerdrop = 0.1                         # Default = 0.1
print("layerdrop:", set_layerdrop)
set_mask_time_prob = 0.05                  # Default = 0.05
print("mask_time_prob:", set_mask_time_prob)
set_mask_time_length = 10                   # Default = 10
print("mask_time_length:", set_mask_time_length)
set_ctc_loss_reduction = "mean"             # Default = "sum"
print("ctc_loss_reduction:", set_ctc_loss_reduction)
set_ctc_zero_infinity = True               # Default = False
print("ctc_zero_infinity:", set_ctc_zero_infinity)
set_gradient_checkpointing = True           # Default = False
print("gradient_checkpointing:", set_gradient_checkpointing)

print("\n------> TRAINING ARGUMENTS... ----------------------------------------\n")
# For setting training_args = TrainingArguments()

set_evaluation_strategy = "steps"           # Default = "no"
print("evaluation strategy:", set_evaluation_strategy)
set_per_device_train_batch_size = 8         # Default = 8
print("per_device_train_batch_size:", set_per_device_train_batch_size)
set_gradient_accumulation_steps = 1         # Default = 1
print("gradient_accumulation_steps:", set_gradient_accumulation_steps)
set_learning_rate = 0.00003                 # Default = 0.00005
print("learning_rate:", set_learning_rate)
set_weight_decay = 0.01                     # Default = 0
print("weight_decay:", set_weight_decay)
set_adam_beta1 = 0.9                        # Default = 0.9
print("adam_beta1:", set_adam_beta1)
set_adam_beta2 = 0.98                       # Default = 0.999
print("adam_beta2:", set_adam_beta2)
set_adam_epsilon = 0.00000001               # Default = 0.00000001
print("adam_epsilon:", set_adam_epsilon)
set_num_train_epochs = 15                   # Default = 3.0
print("num_train_epochs:", set_num_train_epochs)
set_max_steps = 60000                          # Default = -1, overrides epochs
print("max_steps:", set_max_steps)
set_lr_scheduler_type = "linear"            # Default = "linear"
print("lr_scheduler_type:", set_lr_scheduler_type )
set_warmup_ratio = 0.1                      # Default = 0.0
print("warmup_ratio:", set_warmup_ratio)
set_logging_strategy = "steps"              # Default = "steps"
print("logging_strategy:", set_logging_strategy)
set_logging_steps = 1000                      # Default = 500
print("logging_steps:", set_logging_steps)
set_save_strategy = "steps"                 # Default = "steps"
print("save_strategy:", set_save_strategy)
set_save_steps = 1000                         # Default = 500
print("save_steps:", set_save_steps)
set_save_total_limit = 70                   # Optional                 
print("save_total_limit:", set_save_total_limit)
set_fp16 = True                             # Default = False
print("fp16:", set_fp16)
set_eval_steps = 1000                         # Optional
print("eval_steps:", set_eval_steps)
set_load_best_model_at_end = True           # Default = False
print("load_best_model_at_end:", set_load_best_model_at_end)
set_metric_for_best_model = "wer"           # Optional
print("metric_for_best_model:", set_metric_for_best_model)
set_greater_is_better = False               # Optional
print("greater_is_better:", set_greater_is_better)
set_group_by_length = True                  # Default = False
print("group_by_length:", set_group_by_length)

# ------------------------------------------
#        Generating file paths
# ------------------------------------------
print("\n------> GENERATING FILEPATHS... --------------------------------------\n")
# Path to dataframe csv for train dataset
data_train_fp = base_fp + train_name + "_local/" + train_filename + ".csv"
print("--> data_train_fp:", data_train_fp)
# Path to dataframe csv for test dataset
data_test_fp = base_fp + evaluation_name + "_local/" + evaluation_filename + ".csv"
print("--> data_test_fp:", data_test_fp)

# Dataframe file 
# |-----------|---------------------|----------|---------|
# | file path | transcription_clean | duration | spkr_id |
# |-----------|---------------------|----------|---------|
# |   ...     |      ...            |  ..secs  | ......  |
# |-----------|---------------------|----------|---------|
# NOTE: The spkr_id column may need to be removed beforehand if
#       there appears to be a mixture between numerical and string ID's
#       due to this issue: https://github.com/apache/arrow/issues/4168
#       when calling load_dataset()

# Path to datasets cache
data_cache_fp = base_cache_fp + datasetdict_id
print("--> data_cache_fp:", data_cache_fp)
# Path to save vocab.json
vocab_fp = base_fp + train_name + "_local/vocab_" + experiment_id + ".json"
print("--> vocab_fp:", vocab_fp)
# Path to save model output
model_fp = base_fp + train_name + "_local/" + experiment_id
print("--> model_fp:", model_fp)
# Path to save results output
baseline_results_fp = base_fp + train_name + "_local/" + experiment_id + "_baseline_results.csv" 
print("--> baseline_results_fp:", baseline_results_fp)
finetuned_results_fp = base_fp + train_name + "_local/" + experiment_id + "_finetuned_results.csv"
print("--> finetuned_results_fp:", finetuned_results_fp)
# Pre-trained checkpoint model
# For 1) Fine-tuning or
#     2) resuming training from pre-trained model
# If 1) must set use_checkpoint = False
# If 2)must set use_checkpoint = True
# Default model to fine-tune is facebook's model
pretrained_mod = "facebook/wav2vec2-base"
if use_checkpoint:
    pretrained_mod = checkpoint
print("--> pretrained_mod:", pretrained_mod)
# Path to pre-trained tokenizer
# If use_pretrained_tokenizer = True
if use_pretrained_tokenizer:
    print("--> pretrained_tokenizer:", pretrained_tokenizer)

# ------------------------------------------
#         Preparing dataset
# ------------------------------------------
# Run the following scripts to prepare data
# 1) Prepare data from kaldi file: 
# /srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/wav2vec_exp/data_prep.py
# 3) [Optional] Limit the files to certain duration:
# /srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/wav2vec_projects/data_getShortWavs.py
# 2) Split data into train and test:
# /srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/wav2vec_projects/data_split.py

print("\n------> PREPARING DATASET... ------------------------------------\n")
# Read the existing csv saved dataframes and
# load as a DatasetDict 
data = load_dataset('csv', 
                    data_files={'train': data_train_fp,
                                'test': data_test_fp},
                    cache_dir=data_cache_fp)
# Remove the "duration" and "spkr_id" column
#data = data.remove_columns(["duration", "spkr_id"])
#data = data.remove_columns(["duration"])
print("--> dataset...")
print(data)
# Display some random samples of the dataset
print("--> Printing some random samples...")
def show_random_elements(dataset, num_examples=10):
    assert num_examples <= len(dataset), "Picking more elements than in dataset"
    picks = []
    for _ in range(num_examples):
        pick = random.randint(0, len(dataset)-1)
        while pick in picks:
            pick = random.randint(0, len(dataset)-1)
        picks.append(pick)
    df = pd.DataFrame(dataset[picks])
    print(df)
show_random_elements(data["train"], num_examples=5)
print("SUCCESS: Prepared dataset.")
# ------------------------------------------
#       Processing transcription
# ------------------------------------------
# Create vocab.json
# Extracting all distinct letters of train and test set
# and building vocab from this set of letters
print("\n------> PROCESSING TRANSCRIPTION... ---------------------------------------\n")
# Mapping function that concatenates all transcriptions
# into one long transcription and then transforms the
# string into a set of chars. Set batched=True to the 
# map(...) function so that the mapping function has access
# to all transcriptions at once.

chars_to_ignore_regex = '[\,\?\.\!\-\;\:\"]'

def process_transcription(batch):
    #batch["transcription_clean"] = re.sub(chars_to_ignore_regex, '', batch["transcription_clean"]).upper().replace("<UNK>", "<unk>")
    batch["transcription_clean"] = batch["transcription_clean"].upper()
    batch["transcription_clean"] = batch["transcription_clean"].replace("<UNK>", "<unk>")
    return batch

data = data.map(process_transcription)

def extract_all_chars(batch):
    all_text = " ".join(batch["transcription_clean"])
    vocab = list(set(all_text))
    return {"vocab": [vocab], "all_text": [all_text]}
    
if not use_pretrained_tokenizer:
    print("--> Creating map(...) function for vocab...")
    vocabs = data.map(extract_all_chars, batched=True, batch_size=-1, keep_in_memory=True, remove_columns=data.column_names["train"])
    # Create union of all distinct letters in train and test set
    # and convert resulting list into enumerated dictionary
    # Vocab includes a-z, ' , space, UNK, PAD
    vocab_list = list(set(vocabs["train"]["vocab"][0]) | set(vocabs["test"]["vocab"][0]))
    vocab_dict = {v: k for k, v in enumerate(vocab_list)}
    print("--> Vocab len:", len(vocab_dict), "\n", vocab_dict)
    # Give space " " a visible character " | "
    # Include "unknown" [UNK] token for dealing with characters
    # not encountered in training.
    # Add padding token to corresponds to CTC's "blank token".
    vocab_dict["|"] = vocab_dict[" "]
    del vocab_dict[" "]
    vocab_dict["[UNK]"] = len(vocab_dict)
    vocab_dict["[PAD]"] = len(vocab_dict)
    print("--> Vocab len:", len(vocab_dict), "\n", vocab_dict)
    # Save vocab as a json file
    with open(vocab_fp, 'w') as vocab_file:
        json.dump(vocab_dict, vocab_file)
    print("SUCCESS: Created vocabulary file at", vocab_fp)
# Use json file to instantiate an object of the 
# Wav2VecCTCTokenziser class if not using pretrained tokenizer
if use_pretrained_tokenizer:
    tokenizer = Wav2Vec2CTCTokenizer.from_pretrained(pretrained_tokenizer)
else:
    tokenizer = Wav2Vec2CTCTokenizer(vocab_fp, unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")
#tokenizer = save_pretrained(model_fp)
