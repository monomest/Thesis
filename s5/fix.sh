# fix.sh
# Author: Renee Lu
# About: This code fixes any edge case files in the CU Kids Speech Corpus data.

CU_ROOT=$1

# Fixes the badly formatted .trs transcription file
file=$CU_ROOT/spk-04-013/sentences/spk-04-013-sent006.trs
fixfile=fix0.txt
echo "Fixing the badly formatted .trs transcription file '$file'..."
cat $fixfile > $file
