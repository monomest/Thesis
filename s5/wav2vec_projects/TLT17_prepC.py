# TLT17_splitC.py
# Purpose: Split the transcribed TLT data 
#          for Thesis C
# Author: Renee Lu, 2021

# ------------------------------------------
#         Importing libraries
# ------------------------------------------
# For dataframes
import pandas as pd
import numpy as np
# For printing filepath
import os
# For reading files
from pathlib import Path
# For regex
import re
# For dealing with audio files
import soundfile as sf

# ------------------------------------------
print('\nRunning: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
# Setting maximum seconds duration
# ------------------------------------------
print("\n------> Setting duration limit... ------------------------------------ \n")
# Maximum seconds
limit = 15.40
print("--> Fine-tuning files limited to less than or equal to", limit, "seconds.")

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
fp_filepaths_train = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/kaldi_datafiles/train_all_files.txt"
fp_trans_train = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/kaldi_datafiles/TLT2017train.sup"
fp_filepaths_dev = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/kaldi_datafiles/dev_all_files.txt"
fp_trans_dev = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/kaldi_datafiles/TLT2017dev.sup"
print("Input files...")
fp_list = [fp_filepaths_train, fp_trans_train, fp_filepaths_dev, fp_trans_dev]
for fp in fp_list:
    print(fp)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT17_data_split.csv"
pretrain_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT17_data_pretrain.csv"
finetune_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT17_data_finetune.csv"
ignore_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT17_data_ignore.csv"

output_fp = [out_fp, pretrain_fp, finetune_fp, ignore_fp]

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
# Reading in filepaths as list
fp_filepaths_all = [fp_filepaths_train, fp_filepaths_dev]
filepaths_list = []
for fp in fp_filepaths_all:
    with open(fp) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    filepaths_list = filepaths_list + lines

# Reading in transcription as dataframe
fp_trans_list = [fp_trans_train, fp_trans_dev]
trans_df_list = []
for fp in fp_trans_list:
    df = pd.read_csv(fp, sep="\t",
                     names=['recordingID', 'transcription_original'], header=None)
    trans_df_list.append(df)

trans_df = pd.concat(trans_df_list, ignore_index=True)

# Get all the unique words in transcription
unique_words = set()
trans_df['transcription_original'].str.lower().str.split().apply(unique_words.update)
print("Unique words in original transcription:")
print("\n".join(sorted(unique_words)))

# ------------------------------------------
#       Getting transcription
# ------------------------------------------
dNoiseTag2Symb = {
                    "<unk-de>": "<UNK>",
                    "<unk-it>": "<UNK>",
                    "@bgk": " ",
                    "@bkg": " ",
                    "@br": " ",
                    "@breath": " ",
                    "@cough": " ",
                    "@laugh": " ",
                    "@noise": " ",
                    "@ns": " ",
                    "@sil": " ",
                    "@voice": "<UNK>",
                    "@voices": "<UNK>",
                    "à": "<UNK>",
                    "è": "<UNK>", 
                    "ò": "<UNK>"
                    }
def cleanTranscription(row):
    trans = row['transcription_original']
    if trans == trans:
        # Replace noise tags
        for noiseTag, replacement in dNoiseTag2Symb.items():
            trans = trans.replace(noiseTag, replacement)
        # Remove or replace all special characters
        trans = trans.replace("-", " ")
        trans = trans.replace("‘", "'")
        trans = trans.replace("’", "'")
        chars_to_ignore_regex = '[\<\[\]\–\…\)\?\/\-\*\:\&\>\.\;\(\+\_\,\@]'
        trans = re.sub(chars_to_ignore_regex, " ", trans)
        # Replace UNK with <unk>
        trans = trans.replace("UNK", "<unk>")
        # Remove extra whitespace between words
        trans = re.sub(' +', ' ', trans)
        # Remove leading and trailing whitespaces
        trans = trans.strip()
    else:
        trans = np.nan
    return trans

trans_df['transcription_clean'] = trans_df.apply(lambda row: 
                                    cleanTranscription(row), axis=1)
print("Unique characters in cleaned transcription:")
print(sorted(set(trans_df.transcription_clean.sum())))

# ------------------------------------------
#          Get recording ID
# ------------------------------------------
# Get recording ID ---------------------------------------------------------------------v
# /srv/scratch/chacmod/TLT/Dataset/TLT2020challenge/audio/TLT2017train/en_6_8_101/2020117_en_6_8_101.wav
recordID = [fp.split("/")[10].split(".")[0] for fp in filepaths_list]

# ------------------------------------------
#      Construct dataframe
# ------------------------------------------
TLT_df = pd.DataFrame(
            {'recordingID': recordID,
             'filepath': filepaths_list
             })

TLT_df = pd.merge(TLT_df, trans_df, on='recordingID', how="outer")

print("NaNs in each column:")
print("recordingID: ", TLT_df['recordingID'].isnull().sum())
print("filepath: ", TLT_df['filepath'].isnull().sum())
print("transcription_clean: ", TLT_df['transcription_clean'].isnull().sum())
print("transcription_original: ", TLT_df['transcription_original'].isnull().sum())
# ------------------------------------------
#          Data checks
# ------------------------------------------
# Check if has audio file
# Flag rows where the wav file does not exist
# i.e. set has_audio_file = False
print("\n------> Flagging rows where wav file does not exist\n")
print("has_audio_file = False")
fileExists = [os.path.isfile(fp) if fp == fp else False for fp in filepaths_list]
TLT_df['has_audio_file'] = fileExists

# Check if speech is present in audio file
# Flag rows where file is transcribed but
# the audio contains no speech e.g. only silence, noise...
# i.e. no spoken words, only silence or speech tags
print("\n------> Flagging rows where file is transcribed but has no speech\n")
print("has_speech_in_audio = False")
TLT_df['has_speech_in_audio'] = np.nan
TLT_df.loc[(TLT_df.has_audio_file == True) &
           ((TLT_df.transcription_clean == None) | 
            (TLT_df.transcription_clean == "") | 
            (TLT_df.transcription_clean == "<unk>")),
           'has_speech_in_audio'] = False
TLT_df.loc[(TLT_df.has_audio_file == True) &
            ((TLT_df.transcription_clean != None) &
             (TLT_df.transcription_clean != "<unk>") &
             (TLT_df.transcription_clean != "")),
           'has_speech_in_audio'] = True

# Flag if recording is usable or not
# Usable = False if:
#   has_audio_file != True OR
#   has_speech_in_audio != True
print("\n------> Checking if recording is usable or not\n")
print("usable")
def checkUsable(fp, has_audio_file, has_speech_in_audio):
    if has_audio_file != True:
        usable = False
    elif has_speech_in_audio != True:
        usable = False
    else:
        usable = True
    return usable
TLT_df['usable'] = TLT_df.apply(lambda x: checkUsable(x['filepath'],
                                  x['has_audio_file'], 
                                  x['has_speech_in_audio']), axis=1)
# ------------------------------------------
#      Getting duration of audio
# ------------------------------------------
# Get duration of each wav file
print("\n------> Getting duration in seconds of each wav file\n")
print("duration")
def getDuration(fp, fileExists):   
    if fileExists == True:
        duration = len(sf.SoundFile(fp))/sf.SoundFile(fp).samplerate
    else:
        duration = np.nan
    return duration
TLT_df['duration'] = TLT_df.apply(lambda x: getDuration(x['filepath'],
                                    x['has_audio_file']), axis=1)

# ------------------------------------------
#        Splitting
# ------------------------------------------
def splitData(usable, duration, limit):
    if usable != True:
        split = "ignore"
    else:
        if duration <= limit:
            split = "finetune"
        else:
            split = "pretrain"
    return split
TLT_df['set'] = TLT_df.apply(lambda x: splitData(x['usable'], 
                            x['duration'], limit), axis=1)

# Creating set dataframes
TLT_finetune = TLT_df[(TLT_df['set'] == "finetune")]
TLT_pretrain = TLT_df[(TLT_df['set'] == "pretrain")]
TLT_ignore = TLT_df[(TLT_df['set'] == "ignore")]

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
TLT_df.to_csv(out_fp,index=False)
TLT_pretrain.to_csv(pretrain_fp, index=False)
TLT_finetune.to_csv(finetune_fp, index=False)
TLT_ignore.to_csv(ignore_fp, index=False)

for fp in output_fp:
    print("Saved:", fp)

print("Done!")

