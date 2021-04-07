# clean.sh
# Author: Renee
# About: This code deletes all the new files created in the 
#        kaldi_CU/s5 directory after executing run_TDNN*.sh
#        To be run in the s5 directory.

CUR_DIR=$(pwd)	# Path to s5 directory
#CU_ROOT=/media/renee/Windows/Users/rslaj/Documents/02_Work/2019_2020_Taste-of-Research/CU_Kids_Corpus   # Path to CU Kids Speech Corpus
CU_ROOT=/srv/scratch/z5160268/2020_TasteofResearch/CU_Kids_Corpus	# Path to CU Kids Speech Corpus in supercomputer

# Array of files to remove that is common to all options
#commonf=( )
# Array of directories to remove that is common to all options
commond=( mfcc_hires exp/make_hires exp/nnet3_vp )

# Remove common directories
for d in "${commond[@]}"; do
	echo "Removing directory $d."
        rm -r $d 
done   
echo "DONE"
