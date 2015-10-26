import ROOT
import AbstractClasses
import time
import sys
import glob
import json



def ReadFile(p):
    
	Numbers = {
        'nlcstartupB': 0, 
        'nlcstartupC' : 0,
        'nIV150B' : 0,
        'nIV150C' : 0,
        'nIV150m20B' : 0,
        'nIV150m20C' : 0,
        'nIVSlopeB' : 0,
        'nIVSlopeC' : 0,
        'nRecCurrentB' : 0,
        'nRecCurrentC' : 0,
        'nCurrentRatioB' : 0,
        'nCurrentRatioC' : 0,
        'ntotDefectsB' : 0,
        'ntotDefectsC' : 0,
        'ntotDefectsXrayB' : 0,
        'ntotDefectsXrayC' : 0,
        'nBBFullB' : 0,
        'nBBFullC' : 0,
        'nBBXrayB' : 0,
        'nBBXrayC' : 0,
        'nAddressdefB' : 0,
        'nAddressdefC' : 0,
        'nTrimbitdefB' : 0,
        'nTrimbitdefC' : 0,
        'nMaskdefB' : 0,
        'nMaskdefC' : 0,
        'ndeadpixB' : 0,
        'ndeadpixC' : 0,
        'nuniformityB' : 0,
        'nuniformityC' : 0,
        'nNoiseB' : 0,
        'nNoiseC' : 0,
        'nNoiseXrayB' : 0,
        'nNoiseXrayC' : 0,
        'nPedSpreadB' : 0,
        'nPedSpreadC' : 0,
        'nRelGainWB' : 0,
        'nRelGainWC' : 0,
        'nVcalThrWB' : 0,
        'nVcalThrWC' : 0,
        'nLowHREfB' : 0,
        'nLowHREfC' : 0,
        'nBrokenROCFull' : 0,
        'nBrokenROCXray' : 0
}


        Path = p

        filename = "{}/ProductionOverview/ProductionOverviewPage_Total/ModuleFailuresOverview/KeyValueDictPairs.json".format(Path)
        #print filename
    	data = open(filename, 'r')
        moduledefects = json.load(data)

        for mod, defects in moduledefects.iteritems():


            for d, grade in defects.iteritems():

                if (d == 'AddressDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nAddressdefB'] += 1
                    elif tag == "C":
                        Numbers['nAddressdefC'] += 1

                if (d == 'BB_Fulltest' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nBBFullB'] += 1
                    elif tag == "C":
                        Numbers['nBBFullC'] += 1

                if (d == 'BB_X-ray' and grade!=""):
                    if grade == "B" :
                        Numbers['nBBXrayB'] += 1
                    elif grade == "C":
                        Numbers['nBBXrayC'] += 1

                if (d == 'IV150' and grade!=""):
                    for test, g in grade.iteritems():
                        if g != "" :
                            if test == "m20_2" and g == "B":
                                Numbers['nIV150m20B'] += 1
                            elif test == "m20_2" and g == "C":
                                Numbers['nIV150m20C'] += 1
                            elif test == "p17_1" and g == "B":
                                Numbers['nIV150B'] += 1
                            elif test == "p17_1" and g == "C":
                                Numbers['nIV150C'] += 1

                if (d == 'IVRatio150' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nCurrentRatioB'] += 1
                    elif tag == "C":
                        Numbers['nCurrentRatioC'] += 1

                if (d == 'IVSlope' and grade!=""):
                    if grade == "B" :
                        Numbers['nIVSlopeB'] += 1
                    elif grade == "C":
                        Numbers['nIVSlopeC'] += 1

                if (d == 'LCStartup' and grade!=""):
                    if grade == "B" :
                        Numbers['nlcstartupB'] += 1
                    elif grade == "C":
                        Numbers['nlcstartupC'] += 1

                if (d == 'Noise' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nNoiseB'] += 1
                    elif tag == "C":
                        Numbers['nNoiseC'] += 1

                if (d == 'Noise_X-ray' and grade!=""):
                    if grade == "B" :
                        Numbers['nNoiseXrayB'] += 1
                    elif grade == "C":
                        Numbers['nNoiseXrayC'] += 1

                if (d == 'PedestalSpread' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nPedSpreadB'] += 1
                    elif tag == "C":
                        Numbers['nPedSpreadC'] += 1

                if (d == 'RelativeGainWidth' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nRelGainWB'] += 1
                    elif tag == "C":
                        Numbers['nRelGainWC'] += 1

                if (d == 'TotalDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['ntotDefectsB'] += 1
                    elif tag == "C":
                        Numbers['ntotDefectsC'] += 1

                if (d == 'TotalDefects_X-ray' and grade!=""):
                    if grade == "B" :
                        Numbers['ntotDefectsXrayB'] += 1
                    elif grade == "C":
                        Numbers['ntotDefectsXrayC'] += 1

                if (d == 'UniformityProblems' and grade!=""):
                    if grade == "B" :
                        Numbers['nuniformityB'] += 1
                    elif grade == "C":
                        Numbers['nuniformityC'] += 1

                if (d == 'VcalThrWidth' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nVcalThrWB'] += 1
                    elif tag == "C":
                        Numbers['nVcalThrWC'] += 1

                if (d == 'deadPixels' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['ndeadpixB'] += 1
                    elif tag == "C":
                        Numbers['ndeadpixC'] += 1

                if (d == 'lowHREfficiency' and grade!=""):
                    if grade == "B" :
                        Numbers['nLowHREfB'] += 1
                    elif grade == "C":
                        Numbers['nLowHREfC'] += 1

                if (d == 'maskDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nMaskdefB'] += 1
                    elif tag == "C":
                        Numbers['nMaskdefC'] += 1

                if (d == 'trimbitDefects' and grade!=""):
                    tag = "A"
                    for test, g in grade.iteritems():
                        if g == "C":
                            tag = "C"
                        elif (tag!="C" and g == "B"):
                            tag = "B"
                    if tag == "B" :
                        Numbers['nTrimbitdefB'] += 1
                    elif tag == "C":
                        Numbers['nTrimbitdefC'] += 1


    	return Numbers