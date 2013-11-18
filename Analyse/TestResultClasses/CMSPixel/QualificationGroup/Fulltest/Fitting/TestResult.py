# -*- coding: utf-8 -*-
import AbstractClasses
from SCurve_Fitting import *
from PH_Fitting import *
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):

    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Fitting_TestResult'
        self.NameSingle='Fitting'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = '_'
        
    def PopulateResultData(self):

        nRocs = self.Attributes['NumberOfChips']
        directory = self.RawTestSessionDataPath
        refit = self.TestResultEnvironmentObject.Configuration['Fitting']['refit']
        print 'SCurve fitting...'
        fitter = SCurve_Fitting(refit)
        fitter.FitAllSCurve(directory,nRocs)
        print 'linear PH fitting...'
        fitter = PH_Fitting(0,refit)
        fitter.FitAllPHCurves(directory,nRocs)
        print 'tanh PH fitting...'
        fitter = PH_Fitting(3,refit)
        fitter.FitAllPHCurves(directory,nRocs)
