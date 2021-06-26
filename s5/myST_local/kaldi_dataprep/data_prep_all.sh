#!/bin/bash

# Copyright (c) 2020, FBK 
# License: Apache 2.0

tlt_data_dir=$TLT2020
tlt_data_dir_1618=$TLT1618

#tlt_data_dir=/srv/scratch/z5173707/Dataset/TLT/TLT2020challenge
#tlt_data_dir_1618=/srv/scratch/z5173707/Dataset/TLT/TLT2020challenge2P

sup_sfx=sup

. ./utils/parse_options.sh 

if [ -z "${TLT2020}" ] ; then
    echo Error: please set variable TLT2020
    echo
    exit
fi

#for d in train dev eval ; do
for d in train dev ; do

if ! test -d data/${d}
then
    mkdir -p data/${d}
else
    rm data/${d}/*.scp
fi

find -L ${tlt_data_dir}/audio/TLT2017${d} -name "*.wav" > data/${d}/wav.lst
if ! test -s data/${d}/wav.lst ; 
then 
    echo Error: no wav found in ${tlt_data_dir}/audio/TLT2017${d}
    exit
fi

for f in `cat data/${d}/wav.lst`;do echo `basename $f .wav` $f ; done  | sort > data/${d}/wav.scp
cat ${tlt_data_dir}/audio/TLT2017${d}.${sup_sfx} | sort > data/${d}/text

cut -d_ -f1 data/${d}/wav.scp > data/${d}/speakers
paste data/${d}/wav.scp data/${d}/speakers | awk '{print $1,$3}' > data/${d}/utt2spk
utils/utt2spk_to_spk2utt.pl data/${d}/utt2spk > data/${d}/spk2utt

utils/fix_data_dir.sh data/${d}

done

#Add Extra data for training

find -L ${tlt_data_dir_1618}/audio/TLT1618train -name "*.wav" > data/train/wav_extra.lst
for f in `cat data/train/wav_extra.lst`;do echo `basename $f .wav` $f ; done  | sort > data/train/wav_extra.scp
cat data/train/wav_extra.scp >> data/train/wav.scp
cat ${tlt_data_dir_1618}/TLT1618train.norm.trn | sort >> data/train/text
cut -d- -f1 data/train/wav_extra.scp > data/train/speakers_extra
paste data/train/wav_extra.scp data/train/speakers_extra | awk '{print $1,$3}' >> data/train/utt2spk
utils/utt2spk_to_spk2utt.pl data/train/utt2spk > data/train/spk2utt

# Add MyST data for training

# Make a copy of existing data/train directory and rename it to train_tlt
# Remove existing data/train directory
cp -r data/train data/train_tlt
rm -r data/train

# Prepare MyST data, which is outputted to data/train_myst
local/myst_prep.sh

# Combine data/train_tlt and data/train_myst into data/train
mkdir -p data/train
utils/data/combine_data.sh data/train data/train_tlt data/train_myst 

# Fix data
utils/fix_data_dir.sh data/train
