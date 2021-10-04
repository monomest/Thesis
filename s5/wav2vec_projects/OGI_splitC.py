# OGI_splitC.py
# Purpose: Split the transcribed OGI data 
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

print("Input files...")
fp_list = [fp_scripted, fp_scripted_all, fp_spontaneous, fp_spontaneous_all, 
           fp_dev, fp_test]
for fp in fp_list:
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
scripted_df = readCSV(fp_scripted)
spontaneous_df = readCSV(fp_spontaneous)

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

# ------------------------------------------
#       Split into portions
# ------------------------------------------
print("\n------> Splitting into ignore, test, dev, finetune, pretrain... ------\n")
# Formatting dataframes
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
def getCode(fp):
    fp = fp.replace(".wav", ".txt")
    fp = fp.replace("speech", "verify")
    substring = "scripted"
    if substring in fp and os.path.isfile(fp):
        with open(fp, "r") as f:
            code = f.readline().rstrip()
        f.close()
    else:
        code = np.nan    
    return code

print("Getting quality code for scripted files...")
OGI_df['quality_code'] = OGI_df.apply(lambda x: getCode(x['filepath']), axis=1)

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

