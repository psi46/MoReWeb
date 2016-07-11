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


        if 'IVCurveDB' in self.ParentObject.ResultData['SubTestResults']['Database'].ResultData['HiddenData']:
            IVCurveDB = self.ParentObject.ResultData['SubTestResults']['Database'].ResultData['HiddenData']['IVCurveDB']

            voltages = []
            currents = []
            for IVTuple in IVCurveDB:
                if len(IVTuple) > 1:
                    try:
                        voltages.append(-float(IVTuple[0]))
                        currents.append(-float(IVTuple[1]))
                    except:
                        pass

            xp = array.array('d', voltages)
            yp = array.array('d', currents)

            ivGraph2 = ROOT.TGraph(len(voltages), xp, yp)
            ivGraph2.SetLineColor(ROOT.kRed + 1)
            ivGraph2.Draw("L same")
        else:
            print "no iv curve from DB available"

        self.SaveCanvas()
