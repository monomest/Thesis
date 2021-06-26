# myst_get_tags.sh
# About: This code gets all the tags from MyST data
#        To be run from s5 directory.
# Output:
#         local/myst_uniqchar.txt: all unique characters in transcription 
#         local/myst_tags.txt: all the tags and labels from transcription
#	  local/myst_trans.txt: the transcription by itself
#	  MYST_ROOT/transcripts.txt-copy: copy of transcript which we work with
MYST_ROOT=$1
CUR_DIR=$2
#MYST_ROOT=/srv/scratch/chacmod/MyST
#CUR_DIR=/srv/scratch/chacmod/tools/kaldi/egs/tlt_school/s5
FILE=transcripts.txt    # File which has the transcription information
FILE=$MYST_ROOT/$FILE
cp $FILE $FILE-copy
FILE=$FILE-copy

UCHAR=local/myst_uniqchar.txt        # Output file
TRANS=local/myst_trans.txt           # Output file
TAGS=local/myst_tags.txt             # Output file
touch $UCHAR
touch $TRANS
touch $TAGS

# Remove all the extra spaces and replace with a single space
sed -i "s/[[:space:]]\+/ /g" $FILE

# Create local/myst_trans.txt
echo "Creating $TRANS ..."
while read line; do
	fields=$(echo "$line" | grep -o " " | wc -l)
	if [ $fields -gt 0 ]; then
		trans=$(cut -d ' ' -f2- <<< "$line")
		echo "$trans" >> $TRANS
	else
		trans="<discard>"
		echo "$trans" >> $TRANS
	fi
done < $FILE

dos2unix -q $TRANS

echo "Creating $UCHAR ..."
# Create local/myst_uniqchar by getting all the unique characters
cat $TRANS | fold -w1 | sort -u > $UCHAR

echo "Creating $TAGS ..."
# Create local/myst_uniqchar by getting all the tags and labels for < >
echo "Getting the tags < >"
grep -o "<[^>]*>" $TRANS | sort -u >> $TAGS
# ( )
echo "Getting the tags ( )"
grep -o "([^)]*)" $TRANS | sort -u >> $TAGS
# []
echo "Getting the tags [ ]"
grep -o "\[[^]]*\]" $TRANS | sort -u >> $TAGS
# + +
echo "Getting the tags + +"
grep -o "\+[^+]*+" $TRANS | sort -u >> $TAGS
# * *
echo "Getting the tags * *"
grep -o "\*[[:graph:]]*\*" $TRANS | sort -u >> $TAGS
