# myst_fix.sh
# Author: Renee Lu
# About: This applies fixes to the transcription

FILE=local/myst_trans.txt

# Fixes poor transcription 12345
sed -i 's/12345/1 2 3 4 5/' $FILE
