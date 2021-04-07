# cmd.sh
# Author: kaldi
# About: You can change this code depending on which type of queue you are using.
#        If you have no queueing system and want to run on local machine, you can
#	 change all instances of 'queue.pl' to 'run.pl'

export train_cmd="run.pl"
export decode_cmd="run.pl"
export mkgraph_cmd="run.pl"
#export train_cmd="queue.pl" --mem 2G
#export decode_cmd="queue.pl" --mem4G
#export mkgraph_cmd="queue.pl" --mem 8G
