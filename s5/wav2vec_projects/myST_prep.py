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
        # @hes @unk_en @noise @laughs @sil
        as_list[1] = as_list[1].replace("@hes", "").replace("@unk_en", "")
        as_list[1] = as_list[1].replace("@noise", "").replace("laughs", "")
        as_list[1] = as_list[1].replace("@sil", "").replace("\n", "")
        as_list[1] = as_list[1].replace("@", "")
        # Remove extra whitespace between words
        as_list[1] = re.sub(' +', ' ', as_list[1])
        # Remove leading and trailing whitespaces
        transcription.append(as_list[1].strip())
        # Remove any other special characters ,.?!;:
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
    print("VERIFICATION SUCCESS: recording ID's match up!")
    
else :
    print("ERROR: recording ID's for wav.scp and text don't align!")
# Check there are no duplicated recording file paths
if len(record_id_wav) == len(set(record_id_wav)):
   print("VERIFICATION SUCCESS: recording ID's are unique!")
else :
    print("ERROR: recording ID's for wav.scp not unique!")
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
myST = pd.DataFrame(
        {'filepath': filepath,
         'transcription': transcription
         })
# Remove rows where there is no transcription
# i.e. no spoken words, only silence or speech tags
myST = myST[myST.transcription != None]
myST = myST[myST.transcription != ""]

# ------------------------------------------
#      Save dataframe to csv file
# ------------------------------------------
myST.to_csv(myST_fp,index=False)
print("SUCCESS: Saved MyST dataframe to csv file ", myST_fp)
print("Length:", len(myST))
