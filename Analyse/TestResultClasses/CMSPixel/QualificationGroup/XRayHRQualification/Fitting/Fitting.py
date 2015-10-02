import ROOT
import AbstractClasses
import ConfigParser
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser
from TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Fitting.SCurve_Fitting import *
import os

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_Fitting_TestResult'
        self.NameSingle='Fitting'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

        self.FitRevisionScurves = 0

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

        # compare current fit revision with saved revision
        FitRevDict = BetterConfigParser()
        fitRevFileName = directory + "/fits.rev"
        if os.path.isfile(fitRevFileName):

            try:
                FitRevDict.read(fitRevFileName)

                # if fit procedure changed -> refit
                if self.FitRevisionScurves > int(FitRevDict.get('FitRevisions', 'SCurves')):
                    print "info: fit procedure has changed, re-fitting..."
                    refit = True

                # if last fitting was not done completely (eg. STRG+C while fit...) -> refit
                if FitRevDict.get('Fit', 'Complete').strip().lower() != 'true':
                    print "info: last fit was incomplete! re-fitting..."
                    refit = True
            except:
                print "warning: could not read fit revision file!"

        else:
            FitRevDict.add_section('FitRevisions')
            FitRevDict.add_section('Fit')

        # unset complete flag in file
        FitRevDict.set('Fit','Complete', 'false')
        with open(fitRevFileName, 'wb') as fitRevFile:
            FitRevDict.write(fitRevFile)

        # do fitting
        fitter = SCurve_Fitting(refit=refit, HistoDict=HistoDict, ePerVcal=ePerVcal, ParallelProcessing=ParallelProcessing, LimitProcesses=LimitProcesses)
        fitter.FitAllSCurve(directory, nRocs)

        # update saved revision
        FitRevDict.set('FitRevisions','SCurves', str(self.FitRevisionScurves))

        # set complete flag in file
        FitRevDict.set('Fit','Complete', 'true')
        with open(fitRevFileName, 'wb') as fitRevFile:
            FitRevDict.write(fitRevFile)