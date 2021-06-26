# myst_prep.sh
# Author: Renee Lu
# About: This code prepares the MyST dataset for kaldi model building. 
#        Run from s5 directory

MYST_ROOT=/srv/scratch/chacmod/MyST	# Path to data
MYST_AUDIO=/srv/scratch/chacmod/MyST/myst-v0.3.0-171fbda/corpora/myst/data # Path to audio data
CUR_DIR=/srv/scratch/chacmod/tools/kaldi/egs/tlt_school/s5	# s5 directory
DATA_DIR=data
DATA_TRAIN_DIR=$DATA_DIR/train_myst

# Make data directories if they do not exist
[ -d $DATA_DIR ] || mkdir $DATA_DIR
[ -d $DATA_TRAIN_DIR ] || mkdir $DATA_TRAIN_DIR

# This gets the tags and transcription from the MyST transcription
local/myst_get_tags.sh $MYST_ROOT $CUR_DIR

# This applies some fixes to the transcription local/myst_trans.txt
echo "Applying some fixes to transcription..."
local/myst_fix.sh

# This replaces the tags with the proper labels: @hes @sil @unk_en @noise @discard
echo "Replacing tags with proper labels..."
local/myst_replace_tags.sh

# This normalises the transcription
echo "Normalising transcription..."
local/myst_normalise.sh

# Getting list of utterance-IDs
echo "Getting list of utterance-IDs..."
local/myst_get_uttid.sh $MYST_ROOT

# Combine utterance IDs and normalised transcription together
# Output: local/myst_text.txt-tmp
UTTID=local/myst_uttid.txt
TRANS=local/myst_trans_normal.txt
OUTPUT=local/myst_text.txt-tmp
paste -d " " $UTTID $TRANS > $OUTPUT

# Discard utterances if the entire utterance is @sil @noise or @discard 
echo "Discarding utterances if the entire utterance is silence, noise or discard..."
local/myst_remove_discards.sh

# Create text, wav.scp utt2spk and spk2utt files
echo "Creating MyST text, wav.scp, utt2spk and spk2utt files"
local/myst_create_datafiles.sh $DATA_TRAIN_DIR $MYST_AUDIO
