# -*- coding: utf-8 -*-
import ROOT
import array
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

import ROOT
import datetime

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'DigitalCurrent'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_Chips_Chip_{NameSingle}_TestResult'.format(NameSingle=self.NameSingle)
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        try:
            histname = self.ParentObject.HistoDict.get('OnShellQuickTest', 'DigitalCurrent')
            self.ResultData['Plot']['ROOTHisto'] = HistoGetter.get_histo(self.ParentObject.FileHandle, histname)
        except Exception as e:
            print e
            raise e
        self.SpecialPopulateResultData(self, {'name': 'Digital Current'})

    @staticmethod
    def SpecialPopulateResultData(TestResultObject,Parameters):
        try:
            ROOTObject = TestResultObject.ResultData['Plot']['ROOTHisto']
            times = []
            currents = []
            seconds = 0

            for bin in range(1, ROOTObject.GetNbinsX() + 1):
                if ROOTObject.GetBinContent(bin) > 0:
                    times.append(ROOTObject.GetXaxis().GetBinCenter(bin)+seconds)
                    currents.append(ROOTObject.GetBinContent(bin))

            times = array.array('d', times)
            currents = array.array('d', currents)
            graph = ROOT.TGraph(len(times), times, currents)
            graph.SetName(TestResultObject.GetUniqueID())
            graph.SetMarkerStyle(7)
            graph.SetLineStyle(2)
            graph.SetLineColor(ROOT.kBlue)
            graph.Draw('AL ')
            graph.GetXaxis().SetTimeOffset(seconds, 'GMT')
            graph.GetXaxis().SetTitle("Time")
            graph.GetXaxis().SetTimeDisplay(1)
            graph.GetXaxis().SetTimeFormat('%H:%M')
            graph.GetYaxis().SetRangeUser(0,graph.GetYaxis().GetXmax()*1.1)

            delta = datetime.timedelta(seconds=max(times)-min(times))
            #print str(delta)
            TestResultObject.ResultData['KeyValueDictPairs'] = {
                'Duration': {
                    'Value': '{0}'.format(str(delta)),
                    'Label': 'Duration',
                    'Unit': ''
                },
                'MaxCurrent': {
                    'Value': round(max(currents),3),
                    'Label': 'max. Current',
                    'Unit': 'A'
                },
                'MinCurrent': {
                    'Value': round(min(currents),3),
                    'Label': 'min. Current',
                    'Unit': 'A'
                }
            }
            TestResultObject.ResultData['HiddenData'] = {
                'Duration': {
                    'Value': "%d"%(max(times)-min(times)),
                    'Unit': 'seconds',
                    'Label': 'Fulltest duration',
                }
            }
            TestResultObject.ResultData['KeyList'] = ['Duration','MinCurrent','MaxCurrent']
            TestResultObject.ResultData['Plot']['ROOTGraph'] = graph

            if TestResultObject.ResultData['Plot']['ROOTGraph']:
                TestResultObject.Canvas.Clear()
                TestResultObject.ResultData['Plot']['ROOTGraph'].SetTitle("")
                TestResultObject.ResultData['Plot']['ROOTGraph'].GetYaxis().SetTitle("{0:s} / A".format(Parameters['name']))
                TestResultObject.ResultData['Plot']['ROOTGraph'].GetXaxis().CenterTitle()
                TestResultObject.ResultData['Plot']['ROOTGraph'].GetYaxis().SetTitleOffset(1.5)
                TestResultObject.ResultData['Plot']['ROOTGraph'].GetYaxis().CenterTitle()
                TestResultObject.ResultData['Plot']['ROOTGraph'].Draw('APL')
                TestResultObject.ResultData['Plot']['ROOTObject'] = TestResultObject.ResultData['Plot']['ROOTGraph']
            TestResultObject.ResultData['Plot']['Enabled'] = 1
            TestResultObject.ResultData['Plot']['ImageFile'] = TestResultObject.GetPlotFileName()

            TestResultObject.Title = Parameters['name'] if Parameters.has_key('name') else 'Digital Current'
            TestResultObject.SaveCanvas()

        except Exception as e:
            print e
            raise e
