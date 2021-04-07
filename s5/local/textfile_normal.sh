# textfile_normal.sh
# Author: Renee Lu
# About: This code normalises the transcription text from
#        the files 
#        data/train/text
#        data/test/text
#        data/dev/text
# Output: The files themselves will be changed so that the transcription is normalised. 

for file in data/train/text data/test/text data/dev/text; do
	touch $file-uttID.tmp
	touch $file-text.tmp

	while IFS= read -r line
	do
		uttID=$(cut -d " " -f 1 <<< "$line")
		echo "$uttID" >> $file-uttID.tmp
		trans=$(cut -d' ' -f2- <<< "$line")
		echo "$trans" >> $file-text.tmp
	done < "$file"

	# 1. Converts numbers to written words using num2words from python
	python3 local/number2words.py $file-text.tmp

	# 3. Deals with "MR. " "MRS. " and "MS. "
	sed -i "s/MS\. /MS /g; s/MRS\. /MRS /g; s/MR\. /MR /g" $file-text.tmp
	
	# 4. Replaces "&" with "AND"
	sed -i "s/\&/AND/g" $file-text.tmp

	# 6. Replaces hyphens with spaces
	sed -i "s/-/ /g" $file-text.tmp
 
	# 9. Remove all tabs and spaces with a single space
	sed -i "s/[[:space:]]\+/ /g" $file-text.tmp

	# 10. Remove all leading and trailing whitespaces
	sed -i 's/^[[:blank:]]*//;s/[[:blank:]]*$//' $file
	
	paste -d " " $file-uttID.tmp $file-text.tmp > $file-tmp
	cat $file-tmp > $file
	rm $file-tmp

done
