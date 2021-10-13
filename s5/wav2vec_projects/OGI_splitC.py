# OGI_splitC.py
# Purpose: Split the transcribed OGI data 
#          for Thesis C
# Author: Renee Lu, 2021

# ------------------------------------------
#            Information
# ------------------------------------------
#The verification codes:
#1 Good: Only the target word is said.
#2 Maybe: Target word is present, but there's other junk in the file.
#3 Bad: Target word is not said.
#4 Puff: Same as good, but w/ an air puff.

#The naming convention:
#ks000820 --> ks[1gradeid][2spkcode][2uttid]0
#gradeid: K --> 0,b 
#         1 --> 1,c 
#         2 --> 2,d 
#         3 --> 3,e 
#         4 --> 4,f 
#         5 --> 5,g 
#         6 --> 6,h 
#         7 --> 7,i 
#         8 --> 8,j 
#         9 --> 9,k 
#         10 --> a,l 
#Uttid 2 digits, check docs/all.map for scripted
#Uttid is xx for spontaneous speech

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
# For dealing with NaN
import math

# ------------------------------------------
print('\nRunning: ', os.path.abspath(__file__))
# ------------------------------------------

# ------------------------------------------
#           Setting file paths
# ------------------------------------------
print("\n------> Setting filepaths... -----------------------------------------\n")
# Dataframe in csv containing all the data information
fp_scripted = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_scripted.csv"
fp_spontaneous = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/OGI_spontaneous.csv"
fp_scripted_all = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/scripted_all_files.txt"
fp_spontaneous_all = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/spontaneous_all_files.txt"
# Mostafa's split
fp_dev = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_dev_wav.csv"
fp_test = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_test_wav.csv"
# Mappings of utterance ID and transcription
fp_map = "/srv/scratch/chacmod/OGI/docs/all.map"
# Verification files
verif_base = "/srv/scratch/chacmod/OGI/docs/"
fp_verif = [verif_base+"00-verified.txt", verif_base+"01-verified.txt", 
            verif_base+"02-verified.txt", verif_base+"03-verified.txt",
            verif_base+"04-verified.txt", verif_base+"05-verified.txt",
            verif_base+"06-verified.txt", verif_base+"07-verified.txt",
            verif_base+"08-verified.txt", verif_base+"09-verified.txt",
            verif_base+"10-verified.txt"] 

print("Input files...")
fp_list = [fp_scripted, fp_scripted_all, fp_spontaneous, fp_spontaneous_all, 
           fp_dev, fp_test, fp_map]
for fp in fp_list:
    print(fp)
for fp in fp_verif:
    print(fp)

# Output file to save to
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_split.csv"
pretrain_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_pretrain.csv"
finetune_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_finetune.csv"
dev_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_dev.csv"
test_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test.csv"
ignore_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_ignore.csv"

output_fp = [out_fp, pretrain_fp, finetune_fp, dev_fp, test_fp, ignore_fp]

# ------------------------------------------
#         Reading csv files
# ------------------------------------------
print("\n------> Reading in input files... ------------------------------------\n")
def readCSV(fp):
    # Read the csv file as dataframe, and as string type 
    # so that speaker IDs retain leading zeros
    df = pd.read_csv(fp, dtype={'spkr_id': object})
    # Convert duration column to float64
    df["duration"] = df["duration"].apply(pd.to_numeric)
    return df

def getTextFile(fp):
    # Read the text file as a list
    with open(fp, "r") as f:
        lines=f.readlines()
        files = []
        for line in lines:
            # Get filepath and remove ending new line
            files.append(line.replace("\n", ""))
    f.close()
    return files

# Get the dataframes of files that will be used
#scripted_df = readCSV(fp_scripted)
#spontaneous_df = readCSV(fp_spontaneous)

dev_df = readCSV(fp_dev)
filepath_dev = dev_df['filepath'].tolist()
print("dev:", len(filepath_dev))

test_df = readCSV(fp_test)
filepath_test = test_df['filepath'].tolist()
print("test:", len(filepath_test))

# Get all the filepaths of every file
scripted_all = getTextFile(fp_scripted_all)
print("scripted all:", len(scripted_all))
spontaneous_all = getTextFile(fp_spontaneous_all)
print("spontaneous all:", len(spontaneous_all))

# Get all the verification codes
verif_df_list = []
for fp in fp_verif:
    df = pd.read_csv(fp, delim_whitespace=True,
                     names=['filepath', 'quality_code'], header=None)
    verif_df_list.append(df)

verif_df = pd.concat(verif_df_list, ignore_index=True)
verif_df['filepath'] = verif_df['filepath'].str.replace("\.\.", "/srv/scratch/chacmod/OGI")

# ------------------------------------------
#         Getting transcription
# ------------------------------------------
#Here each tag converted to a noise symbol, the dictionary has the tag as key and tuple with two symbol values, when connected to a word and when not connected.
dNoiseTag2Symb = {
        " <asp> "  : " ", #heavily aspirated p, t, or k or puff at end of word
        " <beep> " : " ", #a beep sound
        " <blip> " : " ", #temp signal blip signal goes completely silent for a period
        " <bn> "   : " ", #Background noise
        " <br> "   : " ", #breathing noise
        " <bs> "   : "<UNK>", #background speech
        " <cough> ": " ", # cough sound
        " <ct> "   : " ", # a clear throat
        " <fp> "   : "<UNK>", #generic filled pause/false start
        " <lau> "  : " ", # ??
        " <laugh> ": "<UNK>", #laughter
        " <ln> "   : " ", # line noise
        " <long> " : " ", #elongated word
        " <ls> "   : " ", #lip smack
        " <n> "    : " ", # ??
        " <nitl> " : "<UNK>", # used for foreign language
        " <ns> "   : " ", # non-speech sound
        " <pau> "  : " ", # Silence/pause
        " <pf> "   : " ", # ??
        " <pron> " : " ", # Mispronounciation
        " <sing> " : " ", #Singing
        " <sneeze> ": " ", #Sneezing
        " <sniff> ": " ", #sniffing
        " <sp> "   : " ", #Unkown spelling
        " <tc> "   : " ", #tongue click
        " <uu> "   : "<UNK>", #unintelligible speech
        " <whisper> ": " ", #whispered speech
        " <yawn> " : " ", #yawn
        }

# Get the transcriptions mapping for scripted speech
map_df = pd.read_csv(fp_map, delim_whitespace=True, 
                     names=['uttid', 'transcript'], header=None)

# Scripted transcriptions: Map filepaths to transcriptions
# For each filepath in scripted_all, find the uttID 
# use this uttID to find corresponding transcript in map_df
uttid = [fp[-7:-5].upper() for fp in scripted_all]
scripted_all_trans = [map_df.loc[map_df['uttid'] == code, 
                      'transcript'].iloc[0] for code in uttid]

# Spontaneous transcriptions: 
spontaneous_all_trans_fp = [fp.replace("speech", "trans").replace(".wav", ".txt") 
                            for fp in spontaneous_all]
# Get all the original transcription
spontaneous_all_trans_original = []
for fp in spontaneous_all_trans_fp:
    if os.path.isfile(fp):
        txt = Path(fp).read_text()
        txt = txt.replace("\n", "")
    else:
        txt = np.nan
    spontaneous_all_trans_original.append(txt)

# ------------------------------------------
#     Get speaker ID
# ------------------------------------------
# Get speaker ID -----------------------------------v
# /srv/scratch/chacmod/OGI/trans/spontaneous/00/0/ks001/ks001xx0.wav
spontaneous_spkr_id = [fp.split("/")[9] for fp in spontaneous_all]
scripted_spkr_id = [fp.split("/")[9] for fp in scripted_all]

# ------------------------------------------
#      Construct dataframe
# ------------------------------------------
scripted_df = pd.DataFrame(
            {'filepath': scripted_all,
             'scripted': True,
             'transcription_original': scripted_all_trans,
             'transcription_clean': scripted_all_trans, 
             'spkr_id': scripted_spkr_id
             })
spontaneous_df = pd.DataFrame(
            {'filepath': spontaneous_all,
             'scripted': False,
             'transcription_original': spontaneous_all_trans_original,
             'transcription_clean': spontaneous_all_trans_original,
             'spkr_id': spontaneous_spkr_id
            })
frames = [scripted_df, spontaneous_df]
OGI_df = pd.concat(frames)
OGI_df = pd.merge(OGI_df, verif_df, on='filepath', how="outer")

# ------------------------------------------
#      Clean the transcription
# ------------------------------------------
def cleanTranscription(row):
    trans = row['transcription_original']
    if trans == trans:
        trans = (" " + trans + " ").replace(" ", "  ") 
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

OGI_df['transcription_clean'] = OGI_df.apply(lambda row:
                                    cleanTranscription(row), axis=1)

print("NaNs in each column:")
print("filepath: ", OGI_df['filepath'].isnull().sum())
print("scripted: ", OGI_df['scripted'].isnull().sum())
print("transcription_clean: ", OGI_df['transcription_clean'].isnull().sum())
print("transcription_original: ", OGI_df['transcription_original'].isnull().sum())
print("spkr_id: ", OGI_df['spkr_id'].isnull().sum())

print("Unique characters in cleaned transcription")
print(sorted(set(OGI_df.transcription_clean.sum())))
print(sorted(set(OGI_df.transcription_original.sum())))

# Get all the unique words in transcription
unique_words = set()
OGI_df['transcription_original'].str.split().apply(unique_words.update)
print("Unique words in original transcription:")
print("\n".join(sorted(unique_words)))

# ------------------------------------------
#          Data checks
# ------------------------------------------
# Check if has audio file
# Flag rows where the wav file does not exist
# i.e. set has_audio_file = False
print("\n------> Flagging rows where wav file does not exist\n")
print("has_audio_file = False")
filepaths_list = OGI_df['filepath'].tolist()
fileExists = [os.path.isfile(fp) if fp == fp else False for fp in filepaths_list]
OGI_df['has_audio_file'] = fileExists

# Check if speech is present in audio file
# Flag rows where file is transcribed but
# the audio contains no speech e.g. only silence, noise...
# i.e. no spoken words, only silence or speech tags
print("\n------> Flagging rows where file is transcribed but has no speech\n")
print("has_speech_in_audio = False")
OGI_df['has_speech_in_audio'] = np.nan
OGI_df.loc[(OGI_df.has_audio_file == True) &
           ((OGI_df.transcription_clean == None) |
            (OGI_df.transcription_clean == "") |
            (OGI_df.transcription_clean == "<unk>")),
            'has_speech_in_audio'] = False
OGI_df.loc[(OGI_df.has_audio_file == True) &
            ((OGI_df.transcription_clean != None) &
            (OGI_df.transcription_clean != "<unk>") &
            (OGI_df.transcription_clean != "")),
            'has_speech_in_audio'] = True

# Flag if recording is usable or not
# Usable = False if:
#   has_audio_file != True OR
#   has_speech_in_audio != True
print("\n------> Checking if recording is usable or not\n")
print("usable")
OGI_df['usable'] = True
def checkUsable(fp, has_audio_file, has_speech_in_audio):
    bad_quality = "3"
    if has_audio_file != True:
        usable = False
    elif has_speech_in_audio != True:
        usable = False
    else:
        usable = True
    return usable

OGI_df['usable'] = OGI_df.apply(lambda x: checkUsable(x['filepath'],
                                  x['has_audio_file'],
                                  x['has_speech_in_audio']), 
                                  axis=1)

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
OGI_df['duration'] = OGI_df.apply(lambda x: getDuration(x['filepath'],
                                    x['has_audio_file']), axis=1)

# ------------------------------------------
#       Split into portions
# ------------------------------------------
print("\n------> Splitting into ignore, test, dev, finetune, pretrain... ------\n")
OGI_df['set'] = np.nan
OGI_df['mostafa_set'] = np.nan

# pretrain: if usable == True AND quality_code == "3"
def setPretrain(usable, quality_code):
    pretrain_code = "3"
    if usable == True and math.isnan(quality_code) == False:
        if str(int(quality_code)) == pretrain_code:
            data_set = "pretrain"
        else:
            data_set = np.nan
    else:
        data_set = np.nan
    return data_set
OGI_df['set'] = OGI_df.apply(lambda x: setPretrain(x['usable'],
                                    x['quality_code']),
                                    axis=1)

print("Unique values in 'set' column:", OGI_df['set'].unique())

# ignore: if usable != True
OGI_df['set'] = np.where((OGI_df['usable'] != True), "ignore", OGI_df['set'])

print("Unique values in 'set' column:", OGI_df['set'].unique())

# test: 
# if filepath in filepath_test AND usable == True AND set != ignore
OGI_df['set'] = np.where((OGI_df['filepath'].isin(filepath_test)) & 
                         (OGI_df['usable'] == True) &
                         ((OGI_df['set'] != "ignore") & (OGI_df['set'] != "pretrain")),
                          "test", OGI_df['set'])
OGI_df['mostafa_set'] = np.where((OGI_df['filepath'].isin(filepath_test)),
                                 "test", OGI_df['mostafa_set'])

print("Unique values in 'set' column:", OGI_df['set'].unique())

# dev: if filepath in filepath_dev AND usable == True AND set != ignore and set != test
OGI_df['set'] = np.where((OGI_df['filepath'].isin(filepath_dev)) &
                         (OGI_df['usable'] == True) &
                         ((OGI_df['set'] != "ignore") & (OGI_df['set'] != "test")
                           & (OGI_df['set'] != "pretrain")),
                          "dev", OGI_df['set'])
OGI_df['mostafa_set'] = np.where((OGI_df['filepath'].isin(filepath_dev)),
                                  "dev", OGI_df['mostafa_set'])
print("Unique values in 'set' column:", OGI_df['set'].unique())

# finetune: 
# if scripted = True AND usable == True AND set == NaN
OGI_df['set'] = np.where((OGI_df['usable'] == True) &
                         (OGI_df['scripted'] == True) &
                         ((OGI_df['set'] != "ignore") & (OGI_df['set'] != "test") &
                          (OGI_df['set'] != "dev") & (OGI_df['set'] != "pretrain")),
                          "finetune", OGI_df['set'])
print("Unique values in 'set' column:", OGI_df['set'].unique())

# pretrain:
# if scripted != True AND usable == True AND set == NaN OR
OGI_df['set'] = np.where((OGI_df['usable'] == True) &
                         (OGI_df['scripted'] == False) &
                         ((OGI_df['set'] != "ignore") & (OGI_df['set'] != "dev") &
                          (OGI_df['set'] != "test")),
                          "pretrain", OGI_df['set'])

print("Checking if there's any null values in 'set' column:")
print("nan: ", (OGI_df['set'] == "nan").sum())
print("np.nan:", (OGI_df['set'] == np.nan).sum())

# Making separate dataframes 
OGI_pretrain = OGI_df[(OGI_df['set'] == "pretrain")]
OGI_finetune = OGI_df[(OGI_df['set'] == "finetune")]
OGI_dev = OGI_df[(OGI_df['set'] == "dev")]
OGI_test = OGI_df[(OGI_df['set'] == "test")]
OGI_ignore = OGI_df[(OGI_df['set'] == "ignore")]

print("Unique values in 'set' column:", OGI_df['set'].unique())

# ------------------------------------------
#    Save to CSV
# ------------------------------------------
print("\n------> Saving to CSV... ----------------------------------------------\n")
OGI_df.to_csv(out_fp,index=False)
OGI_pretrain.to_csv(pretrain_fp, index=False)
OGI_finetune.to_csv(finetune_fp, index=False)
OGI_dev.to_csv(dev_fp, index=False)
OGI_test.to_csv(test_fp, index=False)
OGI_ignore.to_csv(ignore_fp, index=False)

for fp in output_fp:
    print("Saved:", fp)

print("Done!")



