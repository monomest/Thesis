# myst_get_uttid.sh
# Author: Renee Lu
# About: This gets the utterance IDs of the MyST files

MYST_ROOT=$1

# Getting list of utterance-IDs
FILE=$MYST_ROOT/transcripts.txt-copy	# Transcripts reference file
UTTID=local/myst_uttid.txt      	# Output file
echo "Creating $UTTID ..."
while read line; do
        uttid=$(cut -d ' ' -f1 <<< "$line")
        echo "$uttid" >> $UTTID
done < $FILE


