# ---------------------------------------------------------
# myST_split.py
# Purpose: Split MyST speech corpus into train and test.
#          Requires myST_dataframe.csv to exist.
#          Must have run myST_prep.py.
# Author: Renee Lu, 2021
# ---------------------------------------------------------
# There are 98441 total wav files, around 7 to 8
# seconds long each. 
# Train = 3-4hrs = 1550 wav files
# Test = 30mins = 300 wav files
# ------------------------------------------
#          Importing libraries
# ------------------------------------------

# For dataframes
import pandas as pd

# ------------------------------------------
#     Setting train and test portions
# ------------------------------------------
num_train = 3300
num_test = 500

# ------------------------------------------
#             Setting filepaths
# ------------------------------------------

# File path to MyST dataframe csv file,
# generated from myST_prep.py and/or
# myST_getShortWavs.py
myST_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_shorten_dataframe.csv"
# Where to save training dataframe
myST_train_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_train.csv"
# Where to save testing
myST_test_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/myST_test.csv"

# ------------------------------------------
#              Custom exceptions
# ------------------------------------------
class SplitPortionsTooLargeError(Exception):
    """Raised when train and split portions larger 
       than number of existing wav files"""
    pass

# ------------------------------------------
#              Splitting data
# ------------------------------------------

try:
    myST_df = pd.read_csv(myST_fp)
    # Check validity of train and test portions
    num_rows = len(myST_df.index)
    if num_train+num_test > num_rows:
        raise SplitPortionsTooLargeError
    # Use the top and bottom files for train and test.
    # Assume train and test portions are so small they
    # will not overlap.
    myST_train = myST_df.head(num_train)
    myST_test = myST_df.tail(num_test)
    # Convert dataframes to csv
    myST_train.to_csv(myST_train_fp, index=False)
    myST_test.to_csv(myST_test_fp, index=False)
    print("SUCCESS: Created train and test portions in",
          myST_train_fp, "and", myST_test_fp)
    train_hours = sum(myST_train['duration'].tolist())/(60*60)
    test_hours = sum(myST_test['duration'].tolist())/(60*60)
    print("Train files:", len(myST_train),
          "| Train hours:", train_hours)
    print("Test files:", len(myST_test),
           "| Test hours:", test_hours)
except FileNotFoundError:
    print("ERROR: File '", myST_fp, "' does not exist. Try running 'myST_prep.py' first.")
except SplitPortionsTooLargeError:
    print("ERROR: The wav files in train (", num_train, ") and test (", num_test,
          ") portions are greater than the amount of existing wav files (",
          num_rows, ").")
