# -*- coding: utf-8 -*-
import AbstractClasses
import ROOT
import os
import ConfigParser
import AbstractClasses.Helper.helper as Helper
import math
import array
from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_TemperatureCycle_TestResult'
        self.NameSingle = 'TemperatureCycle'

        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def OpenFileHandle(self):
        pass

    def analyseTemp(self, fileName):
        print 'analyse Temp for "%s"' % fileName
        # duration = 0
        # temp = 0
        # tempError = 0
        # tempMin = 0
        # tempMax = 0
        # timeMin = 0
        # timeMax = 0
        name = fileName.split('/')[-1].split('.')[0]
        name.strip()
        # varlist = 'time:temp'
        if Helper.fileExists(fileName):
            this_file = open(fileName)
            lines = this_file.readlines()
            lines = [i for i in lines if not i.startswith('#')]
            tuples = [i.strip().split('\t') for i in lines]
            times = [int(i[0]) for i in tuples]
            temps = [float(i[1]) for i in tuples]
            if len(temps) > 0:
                temp = sum(temps) / len(temps)
                temp2 = sum([i * i for i in temps]) / len(temps)
            else:
                temp = 0
                temp2 = 0
                # tempMin = 0
                # tempMax = 0
                timeMin = 0
                timeMax = 0
            #
            # # get RMS Temp
            # tempError = math.sqrt(temp2 - temp * temp)
            # ROOT.TMath.RMS(tuple.GetSelectedRows(),tuple.GetV1())
            #
            if len(temps) > 0:
                #             # get Min Temp
                tempMin = min(temps)
                #             #get Max Temp
                tempMax = max(temps)
                #calculate time difference
                timeMin = min(times)
                timeMax = max(times)
            #
            # duration = timeMax - timeMin
            temp_List = array.array('d', temps)
            time_List = array.array('d', times)
            if not self.ResultData['Plot'].has_key('ROOTObjects'):
                self.ResultData['Plot']['ROOTObjects'] = {}
            # name = '%02d_%s' % (len(self.ResultData['Plot']['ROOTObjects']), name)
            if len(temps):
                graph = ROOT.TGraph(len(temp_List), time_List, temp_List)
                self.ResultData['Plot']['ROOTObject'] = ROOT.TMultiGraph()
            else:
                graph = ROOT.TGraph()

            canvas = self.TestResultEnvironmentObject.Canvas
            self.CanvasSize(canvas)
            canvas.cd()

            graph.SetTitle('')
            graph.Draw("APL")
            graph.SetLineColor(4)
            graph.SetLineWidth(2)
            graph.SetMarkerSize(.2)
            graph.SetMarkerColor(1)
            graph.SetMarkerStyle(8)

            graph.GetXaxis().SetTitle("Time")
            graph.GetXaxis().SetTimeDisplay(1)
            graph.GetYaxis().SetTitle("Temperature [#circ C]")

            graph.GetYaxis().SetDecimals()
            graph.GetYaxis().SetTitleOffset(1.5)
            graph.GetYaxis().CenterTitle()
            graph.Draw("APL")
            canvas.Clear()
            if self.ResultData['Plot']['ROOTObject']:
                if graph:
                    self.ResultData['Plot']['ROOTObject'].Add(graph, "L")
                self.ResultData['Plot']['ROOTObject'].Draw("a")
                self.ResultData['Plot']['ROOTObject'].SetTitle(';Time; Temp [#circ C]')
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTimeDisplay(1)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetDecimals()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.Canvas = canvas
            this_file.close()

    def PopulateResultData(self):
        LogFileName = self.Attributes['LogFileName']
        if LogFileName is not None:
            print LogFileName
            self.analyseTemp(LogFileName)

        if self.verbose: raw_input('Press enter')
        self.ResultData['Plot']['Caption'] = 'Temperature'
        self.SaveCanvas()        
    def CustomWriteToDatabase(self, ParentID):
        pass
