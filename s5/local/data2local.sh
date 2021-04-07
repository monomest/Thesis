# data2local.sh
# Author: Renee Lu
# About: This code copies the segments, spkrs, txt, utt2spk and wav.scp
#        files in data/train, data/test and data/dev directories into
#        local/data/train, local/data/test and local/data/dev
# Output: Refer to above

CUR_DIR=$1

# Copy all the dev, test and train files into local
for dir in data/dev data/test data/train; do
	mkdir -p $CUR_DIR/local/$dir
	for file in segments spkrs text utt2spk wav.scp spk2utt; do
		cp $CUR_DIR/$dir/$file $CUR_DIR/local/$dir/$file
	done
done
