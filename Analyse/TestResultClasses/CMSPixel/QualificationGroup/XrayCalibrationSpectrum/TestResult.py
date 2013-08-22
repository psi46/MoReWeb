'''
    Program: X-Ray Calibration Test Result
    Author: Paul Turner - pturne7@uic.edu
    Version : 1.0
    Release Date : 2013-07-18
'''
import AbstractClasses
import ROOT
import ConfigParser
import os
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_ModuleTestGroup_Module_XRayCalibrationSpectrum_TestResult'
        self.NameSingle='XrayCalibrationSpectrum'
        print self.NameSingle+": "+str(self.Attributes['SubTestResultDictList'])
        for e in self.Attributes['SubTestResultDictList']:
            print 'adding'+str(e)
            self.ResultData['SubTestResultDictList'].append(e)
            pass
        print self.ResultData['SubTestResultDictList']
        self.Attributes['TestedObjectType'] = 'XrayCalibrationSpectrum'
        self.DisplayOptions = {'DisplayOptions':{'Order':1, 'Width':3,'GroupWithNext':False},}
        #self.DisplayOptions['Width'] = 5
#        print self.Attributes
#        for e in self.Attributes['SubTestResultDictList']:
#            print e
###            print '\nadding' + str(e) + '\n'
#            self.ResultData['SubTestResultDictList'].append(e)
    def OpenFileHandle(self):
        #self.FileHandle = self.ParentObject.FileHandle	
        pass

    def PopulateResultData(self):
        PeakCenters = array.array('d',[])
        PeakErrors = array.array('d',[])
        NumElectrons = array.array('d',[])
        print 'sub test resiults'
        print type(self.ResultData['KeyValueDictPairs'])
        for e in self.ResultData['SubTestResults']:
            keyValuePairs = self.ResultData['SubTestResults'][e].ResultData['KeyValueDictPairs']
            print e,keyValuePairs['Center']['Value'],keyValuePairs['TargetNElectrons']['Value']
            PeakCenters.append(keyValuePairs['Center']['Value'])
            PeakErrors.append(keyValuePairs['Center']['Sigma'])
            NumElectrons.append(keyValuePairs['TargetNElectrons']['Value'])
        pointPairs = zip(PeakCenters,NumElectrons,PeakErrors)
        sortedPoints = sorted(pointPairs, key=lambda point: point[1])
        prevPoint = sortedPoints[0][0]
        num = 0
        for e in sortedPoints:
            if e[0] < prevPoint:
                print "Error: Lower VCal for higher energy...possible fit error. Point in question: ",e
                sortedPoints.pop(num)
            num = num + 1
            prevPoint = e[0]
        newSortedPoints = sorted(sortedPoints, key=lambda point: point[0])
        sortedPeakCenters = array.array('d',[])
        sortedNumElectrons = array.array('d',[])
        sortedPeakErrors = array.array('d',[])
        sortedElectronError = array.array('d',[])
        for e in newSortedPoints:
            sortedPeakCenters.append(e[0])
            sortedNumElectrons.append(e[1])
            sortedPeakErrors.append(e[2])
            sortedElectronError.append(0.0)
        self.ResultData['Plot']['ROOTObject'] = ROOT.TGraphErrors(len(sortedPeakCenters),sortedPeakCenters,sortedNumElectrons,sortedPeakErrors,sortedElectronError)
        self.ResultData['Plot']['ROOTObject'].SetTitle("Center of Pulse Height (Vcal units) vs number of electrons;Center of Pulse Height[Vcal];Number of Electrons")
        self.ResultData['Plot']['ROOTObject'].SetMarkerColor(4)
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.6)
        #self.ResultData['Plot']['ROOTObject'].SetMarkerStyle(21)
        self.ResultData['Plot']['ROOTObject'].Fit("pol1","","SAME",sortedPeakCenters[0],sortedPeakCenters[ len(sortedPeakCenters) -1])
        chi2Total = self.ResultData['Plot']['ROOTObject'].GetFunction("pol1").GetChisquare()
        self.ResultData['Plot']['ROOTObject'].Fit("pol1","","SAME",sortedPeakCenters[1],sortedPeakCenters[ len(sortedPeakCenters) -1])
        chi2Right = self.ResultData['Plot']['ROOTObject'].GetFunction("pol1").GetChisquare()
        self.ResultData['Plot']['ROOTObject'].Fit("pol1","","SAME",sortedPeakCenters[0],sortedPeakCenters[ len(sortedPeakCenters) -2])
        chi2Left = self.ResultData['Plot']['ROOTObject'].GetFunction("pol1").GetChisquare()
        if ((chi2Right < chi2Total) or (chi2Left < chi2Total)):
            if chi2Right < chi2Left:
                self.ResultData['Plot']['ROOTObject'].Fit("pol1","","SAME",sortedPeakCenters[1],sortedPeakCenters[ len(sortedPeakCenters) -1])
                print "Excluding Leftmost Point because chi2Total=",chi2Total," and chi2Right=",chi2Right
            else:
                self.ResultData['Plot']['ROOTObject'].Fit("pol1","","SAME",sortedPeakCenters[0],sortedPeakCenters[ len(sortedPeakCenters) -2])
                print "Excluding Rightmost Point because chi2Total=",chi2Total," and chi2Left=",chi2Left
        fit = self.ResultData['Plot']['ROOTObject'].GetFunction("pol1")
        self.ResultData['KeyValueDictPairs'] = {
            'Slope': {
                'Value': round(fit.GetParameter(1),3),
                'Label':'Slope',
                'Unit': 'nElectrons/VCal',
                'Sigma': round(fit.GetParError(1),3),
            },
            'Offset': {
                'Value': round(fit.GetParameter(0),3),
                'Label':'Offset',
                'Unit': 'nElectrons',
                'Sigma': round(fit.GetParError(0),3),
            },
        
        }
        self.ResultData['KeyList'] = ['Slope','Offset']
        self.ResultData['Plot']['ROOTObject'].Draw("APL")
        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'VCal Calibration'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
#            print e,str(e.ResultData['KeyValueDictPairs'])
        pass
#            
##    '''
##    * Function that performs the energy calibration fit for a single chip
##    '''
#    def FitChip(self):
#        for i in range(self.ParentObject.Attributes['NumberOfChips']-self.ParentObject.Attributes['StartChip']):
#            x = []
#            y = []
#            ex = []
#            ey = []
#            for e in self.Configuration.items('Elements'):
#                fitParams []
#                fitErrors []
#                paramHistos []
#                fit = TF1() # Add code to extract fit from subtest
#                for param in range( fit.GetNumberFreeParameters() ):
#                    fitParams.append( fit.GetParameter(param) )
#                    fitErrors.append( fit.GetParError(param) )
#                x.append( fitParams[3] )
#                ex.append( fitErrors[3] )
#                y.append( e[1] )
#                ey.append( 0 )
#            arrx = array('d',x)
#            arry = array('d',y)
#            arrex = array('d',ex)
#            arrey = array('d',ey)
#            n = len(arrx)
#                
#    '''
#            TCanvas* c0 = new TCanvas ("canvas_" + chipID, "Center of Pulse Height (Vcal units) vs number of electrons", 200, 100, 700, 500);
#            c0->SetGrid();
#    '''
#            
#            
#            gr = TGraphErrors(n,ax,ay,aex,aey)
#            gr.SetTitle("Center of Pulse Height (Vcal units) vs number of electrons;Center of Pulse Height[Vcal];Number of Electrons")
#            gr.SetMarkerColor(4)
#            gr.SetMarkerStyle(21)
#            gr.Fit("pol1","","SAME",ax[0],ax[(n-1)])
#            fit = gr.GetFunction("pol1")
#            #HOW TO SAVE THE FIT NOW?
#    '''
#            fit->SetName("fit_" + chipID);
#            ROOT::GetROOT()->GetStyle("Modern")->SetOptFit(1111);
#            ROOT::GetROOT()->SetStyle("Modern");
#            gr->Draw("AP");
#            c0->Update();
#            TString savedir = TString::Format("%s/%s",m_fitDir.Data(),chipID.Data());
#            if(cd(savedir)) {
#            m_outFile->SetWritable(true);
#            c0->Write("",TObject::kOverwrite);
#            fit->Write("",TObject::kOverwrite);
#            m_outFile->SetWritable(false);
#            }
#    '''


    def CustomWriteToDatabase(self, ParentID):
        Row = {
            'ModuleID' : self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'QualificationType': self.ParentObject.Attributes['QualificationType'],
            'Grade':  None,
            'PixelDefects': None,
            'ROCsMoreThanOnePercent': None,
            'Noise': None,
            'Trimming': None,
            'PHCalibration': None,
            'CurrentAtVoltage150': None,
            'IVSlope': None,
            'Temperature': None,
            'StorageFolder':os.path.relpath(self.TestResultEnvironmentObject.TestResultsPath, self.TestResultEnvironmentObject.OverviewPath),
            'RelativeModuleFulltestStoragePath':os.path.relpath(self.StoragePath, self.TestResultEnvironmentObject.TestResultsPath),
            'initialCurrent': None,
            'Comments': '',
            'nCycles': None,
            'CycleTempLow': None,
            'CycleTempHigh':None,
        }
        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            pass
        else:
            with self.TestResultEnvironmentObject.LocalDBConnection:
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute('DELETE FROM ModuleTestResults WHERE ModuleID = :ModuleID AND TestType=:TestType AND QualificationType=:QualificationType AND TestDate <= :TestDate',Row)
                print 'insert into DB - Xray'
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                    '''INSERT INTO ModuleTestResults 
                    (
                        ModuleID,
                        TestDate,
                        TestType,
                        QualificationType,
                        Grade,
                        PixelDefects,
                        ROCsMoreThanOnePercent,
                        Noise,
                        Trimming,
                        PHCalibration,
                        CurrentAtVoltage150,
                        IVSlope,
                        Temperature,
                        StorageFolder,
                        RelativeModuleFulltestStoragePath,
                        initialCurrent,
                        Comments,
                        nCycles,
                        CycleTempLow,
                        CycleTempHigh
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :QualificationType,
                        :Grade,
                        :PixelDefects,
                        :ROCsMoreThanOnePercent,
                        :Noise,
                        :Trimming,
                        :PHCalibration,
                        :CurrentAtVoltage150,
                        :IVSlope,
                        :Temperature,
                        :StorageFolder,
                        :RelativeModuleFulltestStoragePath,
                        :initialCurrent,
                        :Comments,
                        :nCycles,
                        :CycleTempLow,
                        :CycleTempHigh
                    )
                    ''', Row)
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid
            
