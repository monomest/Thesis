# myst_create_datafiles.sh
# Author: Renee Lu
# About: This code creates the files text, wav.scp and utt2spk
#        for the MyST corpus
# Output: text
#         wav.scp
#         utt2spk

DATA_TRAIN_DIR=$1
MYST_AUDIO=$2

# Create text_myst
TEXT=$DATA_TRAIN_DIR/text
FILE=local/myst_text.txt
echo "Creating $TEXT ..."
cp $FILE $TEXT

# Create wav.scp and utt2spk files
WAV=$DATA_TRAIN_DIR/wav.scp
UTT2SPK=$DATA_TRAIN_DIR/utt2spk
touch $WAV
touch $UTT2SPK

echo "Creating $WAV and $UTT2SPK ..."
while IFS= read -r line
do
        uttid=$(cut -d ' ' -f1 <<< "$line")
	myst=$(cut -d "_" -f 1 <<< $uttid)
        dir=$(cut -d "_" -f 2 <<< $uttid)
        date=$(cut -d "_" -f 3 <<< $uttid)
        date2=$(cut -d "_" -f 4 <<< $uttid)
        MX=$(cut -d "_" -f 5 <<< $uttid)
        point=$(cut -d "_" -f 6 <<< $uttid)
        num=$(cut -d "_" -f 7 <<< $uttid)

        file=$MYST_AUDIO/$dir/${myst}_${dir}_${date}_${date2}_${MX}_${point}/${myst}_${dir}_${date}_${date2}_${MX}_${point}_${num}.wav
        echo "$uttid $file" >> $WAV
        echo "$uttid myst_$dir" >> $UTT2SPK

done < $TEXT

# Create spk2utt 
SPK2UTT=$DATA_TRAIN_DIR/spk2utt
echo "Creating $SPK2UTT ..."
utils/utt2spk_to_spk2utt.pl $DATA_TRAIN_DIR/utt2spk > $DATA_TRAIN_DIR/spk2utt
