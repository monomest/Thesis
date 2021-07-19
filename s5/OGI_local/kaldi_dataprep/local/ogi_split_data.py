#!/usr/bin/env python3

import argparse
import pandas as pd
from glob import glob
from os.path import join, isdir
from split_path import Split_Path
from random import shuffle

#This function should split the speakers in the OGI data into train, dev, test. Based on the determined portions.
#Speakers selection done randomly so every time this script run different split will be out.
def Split_Data(sOGIDir, sTrainSpkFile, sTestSpkFile, sDevSpkFile, fTestPortion = 0.15, fDevPortion = 0.15, fTrainPortion = -1):
    #TO DO: Check if 'docs' exist first and return with error
    assert fTestPortion + fDevPortion + fTrainPortion <= 1, "Summation of portions should not exceed 1"
    lTrainSpks, lTestSpkrs, lDevSpkrs = [], [], []
    for sVerFile in glob(join(sOGIDir,'docs','*-verified.txt')):
        with open(sVerFile,'r') as f:
            lLines = f.read().splitlines()
        lSpkrs = set([Split_Path(l.split()[0])[-2] for l in lLines])
        nSpkrs = len(lSpkrs)
        nTestSpkrs = int(nSpkrs * fTestPortion)
        nDevSpkrs = int(nSpkrs * fDevPortion)
        if fTrainPortion == -1: #Use all remaining spkrs for Training
            nTrainSpkrs = nSpkrs - (nTestSpkrs + nDevSpkrs)
        else:
            nTrainSpkrs = int(nSpkrs * fTrainPortion)
        lSpkrs = list(lSpkrs)
        shuffle(lSpkrs)
        for l,n in zip((lTrainSpks, lTestSpkrs, lDevSpkrs),(nTrainSpkrs,nTestSpkrs,nDevSpkrs)):
            l.extend(lSpkrs[:n])
            del lSpkrs[:n]
    with open(sTrainSpkFile,'w') as flTrain, open(sTestSpkFile,'w') as flTest, open(sDevSpkFile,'w') as flDev:
        print('\n'.join(lTrainSpks), file=flTrain)
        print('\n'.join(lTestSpkrs), file=flTest)
        print('\n'.join(lDevSpkrs),  file=flDev)
    return

def ArgParser():
    parser = argparse.ArgumentParser(description='This code for spliting the OGI Kids dataset into Train, Test and Dev based on speakers', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('OGI_Dir',  help='The path to the main directory of OGI data', type=str)
    parser.add_argument('Train_Spkrs_File', help='The path to the file to write the list of training speakers', type=str)
    parser.add_argument('Test_Spkrs_File', help='The path to file to write the list of test speakers', type=str)
    parser.add_argument('Dev_Spkrs_File', help='The path to file to write the list of dev speakers', type=str)
    parser.add_argument('-t','--train_portion', dest='tr_pr', help='The percentatge of speakers used for training', type=float, default=-1)
    parser.add_argument('-s','--test_portion', dest='tst_pr', help='The percentatge of speakers used for testing', type=float, default=0.15)
    parser.add_argument('-d','--dev_portion', dest='dev_pr', help='The percentatge of speakers used for developing', type=float, default=0.15)
    return parser.parse_args()

if __name__ == '__main__':
    args = ArgParser()
    sOGIDir, sTrainSpkFile, sTestSpkFile, sDevSpkFile, fTrainPortion, fTestPortion, fDevPortion = args.OGI_Dir, args.Train_Spkrs_File, args.Test_Spkrs_File, args.Dev_Spkrs_File, args.tr_pr, args.tst_pr, args.dev_pr
    print(args)
    Split_Data(sOGIDir, sTrainSpkFile, sTestSpkFile, sDevSpkFile, fTestPortion, fDevPortion, fTrainPortion)


    

