# analyse_output.sh
# Author: Renee Lu
# About: This code gives you the hypothesised output of the built ASR system
#        and the reference (correct) output of the data. 
#        It also gives you a file which lists the difference between the hypothesis
#        and the reference. 
#        To be run from the s5 directory.
# Output: local/output files

#stage=tri3b
#OUT_DIR=exp/$stage/decode/scoring    # Directory of the output
#stage=tri3b_mmi
#OUT_DIR=exp/$stage/decode2/scoring
stage=nnet3_vp
OUT_DIR=exp/$stage/tdnn/decode_test_hires/scoring
output=local/output    # Path to our created output files
mkdir -p $output
output=$output/$stage
mkdir -p $output

# List of all hypothesis files
tra=$(find $OUT_DIR -type f -name "*.tra")
# Iterate through all the hypothesis files, convert them from int to text and save to local/output
echo "Converting hypothesis files from int to text..."
for hyp in $tra; do
        # Get the name of the .tra file
        #name=$(cut -d "/" -f 5 <<< "$hyp")
    	#name=$(cut -d "." -f 1 <<< "$name")
        name=$(cut -d "/" -f 6 <<< "$hyp")
        name=$(cut -d "." -f 1 <<< "$name")
        # Get the hypothesised transcription of the .tra file, converting from int to text
        # Output this to local/output/$name.txt
        #cat $hyp | utils/int2sym.pl -f 2- exp/$stage/graph/words.txt > $output/$name-hyp.txt
        cat $hyp | utils/int2sym.pl -f 2- exp/tri3b/graph/words.txt > $output/$name-hyp.txt
done

# Copy the reference text into local/output
cp $OUT_DIR/test_filt.txt $output/ref.txt

# Sort the hyp files in local, in case they are out of order
txt=$(find $output -type f -name "*.txt")
echo "$txt"
for file in $txt; do
	# Sort by first field, which is utterance ID
	sort -n -o $file $file -t ' ' -k1
done

echo "Creating diff files..."
# Iterate through all the newly created hypothesis files and create a diff file 
# comparing hypothesis to reference text
hypfiles=$(find $output -type f -name "*-hyp.txt")
for hyp in $hypfiles; do
	# Get the name of the file
	name=$(cut -d "/" -f 4 <<< "$hyp")
	name=$(cut -d "-" -f 1 <<< "$name")
	# Output the difference in columns
	diff -y $hyp $output/ref.txt > $output/$name-diff.txt
done
