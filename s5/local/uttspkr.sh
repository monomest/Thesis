# uttspkr.sh
# Author: Renee Lu
# About: This code gets all the information about utterances and speakers, so that this information
#        can be formatted by other scripts according to kaldi data preparation requirements. 
# Output: 'local/uttInfo.txt' which is a file that contains all the needed information for data preparation.

CU_ROOT=$1    # Path to speech corpus
CUR_DIR=$2    # Path to s5 directory

# Go into CU Kids' Speech Corpus directory
cd $CU_ROOT

# Let the lowest utterance-ID be 10000
uttID=10000

# Iterate through all the speaker's 'story' and 'sentences' folder to
# create a list of the utterances, their times, their speakers, and their filename and path
for dir in spk*/
do
	spkr=$(echo $dir | cut -d '-' -f 2,3 | sed 's/[^0-9]*//g')
	cd $dir
	for subdir in story/ sentences/ summary/
	do
		if [ -d "$subdir" ] 
		then
			cd $subdir
            for trans in *.trs
			do
                [ -e "$trans" ] || echo "WARNING: No .trs files exists in '$dir$subdir' Skipping this directory." 
                [ -e "$trans" ] || break
                firstiter=0
			    begin=1
			    end=0
			    start=0
			    audiopath=$(readlink -f $trans | sed 's/....$//')
			    audiopath=$(echo "${audiopath}.wav")
			    [[ -e "$audiopath" ]] || echo "WARNING: '$audiopath' does not exist. Skipping the .trs file."
			    [[ -e "$audiopath" ]] || break
			    echo "<NEW TRS FILE>" >> $CUR_DIR/local/uttInfo.txt
			
			    while IFS= read -r line
			    do
				    # When the transcription starts
				    if [[ $line == *"<Turn startTime"* ]]
				    then
					    start=1
					    firstiter=1
				    fi

				    # Print the time
				    if [[ $line == *"<Sync time"* ]] && [[ $start -eq 1 ]]
	   			    then
					    time=`echo "$line" | cut -d '"' -f 2`
					    if [[ $begin -eq 1 ]] && [[ $firstiter -eq 1 ]]
					    then
						    echo "<begin:$spkr:$uttID:$time:$audiopath" >> $CUR_DIR/local/uttInfo.txt
						    begin=0
						    firstiter=0
					    else
						    echo "<end:$spkr:$((uttID-1)):$time:$audiopath" >> $CUR_DIR/local/uttInfo.txt
						    echo "<begin:$spkr:$uttID:$time:$audiopath" >> $CUR_DIR/local/uttInfo.txt
					    fi		
				    fi

				    # Print the transcription
				    if [[ $line != *"<"* ]] && [[ start -eq 1  ]]
				    then
						line=$(echo "$line" | tr -d '\r')
						echo "$spkr:$uttID:$line:$audiopath" >> $CUR_DIR/local/uttInfo.txt
					    uttID=$((uttID+1))
				    fi
				done < $trans
			done
			cd ../
		fi		
	done
	cd ../
done
echo "SUCCESS: Created a list of all utterance, speaker, filename and timing information in 'local/uttInfo.txt'"
