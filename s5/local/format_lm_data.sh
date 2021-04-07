# format_lm_data.sh
# Author: Renee Lu
# About: This code formats the Language Model file scripted_txt.tmp
#        To be run in s5 directory.

file=$1
sed -i "s/MS. /MS /g; s/MRS. /MRS /g; s/MR. /MR /g; s/\&/AND/g" $file
sed -i "s/\. /\n/g; s/\.\"/\n/g; s/\?/\n/g; s/\!/\n/g; s/\,\"//g; s/\"//g; s/\,//g; s/\;//g; s/\://g; s/\.//g; s/(//g; s/)//g" $file
sed -i 's/\( \|^\)-\([A-Za-z]\)/\1\2/g; s/\( \|^\)-\( \|^\)/\1\2/g; s/\([A-Za-z]\)-\( \|$\)/\1\2/g; s/- / /g' $file
sed -i 's/\( \|^\)-\([[:punct:]]\)/\1\2/g; s/\([[:punct:]]\)-\( \|$\)/\1\2/g' $file
sed -i 's/ '\''/ /g; s/'\''\( \|$\)//g; s/'\'' / /g' $file
sed -i "s/FIRE- TILL/FIRE TILL/g" $file
# Replace all tabs and spaces with a single space
sed -i "s/[[:space:]]\+/ /g" $file
# Remove all leading whitespaces
sed -i 's/^[ \t]*//' $file
sed -i '/^$/d' $file

