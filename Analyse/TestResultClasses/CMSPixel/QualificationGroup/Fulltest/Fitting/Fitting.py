# -*- coding: utf-8 -*-
import AbstractClasses
from SCurve_Fitting import *
from PH_Fitting import *
import ConfigParser

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):

    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Fitting_TestResult'
        self.NameSingle='Fitting'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = '_'


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

        print 'do fitting...'
        nRocs = self.Attributes['NumberOfChips']
        directory = self.RawTestSessionDataPath
        refit = self.TestResultEnvironmentObject.Configuration['Fitting']['refit']
        print 'SCurve fitting...'
        ePerVcal =  self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor']
        fitter = SCurve_Fitting(refit,HistoDict = self.ParentObject.HistoDict,ePerVcal=ePerVcal, ParallelProcessing=ParallelProcessing, LimitProcesses=LimitProcesses)
        fitter.FitAllSCurve(directory,nRocs)
        print 'linear PH fitting...'
        fitter = PH_Fitting(0,refit,HistoDict = self.ParentObject.HistoDict, ParallelProcessing=ParallelProcessing, LimitProcesses=LimitProcesses)
        fitter.FitAllPHCurves(directory,nRocs)
        print 'tanh PH fitting...'
        fitter = PH_Fitting(3,refit,HistoDict = self.ParentObject.HistoDict, ParallelProcessing=ParallelProcessing, LimitProcesses=LimitProcesses)
        fitter.FitAllPHCurves(directory,nRocs)
        print 'done'
