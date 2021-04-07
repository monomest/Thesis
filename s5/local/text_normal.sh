# text_normal.sh
# Author: Renee Lu
# About: This code normalises the text of a given input file, writing to the input file. 
#        1. Converts numbers to written words using num2words from python
#        2. Converts all to UPPERCASE
#        3. Deals with "MR. " "MRS. " "MS. "
#           e.g "MRS. GORDON" --> "MRS GORDON"
#        4. Replaces "&" with "AND"
#        5. Replaces full stop, ." , ? and ! with a newline
#        6. Replaces hyphens with spaces
#        7. Remove all punctuation besides single quotes
#        8. Keep single quotes only if the pattern is [A-Z]'[A-Z]
#        9. Replace tabs and spaces with a single space
#        10. Remove all leading whitespaces
#        11. Remove all empty lines
# Output: This edits the input file directly.

CUR_DIR=$1	# s5 directory path
file=$2		# Input file path

# 1. Converts numbers to written words using num2words from python
python3 $CUR_DIR/local/number2words.py $file

# 2. Converts text to UPPERCASE
sed -i 's/\(.*\)/\U\1/' $file

# 3. Deals with "MR. " "MRS. " and "MS. "
sed -i "s/MS\. /MS /g; s/MRS\. /MRS /g; s/MR\. /MR /g" $file

# 4. Replaces "&" with "AND"
sed -i "s/\&/AND/g" $file

# 5. Replaces full stop, ." , ? and ! with a newline
sed -i "s/\. /\n/g; s/\.\"/\n/g; s/\?/\n/g; s/\!/\n/g" $file

# 6. Replaces hyphens with spaces
sed -i "s/-/ /g" $file

# 7. Remove all punctuation besides single quotes and replace with a single space
sed -i "s/\,\"/ /g; s/\"/ /g; s/\,/ /g; s/\;/ /g; s/\:/ /g; s/\./ /g; s/(/ /g; s/)/ /g" $file

# 8. Remove single quotes only if the pattern is [A-Z]'[A-Z], else replace single quotes with single spacee
sed -i 's/ '\''/ /g; s/'\''\( \|$\)/ /g; s/'\'' / /g' $file

# 9. Remove all tabs and spaces with a single space
sed -i "s/[[:space:]]\+/ /g" $file

# 10. Remove all leading and trailing whitespaces
sed -i 's/^[[:blank:]]*//;s/[[:blank:]]*$//' $file

# 11. Remove all empty lines
sed -i '/^$/d' $file
