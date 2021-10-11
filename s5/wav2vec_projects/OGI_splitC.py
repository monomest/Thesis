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
        " <bs> "   : "<unk>", #background speech
        " <cough> ": " ", # cough sound
        " <ct> "   : " ", # a clear throat
        " <fp> "   : "<unk>", #generic filled pause/false start
        " <lau> "  : " ", # ??
        " <laugh> ": "<unk>", #laughter
        " <ln> "   : " ", # line noise
        " <long> " : " ", #elongated word
        " <ls> "   : " ", #lip smack
        " <n> "    : " ", # ??
        " <nitl> " : "<unk>"), # used for foreign language
        " <ns> "   : " ", # non-speech sound
        " <pau> "  : " ", # Silence/pause
        " <pf> "   : " ", # ??
        " <pron> " : " ", # Mispronounciation
        " <sing> " : " ", #Singing
        " <sneeze> ": " ", #Sneezing
        " <sniff> ": " ", #sniffing
        " <sp> "   : " ", #Unkown spelling
        " <tc> "   : " ", #tongue click
        " <uu> "   : "<unk>", #unintelligible speech
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
# Get the cleaned transcription
spontaneous_all_trans_spaced = [(" " + trans + " ").replace(" ", "  ") 
                               for trans in spontaneous_all_trans_original]

for idx, txt in enumerate(spontaneous_all_trans_spaced):
    if txt == txt:
        clean_txt = txt
        for noiseTag, replacement in dNoiseTag2Symb.items():
            clean_txt = clean_txt.replace(noiseTag, replacement)
            # Remove or replace all special characters
            text_tmp = text_tmp.replace("‘", "'")
            text_tmp = text_tmp.replace("’", "'")
            chars_to_ignore_regex = '[\<\[\]\–\…\)\?\/\-\*\:\&\>\.\;\(\+\_\,]'
            text_tmp = re.sub(chars_to_ignore_regex, " ", text_tmp)
            # Remove extra whitespace between words
            text_tmp = re.sub(' +', ' ', text_tmp)
            # Remove leading and trailing whitespaces
            text_tmp = text_tmp.strip()
            # Lowercase
            text_tmp = text_tmp.lower()
    else:
        clean_txt = np.nan
    spontaneous_all_trans_spaced[idx] = clean_txt

# Get speaker ID -----------------------------------v
# /srv/scratch/chacmod/OGI/trans/spontaneous/00/0/ks001/ks001xx0.wav
spontaneous_spkr_id = [fp.split("/")[9] for fp in spontaneous_all]
scripted_spkr_id = [fp.split("/")[9] for fp in scripted_all]


# ------------------------------------------
#       Split into portions
# ------------------------------------------
print("\n------> Splitting into ignore, test, dev, finetune, pretrain... ------\n")
# Formatting dataframes
scripted_df = pd.DataFrame(
                {'filepath': scripted_all,
                 'scripted': True,
                 'transcription_original': scripted_all_trans,
                 'transcription_clean': scripted_all_trans,


                            })



scripted_df = scripted_df.rename(columns={"transcription":"transcription_clean"})
scripted_df['usable'] = True
scripted_df['set'] = np.nan

spontaneous_df = spontaneous_df.rename(columns={"transcription":"transcription_clean"})
spontaneous_df['usable'] = True
spontaneous_df['set'] = np.nan

# ignore: if a file is in all_list not in the usable list
used_scripted = scripted_df['filepath'].tolist()
used_spontaneous = spontaneous_df['filepath'].tolist()
usable_list = used_scripted + used_spontaneous
all_list = scripted_all + spontaneous_all
unused_list = list(set(all_list) - set(usable_list))
              # In all_list but not in usable_list
# test: 
# if filepath in filepath_test AND usable == True AND set == NaN
scripted_df['set'] = np.where((scripted_df['filepath'].isin(filepath_test)) & 
                              (scripted_df['usable'] == True) &
                              (scripted_df['set'] != scripted_df['set']),
                              "test", np.nan)
spontaneous_df['set'] = np.where((spontaneous_df['filepath'].isin(filepath_test)) &
                              (spontaneous_df['usable'] == True) &
                              (spontaneous_df['set'] != spontaneous_df['set']),
                              "test", spontaneous_df['set'])
# dev: if filepath in filepath_dev AND usable == True AND set == NaN
scripted_df['set'] = np.where((scripted_df['filepath'].isin(filepath_dev)) &
                          (scripted_df['usable'] == True) &
                          (scripted_df['set'] == "nan"),
                           "dev", scripted_df['set'])
spontaneous_df['set'] = np.where((spontaneous_df['filepath'].isin(filepath_dev)) &
                          (spontaneous_df['usable'] == True) &
                          (spontaneous_df['set'] == "nan"),
                           "dev", spontaneous_df['set'])
# finetune: 
# if scripted AND usable == True AND set == NaN
scripted_df['set'] = np.where((scripted_df['usable'] == True) &
                              (scripted_df['set'] == "nan"),
                              "finetune", scripted_df['set'])
# pretrain:
# if spontaneous AND usable == True AND set == NaN
spontaneous_df['set'] = np.where((spontaneous_df['usable'] == True) &
                                 (spontaneous_df['set'] == "nan"),
                                 "pretrain", spontaneous_df['set'])

print("Checking if there's any null values in 'set' column:")
print((scripted_df.set == "nan").sum())
print((spontaneous_df.set == "nan").sum())

print("Unique values in 'set' column:")
print("Scripted:", scripted_df['set'].unique())
print("Spontaneous:", spontaneous_df['set'].unique())

# Creating set dataframes
unused_df = pd.DataFrame(
          {'filepath': unused_list,
           'transcription_clean': np.nan,
           'duration': np.nan,
           'spkr_id': np.nan,
           'usable': False,
           'set': "ignore"
           })
frames = [scripted_df, spontaneous_df, unused_df]
OGI_df = pd.concat(frames)

# Getting quality code for each scripted file
#def getCode(fp):
#    fp = fp.replace(".wav", ".txt")
#    fp = fp.replace("speech", "verify")
#    substring = "scripted"
#    if substring in fp and os.path.isfile(fp):
#        with open(fp, "r") as f:
#            code = f.readline().rstrip()
#        f.close()
#    else:
#        code = np.nan    
#    return code

print("Getting quality code for scripted files...")
OGI_df = pd.merge(OGI_df, verif_df, on="filepath", how="outer")
#OGI_df['quality_code'] = OGI_df.apply(lambda x: getCode(x['filepath']), axis=1)

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

