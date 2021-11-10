import pandas as pd
import numpy as np

# Setting filepaths
fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_test_light.csv"
out_fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_test_uttlen.csv"
# Read in file
df = pd.read_csv(fp, dtype=str)
# Get total words
df['utterance_length'] = df['transcription_clean'].str.split().str.len()
print(df.utterance_length.describe())
df['utterance_group'] = np.where((df['utterance_length']==1), 
                            1, np.nan)
df['utterance_group'] = np.where((df['utterance_length'] > 1) &
                                 (df['utterance_length'] < 6),
                            5, df['utterance_group'])
df['utterance_group'] = np.where((df['utterance_length'] > 5) &
                                 (df['utterance_length'] < 11),
                            10, df['utterance_group'])
df['utterance_group'] = np.where((df['utterance_length'] > 10) &
                                 (df['utterance_length'] < 21),
                            20, df['utterance_group'])
df['utterance_group'] = np.where((df['utterance_length'] > 20),
                            21, df['utterance_group'])
# Save to output file
df.to_csv(out_fp, index=False)

