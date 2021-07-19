#!/usr/bin/env python3

import argparse
from collections import defaultdict
import random, subprocess, os
import numpy as np


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
    parser = argparse.ArgumentParser(description='This code selecting features from data', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('sUtt_Fram',  help='The path to the utt2num_fram file', type=str)
    parser.add_argument('sFeat_Scp',  help='The path to the feats.scp file', type=str)
    parser.add_argument('sCopy_Feat',  help='The path to copy-feat binary', type=str)
    parser.add_argument('-n','--num-frams', help='number of required frames from each spkr/grad', dest='num_frams', type=int, default=1000)
    parser.add_argument('-l', '--spkrl', help='The file contains list of selected speakers', dest='spkrl', type=str, default='')
    parser.add_argument('-g', '--grade', dest='grd', help='The list of kids grads to be included', action=str2list, default=list(range(0,11)))
    return parser.parse_args()

if __name__ == '__main__':
    args = ArgParser()
    sUtt_Fram, sFeat_Scp, sCopy_Feat = args.sUtt_Fram, args.sFeat_Scp, args.sCopy_Feat
    nFrames = args.num_frams
    sSpkrList = args.spkrl
    lGrads = args.grd

    nPerGrad = int(nFrames/len(lGrads))
    dGrads = defaultdict(list)
    #dFeat = {}

    with open(sFeat_Scp) as fFeat_Scp:
        dFeat = dict([(k,v) for k,v in map(lambda x:x.split(),fFeat_Scp.read().splitlines())])
    with open(sUtt_Fram) as fUtt_Fram:
       lLines = fUtt_Fram.read().splitlines()
    for sLine in lLines:
        sName, nFrames = sLine.split()
        nSel = int(int(nFrames)/3)
        rSel = (nSel,nSel*2)
        dGrads[dGrad2Int[sName[2]]].extend([i for i in zip([sName]*(nSel*2),rSel)])
    for iGrad in lGrads:
        if iGrad not in dGrads:
            print('No samples for grad %d' % iGrad)
            continue
        lSelect = random.sample(dGrads[iGrad],nPerGrad)
        sGrad_Scp = 'tmp{}.scp'.format(iGrad)
        with open(sGrad_Scp,'w') as fGrad:
            for item in lSelect:
                print('{}\t{}[{}:{},:]'.format(item[0],dFeat[item[0]],item[1],item[1]),file=fGrad)
        lCpArg = [sCopy_Feat,'scp:{}'.format(sGrad_Scp),'ark,t:-']
        out = subprocess.run(lCpArg,capture_output=True,text=True)
        if out.returncode != 0:
            print(' '.join(lCpArg),'exit with error {}'.format(out.returncode))
            continue
        #print(out.stdout.splitlines()[0])
        aFeat = np.loadtxt(list(map(lambda x : x.replace(']',''),filter(lambda x : '[' not in x,out.stdout.splitlines()))))
        os.remove(sGrad_Scp)
        np.save('{}.npy'.format(iGrad),aFeat)


    




