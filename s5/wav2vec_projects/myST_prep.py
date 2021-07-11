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

# ------------------------------------------
print('Running: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#          Setting file paths
# ------------------------------------------

# Paths for existing kaldi data prep files
wavscp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/kaldi_datafiles/wav.scp"
text = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/kaldi_datafiles/text"
# Path to save myST dataframe
myST_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_dataframe.csv"

# ------------------------------------------
#    Extracting information from files
# ------------------------------------------
print("\n------> Extracting information from files... ------------------------\n")
# Use wav.scp: Get recording IDs and filepaths
with open(wavscp,"r") as f:
    lines=f.readlines()
    record_id_wav = []
    filepath = []
    for l in lines:
        as_list = l.split(" ")
        record_id_wav.append(as_list[0])
        # Remove new lines from filepath
        filepath.append(as_list[1].replace("\n", ""))
f.close()   
#print(record_id[0:5])
#print(filepath[0:5])

# Use text: Get recording IDs and transcription
with open(text, "r") as f:
    lines=f.readlines()
    record_id_text = []
    transcription = []
    for L in lines:
        # Split lines by " ", for only the 1st space
        as_list = L.split(" ", 1)
        record_id_text.append(as_list[0])
        # Remove all speech tags and new lines from transcription
        # @hes @unk_en @noise @laughs @sil side_speech no_signal "no signal"
        as_list[1] = as_list[1].replace("@hes", "").replace("@unk_en", "")
        as_list[1] = as_list[1].replace("@noise", "").replace("laughs", "")
        as_list[1] = as_list[1].replace("side_speech", "")
        as_list[1] = as_list[1].replace("no_signal", "").replace("no signal", "")
        as_list[1] = as_list[1].replace("@sil", "").replace("\n", "")
        as_list[1] = as_list[1].replace("@", "")
        # Remove extra whitespace between words
        as_list[1] = re.sub(' +', ' ', as_list[1])
        # Remove leading and trailing whitespaces
        transcription.append(as_list[1].strip())
        # Remove any other special characters ,.?!;:
        chars_to_ignore_regex = '[\,\?\.\!\-\;\:\"]'
        as_list[1] = re.sub(chars_to_ignore_regex, '', as_list[1]).lower()

f.close()
#print(record_id_wav[0:5])
#print(record_id_text[0:5])
#print(transcription[0:5])
print("SUCCESS: extracted information from wav.scp and text.")

# ------------------------------------------
#             Verifying data
# ------------------------------------------
print("\n------> Verifying data... --------------------------------------------\n")
# Checking data
# Check recording IDs between files match up
if record_id_wav == record_id_text:
    print("VERIFICATION SUCCESS: recording ID's match up.")
    
else :
    print("ERROR: recording ID's for wav.scp and text don't align.")
# Check there are no duplicated recording file paths
if len(record_id_wav) == len(set(record_id_wav)):
   print("VERIFICATION SUCCESS: recording ID's are unique.")
else :
    print("ERROR: recording ID's for wav.scp not unique.")
    counts = collections.Counter(record_id_wav)
    list(counts)
    [i for i in counts if counts[i]>1]

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
myST = pd.DataFrame(
        {'filepath': filepath,
         'transcription': transcription
         })
# Remove rows where there is no transcription
# i.e. no spoken words, only silence or speech tags
myST = myST[myST.transcription != None]
myST = myST[myST.transcription != ""]
# Remove rows where the wav file does not exist
filepath = myST['filepath'].tolist()
print("--> Dropping rows where the wav file does not exist...")
fileExists = list(map(lambda fp: os.path.isfile(fp), filepath))
# Add column 'file_exist' into dataframe
myST['file_exist'] = fileExists
# Keep only rows where file_exist is True
myST = myST[myST.file_exist == True]
# Drop the file_exist column from dataframe
myST.drop(columns ='file_exist', inplace=True)

# Get duration of each wav file
filepath = myST['filepath'].tolist()
print('--> Getting duration in seconds for each audio file...')
length = list(map(lambda fp: len(sf.SoundFile(fp))/sf.SoundFile(fp).samplerate, filepath))
myST['duration'] = length

# Get speaker id of each wav file
# using a map(...) function and lambda function
# Speaker ID = ------------------------------------------------------v
# /srv/scratch/chacmod/MyST/myst-v0.3.0-171fbda/corpora/myst/data/012019/myst_012019_2013-11-13_08-56-43_MX_1.2/myst_012019_2013-11-13_08-56-43_MX_1.2_003.wav
print("--> Getting speaker id for each wav file...")
spkr_id = list(map(lambda fp: PurePath(fp).parts[9], filepath))
myST['spkr_id'] = spkr_id
# Save spkr_id as string so leading zeros are not removed
myST['spkr_id'] = myST['spkr_id'].astype('str')

# ------------------------------------------
#      Save dataframe to csv file
# ------------------------------------------
print("\n------> Saving dataframe to csv file... ------------------------------\n")
myST.to_csv(myST_fp,index=False)
print("SUCCESS: Saved MyST dataframe to csv file", myST_fp)
print("Dataframe length:", len(myST))
