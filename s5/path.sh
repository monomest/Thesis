# path.sh
# Author: kaldi
# About: This code defines some paths used in run.sh

# Defining Kaldi root directory
export KALDI_ROOT=`pwd`/../../..

# Setting paths to useful tools
export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$PWD:$PATH
[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1
. $KALDI_ROOT/tools/config/common_path.sh

# Variable needed for proper data sorting
export LC_ALL=C
