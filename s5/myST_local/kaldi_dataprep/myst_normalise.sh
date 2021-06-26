# myst_normalise.txt
# Author: Renee Lu
# About: This cleans up and normalises the transcription for MyST dataset
#        Run from s5 directory, and uses local/myst_trans_labelled.txt
# Output: local/myst_trans_normal.txt: normalised transcription
#         local/myst_uniqchar_normalised.txt: unique characters in normalised transcription

FILE=local/myst_trans_labelled.txt
OUT=local/myst_trans_normal.txt		 	# Output file
UCHAR=local/myst_uniqchar_normalised.txt        # Output file

# Remove floating < + [ ) > / and remove/replace these characters ‘ ’ – … Â
echo "Cleaning up the transcription $FILE..."
sed "s/+/ /g; s/</ /g; s/\[/ /g; s/)/ /g; s/>/ /g; s/\// /g; s/‘/'/g; s/’/'/g; s/–/-/g; s/…/ /g; s/ / /g; s/Â/ /g; s/ / /g" $FILE > $OUT

# Insert a space when there is a number followed by a letter or vice versa
sed -i "s/\([0-9]\)\([a-zA-Z]\)/\1 \2/g; s/\([a-zA-Z]\)\([0-9]\)/\1 \2/g" $OUT

# 1. Converts numbers to written words using num2words from python
python3 local/number2words.py $OUT

# 2. Converts text to lowercase
sed -i 's/\(.*\)/\L\1/' $OUT

# 3. Deals with "mr. " "mrs. " and "ms. "
sed -i "s/ms\. /ms /g; s/mrs\. /mrs /g; s/mr\. /mr /g" $OUT

# 4. Replaces "&" with "and"
sed -i "s/\&/ and /g" $OUT

# 5. Replaces full stop , ." , ? and ! with a space
sed -i "s/\. / /g; s/\.\"/ /g; s/\?/ /g; s/\!/ /g" $OUT

# 6. Replaces hyphens with spaces
sed -i "s/-/ /g" $OUT

# 7. Remove all punctuation besides single quotes and replace with a single space
sed -i "s/\,\"/ /g; s/\"/ /g; s/\,/ /g; s/\;/ /g; s/\:/ /g; s/\./ /g; s/(/ /g; s/)/ /g" $OUT

# 8. Remove single quotes only if the pattern is [A-Z]'[A-Z], else replace single quotes with single spacee
sed -i 's/ '\''/ /g; s/'\''\( \|$\)/ /g; s/'\'' / /g' $OUT

# 9. Remove all tabs and spaces with a single space
sed -i "s/[[:space:]]\+/ /g" $OUT

# 10. Remove all leading and trailing whitespaces
sed -i 's/^[[:blank:]]*//;s/[[:blank:]]*$//' $OUT

# Listing all unique characters in normalised transcription
echo "Creating $UCHAR ..."
cat $OUT | fold -w1 | sort -u > $UCHAR
