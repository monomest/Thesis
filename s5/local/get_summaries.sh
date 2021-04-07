# get_summaries.sh
# Author: Renee Lu
# About: This is code is for getting all the text from the
#        spontaneous summaries spoken by children in the 
#        CU Kids Speech Corpus. 
#        Used for kaldi Language Modelling. 

CU_ROOT=$1
CUR_DIR=$2
dir=$3

#CUR_DIR=/media/renee/Windows/Users/rslaj/Documents/02_Work/2019_2020_Taste-of-Research/kaldi/egs/Kaldi_CU/s5  # Path to current s5 directory
#CU_ROOT=/media/renee/Windows/Users/rslaj/Documents/02_Work/2019_2020_Taste-of-Research/CU_Kids_Corpus   # Path to CU Kids Speech Corpus

summariesfile=$dir/tmp/summaries.txt

cd $CU_ROOT

# Find a list of all folders of speakers and loop through them
spkrs=$(find . -type d -name "spk*")
for spkr in $spkrs; do
	# If the speaker has a summary folder
	if [ -d "$spkr/summary" ]; then
		cd $spkr/summary
		trs=$(find . -name "*.trs")
		# If there exists .trs file inside
		if [ -n "$trs" ]; then
			# Record the speakerID
			spkrID=${spkr:6}
                        summarytmp=$dir/tmp/summarytmp_$spkrID.txt
                        touch $summarytmp
                        # Iterate through every .trs file and write the text to local/storytmp_$storyID.txt file
                        for trsfile in $trs; do
                                start=0
                                while IFS= read -r line
                                do
                                        # When the transcription starts
                                        if [[ $line == *"<Turn startTime"* ]]; then
                                                start=1
                                        fi
                                        # Get the transcription
                                        if [[ $line != *"<"* ]] && [[ start -eq 1 ]]; then
                                                trans=$line
                                                trans=$(echo "$trans" | tr -d '\r')
                                                # Convert transcription into all UPPERCASE
                                                trans=$(echo ${trans^^})
                                                # Replace '&LT;' with '<'
                                                trans=$(echo ${trans//&LT;/<})
                                                # Replace '&GT;' with '>'
                                                trans=$(echo ${trans//&GT;/>})
                                                # If transcription has event label, remove the label
                                                array=( "<DISCARD>" "<MP>" "<B>" "<BR>" "<COUGH>" "<GARB>" "<SIL>" "<UU>" )
                                                for remove in "${array[@]}"
                                                do
                                                        trans=$(printf '%s\n' "${trans//$remove/}")
                                                done
                                                # Replace all ? with apostrophe since transcription has words like 'couldn?t' and 'didn?t'
                                                trans=$(echo $trans | sed "s/?/'/")
                                                echo "$trans" >> $summarytmp
                                        fi
                                done < "$trsfile"
			done
                        # Remove all new lines from local/storytmp_$storyID.txt file
                        sed -i ':a;N;$!ba;s/\n/ /g' $summarytmp

                        # Concatenate the contents of local/storytmp_$storyID.txt file into the
                        # total list of story text file, called $storiesfile
                        cat $summarytmp >> $summariesfile
		# Else if no .trs files exist
		else
			echo "WARNING: Skipping a speaker summary because no .trs files exist in '$(pwd)'"
		fi
		cd ../../
	# Else if the speaker doesn't have a summary folder
	else
                spkrID=${spkr:2}
		echo "WARNING: Skipping a speaker summary because no 'summary' folder exists in '$(pwd)/$spkrID'"
	fi
done
