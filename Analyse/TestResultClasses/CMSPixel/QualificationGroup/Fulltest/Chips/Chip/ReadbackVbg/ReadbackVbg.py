import ROOT
import AbstractClasses
import os
from operator import itemgetter
import warnings
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        self.NameSingle = 'ReadbackCalVbg'
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'


    def PopulateResultData(self):
        #ROOT.gStyle.SetOptStat(0)

        #HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        #HistoName = HistoDict.get(self.NameSingle, 'VbgCalibration')
        #print HistoName
        HistoName= 'Readback.Vbg_readback_VdCal_V0'
        ChipNo = self.ParentObject.Attributes['ChipNo']
        ROOTFile = self.ParentObject.ParentObject.FileHandle

        try:
            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(ROOTFile, HistoName).Clone(self.GetUniqueID())
        except:
            pass


        Vbg=round(self.ResultData['Plot']['ROOTObject'].GetBinContent(ChipNo+1),3)
        self.ResultData['KeyValueDictPairs'] = {
                    'Vbg': {
                    'Value':Vbg,
                    'Label':'Vbg'
                    },
                                                }
        self.ResultData['KeyList'] = ['Vbg']