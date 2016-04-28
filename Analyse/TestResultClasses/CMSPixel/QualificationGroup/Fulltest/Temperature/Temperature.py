# -*- coding: utf-8 -*-
import datetime
import array
import math

import ROOT

import AbstractClasses
import AbstractClasses.Helper.helper as Helper
from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Temperature_TestResult'
        self.NameSingle = 'Temperature'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Temperature'

    def analyseTemp(self, fileName):
        print 'analyse Temp for "%s"' % fileName
        duration = 0
        temp = 0
        tempError = 0
        tempMin = 0
        tempMax = 0
        timeMin = 0
        timeMax = 0
        name = fileName.split('/')[-1].split('.')[0]
        name.strip()
        # varlist = 'time:temp'
        if not self.ResultData['Plot'].has_key('ObjectCanvas'):
            self.ResultData['Plot']['ObjectCanvas'] = {}
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
                tempMin = 0
                tempMax = 0
                timeMin = 0
                timeMax = 0
            #
            # # get RMS Temp
            tempError = math.sqrt(temp2 - temp * temp)
            # ROOT.TMath.RMS(tuple.GetSelectedRows(),tuple.GetV1())
            #
            if len(temps) > 0:
                # # get Min Temp
                tempMin = min(temps)
                # #get Max Temp
                tempMax = max(temps)
                # calculate time difference
                timeMin = min(times)
                timeMax = max(times)
            #
            duration = timeMax - timeMin
            temp_List = array.array('d', temps)
            time_List = array.array('d', times)
            if not self.ResultData['Plot'].has_key('ROOTObjects'):
                self.ResultData['Plot']['ROOTObjects'] = {}
            name = '%02d_%s' % (len(self.ResultData['Plot']['ROOTObjects']), name)
            if len(temps):
                graph = ROOT.TGraph(len(temp_List), time_List, temp_List)
                self.ResultData['Plot']['ROOTObjects'][name] = ROOT.TMultiGraph()
            else:
                graph = ROOT.TGraph()
                self.ResultData['Plot']['ROOTObjects'][name] = ROOT.TGraph()

            canvas = self.TestResultEnvironmentObject.Canvas
            self.CanvasSize(canvas)
            canvas.cd()

            graph.SetTitle('')
            graph.Draw("APL")
            graph.SetLineColor(4)
            graph.SetLineWidth(2)

            graph.GetXaxis().SetTitle("Time")
            graph.GetXaxis().SetTimeDisplay(1)
            graph.GetYaxis().SetTitle("Temperature [#circ C]")

            graph.GetYaxis().SetDecimals()
            graph.GetYaxis().SetTitleOffset(1.5)
            graph.GetYaxis().CenterTitle()
            graph.Draw("APL")
            #print self.ParentObject.Attributes['TestTemperature']
            setPoint = \
                self.ParentObject.Attributes['TestTemperature']

            if len(temps):
                avrgGraph = ROOT.TGraphErrors(2)
                avrgGraph.SetTitle('')
                avrgGraph.SetLineColor(ROOT.kRed)
                avrgGraph.SetLineWidth(2)
                avrgGraph.SetPoint(0, timeMin, temp)
                avrgGraph.SetPoint(1, timeMax, temp)
                avrgGraph.SetPointError(0, 0, tempError)
                avrgGraph.SetPointError(1, 0, tempError)
                avrgGraph.SetFillColor(ROOT.kRed)
                avrgGraph.SetFillStyle(0)
                setPointGraph = ROOT.TGraphErrors(2)
                setPointGraph.SetTitle('')
                setPointGraph.SetLineColor(ROOT.kBlack)
                setPointGraph.SetLineWidth(2)
                setPointGraph.SetPoint(0, timeMin, setPoint)
                setPointGraph.SetPoint(1, timeMax, setPoint)
                setPointGraph.SetPointError(0, 0, .5)
                setPointGraph.SetPointError(1, 0, .5)
                setPointGraph.SetFillColor(ROOT.kGreen)
                setPointGraph.SetFillStyle(0)
                self.ResultData['Plot']['ROOTObjects'][name].Add(setPointGraph, '3L')
                self.ResultData['Plot']['ROOTObjects'][name].Add(avrgGraph, '3L')
                self.ResultData['Plot']['ROOTObjects'][name].Add(graph, "L")
                self.ResultData['Plot']['ROOTObjects'][name].Draw("a")
                self.ResultData['Plot']['ROOTObjects'][name].SetTitle(';Time; Temp [#circ C]')
                self.ResultData['Plot']['ROOTObjects'][name].GetXaxis().SetTimeDisplay(1)
                self.ResultData['Plot']['ROOTObjects'][name].GetYaxis().SetDecimals()
                self.ResultData['Plot']['ROOTObjects'][name].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObjects'][name].GetYaxis().CenterTitle()

            self.ResultData['Plot']['ObjectCanvas'][name] = canvas

            # tuple.Draw("time:temp","","APL")
            # get
        #print 'Analysed "%s"' % fileName
        #print 'Temp: %2.2f +/- %2.2f °C, Min: %2.2f, Max %2.2f' % (temp, tempError, tempMin, tempMax)
        #print 'duration: %s - %s, %s, %s' % (
        #    str(datetime.timedelta(seconds=duration)), timeMax - timeMin, timeMax, timeMin)
        return duration, temp, tempError, tempMin, tempMax

    def createTemperaturePlot(self):
        for i in self.ResultData['Plot']['ObjectCanvas']:
            fName = self.GetPlotFileName().split('.')[0].strip()
            fName = fName + '_' + i + '.svg'
            if self.SavePlotFile:
                canvas = self.ResultData['Plot']['ObjectCanvas'][i]
                canvas.SaveAs(fName)
            if 'Execute' in i:
                self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTObjects'][i]

                # self.ResultData['Plot']['ROOTObject'].SetTitle('');
                # self.ResultData['Plot']['ROOTObject'].Draw("APL");
                # self.ResultData['Plot']['ROOTObject'].SetLineColor(4);
                # self.ResultData['Plot']['ROOTObject'].SetLineWidth(2);
                #
                # self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Time ")
                # self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Tempeature [#circ C]")
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].Draw("APL")

    def analyseTempPrepare(self):
        Directory = self.ParentObject.RawTestSessionDataPath
        Directory.rstrip('/')
        fileName = Directory + '/TempLog_Prepare.log'
        duration, temp, tempError, min_temp, max_temp = self.analyseTemp(fileName)
        self.durationPrepare = duration
        self.tempPrepare = temp
        self.tempPrepareError = tempError
        pass

    def analyseTempExecute(self):
        Directory = self.ParentObject.RawTestSessionDataPath
        Directory.rstrip('/')
        fileName = Directory + '/TempLog_Execute.log'
        duration, temp, tempError, min_temp, max_temp = self.analyseTemp(fileName)
        self.duration = duration
        self.tempTest = temp
        self.tempError = tempError

    def analyseTempCleanup(self):
        Directory = self.ParentObject.RawTestSessionDataPath
        Directory.rstrip('/')
        fileName = Directory + '/TempLog_Cleanup.log'
        duration, temp, tempError, min_temp, max_temp = self.analyseTemp(fileName)
        self.durationCleanup = duration
        self.tempCleanup = temp
        self.tempCleanupError = tempError

    def PopulateResultData(self):
        # self.tempPrepare = 0
        # self.tempPrepareError = 0
        # self.tempTest = 0
        # self.tempTestError = 0
        # self.tempCleanup = 0
        # self.tempCleanupError = 0
        # self.duration = 0
        # self.durationPrepare = 0
        #         self.durationCleanup = 0

        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)

        self.analyseTempPrepare()
        self.analyseTempExecute()
        self.analyseTempCleanup()

        self.ResultData['KeyValueDictPairs'] = {
            'TemperaturePrepare': {
                'Value': '%2.2f' % self.tempPrepare,
                'Unit': '°C',
                'Label': 'Temp. preparing test',
            },
            'TemperaturePrepareError': {
                'Value': '%2.2f' % self.tempPrepareError,
                'Unit': '°C',
                'Label': 'Temp. error preparing test',
            },

            'TemperatureTest': {
                'Value': '%2.1f' % self.tempTest,
                'Unit': '°C',
                'Label': 'Temp. while test',
            },
            'TemperatureTestError': {
                'Value': '%2.2f' % self.tempError,
                'Unit': '°C',
                'Label': 'Temp. error while test',
            },

            'TemperatureCleanup': {
                'Value': '%2.2f' % self.tempCleanup,
                'Unit': '°C',
                'Label': 'Temp. cleaning up test',
            },
            'TemperatureCleanupError': {
                'Value': '%2.2f' % self.tempCleanupError,
                'Unit': '°C',
                'Label': 'Temp. error cleaning up test',
            },

            'Temperature': {
                'Value': '%2.2f +/- %2.2f' % (self.tempTest, self.tempError),
                'Unit': '°C',
                'Label': 'Temp. while test',
            },

            'Duration': {
                'Value': '%s' % (str(datetime.timedelta(seconds=self.duration))),
                'Unit': '',
                'Label': 'Duration of test',
            },

            'DurationPrepare': {
                'Value': '%s' % (str(datetime.timedelta(seconds=self.durationPrepare))),
                'Unit': '',
                'Label': 'Duration preparing test',
            },

            'DurationCleanup': {
                'Value': '%s' % (str(datetime.timedelta(seconds=self.duration))),
                'Unit': '',
                'Label': 'Duration to cleanup test',
            },
        }
        self.ResultData['KeyList'] = ['Temperature', 'Duration']
        self.createTemperaturePlot()
        self.ResultData['Plot']['Caption'] = 'Temperature'
        self.SaveCanvas()        
