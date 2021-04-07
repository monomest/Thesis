# cu_data_prep.sh
# Author: Renee Lu
# About: This code is used to preparing the CU Kids' Speech Corpus for kaldi ASR training. 
#        Should be run before creating text, wav.scp, segments and utt2spk files.
#        Should be run from s5 directory.
# Output: local/spkrs.txt
#         local/uttspkr.txt

set -e 	# Exit on error

export LC_ALL=C	# To make sure sorting of files will be performed in same way as C++

CU_ROOT=$1	# Path to speech corpus
CUR_DIR=$2	# Path to s5 directory

#echo "Getting the list of stories in the CU Kids' Speech Corpus..."
#local/stories.sh $CU_ROOT $CUR_DIR 
#cd $CUR_DIR

echo "Creating 'data/train' 'data/test' and 'data/dev' directories..."
# Create train, test and dev inside the data directory
trndir=data/train
tstdir=data/test
devdir=data/dev

mkdir -p $trndir $tstdir $devdir

. ./path.sh || exit 1	# For kaldi root

# Get all the utterance and speaker information to use in data preparation
# according to the kaldi format.

# If the file 'local/spkrs.txt' does not exist, create it
FILE=local/spkrs.txt
if [ ! -e "$FILE" ]; then
	echo "Creating a list of all speakers in the corpus in 'local/spkrs.txt'..."
	local/spkrs.sh $CU_ROOT $CUR_DIR
fi

# If the file 'local/uttInfo.txt' file does not exist, create it
FILE=local/uttInfo.txt
if [ ! -e "$FILE" ]; then
	echo "Generating all utterance and speaker information for kaldi data preparation in 'local/uttInfo.txt'..."
	local/uttspkr.sh $CU_ROOT $CUR_DIR
fi
