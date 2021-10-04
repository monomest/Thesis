# ---------------------------------------------------------
# myST_prep.py
# Purpose: Prepares MyST data for wav2vec2 fine tuning. 
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

# Paths for existing input data prep files
wavlist_fp = base + "wavFileList.scp"
trans_fp = base + "transcripts.txt"
words_fp = base + "list_words"
tags_fp = base + "list_noise_tags"
badFiles_fp = base + "badFiles"

# Paths for output files
myST_fp = base_output + "myST_data.csv"

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

# Use list_noise_tags: Get all tags in the transcription
def getTags(tags_fp):
    with open(tags_fp, "r") as f:
        lines=f.readlines()
        tags = []
        for line in lines:
            # Split lines by " ", for only the 1st space
            as_list = line.split(" ", 1)
            # Get the tags
            tags.append(as_list[1])
    f.close()
    return tags

# Use badFiles: Get all the filepaths of bad files
def getBadFiles(badFiles_fp):
    with open(badFiles_fp, "r") as f:
        lines=f.readlines()
        badFiles = []
        for line in lines:
            # Get filepath and remove ending new line
            badFile_tmp = base_chacmod + line
            badFiles.append(badFile_tmp.replace("\n", ""))
    f.close()
    return badFiles

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

record_id_wav, filepath = getFilepaths(wavlist_fp)
tags = getTags(tags_fp)
badFiles = getBadFiles(badFiles_fp)
record_id_trans, trans_og = getTrans(trans_fp)

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
        # Remove all other tags e.g. <Noise>
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
#             Verifying data
# ------------------------------------------
print("\n------> Verifying data... --------------------------------------------\n")
# Get transcriptions without corresponding wav files
trans_without_wav = [x for x in record_id_trans if x not in record_id_wav]
print("Number of transcriptions without corresponding wav files:",
       len(trans_without_wav))
print("Transcriptions without corresponding wav files:", trans_without_wav)

# Checking number of transcribed and untranscribed samples
print("Total Samples (filepath):", len(filepath))
print("Total Samples (record_id_wav):", len(filepath))
print("Transcribed utterances (record_id_trans)", len(record_id_trans))
print("Transcribed utterances (trans_og)", len(trans_og))
#print("Transcribed utterances (trans_clean)", len(trans_clean))

# Check there are no duplicated recording file paths
def checkDuplicate(record_id):
    if len(record_id) == len(set(record_id)):
        print("VERIFICATION SUCCESS: recording ID's are unique.")
    else :
        print("ERROR: recording ID's for wav.scp not unique.")
        counts = collections.Counter(record_id)
        list(counts)
        [i for i in counts if counts[i]>1]

checkDuplicate(record_id_wav)
checkDuplicate(record_id_trans)

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

# Set NaN in 'transcribed' column as False
myST_df['transcribed'] = df['transcribed'].fillna(False)

# Flag rows where the wav file does not exist
# i.e. set has_audio_file = False
print("\n------> Flagging rows where wav file does not exist\n")
print("has_audio_file = False")
filepath_tmp = myST_df['filepath'].tolist()
fileExists = [os.path.isfile(fp) if fp == fp else False for fp in filepath_tmp]
myST_df['has_audio_file'] = fileExists

# Flag rows where file is transcribed but
# the audio contains no speech e.g. only silence, noise...
# i.e. no spoken words, only silence or speech tags
print("\n------> Flagging rows where file is transcribed but has no speech\n")
print("has_speech_in_audio = False")
myST_df['has_speech_in_audio'] = np.nan
myST_df.loc[(myST_df.has_audio_file == True) & (myST_df.transcribed == True) 
         & ((myST_df.transcription_clean == None) | (myST_df.transcription_clean == "")), 
         'has_speech_in_audio'] = False
myST_df.loc[(myST_df.has_audio_file == True) & (myST_df.transcribed == True) 
         & ((myST_df.transcription_clean != None) & (myST_df.transcription_clean != "")), 
         'has_speech_in_audio'] = True

# Get duration of each wav file
print("\n------> Getting duration in seconds of each wav file\n")
print("duration")
def getDuration(fp, fileExists):
    if fileExists == True:
        duration = len(sf.SoundFile(fp))/sf.SoundFile(fp).samplerate
    else:
        duration = np.nan
    return duration
myST_df['duration'] = myST_df.apply(lambda x: getDuration(x['filepath'], 
                                    x['has_audio_file']), axis=1)

# Get speaker id of each wav file
# using a map(...) function and lambda function
# Speaker ID = --------v
# recordingID = myst_997472_2010-11-01_00-00-00_ME_2.2_007
# Save spkr_id as string so leading zeros are not removed
print("\n------> Getting speaker id of each file\n")
print("spkr_id")
myST_df['spkr_id'] = myST_df['recordingID'].str.split("_").str[1]

# Flag if recording is usable or not
# Usable = False if:
#   filepath in badFiles OR
#   has_audio_file != True OR
#   has_speech_in_audio != True
print("\n------> Checking if recording is usable or not\n")
print("usable")
def checkUsable(fp, has_audio_file, has_speech_in_audio, transcribed, badFiles):
    if fp in badFiles:
        usable = False
    elif has_audio_file != True:
        usable = False
    elif transcribed == True and has_speech_in_audio != True:
        usable = False
    else:
        usable = True
    return usable
myST_df['usable'] = myST_df.apply(lambda x: checkUsable(x['filepath'], 
                                  x['has_audio_file'], x['has_speech_in_audio'], 
                                  x['transcribed'], badFiles), axis=1)

# ------------------------------------------
#      Save dataframe to csv file
# ------------------------------------------
print("\n------> Saving dataframe to csv file... ------------------------------\n")
myST_df.to_csv(myST_fp,index=False)
print("SUCCESS: Saved MyST dataframe to csv file", myST_fp)
print("Dataframe length:", len(myST_df))
