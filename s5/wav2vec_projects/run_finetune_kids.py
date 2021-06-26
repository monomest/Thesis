# run_finetune_kids.py
# Purpose: Uses wav2vec2 to fine tune for kids speech
# Source:
# https://colab.research.google.com/github/patrickvonplaten/notebooks/blob/master/Fine_tuning_Wav2Vec2_for_English_ASR.ipynb
# Author: Renee Lu, 2021

# ------ INSTALL PACKAGES IF NEEDED ------
#pip install datasets==1.8.0
#pip install transformers
#pip install soundfile
#pip install jiwer

# ------ IMPORT REQUIRED PACKAGES ------
# Import datasets and evaluation metric
print("\n------> IMPORTING PACKAGES....\n")
print("-->Importing datasets...")
from datasets import load_dataset, load_metric, ClassLabel
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
print("-->SUCCESS! All packages imported.")

# ------ PREPARING DATASET ------
# Prepare kids' speech corpus


