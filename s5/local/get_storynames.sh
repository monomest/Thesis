# get_storynames.sh
# Author: Renee Lu
# About: This code lists all the unique stories in the CU Kids'
#        Speech Corpus.
# Output: local/storynames.txt

#CU_ROOT=$1	# Path to CU Kids Speech Corpus
#CUR_DIR=$2	# Path to s5 directory

CUR_DIR=/media/renee/Windows/Users/rslaj/Documents/02_Work/2019_2020_Taste-of-Research/kaldi/egs/Kaldi_CU/s5  # Path to current s5 directory
CU_ROOT=/media/renee/Windows/Users/rslaj/Documents/02_Work/2019_2020_Taste-of-Research/CU_Kids_Corpus   # Path to CU Kids Speech Corpus

cd $CU_ROOT

# Find all the unique stories from Grade 1-2 and list them in local/stories.txt
grep -rnw -e 'STORY ID' | sed 's@.*> @@' | sort | uniq > $CUR_DIR/local/storynames.txt 

# Find all the unique stories from Grade 3-5 and then list them in local/stories.txt
find . -name 'story-name' -exec cat {} \; | sort | uniq >> $CUR_DIR/local/storynames.txt

echo "SUCCESS: Created a list of all stories in the speech corpus in 'local/storynames.txt'"
