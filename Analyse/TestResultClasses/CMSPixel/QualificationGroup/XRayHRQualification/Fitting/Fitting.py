import ROOT
import AbstractClasses
import ConfigParser
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser
from TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Fitting.SCurve_Fitting import *

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_Fitting_TestResult'
        self.NameSingle='Fitting'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):

        SysConfiguration = ConfigParser.ConfigParser()
        SysConfiguration.read(['Configuration/SystemConfiguration.cfg'])
        ParallelProcessing = False
        LimitProcesses = None
        try:
            if int(SysConfiguration.get('SystemConfiguration', 'ParallelProcessing').strip())>0:
                ParallelProcessing = True
        except:
            print "no 'ParallelProcessing' option found, running sequentially..."
            pass

        try:
            if int(SysConfiguration.get('SystemConfiguration', 'LimitProcesses').strip())>0:
                LimitProcesses = int(SysConfiguration.get('SystemConfiguration', 'LimitProcesses').strip())
        except:
            pass

        nRocs = self.ParentObject.Attributes['NumberOfChips']
        directory = self.ParentObject.Attributes['SCurvePaths']['HRSCurves_{Rate}'.format(Rate=self.Attributes['Rate'])]
        refit = self.TestResultEnvironmentObject.Configuration['Fitting']['refit']

        print 'SCurve fitting...'
        HistoDict = BetterConfigParser()
        HistoDict.add_section('SCurveFitting')
        HistoDict.set('SCurveFitting','nTrigs', str(10))
        HistoDict.set('SCurveFitting','dir', '')
        HistoDict.set('SCurveFitting','ignoreValidityCheck', '1')
        HistoDict.set('SCurveFitting','inputFileName', self.ParentObject.ParentObject.HistoDict.get('HighRate', 'SCurveDataFileName'))

        ePerVcal =  self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor']
        fitter = SCurve_Fitting(refit,HistoDict = HistoDict,ePerVcal=ePerVcal, ParallelProcessing=ParallelProcessing, LimitProcesses=LimitProcesses)
        fitter.FitAllSCurve(directory, nRocs)