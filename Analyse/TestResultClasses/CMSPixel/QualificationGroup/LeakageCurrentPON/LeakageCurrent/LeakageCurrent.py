import ROOT
import array
import AbstractClasses
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

        for line in self.ParentObject.FileHandle:
            if not line.startswith('#'):
                Values = line.strip().split("\t")

                if first:
                    first = False
                    timeOffset = self.ReadTimestamp(Values[2])

                voltage = abs(float(Values[0]))
                current = abs(float(Values[1]))
                timeAfterStartup = self.ReadTimestamp(Values[2]) - timeOffset

                currents.append(current)
                voltages.append(voltage)
                timestamps.append(timeAfterStartup)

        # take 2nd value measured by Keithley
        if len(voltages) > 1:
            leakageCurrent = currents[1]
            Voltage = voltages[1]
            Timestamp = timestamps[1]
        elif len(voltages) > 0:
            leakageCurrent = currents[0]
            Voltage = voltages[0]
            Timestamp = timestamps[0]
        else:
            leakageCurrent = 0
            Voltage = 0
            Timestamp = 0


        numPoints = len(array.array('d', timestamps))
        tgraph = ROOT.TGraph(numPoints, array.array('d', timestamps), array.array('d', currents))

        self.ResultData['Plot']['ROOTObject'] = tgraph.Clone()
        self.ResultData['Plot']['Caption'] = self.ParentObject.Attributes['ModuleID']


        if self.ResultData['Plot']['ROOTObject']:
            self.Canvas.Clear()

            self.ResultData['Plot']['ROOTObject'].SetName("%s_%r"%(self.ParentObject.Attributes['ModuleID'],self.GetUniqueID()))
            self.ResultData['Plot']['ROOTObject'].SetTitle(";time [s];leakage current")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue+2)
            self.ResultData['Plot']['ROOTObject'].SetMarkerColor(ROOT.kBlue+2)
            self.ResultData['Plot']['ROOTObject'].SetMarkerStyle(21)
            self.ResultData['Plot']['ROOTObject'].Draw('APL')
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetLabelSize(0.05)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetLabelSize(0.05)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitleSize(0.05)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleSize(0.05)

            MaxCurrent = max([abs(current) for current in currents])
            GradeBCurrent = self.TestResultEnvironmentObject.GradingParameters['leakageCurrentPON_B']*1.e-6
            GradeCCurrent = self.TestResultEnvironmentObject.GradingParameters['leakageCurrentPON_C']*1.e-6
            Line = ROOT.TLine()

            self.ResultData['Plot']['ROOTObject'].SetMinimum(0)
            if MaxCurrent < GradeBCurrent:
                self.ResultData['Plot']['ROOTObject'].SetMaximum(1.1*GradeBCurrent)
            else:
                self.ResultData['Plot']['ROOTObject'].SetMaximum(1.1*MaxCurrent)

            Line.SetLineColor(ROOT.kRed)
            lineB = Line.DrawLine(self.ResultData['Plot']['ROOTObject'].GetXaxis().GetXmin(), GradeBCurrent, self.ResultData['Plot']['ROOTObject'].GetXaxis().GetXmax(), GradeBCurrent)

            if MaxCurrent > GradeCCurrent:
                Line.SetLineColor(ROOT.kRed)
                lineC = Line.DrawLine(self.ResultData['Plot']['ROOTObject'].GetXaxis().GetXmin(), GradeCCurrent, self.ResultData['Plot']['ROOTObject'].GetXaxis().GetXmax(), GradeCCurrent)

            el2 = ROOT.TEllipse(Timestamp, leakageCurrent, 4, abs(self.ResultData['Plot']['ROOTObject'].GetMaximum())*0.05)
            el2.SetLineColor(ROOT.kRed)
            el2.SetFillStyle(0)
            el2.Draw('')

        self.ResultData['Plot']['Enabled'] = 1

        self.SaveCanvas()

        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value':self.ParentObject.Attributes['ModuleID'],
                'Label':'Module'
            },
            'LeakageCurrent': {
                'Value': '%0.2e' % float(leakageCurrent),
                'Label':'Leakage current [A]'
            },
            'Voltage': {
                'Value': '%0.2e' % float(Voltage),
                'Label':'Voltage [V]'
            },
        }
        self.ResultData['KeyList'] = ['Module','LeakageCurrent','Voltage']
