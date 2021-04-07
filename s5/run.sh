#!/bin/bash

# run.sh
# Author: Renee Lu
# About: This code is for using the CU Kids' Speech Corpus for kaldi ASR training.

. ./cmd.sh	# Setting local system jobs (local CPU - no external clusters)
. ./path.sh	# Setting paths
set -e

n=5	# Number of jobs
CUR_DIR=$(pwd)	# Path to current s5 directory
#CU_ROOT=/media/renee/Windows/Users/rslaj/Documents/02_Work/2019_2020_Taste-of-Research/CU_Kids_Corpus	# Path to CU Kids Speech Corpus
CU_ROOT=/srv/scratch/z5160268/2020_TasteofResearch/CU_Kids_Corpus	# Path to CU Kids Speech Corpus on supercomputer

stage=2	# This controls what stage to start running from

if [ $stage -le 0 ]; then
	echo
	echo "===== STAGE 0/11 PREPARING RAW DATA ====="
	echo "Run once in the first time after unzipping data"
	echo

	# format.sh only needs to be run once, in the first time after unzipping speech corpus file 
	echo "Formatting transcription files (e.g. removing all empty spaces)..."
	. ./format.sh $CU_ROOT
	cd $CUR_DIR

	# fix.sh only needs to be run once, in the first time after unzipping speech corpus file
	echo "Applying some fixes to the data to remove edge cases..."
	. ./fix.sh $CU_ROOT

	# raw2wav.sh only needs to be run once, in the first time after unzipping speech corpus file
	echo "Converting .raw audio files into .wav formatted files..."
	. ./raw2wav.sh $CU_ROOT
	cd $CUR_DIR
fi


if [ $stage -le 1 ]; then
	echo
	echo "===== STAGE 1/11 PREPARING ACOUSTIC DATA ====="
	echo "Cleaning acoustic data and splitting it into train, test and dev portions"
	echo

	# Prepare data: generate local/uttspkr.txt which has all the information needed for required kaldi files. 
	echo "Generating local/uttspkr.txt which has all the information required for kaldi data preparation..."
	local/cu_data_prep.sh $CU_ROOT $CUR_DIR

	# Creating 'text', 'wav.scp', 'segments', 'utt2spk' and 'spk2utt'
	echo "Creating 'text' 'wav.scp' 'segments' 'utt2spk' and 'spk2utt' files in 'data/train 'data/test' and 'data/dev'..."
        local/cu_split_data.sh

	# Normalising the transcription
	echo "Normalising transcription of 'text' files..."
	local/textfile_normal.sh

	# Copying these created files into local/data directory
	echo "Copying files into local/data directory..."
	local/data2local.sh $CUR_DIR

	# Find the number of speakers and utterances in train, test and dev data
	for portion in train test dev; do
        	numspkrs=$(wc -l < data/$portion/spkrs)
        	numutt=$(wc -l < data/$portion/utt2spk)
        	echo "There are $numspkrs speakers and $numutt utterances in $portion data."
	done
fi

if [ $stage -le 2 ]; then
	echo
	echo "===== STAGE 2/11 EXTRACTING FEATURES ====="
	echo "Extracing Mel Frequency Cepstral Coefficients (MFCC) features"
	echo

	# Create feats.scp file in data/train, data/test and data/dev
	echo "Creating 'feats.scp' in 'data/train' 'data/test' and 'data/dev'..."
    	for part in train test dev; do
        	mfccdir=data/$part/mfcc
        	mfcclog=exp/make_mfcc/$part
        	mkdir -p $mfccdir $mfcclog
        	steps/make_mfcc.sh --nj $n --cmd "$train_cmd" data/$part $mfcclog $mfccdir      # Making feats.scp files for training
        	steps/compute_cmvn_stats.sh data/$part $mfcclog $mfccdir        		# Making cmvn.scp files for training
	
		utils/validate_data_dir.sh data/$part	# Validate the data and check for errors
		utils/fix_data_dir.sh data/$part	# Fix the errors
	done
fi

if [ $stage -le 3 ]; then
	echo 
	echo "===== STAGE 3/11 PREPARING LANGUAGE DATA ====="
	echo "Cleaning language data in preparation for training Language Model"
	echo

	# Prepare dict directory
	# lexicon.txt               [ <word> <phone 1> <phone 2> ... ]
	# nonsilence_phones.txt     [<phone>]
	# silence_phones.txt        [<phone>]
	# optional_silence.txt      [<phone>]

	# Prepare the dict
	local/cu_dict_prep.sh $CU_ROOT || exit 1  #I'm using set -e in the begining not sure if exit 1 needed
	#Prepare lang directory
	utils/prepare_lang.sh data/local/dict "<UNK>" data/local/lang data/lang || exit 1
fi

if [ $stage -le 4 ]; then
	echo
	echo "===== STAGE 4/11 TRAINING LANGUAGE MODEL ====="
	echo "Training the Language Model (LM)"
	echo

	# Train bigram LM
	echo "Training bigram LM..."
	local/cu_train_srilm.sh $CU_ROOT $CUR_DIR
fi

if [ $stage -le 5 ]; then
	echo
	echo "===== STAGE 5/11 TRAINING MONOPHONE MODEL ====="
	echo "Training the monophone Acoustic Model"
	echo

	#Train Monophone model
	steps/train_mono.sh --nj $n --cmd "$train_cmd" data/train/ data/lang/ exp/mono || exit 1

	#Decode the monophone model
	utils/mkgraph.sh --mono data/lang exp/mono exp/mono/graph
	steps/decode.sh --config conf/decode.config --nj $n --cmd "$decode_cmd" exp/mono/graph data/test exp/mono/decode

	# Get alignments from monophone system.
	steps/align_si.sh --nj $n --cmd "$train_cmd" data/train data/lang exp/mono exp/mono_ali
fi

if [ $stage -le 6 ]; then
	echo
	echo "===== STAGE 6/11 TRAINING TRIPHONE MODEL ====="
	echo "Training the triphone Acoustic Model"
	echo

	#Train Triphone Model
	steps/train_deltas.sh --cmd "$train_cmd" 1800 9000 data/train data/lang exp/mono_ali exp/tri1

	#Decode the triphone model
	utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph

	steps/decode.sh --config conf/decode.config --nj $n --cmd "$decode_cmd" \
	exp/tri1/graph data/test exp/tri1/decode

	# align tri1
	steps/align_si.sh --nj $n --cmd "$train_cmd" \
	--use-graphs true data/train data/lang exp/tri1 exp/tri1_ali
fi

if [ $stage -le 7 ]; then
echo 
echo "===== STAGE 7/11 LDA-MLLT FEATURE TRANSFORM ====="
echo "Linear Discriminant Analysis-Maximum Likelihood Linear Transform (LDA-MLLT)"
echo

	#Train tri2b [LDA-MLLT]
	steps/train_lda_mllt.sh --cmd "$train_cmd"  --splice-opts "--left-context=3 --right-context=3" 1800 9000 data/train data/lang exp/tri1_ali exp/tri2b

	#Decode the tri2b model
	utils/mkgraph.sh data/lang exp/tri2b exp/tri2b/graph
	steps/decode.sh --config conf/decode.config --nj $n --cmd "$decode_cmd" \
	exp/tri2b/graph data/test exp/tri2b/decode


	# you could run these scripts at this point, that use VTLN.
	# local/run_vtln.sh
	# local/run_vtln2.sh

	#Align tri2b
	steps/align_si.sh --nj $n --cmd "$train_cmd" --use-graphs true \
	data/train data/lang exp/tri2b exp/tri2b_ali
fi

if [ $stage -le 8 ]; then
	echo
	echo "===== STAGE 8/11 MMI AFTER LDA-MLLT ====="    
	echo "Maximum Mutual Information (MMI)"
	echo

	#Do MMI on top of LDA+MLLT.
	steps/make_denlats.sh --nj $n --cmd "$train_cmd" \
	data/train data/lang exp/tri2b exp/tri2b_denlats
	steps/train_mmi.sh data/train data/lang exp/tri2b_ali exp/tri2b_denlats exp/tri2b_mmi
	#Decode
	steps/decode.sh --config conf/decode.config --iter 4 --nj $n --cmd "$decode_cmd" \
	exp/tri2b/graph data/test exp/tri2b_mmi/decode_it4
	steps/decode.sh --config conf/decode.config --iter 3 --nj $n --cmd "$decode_cmd" \
	exp/tri2b/graph data/test exp/tri2b_mmi/decode_it3
fi

if [ $stage -le 9 ]; then
	echo
	echo "===== STAGE 9/11 BOOSTING ====="
	echo

	# Do the same with boosting.
	steps/train_mmi.sh --boost 0.05 data/train data/lang \
	exp/tri2b_ali exp/tri2b_denlats exp/tri2b_mmi_b0.05
	steps/decode.sh --config conf/decode.config --iter 4 --nj $n --cmd "$decode_cmd" \
	exp/tri2b/graph data/test exp/tri2b_mmi_b0.05/decode_it4
	steps/decode.sh --config conf/decode.config --iter 3 --nj $n --cmd "$decode_cmd" \
	exp/tri2b/graph data/test exp/tri2b_mmi_b0.05/decode_it3
fi

if [ $stage -le 10 ]; then
	echo
	echo "===== STAGE 10/11 MPE ====="
	echo "Minimum Phone Error (MPE)"
	echo

	# Do MPE.
	steps/train_mpe.sh data/train data/lang exp/tri2b_ali exp/tri2b_denlats exp/tri2b_mpe
	steps/decode.sh --config conf/decode.config --iter 4 --nj $n --cmd "$decode_cmd" \
	exp/tri2b/graph data/test exp/tri2b_mpe/decode_it4
	steps/decode.sh --config conf/decode.config --iter 3 --nj $n --cmd "$decode_cmd" \
	exp/tri2b/graph data/test exp/tri2b_mpe/decode_it3
fi

if [ $stage -le 11 ]; then
	echo
	echo "===== STAGE 11/11 LDA- MLLT + SAT ====="
	echo "Speaker Adaptive Training (SAT)"
	echo

	#Train LDA-MLLT+SAT
	steps/train_sat.sh 1800 9000 data/train data/lang exp/tri2b_ali exp/tri3b

	#Decode
	utils/mkgraph.sh data/lang exp/tri3b exp/tri3b/graph

	steps/decode_fmllr.sh --config conf/decode.config --nj $n --cmd "$decode_cmd" \
	exp/tri3b/graph data/test exp/tri3b/decode

	# Align all data with LDA+MLLT+SAT system (tri3b)
	steps/align_fmllr.sh --nj $n --cmd "$train_cmd" --use-graphs true \
	data/train data/lang exp/tri3b exp/tri3b_ali

	# MMI on top of tri3b (i.e. LDA+MLLT+SAT+MMI)
	steps/make_denlats.sh --config conf/decode.config \
	--nj $n --cmd "$train_cmd" --transform-dir exp/tri3b_ali \
	data/train data/lang exp/tri3b exp/tri3b_denlats
	steps/train_mmi.sh data/train data/lang exp/tri3b_ali exp/tri3b_denlats exp/tri3b_mmi

	steps/decode_fmllr.sh --config conf/decode.config --nj $n --cmd "$decode_cmd" \
	--alignment-model exp/tri3b/final.alimdl --adapt-model exp/tri3b/final.mdl \
	exp/tri3b/graph data/test exp/tri3b_mmi/decode

	# Do a decoding that uses the exp/tri3b/decode directory to get transforms from.
	steps/decode.sh --config conf/decode.config --nj $n --cmd "$decode_cmd" \
	--transform-dir exp/tri3b/decode  exp/tri3b/graph data/test exp/tri3b_mmi/decode2
fi

echo "===== SUCCESS: run.sh has completed. ====="
