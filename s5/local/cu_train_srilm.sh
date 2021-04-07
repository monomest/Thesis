#!/bin/bash

# cu_train_srilm.sh
# Author: Renee Lu
# About: This code is for preparing the data/local/dict directory of CU Kids Speech Corpus
#        for kaldi ASR training.
#        Should be run from s5 directory.
# Output: data/local/lm_srilm directory
#         data/local/lm_srilm/tmp directory and contents 

CU_ROOT=$1
CUR_DIR=$2

#CUR_DIR=/media/renee/Windows/Users/rslaj/Documents/02_Work/2019_2020_Taste-of-Research/kaldi/egs/Kaldi_CU/s5  # Path to current s5 directory
#CU_ROOT=/media/renee/Windows/Users/rslaj/Documents/02_Work/2019_2020_Taste-of-Research/CU_Kids_Corpus   # Path to CU Kids Speech Corpus


# Check that the path to the corpus is passed as the argument
if [ $# != 2 ]; then
        echo "Usage: $(basename $0) /path/to/cu_data /path/to/s5_directory"
        exit 1;
fi

#Make sure that srilm installed
echo $KALDI_ROOT/tools/srilm/bin/i686-m64
which ngram-count
if [ $? -ne 0 ]; then
    if [ -d $KALDI_ROOT/tools/srilm/bin/i686-m64 ]; then
        export PATH=$PATH:$KALDI_ROOT/tools/srilm/bin/i686-m64
    fi
fi

langdir=`pwd`/data/lang
dir=`pwd`/data/local/lm_srilm
dirtmp=$dir/tmp

#Check if dir exist, otherwise create it
[ -d $dir ] || mkdir -p $dir || exit 1
[ -d $dirtmp ] || mkdir -p $dirtmp || exit 1

# Get story text
local/get_stories.sh $CU_ROOT $CUR_DIR $dir
# Get sentences text, output to local/sentences.txt
local/get_sentences.sh $CU_ROOT $CUR_DIR $dir
# Get summary text
local/get_summaries.sh $CU_ROOT $CUR_DIR $dir

# Concatenate all the scripted story, sentences and summary text in file $dir/scripted_txt.tmp
for file in $dir/tmp/sentences.txt $dir/tmp/stories.txt $dir/tmp/summaries.txt; do
	cat $file >> $dir/scripted_txt.tmp
done

file=$dir/scripted_txt.tmp
local/text_normal.sh $CUR_DIR $file

#Get unique set of OGI words 
cat $dir/scripted_txt.tmp | tr " " "\n" | sort -u > $dir/scripted_words.tmp

#Use ngram-count from srilm to generate bi gram LM from the list of scripted words
ngram-count -text $dir/scripted_txt.tmp -order 2 -lm $dir/bi.lm

#convert to fst format
arpa2fst --disambig-symbol=#0 --read-symbol-table=$langdir/words.txt $dir/bi.lm $langdir/G.fst
