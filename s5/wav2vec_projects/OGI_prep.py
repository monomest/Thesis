# ---------------------------------------------------------
# OGI_prep.py
# Purpose: Prepares OGI data for wav2vec2 fine tuning. 
#          Assumes OGI has data prep documents for kaldi.
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
wavscp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/kaldi_datafiles/wav.scp"
text = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/kaldi_datafiles/text"
# Path to save OGI dataframe
OGI_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_dataframe.csv"
# Path to save recording IDs
recordID_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_recordID.csv"

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
print(record_id_wav[0:5])
print(filepath[0:5])

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
        # OLD: @ns <unk> @breath @sil @laugh @fp @ct @cough ] -
        # NEW: <NOISE> <SPOKEN_NOISE> !SIL
        as_list[1] = as_list[1].replace("<NOISE>", "").replace("!SIL", "")
        as_list[1] = as_list[1].replace("<SPOKEN_NOISE>", "")
        # Remove extra whitespace between words
        as_list[1] = re.sub(' +', ' ', as_list[1])
        # Remove leading and trailing whitespaces
        transcription.append(as_list[1].strip())
        # Remove any other special characters ,.?!;:
        chars_to_ignore_regex = '[\,\?\.\!\-\;\:\"]'
        as_list[1] = re.sub(chars_to_ignore_regex, '', as_list[1]).lower()

f.close()
print(record_id_wav[0:5])
print(record_id_text[0:5])
print(transcription[0:5])
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
    print("WARNING: recording ID's for wav.scp and text don't align.")
    set_difference = set(record_id_wav) - set(record_id_text)
    list_difference = list(set_difference)
    print(list_difference)
    recordID = pd.DataFrame(
                  {'record_id_wav': record_id_wav,
                    'record_id_text': record_id_text,
                  })
    recordID.to_csv(recordID_fp,index=False)
    print("See recording IDs at", recordID_fp)
# Check there are no duplicated recording file paths
if len(record_id_wav) == len(set(record_id_wav)):
   print("VERIFICATION SUCCESS: recording ID's are unique.")
else :
    print("WARNING: recording ID's for wav.scp not unique.")
    counts = collections.Counter(record_id_wav)
    list(counts)
    [i for i in counts if counts[i]>1]

# ------------------------------------------
#        Putting data into dataframe
# ------------------------------------------
print("\n------> Putting data into dataframe... -------------------------------\n")
# Put filepath, transcription and duration 
# into dataframe.
# Replace old filepath with new filepath
# Clean up transcription i.e. remove tags
# Remove rows where there is no spoken words
# Remove rows where wav file doesn't exist
# Get all unique characters from transcription
# |-----------|---------------|----------|----------|
# |  filepath | transcription | duration | spkr id  |
# |-----------|---------------|----------|----------|
# |    ...    |     ...       |  ..secs  |  ......  |
# |    ...    |     ...       |  ..secs  |  ......  |
OGI = pd.DataFrame(
        {'filepath': filepath,
         'transcription': transcription
         })
# Replace old filepath with new filepath
# old pattern: /srv/scratch/z5160268/2020_TasteofResearch/OREGON_Kids_Corpus/speech/scripted/01/3/ks112/ks1128j0.wav
# new pattern: /srv/scratch/chacmod/OGI/speech/spontaneous/04/3/ks43z/ks43zxx0.wav
# i.e. replace "srv/scratch/z5160268/2020_TasteofResearch/OREGON_Kids_Corpus" with "/srv/scratch/chacmod/OGI"
OGI['filepath'] = OGI['filepath'].str.replace('srv/scratch/z5160268/2020_TasteofResearch/OREGON_Kids_Corpus','srv/scratch/chacmod/OGI')  

# Remove all speech tags and new lines from transcription
# <NOISE> <SPOKEN_NOISE> !SIL ] <BS: > <BR
OGI['transcription'] = OGI['transcription'].str.replace('<NOISE>', '')
OGI['transcription'] = OGI['transcription'].str.replace('<SPOKEN_NOISE', '')
OGI['transcription'] = OGI['transcription'].str.replace('!SIL', '')
OGI['transcription'] = OGI['transcription'].str.replace(']', '')
OGI['transcription'] = OGI['transcription'].str.replace('-', ' ')
OGI['transcription'] = OGI['transcription'].str.replace('<BS:', '')
OGI['transcription'] = OGI['transcription'].str.replace('>', '')
OGI['transcription'] = OGI['transcription'].str.replace('<BR', '')

# Remove extra whitespace between words
OGI['transcription'] = OGI['transcription'].str.replace('\s+', ' ', regex=True)
# Remove leading and trailing whitespaces
OGI['transcription'] = OGI['transcription'].str.strip()
# Remove special characters
def remove_char(trans):
    chars_to_ignore_regex = '[\,\?\.\!\-\;\:\"]'
    return re.sub(chars_to_ignore_regex, '', trans).lower()
OGI['transcription'] = OGI['transcription'].apply(remove_char)

# Remove rows where there is no transcription
# i.e. no spoken words, only silence or speech tags
OGI = OGI[OGI.transcription != None]
OGI = OGI[OGI.transcription != ""]

# Remove rows where the wav file does not exist
filepath = OGI['filepath'].tolist()
print("--> Dropping rows where the wav file does not exist...")
fileExists = list(map(lambda fp: os.path.isfile(fp), filepath))

# Add column 'file_exist' into dataframe
OGI['file_exist'] = fileExists
# Keep only rows where file_exist is True
OGI = OGI[OGI.file_exist == True]
# Drop the file_exist column from dataframe
OGI.drop(columns ='file_exist', inplace=True)

# Get duration of each wav file
filepath = OGI['filepath'].tolist()
print('--> Getting duration in seconds for each audio file...')
length = list(map(lambda fp: len(sf.SoundFile(fp))/sf.SoundFile(fp).samplerate, filepath))
OGI['duration'] = length

# Get speaker id of each wav file
# using a map(...) function and lambda function
# Speaker ID = -----------------------------------v
# /srv/scratch/chacmod/OGI/speech/scripted/04/4/ks406/ks406360.wav
print("--> Getting speaker id for each wav file...")
spkr_id = list(map(lambda fp: PurePath(fp).parts[9], filepath))
OGI['spkr_id'] = spkr_id
# Save spkr_id as string so leading zeros are not removed
OGI['spkr_id'] = OGI['spkr_id'].astype('str')

# Get all the unique characters in the transcription
print("--> Getting list of unique characters in the transcription...")
print("Length:",len(set(OGI.transcription.sum())))
print(set(OGI.transcription.sum()))

# ------------------------------------------
#           Describing dataset
# ------------------------------------------
print("\n------> Describing dataset... ----------------------------------------\n")
print("Duration (in seconds):")
print(OGI.duration.describe())
print("Total hours:", OGI['duration'].sum()/(60*60))

# ------------------------------------------
#      Save dataframe to csv file
# ------------------------------------------
print("\n------> Saving dataframe to csv file... ------------------------------\n")
OGI.to_csv(OGI_fp,index=False)
print("SUCCESS: Saved OGI dataframe to csv file", OGI_fp)
print("Dataframe length:", len(OGI))
