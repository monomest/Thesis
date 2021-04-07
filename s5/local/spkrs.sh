# spkrs.sh
# Author: Renee Lu
# About: This code creates a file which lists all the unique speakers present in the speech corpus.
# Output: 'local/spkrs.txt'

touch local/spkrs.txt

CU_ROOT=$1    # Path to speech corpus
CUR_DIR=$2    # Path to s5 directory

# Go into CU Kids' Speech Corpus directory
cd $CU_ROOT

# Get a list of all speakers and store them in 'spkrs.txt' file
find . -maxdepth 1 -mindepth 1 -type d | cut -d '-' -f 2,3 | tr -d [:alpha:][:punct:] | awk NF | sort | uniq > $CUR_DIR/local/spkrs.txt
