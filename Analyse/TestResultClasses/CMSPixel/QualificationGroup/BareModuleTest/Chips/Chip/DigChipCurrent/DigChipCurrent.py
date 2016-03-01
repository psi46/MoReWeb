import ROOT
import array
import datetime
import AbstractClasses.Helper.HistoGetter as HistoGetter
import AbstractClasses
import TestResultClasses
#import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.DigitalCurrent.DigitalCurrent
#class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.DigitalCurrent.DigitalCurrent.TestResult):
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
    	# Call Overridden CustomInit()
    	# super(TestResult, self).CustomInit()    	
        #ROOTConfiguration.initialise_ROOT()
        self.Name='CMSPixel_QualificationGroup_BareModuleTest_Chips_Chip_DigitalCurrent_TestResult'
        self.NameSingle='DigChipCurrent'
        #self.NameSingle='DigitalCurrent'
        self.chipNo = self.ParentObject.Attributes['ChipNo']

        
            
        
    def PopulateResultData(self):

        ChipNo=self.ParentObject.Attributes['ChipNo']
        self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        histname = self.HistoDict.get(self.NameSingle,'DigitalCurrent')
        #print 'inside DigChipCurrent ',histname, self.HistoDict

        #if self.HistoDict.has_option(self.NameSingle,'DigChipCurrent'):
        #    histname = self.HistoDict.get(self.NameSingle,'DigitalCurrent')
        #    object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
        #    print 'aqui bla bla bla !!bjkhnkjad', object
        #self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())
        #print 'once again: ',object
        
        object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
        if object == None: 
            print 'here inside bla bla bla DigChipCurrent: '
            
            self.ResultData['KeyValueDictPairs'] = {
                'Duration': {
                    'Value': 'None',
                    'Label': 'Duration',
                    'Unit': ''                
                    },
                'MaxCurrent': {
                    'Value': 'None',
                    'Label': 'max. Current',
                    'Unit': 'A'
                    },
                'MinCurrent': {
                    'Value': 'None',
                    'Label': 'min. Current',
                    'Unit': 'A'
                    }
                }
        else:
            self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())
            ROOTObject = self.ResultData['Plot']['ROOTObject']

            times = []
            currents = []
            title = ROOTObject.GetTitle()
            seconds = float(title.split(':')[-1])
            print title,seconds
            seconds = 0
            # raw_input()
        #print 'bins bla bla: ',self.ResultData['Plot']['ROOTObject'].GetNbinsX()
        
            for bin in range(1,ROOTObject.GetNbinsX()+1):
                if ROOTObject.GetBinContent(bin)>0:
                    times.append(ROOTObject.GetXaxis().GetBinCenter(bin)+seconds)
                    currents.append(ROOTObject.GetBinContent(bin))
                #print bin,times[-1],currents[-1]
                    times = array.array('d',times)
                    currents = array.array('d',currents)

            graph = ROOT.TGraph(len(times),times,currents)
            graph.SetName(self.GetUniqueID())
            graph.SetMarkerStyle(7)
            graph.SetLineStyle(2)
            graph.SetLineColor(ROOT.kBlue)
            graph.Draw('AL ')
            graph.GetXaxis().SetTimeOffset(seconds,'GMT')
            graph.GetXaxis().SetTitle("Time")
            graph.GetXaxis().SetTimeDisplay(1)
        # if max(times) > 30*60:
            graph.GetXaxis().SetTimeFormat('%H:%M')
            graph.GetYaxis().SetRangeUser(0,graph.GetYaxis().GetXmax()*1.1)
        

            delta = datetime.timedelta(seconds = max(times)-min(times))
            print str(delta)
            self.ResultData['KeyValueDictPairs'] = {
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

            self.ResultData['KeyList'] = ['Duration','MinCurrent','MaxCurrent']
            self.ResultData['Plot']['ROOTGraph'] = graph

            if self.ResultData['Plot']['ROOTGraph']:
                self.Canvas.Clear()
                self.ResultData['Plot']['ROOTGraph'].SetTitle("")
                self.ResultData['Plot']['ROOTGraph'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTGraph'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTGraph'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTGraph'].Draw('APL')
                self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTGraph']
                self.ResultData['Plot']['Enabled'] = 1
                self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
                print self.GetPlotFileName()
                self.Title = 'Digital Current'
            if self.SavePlotFile:
            #print 'SavePlotFile', self.SavePlotFile
                self.Canvas.SaveAs(self.GetPlotFileName())

