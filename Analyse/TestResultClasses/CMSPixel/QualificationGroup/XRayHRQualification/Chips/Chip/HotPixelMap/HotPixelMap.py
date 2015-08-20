# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_HotPixelMap_TestResult'
        self.NameSingle = 'HotPixelMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.HotPixelsList = set()
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']

        ROOT.gPad.SetLogx(0)
        ROOT.gStyle.SetOptStat(0)
        self.Canvas.Clear()
        self.ResultData['Plot']['ROOTObject'] = None

        if 'MaskHotPixels' in self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']:
            rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['MaskHotPixels']
            histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'HotPixelMap').format(ChipNo=self.ParentObject.Attributes['ChipNo'])

            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())

        else:
            if 'RetrimHotPixelsPath' in self.ParentObject.ParentObject.ParentObject.Attributes:
                self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0., self.nCols, self.nRows, 0., self.nRows) 
                Directory = self.ParentObject.ParentObject.ParentObject.Attributes['RetrimHotPixelsPath']
                MaskFileName = Directory + '/' + self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'MaskFile')
                MaskFileLines = []

                try:
                    with open(MaskFileName, "r") as f:
                        MaskFileLines = f.readlines()
                except:
                    print "could not open mask file '%s'"%MaskFileName

                for MaskFileLine in MaskFileLines:
                    line = MaskFileLine.strip().split(' ')
                    if len(line) >= 4 and line[0].lower() == 'pix' and int(line[1]) == int(ChipNo):
                        self.ResultData['Plot']['ROOTObject'].SetBinContent(1 + int(line[2]), 1 + int(line[3]), 1)


        if self.ResultData['Plot']['ROOTObject']:
            for col in range(0, self.nCols):
                for row in range(0, self.nRows):
                    if self.ResultData['Plot']['ROOTObject'].GetBinContent(1+col,1+row) > 0:
                        self.HotPixelsList.add((ChipNo, col, row))

            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')

        self.ResultData['HiddenData']['ListOfHotPixels'] = {'Label': 'Masked Hot Pixels List', 'Value': self.HotPixelsList}
        self.ResultData['HiddenData']['NumberOfHotPixels'] = {'Label': 'Masked Hot Pixels', 'Value': len(self.HotPixelsList)}

        self.Title = 'Masked Hot Pixels {Rate}: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'],Rate=self.Attributes['Rate'])
        self.SaveCanvas()        


