# myst_replace_tags.sh
# Author: Renee Lu
# About: This code maps the tags in MyST transcription to labels
#        @hes @unk_en @noise @laughs @sil
# Output: Writes to local/myst_trans_labelled.txt

INFILE=local/myst_trans.txt
FILE=local/myst_trans_labelled.txt

HESFILE=local/myst_hes.txt
LAUGHFILE=local/myst_laughs.txt
NOISEFILE=local/myst_noise.txt
SILFILE=local/myst_sil.txt
UNKFILE=local/myst_unk_en.txt
DISCARDFILE=local/myst_discard.txt

# Makes a copy of the transcription file and call it _labelled
cp $INFILE $FILE

# Map all *WORD* to WORD
echo "Mapping *WORD* to WORD..."
sed -i 's/\(\*\)\([[:graph:]]*\)\(\*\)/ \2 /g' $FILE


# Replace all the hesitation tags with '@hes' in myst_trans.txt
echo "Replacing hesitation tags with @hes..."
while IFS= read -r line
do
        sed -i "s/$line/ @hes /g" $FILE
done < $HESFILE

# Replace all the laugh tags with '@laughs' in myst_trans.txt
echo "Replacing laugh tags with @laughs..."
while IFS= read -r line
do
        sed -i "s/$line/ @laughs /g" $FILE
done < $LAUGHFILE

# Replace all the noise tags with '@noise' in myst_trans.txt
echo "Replacing noise tags with @noise..."
while IFS= read -r line
do
        sed -i "s/$line/ @noise /g" $FILE
done < $NOISEFILE

# Replace all the silence tags with '@sil' in myst_trans.txt
echo "Replacing silence tags with @sil..."
while IFS= read -r line
do
        sed -i "s/$line/ @sil /g" $FILE
done < $SILFILE

# Replace all the unknown english tags with '@unk_en' in myst_trans.txt
echo "Replacing unknown english tags with @unk_en..."
while IFS= read -r line
do
        sed -i "s/$line/ @unk_en /g" $FILE
done < $UNKFILE

# Replace all the discard tags with '@discard' in myst_trans.txt
echo "Replacing discard tags with @discard..."
while IFS= read -r line
do
        sed -i "s/$line/ @discard /g" $FILE
done < $DISCARDFILE
