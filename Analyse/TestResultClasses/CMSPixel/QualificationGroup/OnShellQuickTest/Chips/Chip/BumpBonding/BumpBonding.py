import ROOT
import AbstractClasses.Helper.HistoGetter as HistoGetter
from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'BumpBonding'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_OnShellQuickTest_ROC'

        self.BumpbondingDefectsList = set([])
        self.ResultData['KeyValueDictPairs']['BumpBondingDefects'] = {'Value': '', 'Label': 'Bump Bonding Defects'}
        self.ResultData['KeyValueDictPairs']['NBumpBondingDefects'] = {'Value': '-', 'Label': 'N Bump Bonding Defects'}
        self.ResultData['KeyList'].append('NBumpBondingDefects')

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        HistoName = HistoDict.get('OnShellQuickTest', 'BumpBonding')
        ChipNo = self.ParentObject.Attributes['ChipNo']
        ROOTFile = self.ParentObject.ParentObject.FileHandle

        try:
            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(ROOTFile, HistoName, rocNo=ChipNo).Clone(self.GetUniqueID())
        except:
            self.ResultData['Plot']['ROOTObject'] = None

        ChipNo = self.ParentObject.Attributes['ChipNo']
        if self.ResultData['Plot']['ROOTObject']:
            for column in range(self.nCols):
                for row in range(self.nRows):
                    defectIndicator = self.ResultData['Plot']['ROOTObject'].GetBinContent(column + 1, row + 1)
                    if defectIndicator > 0:
                        self.BumpbondingDefectsList.add((ChipNo, column, row))

            self.ResultData['KeyValueDictPairs']['BumpBondingDefects']['Value'] = self.BumpbondingDefectsList
            self.ResultData['KeyValueDictPairs']['NBumpBondingDefects']['Value'] = len(self.BumpbondingDefectsList)

            self.ResultData['Plot']['ROOTObject'].Draw("colz")

        self.Title = 'BumpBonding'
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'svg'
        self.SaveCanvas()