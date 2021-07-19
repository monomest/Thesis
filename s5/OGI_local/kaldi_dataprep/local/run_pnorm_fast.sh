#!/bin/bash

# This is p-norm neural net training, with the "fast" script, on top of adapted
# 40-dimensional features.
# This version uses 460 hours of "clean" (typically relatively un-accented)
# training data.
# We're using 6 jobs rather than 4, for speed.

# Note: we highly discourage running this with --use-gpu false, it will
# take way too long.

train_stage=-10
use_gpu=true

. ./cmd.sh
. ./path.sh
. utils/parse_options.sh


if $use_gpu; then
  if ! cuda-compiled; then
    cat <<EOF && exit 1
This script is intended to be used with GPUs but you have not compiled Kaldi with CUDA
If you want to use GPUs (and have them), go to src/, and configure and make on a machine
where "nvcc" is installed.
EOF
  fi
  #parallel_opts="--gpu 1"
  num_threads=1
  minibatch_size=512
  dir=exp/nnet_pnorm_fast_gpu_raw_temp
else
  # with just 4 jobs this might be a little slow.
  num_threads=16
  parallel_opts="--num-threads $num_threads"
  minibatch_size=128
  dir=exp/nnet6a_clean_460
fi

. ./cmd.sh
. utils/parse_options.sh


steps/nnet2/train_pnorm_fast.sh --stage $train_stage \
   --samples-per-iter 400000 --mix-up 10000\
   --num-epochs 7 --num-epochs-extra 3 \
   --parallel-opts "$parallel_opts" \
   --num-threads "$num_threads" \
   --minibatch-size "$minibatch_size" \
   --num-jobs-nnet 1  \
   --initial-learning-rate 0.01 --final-learning-rate 0.001 \
   --num-hidden-layers 4 \
   --pnorm-input-dim 1000 --pnorm-output-dim 200 \
   --cmd "$decode_cmd" --feat-type raw \
    data/train data/lang exp/tri3b_ali $dir || exit 1
#fi
'''
steps/nnet2/decode.sh --nj 1 --cmd "$decode_cmd" \
    --transform-dir exp/tri3b/decode \
    exp/tri3b/graph data/test $dir/decode || exit 1;

'''
steps/nnet2/decode.sh --nj 1 --cmd "$decode_cmd" --skip_scoring true\
    exp/tri3b/graph data/test $dir/decode || exit 1;

local/score.sh data/test/ data/lang/ $dir/decode/

exit 0;
