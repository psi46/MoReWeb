'''
    Program: X-Ray Calibration Test Result
    Author: Paul Turner - pturne7@uic.edu
    Version : 1.0
    Release Date : 2013-07-18
'''
import AbstractClasses
import ROOT
import ConfigParser
from array import array
from ROOT import TF1,TGraphErrors

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
#        print self.Attributes
#        for e in self.Attributes['SubTestResultDictList']:
#            print e
###            print '\nadding' + str(e) + '\n'
#            self.ResultData['SubTestResultDictList'].append(e)
    def OpenFileHandle(self):
        #self.FileHandle = self.ParentObject.FileHandle	
        pass
    
    def PopulateResultData(self):
        print 'sub test resiults'
        print type(self.ResultData['KeyValueDictPairs'])
        for e in self.ResultData['SubTestResults']:
            keyValuePairs = self.ResultData['SubTestResults'][e].ResultData['KeyValueDictPairs']
            print e,keyValuePairs['Center']['Value']
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
#            
#
#
