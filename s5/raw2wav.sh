# raw2wav.sh
# Author: Renee Lu
# About: This code is used to convert all the .raw audio files for the
# CU Kids' Audio Speech Corpus into .wav files. 
# .raw file specifications: 16kHz sampling, 16 bits/sample, 1 channel, signed (assumed)
# .wav file specifications: 16kHz sampling, 16 bits/sample, 1 channel
# Output: '.wav' files corresponding to each .raw file 

# Get path to the CU Kids Corpus data
CU_ROOT=$1 

cd $CU_ROOT

# Count number of files that have the .wav extension
wavfiles=$(find . -name '*.wav' | wc -l)

if [ $wavfiles -gt 0 ]; then 

	echo "WARNING: Cannot convert .raw files into .wav files because found $wavfiles .wav files already existing."
	read -r -p "Do you want to remove all existing .wav files and then convert? [y/N] " response
	
	if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
	then
		echo "Removing all existing .wav files..."
		find . -name "*.wav" -exec rm -rf {} \;
                echo "Coverting .raw audio into .wav files..."
		find . -name '*.raw' -exec sox -r 16k -e signed -b 16 -c 1 {} {}.wav \;
		echo "Cleaning up names of new .wav files..."
		find . -name '*.wav' -execdir sh -c \
		'for arg; do mv "$arg" "${arg%.raw.wav}".wav; done' _ {} \+
		echo "SUCCESS: Conversion completed!"
	else
		echo "Using existing .wav files for all subsequent tasks."
	fi	
else
	echo "No .wav files found. Converting .raw audio into .wav files..."
	find . -name '*.raw' -exec sox -r 16k -e signed -b 16 -c 1 {} {}.wav \;
	echo "Cleaning up names of new wav files..."
	find . -name '*.wav' -execdir sh -c \
	'for arg; do mv "$arg" "${arg%.raw.wav}".wav; done' _ {} \+
	echo "SUCCESS: Conversion completed!"
fi
