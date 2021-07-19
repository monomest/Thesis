#!/usr/bin/env python3

#The main directory of the OGI data should contains docs directory

#The verification codes:
#1 Good: Only the target word is said.
#2 Maybe: Target word is present, but there's other junk in the file.
#3 Bad: Target word is not said.
#4 Puff: Same as good, but w/ an air puff.

#The naming convention:
#ks000820 --> ks[1gradeid][2spkcode][2uttid]0
#gradeid: K --> 0,b 
#         1 --> 1,c 
#         2 --> 2,d 
#         3 --> 3,e 
#         4 --> 4,f 
#         5 --> 5,g 
#         6 --> 6,h 
#         7 --> 7,i 
#         8 --> 8,j 
#         9 --> 9,k 
#         10 --> a,l 
#Uttid 2 digits, check docs/all.map for scripted
#Uttid is xx for spontaneous speech

import pandas as pd
import numpy as np
import glob, sys
from os.path import join, isfile, splitext, basename, normpath
import argparse
import re

re.DOTALL

dGrad2Int = {
        '0' : 0,
        'b' : 0,
        '1' : 1,
        'c' : 1,
        '2' : 2,
        'd' : 2,
        '3' : 3,
        'e' : 3,
        '4' : 4,
        'f' : 4,
        '5' : 5,
        'g' : 5,
        '6' : 6,
        'h' : 6,
        '7' : 7,
        'i' : 7,
        '8' : 8,
        'j' : 8,
        '9' : 9,
        'k' : 9,
        'a' : 10,
        'l' : 10
        }
#There are different type of noise tags in the OGI trans files see https://catalog.ldc.upenn.edu/docs/LDC2006S35/labeling.pdf for details.
#Here each tag converted to a noise symbole, the dictionary has the tag as key and tuple with two symbol values, when connected to a word and when not connected.

dNoiseTag2Symb = {
        "<asp>"  : ('',''), #heavily aspirated p, t, or k or puff at end of word
        "<beep>" : ('',''), #a beep sound
        "<blip>" : ('',''), #temp signal blip signal goes completely silent for a period
        "<bn>"   : ('','<NOISE>'), #Background noise
        "<br>"   : ('','<NOISE>'), #breathing noise
        "<bs>"   : ('','<SPOKEN_NOISE>'), #background speech
        "<cough>": ('','<NOISE>'), # cough sound
        "<ct>"   : ('','<NOISE>'), # a clear throat
        "<fp>"   : ('','<SPOKEN_NOISE>'), #generic filled pause/false start
        "<lau>"  : ('',''), # ??
        "<laugh>": ('<SPOKEN_NOISE>','<SPOKEN_NOISE>'), #laughter
        "<ln>"   : ('','<NOISE>'), # line noise
        "<long>" : ('',''), #elongated word
        "<ls>"   : ('','<NOISE>'), #lip smack
        "<n>"    : ('',''), # ??
        "<nitl>" : ('',''), # need special handeling, used for forigen language, can remove all and replace with SN --
        "<ns>"   : ('','<NOISE>'), # non-speech sound
        "<pau>"  : ('','!SIL'), # Silence/pause
        "<pf>"   : ('',''), # ??
        "<pron>" : ('',''), # Also need special handeling --
        "<sing>" : ('',''), #Singing
        "<sneeze>": ('','<NOISE>'), #Sneezing
        "<sniff>": ('','<NOISE>'), #sniffing
        "<sp>"   : ('',''), #Unkown spelling -- 
        "<tc>"   : ('<NOISE>','<NOISE>'), #tongue click
        "<uu>"   : ('<SPOKEN_NOISE>','<SPOKEN_NOISE>'), #unintelligible speech
        "<whisper>": ('',''), #whispered speech
        "<yawn>" : ('',''), #yawn
        }

#Function to replace the tag with symbol, return first element in the dNoiseTag2Symb tuble if connected and second element if not

def replace(match):
  if match.group(1).isalpha() or match.group(3).isalpha(): 
    symb = dNoiseTag2Symb[match.group(2)][0]
  else:
    symb = dNoiseTag2Symb[match.group(2)][1]
  return ' '.join([match.group(1),symb,match.group(3)])

def apply_re_on_files(lFiles,lRe,isUpper=False):
    lTrans = []
    for sFile in lFiles:
        with open(sFile,'r') as f:
            sContent = ' '.join(f.read().splitlines()) # some files has more than one line, merge them so one string returned for each file
        for ptrn,repl in lRe:
            sContent = ptrn.sub(repl,sContent)
        if isUpper:
            sContent = sContent.upper()
        lTrans.append(sContent)
    return lTrans

#TODO:Let function takes file names strings not file objects and open it as append
def get_scripted(sOGIDir, fTxt, fUtt2Spk, fWavScp, sSpkrList='', lVerf = [1,2,4], lGrades = [0,1,2,3,4,5,6,7,8,9,10]):
    
    #Regular Expression to normalize the text
    #p = re.compile('([\w\s]+)[\W](\s|$)')
    rP_norm = re.compile('([\w\s]+)[\'\",\.](\s|$)|\*')

    sDocsDir = join(sOGIDir,'docs')
    print(sSpkrList)
    if isfile(sSpkrList):#Load list of selected speakers 
        with open(sSpkrList) as flSpkrList:
            lSelectSpkrs = flSpkrList.read().splitlines()
        print(lSelectSpkrs[0], len(lSelectSpkrs))
    else:
        lSelectSpkrs = None
    dfMap = pd.read_csv(join(sDocsDir,'all.map'),sep=' ',names=['id','trans'])
    aVerFiles = np.asarray([join(sOGIDir,'docs',str(i).zfill(2)+'-verified.txt') for i in lGrades],dtype=str) #The ver files exist in the docs directory as 00-verified.txt, 01-verified.txt, ....
    aIsFile = np.asarray([isfile(f) for f in aVerFiles],dtype=bool) #Check that all ver files are exist
    if not np.all(aIsFile):
        print('Missing Files: ',' '.join(aVerFiles[~aIsFile]))
        return
    #Read ver files
    aDataFrames = (pd.read_csv(f,sep=' ',names=['path','ver']) for f in aVerFiles) 
    dfVer = pd.concat(aDataFrames,ignore_index=True)
    dfVer.path[dfVer.ver.isin(lVerf)]
    aPaths = dfVer.path.values
    if lSelectSpkrs != None:
        lSpkrs = [splitext(basename(sPath))[0][:5] for sPath in aPaths]
        lInxSelcSpkrs = [i for i in range(len(lSpkrs)) if lSpkrs[i] in lSelectSpkrs]
        aPaths = aPaths[lInxSelcSpkrs]
    for sPath in aPaths:
        sRecId = splitext(basename(sPath))[0]
        sUttId = sRecId #Each recording contains one segment
        sSpkId = sRecId[:5]
        sTransId = sRecId[5:7].upper()
        sWavAbsPath = normpath(join(sDocsDir,sPath))
        aTransMask = dfMap.id==sTransId
        if not aTransMask.any():
            print('Invalid Trans ID:%s in Utt %s' % (sWavAbsPath,sTransId))
            continue
        sTrans = dfMap.trans[dfMap.id==sTransId].iloc[0].upper()
        sTrans = rP_norm.sub(r'\1\2',sTrans)
        print(sSpkId+'-'+sUttId, sTrans, file=fTxt)
        print(sSpkId+'-'+sUttId, sSpkId, file=fUtt2Spk)
        print(sSpkId+'-'+sUttId, sWavAbsPath, file=fWavScp)
    #print(dfVer.path.values,file=fOutFile)
    return

def get_spont(sOGIDir, fTxt, fUtt2Spk, fWavScp, sSpkrList='', lGrades = [0,1,2,3,4,5,6,7,8,9,10]):
    #1- get all trans files that match spkids, 2- Make sure each trans has wav file,
    #3- loop on trans files, 4- Treat the noise tags, 5- treat the [] remove what between them, 
    Get_basename = lambda s : splitext(basename(s))[0]
    #Get_SpkrID = lambda s : splitext(basename(s))[0][:5]
    
    sTransDir = join(sOGIDir,'trans/spontaneous')
    sWavDir = join(sOGIDir,'speech/spontaneous')
    
    #Get all trans & wav files
    lTransFiles = np.asarray(glob.glob(join(sTransDir,'**/*.txt'),recursive=True))
    lWavFiles = np.asarray(glob.glob(join(sWavDir,'**/*.wav'),recursive=True))
    lUttIDs = (np.asarray(list(map(Get_basename,lWavFiles))),np.asarray(list(map(Get_basename,lTransFiles))))

    #Find wav files that have trans files 
    lValidFiles = np.intersect1d(*lUttIDs,return_indices=True)
    
    #Update file lists
    lWavFiles = lWavFiles[lValidFiles[1]]
    lTransFiles = lTransFiles[lValidFiles[2]]
    lUttID = lUttIDs[0][lValidFiles[1]]

    #Get files of selected speakers & grades
    lSpkrID = np.asarray([s[:5] for s in lUttID])
    lGradID = np.asarray([dGrad2Int[s[2]] for s in lUttID])

    if isfile(sSpkrList):#Load list of selected speakers
        with open(sSpkrList) as flSpkrList:
            lSelectSpkrs = flSpkrList.read().splitlines()
        print(lSelectSpkrs[0], len(lSelectSpkrs))
        lSelectedFilesMap = np.in1d(lSpkrID,lSelectSpkrs) & np.in1d(lGradID,lGrades)

        #Update file lists
        lWavFiles = lWavFiles[lSelectedFilesMap]
        lTransFiles = lTransFiles[lSelectedFilesMap]
        lUttID = lUttID[lSelectedFilesMap]
        lSpkrID = lSpkrID[lSelectedFilesMap]
    
    #Map noise tags to kaldi symbols
    sPatterns = '|'.join(dNoiseTag2Symb.keys())
    rP_noise_Ncnctd = re.compile('(?<!\w)'+'('+sPatterns+')'+'(?!\w)')
    rP_noise_cnctd = re.compile(sPatterns)
    rP_norm = re.compile('([\w\s]+)[\'\",\.](\s|$)|\*')
    rP_norm2 = re.compile('<(?!NOISE|SPOKEN_NOISE)|(?<!NOISE)>|(?<!SPOKEN_NOISE)>')
    rP_CuttOff = re.compile('\[.+\]|\(.+\)')
    lTrans = apply_re_on_files(lTransFiles,((rP_noise_Ncnctd,lambda s: ' '+dNoiseTag2Symb[s.group(0)][1]+' '),(rP_noise_cnctd,lambda s: ' '+dNoiseTag2Symb[s.group(0)][0]+' '),(rP_norm,r'\1\2'),(rP_CuttOff,'')),isUpper= True)

    for sSpkId, sUttId, sTrans,sWavAbsPath in zip(lSpkrID, lUttID, lTrans, lWavFiles):
        print(sSpkId+'-'+sUttId, sTrans, file=fTxt)
        print(sSpkId+'-'+sUttId, sSpkId, file=fUtt2Spk)
        print(sSpkId+'-'+sUttId, sWavAbsPath, file=fWavScp)
    return


class str2list(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(str2list, self).__init__(option_strings, dest, **kwargs)
    def parse_str(self,text):
        r = []
        for p in text.split(','):
            if '-' in p:
                s, e = [int(i) for i in p.split('-')]
                r.extend(range(s,e+1))
            else:
                r.append(int(p))
        return r
    def __call__(self, parser, namespace, values, option_string=None):
        #print('%r %r %r' % (namespace, values, option_string))
        setattr(namespace, self.dest, self.parse_str(values))

def ArgParser():
    parser = argparse.ArgumentParser(description='This code for creating Kaldi files for OGI Kids dataset', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('OGI_Dir',  help='The path to the main directory of OGI data', type=str)
    parser.add_argument('Text_File',  help='The path to the text file with <UttID> <Trans>', type=str)
    parser.add_argument('Utterance_to_Speakers_File',  help='The path to the Utterance to Speaker mapping file', type=str)
    parser.add_argument('Wav_Scp_File',  help='The path to the file contains list of wav files <RecID> <wavfile>', type=str)
    parser.add_argument('-r','--read', help='Use this option to enable processing scripted (read) part of the OGI data', dest='process_read_data', action='store_true',default=False)
    parser.add_argument('-s','--spontaneous', help='Use this option to enable processing of spontaneous part of the data', dest='process_spontaneous_data', action='store_true', default=False)
    parser.add_argument('-l', '--spkrl', help='The file contains list of selected speakers', dest='spkrl', type=str, default='')
    parser.add_argument('-v', '--verify', help='The list of selected verification codes', dest='ver', action=str2list, default=[1,2,4])
    parser.add_argument('-g', '--grade', dest='grd', help='The list of kids grads to be included', action=str2list, default=list(range(0,11)))
    return parser.parse_args()

if __name__ == '__main__':
    args = ArgParser()
    sOGIDir, sTxt, sUtt2Spk, sWavScp = args.OGI_Dir, args.Text_File, args.Utterance_to_Speakers_File, args.Wav_Scp_File
    sSpkrList = args.spkrl
    lVerf = args.ver
    lGrades = args.grd
    with open(sTxt,'a') as fTxt, open(sUtt2Spk,'a') as fUtt2Spk, open(sWavScp,'a') as fWavScp:
        if args.process_read_data:
            get_scripted(sOGIDir, fTxt, fUtt2Spk, fWavScp, sSpkrList=sSpkrList, lVerf = lVerf, lGrades = lGrades)
        if args.process_spontaneous_data:
            get_spont(sOGIDir, fTxt, fUtt2Spk, fWavScp, sSpkrList=sSpkrList, lGrades = lGrades)




    



