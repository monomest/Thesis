# clean.sh
# Author: Renee
# About: This code deletes all the new files created in the 
#        kaldi_CU/s5 directory after executing run.sh
#        To be run in the s5 directory.

CUR_DIR=$(pwd)	# Path to s5 directory
#CU_ROOT=/media/renee/Windows/Users/rslaj/Documents/02_Work/2019_2020_Taste-of-Research/CU_Kids_Corpus   # Path to CU Kids Speech Corpus
CU_ROOT=/srv/scratch/z5160268/2020_TasteofResearch/CU_Kids_Corpus	# Path to CU Kids Speech Corpus in supercomputer

# Array of files to remove that is common to all options
commonf=( core.* logios.log )
# Array of directories to remove that is common to all options
commond=( exp data )

# Array of local files to remove: Option 0 and 1
localf=( local/spkrs.txt local/spkrs.txt local/tags.txt local/uniqchar.txt local/uttInfo.txt )
# Array of local directories to remove: Option 0 and 1
locald=( local/data )

echo "Do you want to start at:"
read -r -p "(0) STAGE 0: Remove everything, including .wav files (1) STAGE 1: Resplit data and train models again (2) STAGE 2: Keep existing data portions and train models again [0/1/2] " response
	if [[ "$response" =~ ^([0])$ ]] || [[ "$response" =~ ^([1])$ ]]; then
		echo "Removing files..."	
                # Remove common files
		for f in "${commonf[@]}"; do
			echo "Removing file $f."
			rm $f
		done
		# Remove common directories
		for d in "${commond[@]}"; do
			echo "Removing directory $d."
			rm -r $d
		done 
		# Remove local files
		for f in "${localf[@]}"; do
			echo "Removing file $f."
			rm $f
		done
		# Remove local/data
		for d in "${locald[@]}"; do
			echo "Removing directory $d."
			rm -r $d
		done
		# Remove all .wav files if STAGE 0
		if [[ "$response" =~ ^([0])$ ]]; then
			echo "Removing all .wav files."
			cd $CU_ROOT
			find . -name "*.wav" -exec rm {} \;
		fi
	elif [[ "$response" =~ ^([2])$ ]]; then
		echo "Removing files..."        
                # Remove common files
                for f in "${commonf[@]}"; do
                        echo "Removing file $f."
                        rm $f 
                done 
                # Remove common directories
                for d in "${commond[@]}"; do
                        echo "Removing directory $d."
                        rm -r $d 
                done   
		# Make s5/data directory
		mkdir data
		# Copy all the dev, test and train files into local
		echo "Copying all split data portion files into s5/data"
		for dir in dev test train; do
        		mkdir data/$dir
        		for file in segments spkrs text utt2spk wav.scp spk2utt; do
                		cp local/data/$dir/$file data/$dir/$file
        		done
		done
	else
		echo "Your response is invalid. Please enter either '0' or '1' or '2' corresponding to which action you want to take."
		
	fi
echo "DONE"
