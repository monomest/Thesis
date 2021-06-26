# myst_remove_discards.sh
# Author: Renee Lu
# About: This code discards utterances in local/myst_text.txt-tmp 
#        if the entire utterance is @sil @noise or @discard 
# Output: local/myst_text.txt
	
INFILE=local/myst_text.txt-tmp
FILE=local/myst_text.txt

cp $INFILE $FILE

# Remove utterance if it is just @sil @noise or @discard
sed -i '/.*[0-9] @sil$/d; /.*[0-9] @noise$/d; /.*[0-9] @discard$/d;' $FILE

# Delete leftover @discard labels
sed -i 's/ @discard / /g' $FILE
