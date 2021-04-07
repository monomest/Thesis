# get_sentences.sh
# Author: Renee Lu
# About: This code lists all the scripted 'sentences' the children are prompted to read
#        from the CU Kids Speech Corpus. 
#        Used for kaldi Language Modelling.
# Output: local/sentences.txt: all the text from every scripted sentence. Each new sentence is on a new line.

CU_ROOT=$1 	# Path to CU Kids Speech Corpus
CUR_DIR=$2	# Path fo s5 directory
dir=$3

#CUR_DIR=/media/renee/Windows/Users/rslaj/Documents/02_Work/2019_2020_Taste-of-Research/kaldi/egs/Kaldi_CU/s5  # Path to current s5 directory
#CU_ROOT=/media/renee/Windows/Users/rslaj/Documents/02_Work/2019_2020_Taste-of-Research/CU_Kids_Corpus   # Path to CU Kids Speech Corpus

spkdir=$CU_ROOT/spk-03-034/sentences	# Path to a speaker's 'sentences' folder

# Go into $dir and output all the 25 sentences into local/sentences.txt file
cd $spkdir
find . -name "*.txt" -exec cat {} >> $dir/tmp/sentences.txt \;
