# number2words.py
# Author: Martin Evans, https://stackoverflow.com/questions/40040177/search-and-replace-numbers-with-words-in-file
#         Modified by Renee Lu
# About: Searches and replaces numbers with words in a file.
# Output: Edits the original input file. 

import re
import num2words
import argparse

def Convert_Num(infile):

	with open(infile) as f_input:
		text = f_input.read()

	text = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), text)

	with open(infile, 'w') as f_output:
    		f_output.write(text)

	return

def ArgParser():
	parser = argparse.ArgumentParser(description='This code for converting numbers into written words in a file.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('infile',  help='The input file', type=str)
	return parser.parse_args()

if __name__ == '__main__':
	args = ArgParser()    
	infile=args.infile
	Convert_Num(infile)    
