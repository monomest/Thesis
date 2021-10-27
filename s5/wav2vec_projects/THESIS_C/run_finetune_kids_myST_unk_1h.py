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
experiment_id = "20211025-base-myST-1h"
print("experiment_id:", experiment_id)

# DatasetDict Id
# For 1) naming cache directory and 
#     2) saving the DatasetDict object
datasetdict_id = "myST-1h-finetune"
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
train_name = "myST"
train_filename = "THESIS_C/myST_data_finetune_unk_1h_light"
print("train_name:", train_name)
print("train_filename:", train_filename)

# Evaluation dataset name and filename
# Dataset name and filename of the csv file containing the evaluation data
# For generating filepath to file location
evaluation_name = "myST"
evaluation_filename = "THESIS_C/myST_data_dev_unk_light"
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
set_layerdrop = 0.01                        # Default = 0.1
print("layerdrop:", set_layerdrop)
set_mask_time_prob = 0.075                  # Default = 0.05
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
set_learning_rate = 0.00005                 # Default = 0.00005
print("learning_rate:", set_learning_rate)
set_weight_decay = 0.01                     # Default = 0
print("weight_decay:", set_weight_decay)
set_adam_beta1 = 0.9                        # Default = 0.9
print("adam_beta1:", set_adam_beta1)
set_adam_beta2 = 0.98                       # Default = 0.999
print("adam_beta2:", set_adam_beta2)
set_adam_epsilon = 0.00000001               # Default = 0.00000001
print("adam_epsilon:", set_adam_epsilon)
set_num_train_epochs = 590                  # Default = 3.0
print("num_train_epochs:", set_num_train_epochs)
set_max_steps = 13000                       # Default = -1, overrides epochs
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
set_save_total_limit = 30                   # Optional                 
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

#chars_to_ignore_regex = '[\,\?\.\!\-\;\:\"]'

def process_transcription(batch):
    #batch["transcription_clean"] = re.sub(chars_to_ignore_regex, '', batch["transcription_clean"]).upper()
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
# ------------------------------------------
#    Create Wav2Vec2 Feature Extractor
# ------------------------------------------
print("\n------> CREATING WAV2VEC2 FEATURE EXTRACTOR... -----------------------\n")
# Instantiate a Wav2Vec2 feature extractor:
# - feature_size: set to 1 because model was trained on raw speech signal
# - sampling_rate: sampling rate the model is trained on
# - padding_value: for batched inference, shorter inputs are padded
# - do_normalize: whether input should be zero-mean-unit-variance
#   normalised or not. Usually, speech models perform better when true.
# - return_attention_mask: set to false for Wav2Vec2, but true for
#   fine-tuning large-lv60
feature_extractor = Wav2Vec2FeatureExtractor(feature_size=1, sampling_rate=16000, padding_value=0.0, do_normalize=True, return_attention_mask=False)
# Feature extractor and tokenizer wrapped into a single
# Wav2Vec2Processor class so we only need a model and processor object
processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)
# Save to re-use the just created processor and the fine-tuned model
processor.save_pretrained(model_fp)
print("SUCCESS: Created feature extractor.")

# ------------------------------------------
#             Pre-process Data
# ------------------------------------------
print("\n------> PRE-PROCESSING DATA... ----------------------------------------- \n")
# Audio files are stored as .wav format
# We want to store both audio values and sampling rate
# in the dataset. 
# We write a map(...) function accordingly.
def speech_file_to_array_fn(batch):
    speech_array, sampling_rate = sf.read(batch["filepath"])
    batch["speech"] = speech_array
    batch["sampling_rate"] = sampling_rate
    batch["target_text"] = batch["transcription_clean"]
    return batch
data = data.map(speech_file_to_array_fn, remove_columns=data.column_names["train"], num_proc=4)
# Check a few rows of data to verify data properly loaded
print("--> Verifying data with a random sample...")
rand_int = random.randint(0, len(data["train"])-1)
print("Target text:", data["train"][rand_int]["target_text"])
print("Input array shape:", np.asarray(data["train"][rand_int]["speech"]).shape)
print("Sampling rate:", data["train"][rand_int]["sampling_rate"])
# Process dataset to the format expected by model for training
# Using map(...)
# 1) Check all data samples have same sampling rate (16kHz)
# 2) Extract input_values from loaded audio file.
#    This only involves normalisation but could also correspond
#    to extracting log-mel features
# 3) Encode the transcriptions to label ids

def prepare_dataset(batch):
    # check that all files have the correct sampling rate
    assert (
        len(set(batch["sampling_rate"])) == 1
    ), f"Make sure all inputs have the same sampling rate of {processor.feature_extractor.sampling_rate}."

    batch["input_values"] = processor(batch["speech"], sampling_rate=batch["sampling_rate"][0]).input_values

    with processor.as_target_processor():
        batch["labels"] = processor(batch["target_text"]).input_ids
    return batch
data_prepared = data.map(prepare_dataset, remove_columns=data.column_names["train"], batch_size=8, num_proc=4, batched=True)

print("SUCCESS: Data ready for training and evaluation.")

# ------------------------------------------
#         Training & Evaluation
# ------------------------------------------
# Set up the training pipeline using HuggingFace's Trainer:
# 1) Define a data collator: Wav2Vec has much larger input
#    length than output length. Therefore, it is more
#    efficient to pad the training batches dynamically meaning
#    that all training samples should only be padded to the longest
#    sample in their batch and not the overall longest sample.
#    Therefore, fine-tuning Wav2Vec2 required a special 
#    padding data collator, defined below.
# 2) Evaluation metric: we evaluate the model using word error rate (WER)
#    We define a compute_metrics function accordingly.
# 3) Load a pre-trained checkpoint
# 4) Define the training configuration
print("\n------> PREPARING FOR TRAINING & EVALUATION... ----------------------- \n")
# 1) Defining data collator
print("--> Defining data collator...")

@dataclass
class DataCollatorCTCWithPadding:
    """
    Data collator that will dynamically pad the inputs received.
    Args:
        processor (:class:`~transformers.Wav2Vec2Processor`)
            The processor used for proccessing the data.
        padding (:obj:`bool`, :obj:`str` or :class:`~transformers.tokenization_utils_base.PaddingStrategy`, `optional`, defaults to :obj:`True`):
            Select a strategy to pad the returned sequences (according to the model's padding side and padding index)
            among:
            * :obj:`True` or :obj:`'longest'`: Pad to the longest sequence in the batch (or no padding if only a single
                sequence if provided).
            * :obj:`'max_length'`: Pad to a maximum length specified with the argument :obj:`max_length` or to the
                maximum acceptable input length for the model if that argument is not provided.
            * :obj:`False` or :obj:`'do_not_pad'` (default): No padding (i.e., can output a batch with sequences of
              different lengths).
        max_length (:obj:`int`, `optional`):
            Maximum length of the ``input_values`` of the returned list and optionally padding length (see above).
        max_length_labels (:obj:`int`, `optional`):
            Maximum length of the ``labels`` returned list and optionally padding length (see above).
        pad_to_multiple_of (:obj:`int`, `optional`):
            If set will pad the sequence to a multiple of the provided value.
            This is especially useful to enable the use of Tensor Cores on NVIDIA hardware with compute capability >=
            7.5 (Volta).
    """

    processor: Wav2Vec2Processor
    padding: Union[bool, str] = True
    max_length: Optional[int] = None
    max_length_labels: Optional[int] = None
    pad_to_multiple_of: Optional[int] = None
    pad_to_multiple_of_labels: Optional[int] = None

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        # split inputs and labels since they have to be of different lenghts and need
        # different padding methods
        input_features = [{"input_values": feature["input_values"]} for feature in features]
        label_features = [{"input_ids": feature["labels"]} for feature in features]

        batch = self.processor.pad(
            input_features,
            padding=self.padding,
            max_length=self.max_length,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors="pt",
        )
        with self.processor.as_target_processor():
            labels_batch = self.processor.pad(
                label_features,
                padding=self.padding,
                max_length=self.max_length_labels,
                pad_to_multiple_of=self.pad_to_multiple_of_labels,
                return_tensors="pt",
            )
        # replace padding with -100 to ignore loss correctly
        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)   
        batch["labels"] = labels
        return batch
data_collator = DataCollatorCTCWithPadding(processor=processor, padding=True)
print("SUCCESS: Data collator defined.")

# 2) Evaluation metric
#    Using word error rate (WER)
print("--> Defining evaluation metric...")
# The model will return a sequence of logit vectors y.
# A logit vector yi contains the log-odds for each word in the
# vocabulary defined earlier, thus len(yi) = config.vocab_size
# We are interested in the most likely prediction of the mode and 
# thus take argmax(...) of the logits. We also transform the
# encoded labels back to the original string by replacing -100
# with the pad_token_id and decoding the ids while making sure
# that consecutive tokens are not grouped to the same token in
# CTC style.
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

# 3) Load pre-trained checkpoint
# Load pre-trained Wav2Vec2 checkpoint. The tokenizer's pad_token_id
# must be to define the model's pad_token_id or in the case of Wav2Vec2ForCTC
# also CTC's blank token. To save GPU memory, we enable PyTorch's gradient
# checkpointing and also set the loss reduction to "mean".
print("--> Loading pre-trained checkpoint...")
model = Wav2Vec2ForCTC.from_pretrained(
    pretrained_mod,
    vocab_size=len(processor.tokenizer),
    hidden_dropout=set_hidden_dropout,
    activation_dropout=set_activation_dropout,
    attention_dropout=set_attention_dropout,
    feat_proj_dropout=set_feat_proj_dropout,
    layerdrop=set_layerdrop,
    mask_time_prob=set_mask_time_prob,
    mask_time_length=set_mask_time_length,
    ctc_loss_reduction=set_ctc_loss_reduction,
    ctc_zero_infinity=set_ctc_zero_infinity,
    gradient_checkpointing=set_gradient_checkpointing,
    pad_token_id=processor.tokenizer.pad_token_id
)

# The first component of Wav2Vec2 consists of a stack of CNN layers
# that are used to extract acoustically meaningful - but contextually 
# independent - features from the raw speech signal. This part of the
# model has already been sufficiently trained during pretrainind and 
# as stated in the paper does not need to be fine-tuned anymore. 
# Thus, we can set the requires_grad to False for all parameters of 
# the feature extraction part.
model.freeze_feature_extractor()
print("SUCCESS: Pre-trained checkpoint loaded.")

# 4) Configure training parameters
#    - group_by_length: makes training more efficient by grouping
#      training samples of similar input length into one batch.
#      Reduces useless padding tokens passed through model.
#    - learning_rate and weight_decay: heuristically tuned until
#      fine-tuning has become stable. These paramteres strongly
#      depend on Timit dataset and might be suboptimal for this
#      dataset.
# For more info: https://huggingface.co/transformers/master/main_classes/trainer.html?highlight=trainer#trainingarguments

training_args = TrainingArguments(
  output_dir=model_fp,
  evaluation_strategy=set_evaluation_strategy,
  per_device_train_batch_size=set_per_device_train_batch_size,
  gradient_accumulation_steps=set_gradient_accumulation_steps,
  learning_rate=set_learning_rate,
  weight_decay=set_weight_decay,
  adam_beta1=set_adam_beta1,
  adam_beta2=set_adam_beta2,
  adam_epsilon=set_adam_epsilon,
  num_train_epochs=set_num_train_epochs,
  max_steps=set_max_steps,
  lr_scheduler_type=set_lr_scheduler_type,
  warmup_ratio=set_warmup_ratio,
  logging_strategy=set_logging_strategy,
  logging_steps=set_logging_steps,
  save_strategy=set_save_strategy,
  save_steps=set_save_steps,
  save_total_limit=set_save_total_limit,
  fp16=set_fp16,
  eval_steps=set_eval_steps,
  load_best_model_at_end=set_load_best_model_at_end,
  metric_for_best_model=set_metric_for_best_model,
  greater_is_better=set_greater_is_better,
  group_by_length=set_group_by_length
)
# All instances can be passed to Trainer and 
# we are ready to start training!
trainer = Trainer(
    model=model,
    data_collator=data_collator,
    args=training_args,
    compute_metrics=compute_metrics,
    train_dataset=data_prepared["train"],
    eval_dataset=data_prepared["test"],
    tokenizer=processor.feature_extractor,
)

# ------------------------------------------
#               Training
# ------------------------------------------
# While the trained model yields a satisfying result on Timit's
# test data, it is by no means an optimally fine-tuned model
# for children's data.

if training:
    print("\n------> STARTING TRAINING... ----------------------------------------- \n")
    torch.cuda.empty_cache()
    # Train
    if use_checkpoint:
        trainer.train(pretrained_mod)
    else:
        trainer.train()
    # Save the model
    model.save_pretrained(model_fp)

# ------------------------------------------
#            Evaluation
# ------------------------------------------
# Evaluate fine-tuned model on test set.
print("\n------> EVALUATING MODEL... ------------------------------------------ \n")
torch.cuda.empty_cache()

if eval_pretrained:
    processor = Wav2Vec2Processor.from_pretrained(eval_model)
    model = Wav2Vec2ForCTC.from_pretrained(eval_model)
else:
    processor = Wav2Vec2Processor.from_pretrained(model_fp)
    model = Wav2Vec2ForCTC.from_pretrained(model_fp)

# Now, we will make use of the map(...) function to predict 
# the transcription of every test sample and to save the prediction 
# in the dataset itself. We will call the resulting dictionary "results".
# Note: we evaluate the test data set with batch_size=1 on purpose due 
# to this issue (https://github.com/pytorch/fairseq/issues/3227). Since 
# padded inputs don't yield the exact same output as non-padded inputs, 
# a better WER can be achieved by not padding the input at all.
def map_to_result(batch):
  model.to("cuda")
  input_values = processor(
      batch["speech"], 
      sampling_rate=batch["sampling_rate"], 
      return_tensors="pt"
  ).input_values.to("cuda")

  with torch.no_grad():
    logits = model(input_values).logits

  pred_ids = torch.argmax(logits, dim=-1)
  batch["pred_str"] = processor.batch_decode(pred_ids)[0]
  
  return batch

results = data["test"].map(map_to_result)
# Save results to csv
results_df = results.to_pandas()
results_df = results_df.drop(columns=['speech', 'sampling_rate'])
results_df.to_csv(finetuned_results_fp)
print("Saved results to:", finetuned_results_fp)

# Getting the WER
print("--> Getting fine-tuned test results...")
print("Fine-tuned Test WER: {:.3f}".format(wer_metric.compute(predictions=results["pred_str"], 
      references=results["target_text"])))
# Showing prediction errors
print("--> Showing some fine-tuned prediction errors...")
show_random_elements(results.remove_columns(["speech", "sampling_rate"]))
# Deeper look into model: running the first test sample through the model, 
# take the predicted ids and convert them to their corresponding tokens.
print("--> Taking a deeper look...")
model.to("cuda")
input_values = processor(data["test"][0]["speech"], sampling_rate=data["test"][0]["sampling_rate"], return_tensors="pt").input_values.to("cuda")

with torch.no_grad():
  logits = model(input_values).logits

pred_ids = torch.argmax(logits, dim=-1)

# convert ids to tokens
print(" ".join(processor.tokenizer.convert_ids_to_tokens(pred_ids[0].tolist())))

# Evaluate baseline model on test set if eval_baseline = True
if eval_baseline:
    print("\n------> EVALUATING BASELINE MODEL... ------------------------------------------ \n")
    torch.cuda.empty_cache()
    processor = Wav2Vec2Processor.from_pretrained(baseline_model)
    model = Wav2Vec2ForCTC.from_pretrained(baseline_model)
    tokenizer = Wav2Vec2CTCTokenizer.from_pretrained(baseline_model)

    # Now, we will make use of the map(...) function to predict 
    # the transcription of every test sample and to save the prediction 
    # in the dataset itself. We will call the resulting dictionary "results".
    # Note: we evaluate the test data set with batch_size=1 on purpose due 
    # to this issue (https://github.com/pytorch/fairseq/issues/3227). Since 
    # padded inputs don't yield the exact same output as non-padded inputs, 
    # a better WER can be achieved by not padding the input at all.

    results = data["test"].map(map_to_result)
    # Saving results to csv
    results_df = results.to_pandas()
    results_df = results_df.drop(columns=['speech', 'sampling_rate'])
    results_df.to_csv(baseline_results_fp)
    print("Saved results to:", baseline_results_fp)
    # Getting the WER
    print("--> Getting baseline test results...")
    print("Baseline Test WER: {:.3f}".format(wer_metric.compute(predictions=results["pred_str"], 
          references=results["target_text"])))
    # Showing prediction errors
    print("--> Showing some baseline prediction errors...")
    show_random_elements(results.remove_columns(["speech", "sampling_rate"]))
    # Deeper look into model: running the first test sample through the model, 
    # take the predicted ids and convert them to their corresponding tokens.
    print("--> Taking a deeper look...")
    model.to("cuda")
    input_values = processor(data["test"][0]["speech"], sampling_rate=data["test"][0]["sampling_rate"], return_tensors="pt").input_values.to("cuda")

    with torch.no_grad():
        logits = model(input_values).logits

    pred_ids = torch.argmax(logits, dim=-1)

    # convert ids to tokens
    print(" ".join(processor.tokenizer.convert_ids_to_tokens(pred_ids[0].tolist())))

print("\n------> SUCCESSFULLY FINISHED ---------------------------------------- \n")
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Finished:", dt_string)
