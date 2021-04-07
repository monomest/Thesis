# cu_data_check.sh
# Author: Renee Lu
# About: This script checks whether the data has already been split into train, test and dev portions.
#        Depending on the outcome, it will then either resplit the data or use the existing split portions.

CU_ROOT=$1
CUR_DIR=$2

echo "Checking if data has already been prepared in local/data..."
exist=0
remove=0
split=0
for part in $CUR_DIR/local/data/train data/test data/dev; do
        if [ -e "$part/text" ];then
                echo "WARNING: Found '$part/text' already existing"
                exist=$(($exist+1))
        fi
        if [ -e "$part/segments" ];then
                echo "WARNING: Found '$part/segments' already existing"
                exist=$(($exist+1))
        fi
        if [ -e "$part/utt2spk" ];then
                echo "WARNING: Found '$part/utt2spk' already existing"
                exist=$(($exist+1))
        fi
        if [ -e "$part/wav.scp" ];then
                echo "WARNING: Found '$part/wav.scp' already existing"
                exist=$(($exist+1))
        fi
done

# If not all files exist, delete all and start again
# If all files exist, ask if delete all and start again or else skip it
# If no files exist, start again

if [[ "$exist" -eq 0 ]]; then
        echo "No existing prepared data found."
        split=1
elif [[ "$exist" -lt 12 ]]; then
        echo "Found only $exist out of 12 files already existing. Removing existing files..."
        remove=1
	split=1
elif [[ "$exist" -eq 12 ]]; then
        echo "All $exist out of 12 files were found."
        read -r -p "Do you want to remove these files and split the data into new train, test and dev portions? [y/N] " response

        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
        then
                remove=1
		split=1
        else
                echo "Using existing train, test and dev portions."
		remove=0
		split=0
        fi
else
        echo "Error: Found $exist existing files but only checked for 12. Something is wrong with the code."
fi

if [[ "$remove" -eq 1 ]]; then
        for part in data/train data/test data/dev; do
                if [ -e "$part/text" ];then
                        rm $part/text
                        echo "Removed '$part/text'"
                fi
                if [ -e "$part/segments" ];then
                        rm $part/segments
                        echo "Removed '$part/segments'"
                fi
                if [ -e "$part/utt2spk" ];then
                        rm $part/utt2spk
                        echo "Removed '$part/utt2spk'"
                fi
                if [ -e "$part/wav.scp" ];then
                        rm $part/wav.scp
                        echo "Removed '$part/wav.scp'"
                fi
        done

fi

# Prepare data: generate local/uttspkr.txt which has all the information needed for required kaldi files. 
local/cu_data_prep.sh $CU_ROOT $CUR_DIR

# Creating 'text', 'wav.scp', 'segments' and 'utt2spk'
echo "Creating 'text' 'wav.scp' 'segments' and 'utt2spk' files in 'data/train 'data/test' and 'data/dev'..."
if [[ "$split" -eq 1 ]]; then
        local/cu_split_data.sh
fi

# Find the number of speakers and utterances in train, test and dev data
for portion in train test dev; do
	numspkrs=$(wc -l < data/$portion/spkrs)
        numutt=$(wc -l < data/$portion/utt2spk)
        echo "There are $numspkrs speakers and $numutt utterances in $portion data."
done
