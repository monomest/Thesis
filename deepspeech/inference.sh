# inference.sh
# Author: Renee Lu
# About: This script performs inference using DeepSpeech

#! /bin/bash
# IFS = Input Field Separator

# Set model
MODEL="deepspeech-0.9.3-models.pbmm"
echo "Model: $MODEL"

# Set data path
# OGI
#data_fp="/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/OGI_local/THESIS_C/OGI_data_test_light.csv"
# MyST
#data_fp="/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/myST_local/THESIS_C/myST_data_test_light.csv"
# TLT17
data_fp="/srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/TLT_local/THESIS_C/TLT17eval_data_test_light.csv"
echo "TLT17 test set: $data_fp"
echo ""

# Column names
echo "filepath,transcription_clean,prediction"
while IFS="," read -r filepath transcription_clean
do
  # Get output from DeepSpeech and redirect stderr to dev/null
  prediction=$(deepspeech --model $MODEL --audio $filepath 2>/dev/null)
  echo "$filepath,$transcription_clean,$prediction"
done < <(tail -n +2 $data_fp)
