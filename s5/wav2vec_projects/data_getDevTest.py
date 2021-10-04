# ---------------------------------------------------------
# data_prep.py
# Purpose: Gets Mostafa's dev/test split of data 
#          Assumes wav.scp file exists
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
wavscp = "/srv/scratch/chacmod/renee_thesis/test_dev_mostafa/ogi/test/wav.scp"
# Path to save data dataframe
data_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_test_wav.csv"

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

# Replace Mostafa's directory with chacmod directory

# myST
#chacmodfp = '/srv/scratch/chacmod/MyST/myst-v0.3.0-171fbda/corpora/myst/data'
#mostafafp = '/srv/scratch/z5173707/Dataset/MyST//data'

# OGI
chacmodfp = '/srv/scratch/chacmod/OGI/speech'
mostafafp = '/srv/scratch/z5173707/Dataset/OGI/speech'

filepath = [f.replace(mostafafp, chacmodfp) for f in filepath]

print("SUCCESS: extracted information from wav.scp.")

# ------------------------------------------
#             Verifying data
# ------------------------------------------
print("\n------> Verifying data... --------------------------------------------\n")
# Checking data
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
# |-----------|---------------|----------|
# |  filepath |  duration     | spkr id  |
# |-----------|---------------|----------|
# |    ...    |     ...secs   |  ...     |
# |    ...    |     ...secs   |  ...     |
data = pd.DataFrame(
        {'filepath': filepath,
         })

# Get duration of each wav file
filepath = data['filepath'].tolist()
print('--> Getting duration in seconds for each audio file...')
length = list(map(lambda fp: len(sf.SoundFile(fp))/sf.SoundFile(fp).samplerate, filepath))
data['duration'] = length

# Speaker ID = ------------------------------------------------------v
# /srv/scratch/chacmod/MyST/myst-v0.3.0-171fbda/corpora/myst/data/012019/myst_012019_2013-11-13_08-56-43_MX_1.2/myst_012019_2013-11-13_08-56-43_MX_1.2_003.wav

# Speaker ID = -----------------------------------v
# /srv/scratch/chacmod/OGI/speech/scripted/04/4/ks406/ks406360.wav

print("--> Getting speaker id for each wav file...")
spkr_id = list(map(lambda fp: PurePath(fp).parts[9], filepath))
data['spkr_id'] = spkr_id
# Save spkr_id as string so leading zeros are not removed
data['spkr_id'] = data['spkr_id'].astype('str')

# ------------------------------------------
#      Save dataframe to csv file
# ------------------------------------------
print("\n------> Saving dataframe to csv file... ------------------------------\n")
data.to_csv(data_fp,index=False)
print("SUCCESS: Saved dataframe to csv file", data_fp)
print("Dataframe length:", len(data))
