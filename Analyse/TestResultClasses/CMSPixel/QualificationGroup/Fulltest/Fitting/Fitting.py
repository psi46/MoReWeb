# -*- coding: utf-8 -*-
import AbstractClasses
from SCurve_Fitting import *
from PH_Fitting import *
import ConfigParser
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):

    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Fitting_TestResult'
        self.NameSingle='Fitting'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = '_'

        self.FitRevisionScurves = 0
        self.FitRevisionPHlin = 0
        self.FitRevisionPHtan = 0

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

        refitScurves = refit
        refitPHlin = refit
        refitPHtan = refit

        # compare current fit revision with saved revision
        FitRevDict = BetterConfigParser()
        fitRevFileName = directory + "/fits.rev"
        if os.path.isfile(fitRevFileName):

            try:
                FitRevDict.read(fitRevFileName)

                # if fit procedure changed -> refit
                if self.FitRevisionScurves > int(FitRevDict.get('FitRevisions', 'SCurves')):
                    print "info: fit procedure has changed, re-fitting scurves..."
                    refitScurves = True
                if self.FitRevisionPHlin > int(FitRevDict.get('FitRevisions', 'PHlin')):
                    print "info: fit procedure has changed, re-fitting ph lin..."
                    refitPHlin = True
                if self.FitRevisionPHtan > int(FitRevDict.get('FitRevisions', 'PHtan')):
                    print "info: fit procedure has changed, re-fitting ph tan..."
                    refitPHtan = True

                # if last fitting was not done completely (eg. STRG+C while fit...) -> refit
                if FitRevDict.get('Fit', 'Complete').strip().lower() != 'true':
                    print "info: last fit was incomplete! re-fitting all..."
                    refitScurves = True
                    refitPHlin = True
                    refitPHtan = True
            except:
                print "warning: could not read fit revision file!"

        else:
            FitRevDict.add_section('FitRevisions')
            FitRevDict.add_section('Fit')

        # unset complete flag in file
        FitRevDict.set('Fit','Complete', 'false')
        with open(fitRevFileName, 'wb') as fitRevFile:
            FitRevDict.write(fitRevFile)

        print 'SCurve fitting...'
        ePerVcal =  self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor']
        fitter = SCurve_Fitting(refit=refitScurves, HistoDict=self.ParentObject.HistoDict,ePerVcal=ePerVcal, ParallelProcessing=ParallelProcessing, LimitProcesses=LimitProcesses)
        fitter.FitAllSCurve(directory,nRocs)
        print 'linear PH fitting...'
        fitter = PH_Fitting(fitMode=0, refit=refitPHlin, HistoDict=self.ParentObject.HistoDict, ParallelProcessing=ParallelProcessing, LimitProcesses=LimitProcesses)
        fitter.FitAllPHCurves(directory,nRocs)
        print 'tanh PH fitting...'
        fitter = PH_Fitting(fitMode=3, refit=refitPHtan, HistoDict=self.ParentObject.HistoDict, ParallelProcessing=ParallelProcessing, LimitProcesses=LimitProcesses)
        fitter.FitAllPHCurves(directory,nRocs)

        # update saved revisions
        FitRevDict.set('FitRevisions','SCurves', str(self.FitRevisionScurves))
        FitRevDict.set('FitRevisions','PHlin', str(self.FitRevisionPHlin))
        FitRevDict.set('FitRevisions','PHtan', str(self.FitRevisionPHtan))

        # unset complete flag in file
        FitRevDict.set('Fit','Complete', 'true')
        with open(fitRevFileName, 'wb') as fitRevFile:
            FitRevDict.write(fitRevFile)

        print 'done'
