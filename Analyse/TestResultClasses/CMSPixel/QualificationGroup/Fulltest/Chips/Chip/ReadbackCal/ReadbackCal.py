import ROOT
import glob
import AbstractClasses
import os
import re
from operator import itemgetter
import warnings
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_ReadbackCal_TestResult'
        self.NameSingle = 'ReadbackCal'

        self.ResultData['HiddenData']['ReadbackCal'] = {}
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'

        self.ResultData['KeyValueDictPairs']['Vbg'] = {'Label': 'Vbg', 'Value': '-1'}
        self.ResultData['KeyValueDictPairs']['par0ia'] = {'Label': 'par0ia', 'Value': '-1'}
        self.ResultData['KeyValueDictPairs']['par1ia'] = {'Label': 'par1ia', 'Value': '-1'}
        self.ResultData['KeyValueDictPairs']['par2ia'] = {'Label': 'par2ia', 'Value': '-1'}

    def PopulateResultData(self):
        Directory = self.RawTestSessionDataPath
            
        rbfilename = '{Directory}/readbackCal*_C{ChipNo}.dat'.format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
        names = glob.glob(rbfilename)
        ReadbackCalibrated = False

        if(len(names)>0):
            # sort by creation date
            names.sort(key=lambda x: os.stat(os.path.join('', x)).st_mtime)
            names = [(os.stat(os.path.join('', x)).st_mtime, x) for x in names]
            names.sort(key = itemgetter(0))
            # get newest file
            name = names[-1][1]
            ReadbackCalFileName = name

            if os.path.exists(ReadbackCalFileName):
                ReadbackCalFile = open(ReadbackCalFileName, "r")
           # self.ResultData['HiddenData']['ReadbcakCal']['File'+i] = ReadbackCalFile

                if ReadbackCalFile :
                    for Line in ReadbackCalFile:
                        LineArray = Line.strip().split()
                        RbCalParameterName = LineArray[0]
                        
                        RbCalParameterValue = float(LineArray[1])
                        if abs(RbCalParameterValue-1.0) > 1e-6:
                            ReadbackCalibrated = True
                        self.ResultData['KeyValueDictPairs'][RbCalParameterName.lower()] = {
                            'Value': '{0:.2e}'.format(RbCalParameterValue),
                            'Label': RbCalParameterName
                        }
                        self.ResultData['KeyList'] += [RbCalParameterName.lower()]
                    ReadbackCalFile.close()
        else:
            warnings.warn('No readback calibration file found!')



        # Adding Vbg
        HistoName= 'Readback.Vbg_readback_VdCal_V0'
        ChipNo = self.ParentObject.Attributes['ChipNo']
        ROOTFile = self.ParentObject.ParentObject.FileHandle

        try:
            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(ROOTFile, HistoName).Clone(self.GetUniqueID())
        except:
            pass

        try:
            Vbg = round(self.ResultData['Plot']['ROOTObject'].GetBinContent(ChipNo+1),3)
            self.ResultData['KeyValueDictPairs']['Vbg'] = {'Label': 'Vbg', 'Value': Vbg}
            self.ResultData['KeyList'].append('Vbg')
        except:
            ReadbackCalibrated = False

        try:
            par0ia = self.ParentObject.ResultData['SubTestResults']['ReadbackCalIana'].ResultData['KeyValueDictPairs']['par0ia']['Value']
            par1ia = self.ParentObject.ResultData['SubTestResults']['ReadbackCalIana'].ResultData['KeyValueDictPairs']['par1ia']['Value']
            par2ia = self.ParentObject.ResultData['SubTestResults']['ReadbackCalIana'].ResultData['KeyValueDictPairs']['par2ia']['Value']
            self.ResultData['KeyValueDictPairs']['par0ia'] = {'Label': 'par0ia', 'Value': par0ia}
            self.ResultData['KeyList'].append('par0ia')
            self.ResultData['KeyValueDictPairs']['par1ia'] = {'Label': 'par1ia', 'Value': par1ia}
            self.ResultData['KeyList'].append('par1ia')
            self.ResultData['KeyValueDictPairs']['par2ia'] = {'Label': 'par2ia', 'Value': par2ia}
            self.ResultData['KeyList'].append('par2ia')
        except:
            ReadbackCalibrated = False

        self.ResultData['KeyValueDictPairs']['ReadbackCalibrated'] = {'Label': 'Calibrated', 'Value': 'True' if ReadbackCalibrated else 'False'}
        self.ResultData['KeyList'].append('ReadbackCalibrated')
