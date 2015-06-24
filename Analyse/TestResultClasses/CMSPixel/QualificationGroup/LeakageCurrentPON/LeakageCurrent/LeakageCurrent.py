import ROOT
import array
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import numpy
import ROOT
import time
import datetime

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_LeakageCurrentPON_LeakageCurrent_TestResult'
        self.NameSingle='LeakageCurrent'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def ReadTimestamp(self, value):
        TimestampConverted = 0
        try:
            TimestampConverted = float(value)
        except:
            TimestampConverted = time.mktime(datetime.datetime.strptime(value[0:19], "%Y-%m-%d %H:%M:%S").timetuple())
            TimestampConverted += float("0.%s"%value[20:24])
        return TimestampConverted

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        voltages = []
        currents = []
        timestamps = []

        first = True
        timeOffset = 0
        minCurrent = 999
        minCurrentPos = 0
        minCurrentVoltage = 0

        for line in self.ParentObject.FileHandle:
            if not line.startswith('#'):
                Values = line.strip().split("\t")

                if first:
                    first = False
                    timeOffset = self.ReadTimestamp(Values[2])

                voltage = float(Values[0])
                current = float(Values[1])
                timeAfterStartup = self.ReadTimestamp(Values[2]) - timeOffset

                currents.append(current)
                voltages.append(voltage)
                timestamps.append(timeAfterStartup)

        # take 2nd value measured by Keithley
        leakageCurrent = currents[1]
        Voltage = voltages[1]

        numPoints = len(numpy.array(timestamps))
        tgraph = ROOT.TGraph(numPoints, numpy.array(timestamps), numpy.array(currents))

        self.ResultData['Plot']['ROOTGraph'] = tgraph.Clone()
        self.ResultData['Plot']['Caption'] = self.ParentObject.Attributes['ModuleID']


        if self.ResultData['Plot']['ROOTGraph']:
            self.Canvas.Clear()

            self.ResultData['Plot']['ROOTGraph'].SetName("%s_%r"%(self.ParentObject.Attributes['ModuleID'],self.GetUniqueID()))
            self.ResultData['Plot']['ROOTGraph'].SetTitle(";time [s];leakage current")
            self.ResultData['Plot']['ROOTGraph'].GetXaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTGraph'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTGraph'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTGraph'].GetYaxis().CenterTitle()

            self.ResultData['Plot']['ROOTGraph'].Draw('APL')
            self.ResultData['Plot']['ROOTGraph'].GetXaxis().SetLabelSize(0.05)
            self.ResultData['Plot']['ROOTGraph'].GetYaxis().SetLabelSize(0.05)
            self.ResultData['Plot']['ROOTGraph'].GetXaxis().SetTitleSize(0.05)
            self.ResultData['Plot']['ROOTGraph'].GetYaxis().SetTitleSize(0.05)

            self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTGraph']

        self.ResultData['Plot']['Enabled'] = 1

        self.SaveCanvas()

        self.ResultData['Plot']['ROOTObject'] = 0

        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value':self.ParentObject.Attributes['ModuleID'],
                'Label':'Module'
            },
            'LeakageCurrent': {
                'Value': leakageCurrent,
                'Label':'Leakage current [A]'
            },
            'Voltage': {
                'Value': Voltage,
                'Label':'Voltage [V]'
            },
        }
        self.ResultData['KeyList'] = ['Module','LeakageCurrent','Voltage']
