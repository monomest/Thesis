# format.sh
# Author: Renee Lu
# About: This code removes all the blank white spaces in the .trs and .txt transcription files
#        in the CU Kids Speech Corpus. Only need to run once. 

CU_ROOT=$1
cd $CU_ROOT

echo "Formatting all transcription files..."
files=$(find . \( -name "*.trs" -o -name "*.txt" \))
for file in $files; do
	# Remove unwanted extra spaces
	sed -i '/^[[:space:]]*$/d' $file	
	dos2unix -q $file
	sed -i '/^$/d' $file
	# Remove '/91' '/92' characters and replace with single quote
        # Remove '/93' '/94' characters
	# https://superuser.com/questions/199799/vim-shows-strange-characters-91-92
	sed -i "s/\x91/'/g; s/\x92/'/g" $file
	if [[ $file == *".txt" ]]; then
		# Replace all tabs and spaces with a single space
		sed -i "s/[[:space:]]\+/ /g" $file
		# Remove all leading whitespaces
		sed -i 's/^[ \t]*//' $file
		# Remove '/93' '/94' characters
        	sed -i "s/\x93/\"/g; s/\x94//g; s/\x85//g" $file
	fi
done
