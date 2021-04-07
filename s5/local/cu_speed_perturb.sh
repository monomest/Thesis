# cu_speed_perturb.sh
# Author: Renee Lu
# About: This code speed perturbs the CU Kids Speech Corpus
#        It randomly selects a warp factor between 0.9 to 1.1
#        and applies that to each speech file in the corpus.
# Assumes: there exists s5/data/train & s5/data/dev & s5/data/test
#          and the files in here are the same as local/data

DATA_PATH = /srv/scratch/z5160268/2020_TasteofResearch/kaldi/egs/renee_thesis/s5/data
