# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.IVCurve.IVCurve
import array

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.IVCurve.IVCurve.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()
        self.Attributes['Reception'] = True

    def PopulateResultData(self):
        super(TestResult, self).PopulateResultData()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetMoreLogLabels()

        IVfromDB = None
        try:
            IVfromDB = self.ParentObject.ResultData['SubTestResults']['Database'].ResultData['HiddenData']['LeakageCurrent150p17']

            xp = array.array('d',[150])
            yp = array.array('d',[IVfromDB])

            ivGraph = ROOT.TGraph(1, xp, yp)
            ivGraph.SetMarkerColor(ROOT.kRed+1)
            ivGraph.Draw("P* same")

        except:
            pass

        if IVfromDB:
            self.ResultData['KeyValueDictPairs']['IV150DB'] = {'Label': 'I(150 V) Fulltest', 'Value': "%1.2f"%(float(IVfromDB)*1e6), 'Unit': 'μA'}
            self.ResultData['KeyList'].append('IV150DB')

        self.SaveCanvas()
