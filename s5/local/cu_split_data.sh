# cu_split_data.sh
# Author: Renee Lu
# About: This code uses local/uttInfo.txt to create all the
#        files needed in kaldi data preparation.
#        By doing so, it splits the data into train, test and dev.
# Output: 'data/[train, test, dev]/text' which is a text file formatted like
#         <speaker-ID>-<utterance-ID> <TRANSCRIPTION>
#         
#        'data/[train, test, dev]/wav.scp' which is a file formatted like
#         <recording-ID> <extended-filename>  
#
#        'data/[train, test, dev]/segments' which is a file formatted like
#         <utterance-ID> <recording-ID> <begin-time> <end-time>
#
#        'data/[train, test, dev]/utt2spk' which is a file formatted like
#         <utterance-ID> <spkr-ID>
#
#	 'data/[train, test, dev]/spkrs' which is a file that lists all
#         the unique speakers from that data portion
#
#	 'data/[train, test, dev]/spk2utt'
#
#	 'local/tags.txt' which is a file listing all the transcription
#         event labels
#
#        'local/uniqchar.txt' which is a file listing all the unique
#         characters present in the 'text' file

for dir in data/train data/test data/dev
do
	touch $dir/text
	touch $dir/wav.scp
	touch $dir/segments
	touch $dir/utt2spk
	touch $dir/spkrs
	touch $dir/spkrs_tmp
done

touch local/tags.txt
touch local/tags_tmp.txt

touch local/uniqchar.txt
touch local/uniqchar_tmp.txt

export LC_ALL=C	# For sorting purposes

# Default train, test and dev proportions if no input given
proptrain=0.7
numtest=0.15
propdev=0.15

proptest="$(echo "1-$numtest" | bc)"	# Used in random assignment later on

file="local/uttInfo.txt"
previousLine=""
previousSpkr=""
segmented="0"
previousBegin=""

# utterances to discard
discardutt=()
discardrecord=()

linenumber=0
totlines=$(wc -l < local/uttInfo.txt)

while IFS= read -r line
do
	linenumber=$((linenumber+1))
	if [[ $line != "<"* ]] 
	then
		spkrID=$(cut -d ":" -f 1 <<< "$line")
		uttID=$(cut -d ":" -f 2 <<< "$line")
		recordingID=$uttID
		trans=$(cut -d ":" -f 3 <<< "$line")
		# Convert transcription into all UPPERCASE
		trans=$(echo ${trans^^})
		# Replace '&LT;' with '<'
		trans=$(echo ${trans//&LT;/<})
		# Replace '&GT;' with '>'
		trans=$(echo ${trans//&GT;/>})
		# If transcription has the <MP> event label, remove the label
		remove="<MP>"
		trans=$(printf '%s\n' "${trans//$remove/}")
		# Replace all ? with apostrophe since transcription has words like 'couldn?t' and 'didn?t'
		trans=$(echo $trans | sed "s/?/'/")
		# If transcription has nothing, label as <SIL> silence
		if [[ $trans == "" ]]
		then
			trans="<SIL>"
		fi
		# If transcription is <DISCARD>, add this to discard array
		if [[ $trans == *"<DISCARD>"*  ]]; then
			discardID="$spkrID-$uttID"
                	echo "WARNING: Will discard $discardID because transcription is <DISCARD>"
			discardutt+=( $discardID )
			discardID="$recordingID"
			discardrecord+=( $discardID )
		fi
		extendedFilename=$(cut -d ":" -f 4 <<< $line)	
		# Split spkr into train, test or dev portion of data.
		if [[ $spkrID != $previousSpkr ]]
		then
			number=$(awk -v seed="$RANDOM" 'BEGIN{srand(seed);print rand()}')
			if (( $(echo "$number < $proptrain" | bc -l) ))
			then
				dataType="data/train"
			elif (( $(echo "$number > $proptest" | bc -l) ))
			then
				dataType="data/test"
			else
				dataType="data/dev"
			fi
		fi
		previousSpkr=$spkrID

		# Write to text file according to 'text' file format
		echo "$spkrID-$uttID $trans" >> $dataType/text
		
		# Write to wav.scp file according to its format
		echo "$recordingID $extendedFilename" >> $dataType/wav.scp

		# Write to utt2spk file according to its format
		echo "$spkrID-$uttID $spkrID" >> $dataType/utt2spk
		
		# If this line is the last line
		if [ "$linenumber" -eq "$totlines" ]; then
			
                        length=$(soxi -D "$extendedFilename") 
                        # Write to segments file according to its format
                        echo "$spkrID-$uttID $recordingID $previousBegin $length" >> $dataType/segments
		fi

	fi
	
	if [[ $line == "<begin"* ]]
	then
		begin=$(cut -d ":" -f 4 <<< "$line")
		beginspkrID=$(cut -d ":" -f 2 <<< "$line")
		beginuttID=$(cut -d ":" -f 3 <<< "$line")
	
	fi	
	
	if [[ $line == "<end"* ]]
	then 
		end=$(cut -d ":" -f 4 <<< "$line")
		endspkrID=$(cut -d ":" -f 2 <<< "$line")
		enduttID=$(cut -d ":" -f 3 <<< "$line")

		if [[ $previousLine == "<begin"* ]] && [[ $beginspkrID == $endspkrID ]] && [[ $beginuttID == $enduttID ]]

		then
			trans="<SIL>"
			spkrID=$endspkrID
			uttID=$enduttID
			extendedFilename=$(cut -d ":" -f 5 <<< $line)
			recordingID=$uttID

			# Split spkr into train, test or dev portion of data if needed
                	if [[ $spkrID != $previousSpkr ]]
                	then
                        	number=$(awk -v seed="$RANDOM" 'BEGIN{srand(seed);print rand()}')
                        	if (( $(echo "$number < $proptrain" | bc -l) ))
                        	then
                                	dataType="data/train"
                        	elif (( $(echo "$number > $proptest" | bc -l) ))
                       		then
                                	dataType="data/test"
                        	else
                                	dataType="data/dev"
                        	fi
                	fi
                	
			previousSpkr=$spkrID

			# Write to text file according to 'text' file format
        	        echo "$spkrID-$uttID $trans" >> $dataType/text
                
                	# Write to wav.scp file according to its format
                	echo "$recordingID $extendedFilename" >> $dataType/wav.scp

                	# Write to utt2spk file according to its format
                	echo "$spkrID-$uttID $spkrID" >> $dataType/utt2spk

			# Write to segments file according to its format
			echo "$spkrID-$uttID $recordingID $begin $end" >> $dataType/segments
			
			previousBegin=$begin
			segmented="1"
		fi
	fi

	if [[ $line == "<NEW TRS FILE>"  ]]
	then
		if [[ $beginspkrID != "" ]] && [[ $previousLine != "<"* ]] &&  [[ $beginspkrID == $spkrID ]] && [[ $beginuttID == $uttID ]]
		then
			wav=$(cut -d ":" -f 4 <<< "$previousLine")	
			length=$(soxi -D "$wav") 
			# Write to segments file according to its format
			echo "$spkrID-$uttID $recordingID $begin $length" >> $dataType/segments
			
			previousBegin=$begin

	                if (( $(echo "$begin > $length" | bc -l) )); then
        	                echo "WARNING: Will discard $spkrID-$uttID because it is badly formatted where begin is $begin and end is $length"
	                        discardID="$spkrID-$uttID"
	                        discardutt+=( $discardID )
        	                discardID="$recordingID"
                	        discardrecord+=( $discardID )
			fi
			segmented="1"
		fi
		
		begin=""
		beginspkrID=""
		beginuttID=""

		end=""
		endspkrID=""
		enduttID=""
	fi

	if [[ $segmented == "0" ]] && [[ $beginspkrID != ""  ]] && [[ $beginspkrID == $endspkrID ]] && [[ $beginspkrID == $spkrID ]] && [[ $beginuttID == $enduttID ]] && [[ $beginuttID == $uttID ]]
	then
		if (( $(echo "$begin > $end" | bc -l) )); then
			echo "WARNING: Will discard $spkrID-$uttID because it is badly formatted where begin is $begin and end is $end"
                        discardID="$spkrID-$uttID"
                        discardutt+=( $discardID )
                        discardID="$recordingID"
                        discardrecord+=( $discardID )
		fi
		echo "$spkrID-$uttID $recordingID $begin $end" >> $dataType/segments
		previousBegin=$begin
	fi
	previousLine=$line

	segmented="0"

done < "$file"

# Create spk2utt file in data/train, data/test and data/dev
echo "Creating 'spk2utt' files in 'data/train', 'data/test' and 'data/dev'..."
# Discard certain utterances and sort the files
for dir in data/train data/dev data/test; do
	#  Discard all the discard utterances
	for file in text utt2spk wav.scp segments; do
		if [[ $file != "wav.scp" ]]; then
			for utterance in "${discardutt[@]}"; do
				echo "Removing utterance $utterance from $dir/$file to clean data..."
				sed -i "/$utterance/d" $dir/$file
			done
		else
			for recording in "${discardrecord[@]}"; do
				echo "Removing record-ID $recording from $dir/$file to clean data..."
				sed -i "/$recording/d" $dir/$file
			done
		fi

	done

	# Remove all floating hyphens and hyphens in words except for hyphens in hyphenated words, in the transcription text
	sed -i 's/\( \|^\)-\([A-Z]\)/\1\2/g; s/\( \|^\)-\(\|^\)/\1\2/g; s/\([A-Z]\)-\( \|$\)/\1\2/g' $dir/text

	#Sort Files
        sort -o $dir/text $dir/text
        sort -o $dir/utt2spk $dir/utt2spk
        sort -o $dir/wav.scp $dir/wav.scp
        sort -o $dir/segments $dir/segments

        utils/utt2spk_to_spk2utt.pl $dir/utt2spk > $dir/spk2utt

done

for dir in data/train data/test data/dev
do
        # Find unique characters in each 'text' file
        grep -o  . $dir/text | sort -u >> local/uniqchar_tmp.txt

        # List all event labels from transcription
        grep -o "<[A-Z]*.>" $dir/text | sort -u >> local/tags_tmp.txt

	# Replace event labels with <SPOKEN_NOISE>, <NOISE> or !SIL
	sed -i 's/<B>/<SPOKEN_NOISE>/g; s/<BR>/<SPOKEN_NOISE>/g; s/<COUGH>/<NOISE>/g; s/<GARB>/<NOISE>/g; s/<SIL>/!SIL/g; s/<UU>/<SPOKEN_NOISE>/g' $dir/text

done

echo "Listing all unique characters in 'text' file to 'local/uniqchar.txt'..."
# Create local/uniqchar.txt which lists all the unique characters in local/text file
cat local/uniqchar_tmp.txt | sort -u > local/uniqchar.txt
rm local/uniqchar_tmp.txt

# Find a list of all the event labels <> from transcription 
echo "Listing all event labels in 'local/tags.txt'..."
cat local/tags_tmp.txt | sort -u > local/tags.txt
rm local/tags_tmp.txt

# Make a spkrs file in data/train data/test and data/dev listing the number of unique speakers
for dir in train test dev; do
        cat data/$dir/utt2spk | cut -d "-" -f 1 > data/$dir/spkrs_tmp && sort -u data/$dir/spkrs_tmp > data/$dir/spkrs
        rm data/$dir/spkrs_tmp
done
