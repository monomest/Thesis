# ---------------------------------------------------------
# myST_prep.py
# Purpose: Prepares MyST data for wav2vec2 fine tuning.
#          Replaces noise tags with <UNK> 
#          Assumes MyST has data prep documents for kaldi.
# Author: Renee Lu, 2021
# ---------------------------------------------------------

# ------------------------------------------
#          Importing libraries
# ------------------------------------------

# For counting for duplicates
import collections
from collections import Counter
# For dataframes
import pandas as pd
import numpy as np
# For regex
import re
# For checking files
import os.path
# For dealing with audio files
import soundfile as sf
# For file system related methods
from pathlib import PurePath
# For printing filepath
import os
# For text normalisation
import unicodedata
# For converting numbers into words
from num2words import num2words

# ------------------------------------------
print('Running: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#          Setting file paths
# ------------------------------------------

# Base path to required files
base = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/kaldi_datafiles/"
# Base path to MyST directory in chacmod directory
base_chacmod = "/srv/scratch/chacmod/MyST/"
# Base path to output
base_output = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/"
# Path to existing myST_data.csv
myST_fp_existing = base_output + "myST_data_split.csv"

# Paths for existing input data prep files
wavlist_fp = base + "wavFileList.scp"
trans_fp = base + "transcripts.txt"
words_fp = base + "list_words"
tags_fp = base + "list_noise_tags"
badFiles_fp = base + "badFiles"

# Paths for output files
myST_fp = base_output + "myST_data_split_unk.csv"

# ------------------------------------------
#    Extracting information from files
# ------------------------------------------
print("\n------> Extracting information from files... ------------------------\n")

# Use wavFileList.scp: Get recording IDs and filepaths
# filepath: 
# myst-v0.3.0-171fbda/corpora/myst/data/997472/myst_997472_2010-11-01_00-00-00_ME_2.2/
#   myst_997472_2010-11-01_00-00-00_ME_2.2_002.wav
# -------------------------------------------^ recording ID
def getFilepaths(wavlist_fp):
    with open(wavlist_fp, "r") as f:
        lines=f.readlines()
        record_id_wav = []
        filepath = []
        for line in lines:
            # Get recording ID
            as_list = line.split("/")
            id_tmp = as_list[6]
            id_tmp = id_tmp.replace("\n", "")
            id_tmp = id_tmp.replace(".wav","")
            record_id_wav.append(id_tmp)
            # Get filepath by adding base filepath and removing new line
            filepath_tmp = base_chacmod + line
            filepath.append(filepath_tmp.replace("\n", ""))
    f.close()
    return record_id_wav, filepath

# Use transcripts.txt: Get recording IDs and original transcription
# <recording ID> <transcription>
def getTrans(trans_fp):
    with open(trans_fp, "r") as f:
        lines=f.readlines()
        record_id_trans = []
        trans_og = []
        for line in lines:
            # Split lines by " ", for only the 1st space
            as_list = line.split(" ", 1)
            # Get recording ID
            record_id_trans.append(as_list[0])
            # Get original transcription
            trans_og.append(as_list[1])
    f.close()
    return record_id_trans, trans_og

def readCSV(fp):
    # Read the csv file as dataframe, and as string type
    # so that speaker IDs retain leading zeros
    df = pd.read_csv(fp, dtype={'spkr_id': object})
    # Convert duration column to float64
    df["duration"] = df["duration"].apply(pd.to_numeric)
    return df

record_id_wav, filepath = getFilepaths(wavlist_fp)
record_id_trans, trans_og = getTrans(trans_fp)
myST_existing = readCSV(myST_fp_existing)

print("------> List of unique characters in transcription...")
print(sorted(list({l for word in trans_og for l in word})))

print("SUCCESS: extracted all data information.")

# ------------------------------------------
#   Clean transcription
# ------------------------------------------
def cleanTranscript(trans_og):
    trans_clean = []
    for text in trans_og:
        # Normalise
        text_tmp = unicodedata.normalize("NFKD", text)
        # Handle special words and tags that occur in words list
        # -- Words -- 
        text_tmp = text_tmp.replace("(())", " ")
        text_tmp = text_tmp.replace("(*)", " ")
        text_tmp = text_tmp.replace("[]", " ")
        text_tmp = text_tmp.replace("12345", "one two three four five")
        text_tmp = text_tmp.replace("0-19-1-9-2-5-3-5-4-5-5-3",
                    "zero nineteen one nine two five three five four five five three")
        text_tmp = text_tmp.replace("1220", "twelve twenty")
        text_tmp = text_tmp.replace("15ml", "fifteen milliliters")
        text_tmp = text_tmp.replace("17gms", "seventeen grams")
        text_tmp = text_tmp.replace("20gms", "twenty grams")
        text_tmp = text_tmp.replace("220", "two twenty")
        text_tmp = text_tmp.replace("300Mg", "three hundred milligrams")
        text_tmp = text_tmp.replace("50g", "fifty grams")
        text_tmp = text_tmp.replace("75ml", "seventy five milliliters")
        text_tmp = text_tmp.replace("75mm", "seventy five millimeters")
        text_tmp = text_tmp.replace("(8)", "you hear")
        text_tmp = text_tmp.replace("(80)", "i noticed that")
        text_tmp = text_tmp.replace("+88+", "eighty eight eighty eight eighty eight")
        text_tmp = text_tmp.replace("[00:00:01]", " ")
        text_tmp = text_tmp.replace("Speaker 2:", " ")
        text_tmp = text_tmp.replace("+A47:A60", " ")
        # -- Tags --
        text_tmp = text_tmp.replace("<Ah>", "ah")
        text_tmp = text_tmp.replace("<ah umm>", "ah umm")
        text_tmp = text_tmp.replace("<Ah umm>", "ah umm")
        text_tmp = text_tmp.replace("<At>", "at")
        text_tmp = text_tmp.replace("<fsssssshhh>", "fsssssshhh")
        text_tmp = text_tmp.replace("<umm>", "umm")
        unk_list = ["<indiscernible>","<Indiscernible>", "<indiscernibley>",
                    "<noise>","<Noise>","<nosie>","side_s[eech>",
                    "<side signal>","<side speaker>","<side Speaker>",
                    "<Side speaker>","<Side Speaker>","<side speakers>",
                    "<Side speakers>","<'side_speech>","<side _ speech>",
                    "<side _speech>","<side speech>","<side_ speech>",
                    "<side_speech>","<side-speech>","<side Speech>",
                    "< Side speech>","<Side speech>","<Side_ speech>",
                    "<Side_speech>","< Side Speech>","<Side Speech>",
                    "<sied_speech>","<singing>","< Singing>","<Singing>",
                    "<unaudible>","<Unclear audio>","<unclear voice>",
                    "<unclear voice >","< Unclear voice>","<Unclear voice>",
                    "<whisper>","<Whisper>"]
        for noise_tag in unk_list:
            text_tmp = text_tmp.replace(noise_tag, "'UNK'")
        # Remove all other tags
        text_tmp = re.sub('<[^>]*>', '', text_tmp)
        # Replace "-" with a space
        text_tmp = text_tmp.replace("-", " ")
        # Add a space whenever number is adjacent to non-number
        text_tmp = re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", text_tmp)
        # Remove or replace all special characters
        text_tmp = text_tmp.replace("‘", "'")
        text_tmp = text_tmp.replace("’", "'")
        chars_to_ignore_regex = '[\<\[\]\–\…\)\?\/\-\*\:\&\>\.\;\(\+\_\,]'
        text_tmp = re.sub(chars_to_ignore_regex, " ", text_tmp)
        #Split into text and numbers
        text_list = re.split('(\d+)',text_tmp) 
        # Replace numbers with words
        for index, part in enumerate(text_list):
            if part.isnumeric():
                text_list[index] = num2words(part)
        text_tmp = ''.join(text_list)
        # Replace 'UNK' with <UNK>
        text_tmp = text_tmp.replace("'UNK'", "<UNK>")
        # Replace - and , with space again
        text_tmp = text_tmp.replace("-", " ")
        text_tmp = text_tmp.replace(",", " ")
        # Remove extra whitespace between words
        text_tmp = re.sub(' +', ' ', text_tmp)
        # Remove leading and trailing whitespaces
        text_tmp = text_tmp.strip()
        # Lowercase
        text_tmp = text_tmp.lower()
        # Append to trans list
        trans_clean.append(text_tmp)
    return trans_clean

trans_clean = cleanTranscript(trans_og)

print("SUCCESS: Cleaned transcript.")
print("------> List of unique characters in cleaned transcription...")
print(sorted(list({l for word in trans_clean for l in word})))

# ------------------------------------------
#        Putting data into dataframe
# ------------------------------------------
print("\n------> Putting data into dataframe... -------------------------------\n")
# Put filepath, transcription and duration 
# into dataframe.
# Remove rows where there is no spoken words
# Remove rows where wav file doesn't exist
# |-----------|---------------|----------|----------|
# |  filepath | transcription | duration | spkr id  |
# |-----------|---------------|----------|----------|
# |    ...    |     ...       |  ..secs  |  ......  |
# |    ...    |     ...       |  ..secs  |  ......  |

myST_df = pd.DataFrame(
        {'recordingID': record_id_wav,
         'filepath': filepath,
         })

trans_df = pd.DataFrame(
        {'recordingID': record_id_trans,
         'transcription_original': trans_og,
         'transcription_clean': trans_clean,
         'transcribed': True
        })

myST_df = pd.merge(myST_df, trans_df, on='recordingID', how="outer")  

# Copy new transcription to existing dataframe with old transcription
myST_existing['transcription_clean'] = myST_df['transcription_clean']          

# ------------------------------------------
#      Save dataframe to csv file
# ------------------------------------------
print("\n------> Saving dataframe to csv file... ------------------------------\n")
myST_existing.to_csv(myST_fp,index=False)
print("SUCCESS: Saved MyST dataframe to csv file", myST_fp)
print("Dataframe length:", len(myST_existing))
