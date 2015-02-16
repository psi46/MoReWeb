# -*- coding: utf-8 -*-
import ROOT
import array
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_DigitalCurrent_TestResult'
        self.NameSingle='DigitalCurrent'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        try:
            histname = self.ParentObject.HistoDict.get(self.NameSingle, 'DigitalCurrent')
            print histname
            object = HistoGetter.get_histo(self.ParentObject.FileHandle, histname)
            print object
            self.ResultData['Plot']['ROOTObject'] = self.get_Current_Graph(object)
            self.ResultData['Plot']['Graph'] = object.Clone(self.GetUniqueID())
            print self.ResultData['Plot']['ROOTObject']

            if self.ResultData['Plot']['ROOTObject']:
                self.Canvas.Clear()
                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("digital current / A")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].Draw('APL')
            if self.SavePlotFile:
                print 'SavePlotFile', self.SavePlotFile
                self.Canvas.SaveAs(self.GetPlotFileName())
            self.ResultData['Plot']['Enabled'] = 1
            self.Title = 'Digital Current'
            self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
            print self.GetPlotFileName()
        except Exception as e:
            print e

        # raw_input(self.NameSingle)

    def get_Current_Graph(self,object):
        print 'get_Current_Graph'
        print 'type:',type(object)
        times = []
        currents = []
        title = object.GetTitle()
        seconds = float(title.split(':')[-1])
        print title,seconds
        seconds = 0
        # raw_input()
        for bin in range(1,object.GetNbinsX()+1):
            if object.GetBinContent(bin):
                times.append(object.GetXaxis().GetBinCenter(bin)+seconds)
                currents.append(object.GetBinContent(bin))
                print bin,times[-1],currents[-1]
        times = array.array('d',times)
        currents = array.array('d',currents)
        graph = ROOT.TGraph(len(times),times,currents)
        graph.SetMarkerStyle(7)
        graph.SetLineStyle(2)
        graph.SetLineColor(ROOT.kBlue)
        graph.Draw('AL ')
        graph.GetXaxis().SetTimeOffset(seconds,'GMT')
        graph.GetXaxis().SetTitle("Time")
        graph.GetXaxis().SetTimeDisplay(1)
        # if max(times) > 30*60:
        graph.GetXaxis().SetTimeFormat('%H:%M')
        graph.GetXaxis().LabelsOption('v'   )
        graph.GetYaxis().SetRangeUser(0,graph.GetYaxis().GetXmax()*1.1)
        return graph

