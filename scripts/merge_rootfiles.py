#!/usr/bin/env python
import argparse
import os
import ROOT

'''
combines pxar generated .root files

how to use:

./merge_rootfiles.py -i firstInputFile.root -o outputFile.root
./merge_rootfiles.py -i secondInputFile.root -o outputFile.root -a
./merge_rootfiles.py -i thirdInputFile.root -o outputFile.root -a
...

and select the objects (with y/n) or whole folders (with s/b)

'''

parser = argparse.ArgumentParser(description='combine pxar root files')
parser.add_argument('-o','--output',dest='output',metavar='PATH',
                     help='outputfile',
                     default='')

parser.add_argument('-i','--input',dest='input',metavar='PATH',
                     help='inputfile',
                     default='')
parser.add_argument('-a', '--append', dest = 'append', action = 'store_true', default = False,
                    help='appends to root file')

args = parser.parse_args()

def getall(d, basepath="/"):
    for key in d.GetListOfKeys():
        kname = key.GetName()
        if key.IsFolder():
            for i in getall(d.Get(kname), basepath+kname+"/"):
                yield i
        else:
            yield basepath+kname, d.Get(kname)

def getdirs(d, basepath="/"):
    dirs = []
    for key in d.GetListOfKeys():
        if key.IsFolder():
            dirs.append(key.GetName())
    return dirs

if os.path.isfile(args.input):
    rootInput = ROOT.TFile(args.input, "READ")
    rootOutput = ROOT.TFile(args.output, "UPDATE" if args.append else "RECREATE")
    outputDirs = getdirs(rootOutput)
    print "input: ", getdirs(rootInput)
    print "output: ", outputDirs

    allObjects = getall(rootInput)

    copyMasks = []
    copySkip = []
    copyAll = False

    for i in allObjects:
        parts = i[0].split('/')[1:]
        copyObject = False
        if parts[0] in copyMasks:
            copyObject = True
        elif parts[0] in copySkip:
            copyObject = False

        if not copyObject and not copyAll and not parts[0] in copySkip:
            selected = False
            while not selected:
                print "copy \x1b[32m%s\x1b[0m? \n y    yes\n n    no\n b    copy whole folder \x1b[32m%s\x1b[0m\n s    skip whole folder \x1b[31m%s\x1b[0m\n a    copy all histograms"%(i[0],parts[0],parts[0])
                inp = raw_input()
                if inp == 'a':
                    selected = True
                    copyAll = True
                elif inp == 'b':
                    copyMasks.append(parts[0])
                    copyObject = True
                    selected = True
                elif inp == 's':
                    copySkip.append(parts[0])
                    copyObject = False
                    selected = True
                elif inp == 'y':
                    copyObject = True
                    selected = True
                elif inp == 'n':
                    copyObject = False
                    selected = True

        if copyObject or copyAll:
            print "copy ",parts
            if parts[0] not in outputDirs:
                subdir = rootOutput.mkdir(parts[0])
                outputDirs.append(parts[0])
            else:
                subdir = rootOutput.Get(parts[0])
            i[1].SetDirectory(subdir)

    rootOutput.Write()
    rootOutput.Close()
    rootInput.Close()
