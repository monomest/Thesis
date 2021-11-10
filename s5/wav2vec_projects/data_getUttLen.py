import pandas as pd
import numpy as np

# Setting filepaths
fp = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_test_light.csv"
out = "/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_test_uttlen"
# Read in file
df = pd.read_csv(fp, dtype=str)
# Get total words
df['utterance_length'] = df['transcription_clean'].str.split().str.len()
print(df.utterance_length.describe())
df['utterance_group'] = np.where((df['utterance_length']==1), 
                            1, np.nan)
df['utterance_group'] = np.where((df['utterance_length'] > 1) &
                                 (df['utterance_length'] < 6),
                            2, df['utterance_group'])
df['utterance_group'] = np.where((df['utterance_length'] > 5) &
                                 (df['utterance_length'] < 11),
                            3, df['utterance_group'])
df['utterance_group'] = np.where((df['utterance_length'] > 10) &
                                 (df['utterance_length'] < 21),
                            4, df['utterance_group'])
df['utterance_group'] = np.where((df['utterance_length'] > 20),
                            5, df['utterance_group'])
# Save to output file
out_fp = out+".csv"
df.to_csv(out_fp, index=False)
for i in range(1,6):
    out_fp = out+str(i)+".csv"
    save_df = df[(df['utterance_group'] == i)]
    save_df.to_csv(out_fp, index=False)
