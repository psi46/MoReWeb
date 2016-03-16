# -*- coding: utf-8 -*-
import ROOT
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBondingMap.BumpBondingMap

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBondingMap.BumpBondingMap.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()

    def PopulateResultData(self):
        try:
            super(TestResult, self).PopulateResultData()
            for pix in self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['DeadPixels']['Value']:
                self.ResultData['Plot']['ROOTObject'].SetBinContent(1+pix[1], 1+pix[2], 0)
            self.SaveCanvas()
        except:
            print "No standard BumpBonding test found!"
