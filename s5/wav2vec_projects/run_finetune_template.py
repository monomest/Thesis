# run_finetune.py
# Fine tunes wav2vec 2.0 for English ASR with HuggingFace Transformers
# Using the TIMIT corpus
# Source: https://huggingface.co/blog/fine-tune-wav2vec2-english

#!pip install datasets==1.4.1
#!pip install transformers==4.4.0
#To load audio files
#!pip install soundfile
# Evaluate fine-tuned model using WER metric
#!pip install jiwer

print("================= run_finetune.py =================")
print("This python code finetunes wav2vec 2.0 for English ASR")
print("using HuggingFace Transformers with the TIMIT corpus.")
print("=======================================================")

# -----------------------------------------------------------------
#          PREPARE DATA, TOKENIZER AND FEATURE EXTRACTOR
# -----------------------------------------------------------------
# Feature extractor processes speech signal to model's input format
# Tokenizer decodes the model's prediction

# Load the dataset
print("\n------> loading the dataset...\n")
from datasets import load_dataset, load_metric
timit = load_dataset("timit_asr", cache_dir="/srv/scratch/chacmod/.cache/huggingface/datasets/")
print(timit)
# We do not consider phoneme classification - interested in word WER
timit = timit.remove_columns(["phonetic_detail", "word_detail", "dialect_region", "id", "sentence_type", "speaker_id"])

# Normalize text to only have lower case letter
print("\n------> normalizing the text...\n")
import re
chars_to_ignore_regex = '[\,\?\.\!\-\;\:\"]'

def remove_special_characters(batch):
    batch["text"] = re.sub(chars_to_ignore_regex, '', batch["text"]).lower()
    return batch

timit = timit.map(remove_special_characters)

# Extract all distinct letters of the training and test data
# to build our vocabulary from this set of letters
# Use a mapping function that concatenates all transcriptions
# into one long transcription and then transforms the string
# into a set of chars. 
# Set batched=True to the map(...) function so that
# the mapping function has access to all transcriptions at once
print("\n------> extracting vocabulary of letters...\n")
def extract_all_chars(batch):
  all_text = " ".join(batch["text"])
  vocab = list(set(all_text))
  return {"vocab": [vocab], "all_text": [all_text]}

vocabs = timit.map(extract_all_chars, batched=True, batch_size=-1, keep_in_memory=True, remove_columns=timit.column_names["train"])
# Create union of all distinct letters in the datasets
# and convert resulting list into enumerated dictionary
vocab_list = list(set(vocabs["train"]["vocab"][0]) | set(vocabs["test"]["vocab"][0]))

vocab_dict = {v: k for k, v in enumerate(vocab_list)}
print("Vocab Dict: " + str(vocab_dict))
# Set " " as its own token class denoted visibly as " | "
vocab_dict["|"] = vocab_dict[" "]
del vocab_dict[" "]
# Add an "unknown" token and padding token corresponsing to CTC's "blank token"
vocab_dict["[UNK]"] = len(vocab_dict)
vocab_dict["[PAD]"] = len(vocab_dict)
print("Vocab length: " + str(len(vocab_dict)))

# Save vocab as a json file
import json
with open('vocab.json', 'w') as vocab_file:
    json.dump(vocab_dict, vocab_file)

# Use json file to instantiate an object of
# the Wav2Vec2CTCTokenizer class
print("\n------> creating tokenizer...\n")
from transformers import Wav2Vec2CTCTokenizer

tokenizer = Wav2Vec2CTCTokenizer("./vocab.json", unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")

# Create wav2vec 2.0 feature extractor
# If fine-tuning large-lv60 use attention_mask=True
print("\n------> creating feature extractor...\n")
from transformers import Wav2Vec2FeatureExtractor

feature_extractor = Wav2Vec2FeatureExtractor(feature_size=1, sampling_rate=16000, padding_value=0.0, do_normalize=True, return_attention_mask=False)

# Feature extractor and tokenizer are wrapped into
# a single Wav2Vec2Processor class so we only need a 
# model and processor object
from transformers import Wav2Vec2Processor

processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)

# Preprocess data
print("\n------> preprocessing data...\n")
print("Training sample: " + str(timit["train"][0]))

# Store both audio data and sampling rate
import soundfile as sf

def speech_file_to_array_fn(batch):
    speech_array, sampling_rate = sf.read(batch["file"])
    batch["speech"] = speech_array
    batch["sampling_rate"] = sampling_rate
    batch["target_text"] = batch["text"]
    return batch

timit = timit.map(speech_file_to_array_fn, remove_columns=timit.column_names["train"], num_proc=4)

# Final check of correct data preparation
import random
import numpy as np

rand_int = random.randint(0, len(timit["train"]))

print("Target text:", timit["train"][rand_int]["target_text"])
print("Input array shape:", np.asarray(timit["train"][rand_int]["speech"]).shape)
print("Sampling rate:", timit["train"][rand_int]["sampling_rate"])

# Process dataset to the format expected by the model for training
# 1) Check all data samples have 16kHz sample rate
# 2) Extract input_values from the loaded audio file.
# In this case, this only includes normalisation, but 
# for other speech models, this step could correspond to
# extracting log-mel features
# 3) Encode transcriptions to label ids

def prepare_dataset(batch):
    # check that all files have the correct sampling rate
    assert (
        len(set(batch["sampling_rate"])) == 1
    ), f"Make sure all inputs have the same sampling rate of {processor.feature_extractor.sampling_rate}."

    batch["input_values"] = processor(batch["speech"], sampling_rate=batch["sampling_rate"][0]).input_values

    with processor.as_target_processor():
        batch["labels"] = processor(batch["target_text"]).input_ids
    return batch

timit_prepared = timit.map(prepare_dataset, remove_columns=timit.column_names["train"], batch_size=8, num_proc=4, batched=True)

# ------------------------------------------------------
#           TRAINING AND EVALUATION
# ------------------------------------------------------

# Set up trainer
import torch

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

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

# Initialise data collator
data_collator = DataCollatorCTCWithPadding(processor=processor, padding=True)

# Define WER evaluation metric
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

from transformers import Wav2Vec2ForCTC

model = Wav2Vec2ForCTC.from_pretrained(
    "facebook/wav2vec2-base", 
    gradient_checkpointing=True, 
    ctc_loss_reduction="mean", 
    pad_token_id=processor.tokenizer.pad_token_id,
)

# Keep pre-trained model
model.freeze_feature_extractor()

# Training arguments
from transformers import TrainingArguments

training_args = TrainingArguments(
  output_dir="./wav2vec2-base-timit-demo",
  group_by_length=True,
  per_device_train_batch_size=32,
  evaluation_strategy="steps",
  num_train_epochs=30,
  fp16=True,
  save_steps=500,
  eval_steps=500,
  logging_steps=500,
  learning_rate=1e-4,
  weight_decay=0.005,
  warmup_steps=1000,
  save_total_limit=2,
)

from transformers import Trainer

trainer = Trainer(
    model=model,
    data_collator=data_collator,
    args=training_args,
    compute_metrics=compute_metrics,
    train_dataset=timit_prepared["train"],
    eval_dataset=timit_prepared["test"],
    tokenizer=processor.feature_extractor,
)

# Training will take between 90 and 180 minutes depending on the GPU 
trainer.train()
