# analyse_diff_output.sh
# Author: Renee Lu
# About: This code compares two different kaldi hypotheses side by side.
#        To be run in the s5 directory.
# Output: local/name-diff.txt

dira=nnet3_vp
filea=17-hyp.txt

dirb=tri3b_mmi
fileb=17-hyp.txt

output=local/output/$dira-$dirb-diff

# Get diff file of everything
echo "Comparing $dira/$filea | $dirb/$fileb" > $output
diff -y local/output/$dira/$filea local/output/$dirb/$fileb $ref >> $output

# Get diff file suppressing common lines
echo "Comparing $dira/$filea | $dirb/$fileb suppressing common lines" > $output-diff
diff -y --suppress-common-lines local/output/$dira/$filea local/output/$dirb/$fileb $ref >> $output-diff
