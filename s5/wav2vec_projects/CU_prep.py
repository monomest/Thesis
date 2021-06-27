# ---------------------------------------------------------
# CU_test_prep.py
# Purpose: Prepares CU test data for wav2vec2 fine tuning. 
#          Assumes CU has data prep documents for kaldi.
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

# ------------------------------------------
#          Setting file paths
# ------------------------------------------

# Paths for existing kaldi data prep files
wavscp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/local/data/test_CU/wav.scp"
text = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/local/data/test_CU/text"
# Path to save CU dataframe
CU_test_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/CU_test_dataframe.csv"

# ------------------------------------------
#    Extracting information from files
# ------------------------------------------

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
        # <SPOKEN_NOISE> <NOISE> !SIL
        as_list[1] = as_list[1].replace("<SPOKEN_NOISE>", "").replace("<NOISE>", "")
        as_list[1] = as_list[1].replace("!SIL", "").replace("<", "")
        as_list[1] = as_list[1].replace(">", "").replace("\n", "")
        as_list[1] = as_list[1].replace("_", "").replace("!", "")
        # Remove extra whitespace between words
        as_list[1] = re.sub(' +', ' ', as_list[1])
        # Remove leading and trailing whitespaces
        transcription.append(as_list[1].strip())
        # Remove any other special characters ,.?!;: and to lowercase
        chars_to_ignore_regex = '[\,\?\.\!\-\;\:\"]'
        as_list[1] = re.sub(chars_to_ignore_regex, '', as_list[1].lower() + " ")

f.close()
#print(record_id_wav[0:5])
#print(record_id_text[0:5])
#print(transcription[0:5])

# ------------------------------------------
#             Verifying data
# ------------------------------------------

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

# Put filepath and transcription into dataframe
# |-----------|---------------|
# |  filepath | transcription |
# |-----------|---------------|
# |    ...    |     ...       |
# |    ...    |     ...       |
CU_test = pd.DataFrame(
        {'filepath': filepath,
         'transcription': transcription
         })
# Remove rows where there is no transcription
# i.e. no spoken words, only silence or speech tags
CU_test = CU_test[CU_test.transcription != None]
CU_test = CU_test[CU_test.transcription != ""]

# ------------------------------------------
#      Save dataframe to csv file
# ------------------------------------------
CU_test.to_csv(CU_test_fp,index=False)
print("SUCCESS: Saved CU test dataframe to csv file ", CU_test_fp)
print("Length:", len(CU_test))
