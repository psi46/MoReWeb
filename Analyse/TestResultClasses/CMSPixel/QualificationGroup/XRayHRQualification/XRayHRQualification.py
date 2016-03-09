import os
import sys
import ROOT
import os.path
import glob
import copy

from AbstractClasses.GeneralTestResult import GeneralTestResult
import subprocess
import warnings
import traceback
#import PixelDB


class TestResult(GeneralTestResult):
    def testDBFilling2(self, HighRateDataModule , HighRateDataAggr, HighRateDataAllNoise, HighRateDataInterp
                                             ,HighRateDataRoc
                                             ,HighRateDataAggrRoc
                                             ,HighRateDataAllNoiseRoc
                                             ,HighRateDataInterpRoc):
#            print "TOMMASO ALL DATA"
#            print "HighRateDataModule",HighRateDataModule
#            print "HighRateDataAggr",HighRateDataAggr
#            print "HighRateDataAllNoise",HighRateDataAllNoise
#            print "HighRateDataInterp",HighRateDataInterp
#            print "HighRateDataRoc",HighRateDataRoc
#            print "HighRateDataAggrRoc",HighRateDataAggrRoc
#            print "HighRateDataAllNoiseRoc",HighRateDataAllNoiseRoc
#            print "HighRateDataInterpRoc",HighRateDataInterpRoc

            #
            # MODULES
            #

            #
            #create Module part common to all the tests
            #
            fullmodule_id = HighRateDataModule['ModuleID']
            result = HighRateDataModule['HRGrade']
            macroVersion = HighRateDataModule['MacroVersion']
            addrPixBad = HighRateDataModule['AddrPixelsBad']
            addrPixHot = HighRateDataModule['AddrPixelsHot']
            n_hot_pixels = HighRateDataModule['NHotPixel']
            n_con_nonuniform= HighRateDataModule['ROCsWithUniformityProblems']

#
# prepare
#

            interpEffTestPoint = {}
            interpEff={}
            nPixelsNoise={}
            meanNoiseAllPixels = {}
            widthNoiseAllPixels = {}
            addrPixelNoise = {}
            measuredHitRate = {}
            nPixelNoHit = {}
            nBinsLowHigh = {}
            #
            # these are the common parts, now I do
            # 1- INTERP: search in HighRateDataInterp, HighRateDataInterpRoc , loop on the rates
            #            

            for rate, payload in HighRateDataInterp.iteritems():
                  print " Studying interpolation per Rate = ", rate
                  interpEffTestPoint[rate] = payload['InterpEffTestpoint']
                  interpEff[rate] = payload['InterpEffTestpoint']
                  
            #
            # now Noise
            #
            #
            for rate, payload in HighRateDataAllNoise.iteritems():
                  print " Studying Noise per Rate = ", rate            

                  nPixelsNoise[rate] = payload['NPixelsNoise']['Value']
                  meanNoiseAllPixels[rate] = payload['MeanNoiseAllPixels']
                  widthNoiseAllPixels[rate] = payload['WidthNoiseAllPixels']
                  addrPixelNoise[rate] = payload['AddrPixelsNoise']['Value']
                  
            #
            # now Aggregate (which is hitmap)
            #
            #
            for rate, payload in HighRateDataAggr.iteritems():
                  print ' Studying Hitmap per Rate = ', rate
                  measuredHitRate[rate] = payload['MeasuredHitrate']
                  nPixelNoHit[rate] = payload['NPixelNoHit']
                  nBinsLowHigh[rate] = payload['NBinsLowHigh']                  
                  

            #
            # try and accumulate
            #
                  
            rates = list(set(interpEffTestPoint.keys())|set(nPixelsNoise.keys())|set(measuredHitRate.keys()))

            # fill a result per rate

            for rate in rates:
                  print "Filling a test for rate=", rate
                  print "  - ModID",  fullmodule_id
                  print '  - Grade', result 
                  print "  - Macroversion", macroVersion
                  print "  - Addr Bad Pixels", addrPixBad
                  print "  - Addr HotPixels", addrPixHot
                  print "  - Num HotPixels", n_hot_pixels
                  print "  - Roc with Unif Prob", n_con_nonuniform
            # now rate dependent
                  print "   - Interp eff testpoint", interpEffTestPoint.get(rate, -99)
                  print "   - Interp eff", interpEff.get(rate, -99)
                  print "   - N Pixel Noise", nPixelsNoise.get(rate, -99)
                  print "   - Mean Noise All Pixel", meanNoiseAllPixels.get(rate, -99)
                  print "   - Width Noise All Pixel", widthNoiseAllPixels.get(rate, -99)
                  print "   - Addr Pixel Noise", addrPixelNoise.get(rate, -99)
                  print "   - Measered Hit Rate", measuredHitRate.get(rate, -99)
                  print "   - N Pixel No Hit", nPixelNoHit.get(rate, -99)
                  print "   - N Bins Low High", nBinsLowHigh.get(rate, -99)

            #
            # per roc
            #
            # common
            
            addrPixBad_roc={}
            addrPixHot_roc = {}
            n_hot_pixels_roc = {}
            n_con_nonuniform_roc = {}


            for roc, payload in HighRateDataRoc.iteritems():
                roc_pos = payload['RocPos']
                addrPixBad_roc[roc_pos] =  payload['AddrPixelsBad']
                addrPixHot_roc[roc_pos] =  payload['AddrPixelsHot']
                n_hot_pixels_roc[roc_pos] = payload['NHotPixel']
                n_con_nonuniform_roc[roc_pos] = -99

            #
            # interp
            #
            interpEffTestPoint_roc = {}
            interpEff_roc = {}
            for rate, payload1 in HighRateDataInterpRoc.iteritems():
                interpEffTestPoint_roc[rate] = {}
                interpEff_roc[rate] = {}
                for roc, payload in payload1.iteritems():
                    roc_pos = payload['RocPos']
                    print " Studying interpolation per Rate = ", rate, " and ROC=",roc_pos
                    interpEffTestPoint_roc[rate][roc_pos] = payload['InterpEffTestpoint']
                    interpEff_roc[rate][roc_pos] = payload['InterpEffTestpoint']
                    
                
            #
            # Noise
            #
            nPixelsNoise_roc = {}
            meanNoiseAllPixels_roc = {}
            widthNoiseAllPixels_roc = {}
            addrPixelNoise_roc = {}
    
            for rate, payload1 in HighRateDataAllNoiseRoc.iteritems():
                nPixelsNoise_roc [rate] = {}
                meanNoiseAllPixels_roc[rate] = {}
                widthNoiseAllPixels_roc[rate] = {}
                addrPixelNoise_roc[rate] = {}
                for roc, payload in payload1.iteritems():
                    roc_pos = payload['RocPos']
                    print " Studying Noise per Rate = ", rate, " and ROC=",roc_pos
                    nPixelsNoise_roc[rate][roc_pos] = payload['NPixelsNoise']
                    meanNoiseAllPixels_roc[rate][roc_pos] = payload['MeanNoiseAllPixels']
                    widthNoiseAllPixels_roc[rate][roc_pos] = payload['WidthNoiseAllPixels']
                    addrPixelNoise_roc[rate][roc_pos] = "%s"%payload['AddrPixelsNoise'] #['Value']
            #        
            # Aggregate (hitmap)
            #
            measuredHitRate_roc = {}
            nPixelNoHit_roc = {}
            nBinsLowHigh_roc = {}

            for rate, payload1 in HighRateDataAggrRoc.iteritems():
                measuredHitRate_roc[rate] = {}
                nPixelNoHit_roc[rate] = {}
                nBinsLowHigh_roc[rate] = {}

                for roc, payload in payload1.iteritems():
                    roc_pos = payload['RocPos']
                    print " Studying Hitmap per Rate = ", rate, " and ROC=",roc_pos
                    measuredHitRate_roc[rate][roc_pos] = payload['MeasuredHitrate']
                    nPixelNoHit_roc[rate][roc_pos] = payload['NPixelNoHit']
                    nBinsLowHigh_roc[rate][roc_pos] = payload['NBinsLowHigh']                  
                    
            #
            # Summary!
            #         

            print " ROC SUMMARY"

            for rate in rates:
                for roc in addrPixBad_roc.keys():
                    print " Filling ROC tests for rate", rate, " and POS=", roc
                    print "  - ModID",  fullmodule_id
                    print '  - Grade (WARNING!!!!!!)', result 
                    print "  - Macroversion", macroVersion
                    print "  - Addr Bad Pixels", addrPixBad_roc[roc]
                    print "  - Addr HotPixels", addrPixHot_roc[roc]
                    print "  - Num HotPixels", n_hot_pixels_roc[roc]
                    print "  - Roc with Unif Prob", n_con_nonuniform_roc[roc]
            # now rate dependent
                    print "   - Interp eff testpoint", interpEffTestPoint_roc[rate][roc] if rate in interpEffTestPoint_roc else -99
    	            print "   - Interp eff", interpEff_roc[rate][roc]  if rate in interpEff_roc else -99
                    print "   - N Pixel Noise", nPixelsNoise_roc[rate][roc] if rate in nPixelsNoise_roc else -99
                    print "   - Mean Noise All Pixel", meanNoiseAllPixels_roc[rate][roc] if rate in meanNoiseAllPixels_roc else -99
                    print "   - Width Noise All Pixel", widthNoiseAllPixels_roc[rate][roc] if rate in widthNoiseAllPixels_roc else -99
                    print "   - Addr Pixel Noise", addrPixelNoise_roc[rate][roc] if rate in addrPixelNoise_roc else -99
                    print "   - Measered Hit Rate", measuredHitRate_roc[rate][roc] if rate in measuredHitRate_roc else -99
                    print "   - N Pixel No Hit", nPixelNoHit_roc[rate][roc] if rate in nPixelNoHit_roc else -99
                    print "   - N Bins Low High", nBinsLowHigh_roc[rate][roc] if rate in nBinsLowHigh_roc else -99

#                    print "   - Width Noise All Pixel", widthNoiseAllPixels.get(rate, -99)
#                    print "   - Addr Pixel Noise", addrPixelNoise.get(rate, -99)
#                    print "   - Measered Hit Rate", measuredHitRate.get(rate, -99)
#                    print "   - N Pixel No Hit", nPixelNoHit.get(rate, -99)
 #                   print "   - N Bins Low High", nBinsLowHigh.get(rate, -99)

                


                  
            return




    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_TestResult'
        self.NameSingle = 'XRayHRQualification'
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['NumberOfChips'] = self.nTotalChips
        self.CreateJSONIndex = True
        #self.MergePyxarData()

        self.AddCommentsToKeyValueDictPairs = True
        if self.Attributes['ModuleVersion'] == 1:
            if self.Attributes['ModuleType'] == 'a':
                self.Attributes['StartChip'] = 0
            elif self.Attributes['ModuleType'] == 'b':
                self.Attributes['StartChip'] = 7
            else:
                self.Attributes['StartChip'] = 0

        elif self.Attributes['ModuleVersion'] == 2:
            self.Attributes['StartChip'] = 0
        elif self.Attributes['ModuleVersion'] == 3:
            self.Attributes['NumberOfChips'] = 1
            self.Attributes['StartChip'] = 0
        
        self.Attributes['Rates'] = {
            'HREfficiency':[],
            'HRData':[],
            'HRSCurves':[],
            'RetrimHotPixels':[]
        }

        self.FileHandle = []

        self.Attributes['InterpolatedEfficiencyRates'] = []
        for r in range(1, int(1 + self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_NInterpolationRates'])):
            self.Attributes['InterpolatedEfficiencyRates'].append(int(self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_InterpolationRate%d'%r]))

        self.Attributes['ROOTFiles'] = {}
        self.Attributes['SCurvePaths'] = {}
        self.Attributes['Ntrig'] = {}

        try:
            self.AnalyzeHRQualificationFolder()
        except Exception as inst:
            self.TestResultEnvironmentObject.ErrorList.append(
               {'ModulePath': self.TestResultEnvironmentObject.ModuleDataDirectory,
                'ErrorCode': inst,
                'FinalResultsStoragePath':'unkown'
                }
            )            
            # Start red color
            sys.stdout.write("\x1b[31m")
            sys.stdout.flush()
            print "\x1b[31mProblems in X-ray HR directory structure detected, skip qualification directory! %s"%self.TestResultEnvironmentObject.ModuleDataDirectory
            # Print traceback
            exc_type, exc_obj, exc_tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_obj, exc_tb) 
            # Reset color
            sys.stdout.write("\x1b[0m")
            sys.stdout.flush()


    def AnalyzeHRQualificationFolder(self):

        self.logfilePaths = []

        HREfficiencyPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HREfficiency_*')
        for Path in HREfficiencyPaths:
            FolderName = os.path.basename(Path)
            Rate = int(FolderName.split('_')[2])
            self.Attributes['Rates']['HREfficiency'].append(Rate)
            ROOTFiles = glob.glob(Path+'/*.root')
            self.Attributes['ROOTFiles']['HREfficiency_{Rate}'.format(Rate=Rate)] = ROOT.TFile.Open(ROOTFiles[0])
            self.FileHandle.append(self.Attributes['ROOTFiles']['HREfficiency_{Rate}'.format(Rate=Rate)])

            self.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=Rate)] = 50 #pxar default
            NTriggersReadFromFile = False
            testParametersFilename = "/".join(ROOTFiles[0].split("/")[0:-1]) + "/testParameters.dat"
            if os.path.exists(testParametersFilename):
                testParametersFile = open(testParametersFilename, "r")
                if testParametersFile:
                    testParametersSection = ""
                    for line in testParametersFile:
                        sline = line.strip()
                        if sline[0:2] == "--":
                            testParametersSection = sline[2:].strip()
                        elements = sline.strip().split(" ")
                        if testParametersSection.lower() == "highrate" and elements[0].lower() == "ntrig":
                            NTriggersReadFromFile = True
                            self.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=Rate)] = float(elements[-1])
                    testParametersFile.close()
            if not NTriggersReadFromFile:
                print '\x1b[31mWARNING: testParameters.dat file not found in "%s", using default number of triggers Ntrig = %d\x1b[0m'%(FolderName, self.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=Rate)])

            # find pxar logfile
            logfilePath = ("%s.log"%ROOTFiles[0][:-5]) if len(ROOTFiles) > 0 and len(ROOTFiles[0]) > 4 else ''
            if os.path.isfile(logfilePath):
                self.logfilePaths.append(logfilePath)
            else:
                files = [f for f in os.listdir(self.RawTestSessionDataPath) if f.endswith('.log')]
                if len(files) == 1:
                    self.logfilePaths.append(files[0])
                else:
                    print "X-ray HREfficiency: either no or multiple .log files found! error statistics are not available. Please name the .log file the same as the .root file to avoid ambiguousness if more than 1 logfiles are present in the folder."


        self.Attributes['Rates']['HREfficiency'].sort()

        HRDataPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HRData_*')
        for Path in HRDataPaths:
            FolderName = os.path.basename(Path)
            Rate = int(FolderName.split('_')[2])
            self.Attributes['Rates']['HRData'].append(Rate)
            ROOTFiles = glob.glob(Path+'/*.root')
            self.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=Rate)] = ROOT.TFile.Open(ROOTFiles[0])
            self.FileHandle.append(self.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=Rate)])

            # find pxar logfile
            logfilePath = ("%s.log"%ROOTFiles[0][:-5]) if len(ROOTFiles) > 0 and len(ROOTFiles[0]) > 4 else ''
            if os.path.isfile(logfilePath):
                self.logfilePaths.append(logfilePath)
            else:
                files = [f for f in os.listdir(self.RawTestSessionDataPath) if f.endswith('.log')]
                if len(files) == 1:
                    self.logfilePaths.append(files[0])
                else:
                    print "X-ray HRData: either no or multiple .log files found! error statistics are not available. Please name the .log file the same as the .root file to avoid ambiguousness if more than 1 logfiles are present in the folder."


        HRSCurvesPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HRS[Cc]urves_*')
        for Path in HRSCurvesPaths:
            FolderName = os.path.basename(Path)
            try:
                Rate = int(FolderName.split('_')[2])
            except:
                Rate = 0
            self.Attributes['Rates']['HRSCurves'].append(Rate)
            self.Attributes['SCurvePaths']['HRSCurves_{Rate}'.format(Rate=Rate)] = Path
            ROOTFiles = glob.glob(Path+'/*.root')
            if len(ROOTFiles) == 1:
                self.Attributes['ROOTFiles']['HRSCurves_{Rate}'.format(Rate=Rate)] = ROOT.TFile.Open(ROOTFiles[0])
                self.FileHandle.append(self.Attributes['ROOTFiles']['HRSCurves_{Rate}'.format(Rate=Rate)])

            # find pxar logfile
            logfilePath = ("%s.log"%ROOTFiles[0][:-5]) if len(ROOTFiles) > 0 and len(ROOTFiles[0]) > 4 else ''
            if os.path.isfile(logfilePath):
                self.logfilePaths.append(logfilePath)
            else:
                files = [f for f in os.listdir(self.RawTestSessionDataPath) if f.endswith('.log')]
                if len(files) == 1:
                    self.logfilePaths.append(files[0])
                else:
                    print "X-ray HRSCurves: either no or multiple .log files found! error statistics are not available. Please name the .log file the same as the .root file to avoid ambiguousness if more than 1 logfiles are present in the folder."


        HRHotPixelsPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_MaskHotPixels_*')
        if len(HRHotPixelsPaths) > 1:
                warnings.warn("multiple MaskHotPixel tests found, using first one: %s"%HRHotPixelsPaths[0])

        for Path in HRHotPixelsPaths:
            FolderName = os.path.basename(Path)
            ROOTFiles = glob.glob(Path+'/*.root')
            if len(ROOTFiles) > 1:
                warnings.warn("The directory '%s' contains more than one .root file, choosing first one: '%s'"%(FolderName, ROOTFiles[0]))
            self.Attributes['ROOTFiles']['MaskHotPixels'] = ROOT.TFile.Open(ROOTFiles[0])
            self.FileHandle.append(self.Attributes['ROOTFiles']['MaskHotPixels'])

            # find pxar logfile
            logfilePath = ("%s.log"%ROOTFiles[0][:-5]) if len(ROOTFiles) > 0 and len(ROOTFiles[0]) > 4 else ''
            if os.path.isfile(logfilePath):
                self.logfilePaths.append(logfilePath)
            else:
                files = [f for f in os.listdir(self.RawTestSessionDataPath) if f.endswith('.log')]
                if len(files) == 1:
                    self.logfilePaths.append(files[0])
                else:
                    print "X-ray MaskHotPixels: either no or multiple .log files found! error statistics are not available. Please name the .log file the same as the .root file to avoid ambiguousness if more than 1 logfiles are present in the folder."

            break

        RetrimHotPixelsPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_RetrimHotPixel*_*')
        for Path in RetrimHotPixelsPaths:
            FolderName = os.path.basename(Path)
            try:
                Rate = int(FolderName.split('_')[2])
            except:
                Rate = 0
            self.Attributes['Rates']['RetrimHotPixels'].append(Rate)
            ROOTFiles = glob.glob(Path+'/*.root')

            if len(ROOTFiles) > 1:
                warnings.warn("The directory '%s' contains more than one .root file, choosing first one: '%s'"%(FolderName, ROOTFiles[0]))
            if len(ROOTFiles) >= 1:
                self.Attributes['ROOTFiles']['RetrimHotPixels_{Rate}'.format(Rate=Rate)] = ROOT.TFile.Open(ROOTFiles[0])
                self.Attributes['RetrimHotPixelsPath'] = Path
                self.FileHandle.append(self.Attributes['ROOTFiles']['RetrimHotPixels_{Rate}'.format(Rate=Rate)])

            # find pxar logfile
            logfilePath = ("%s.log"%ROOTFiles[0][:-5]) if len(ROOTFiles) > 0 and len(ROOTFiles[0]) > 4 else ''
            if os.path.isfile(logfilePath):
                self.logfilePaths.append(logfilePath)
            else:
                files = [f for f in os.listdir(self.RawTestSessionDataPath) if f.endswith('.log')]
                if len(files) == 1:
                    self.logfilePaths.append(files[0])
                else:
                    print "X-ray RetrimHotPixels: either no or multiple .log files found! error statistics are not available. Please name the .log file the same as the .root file to avoid ambiguousness if more than 1 logfiles are present in the folder."



        PixelAlivePaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_PixelAlive_*')
        for Path in PixelAlivePaths:
            ROOTFiles = glob.glob(Path+'/*.root')
            self.Attributes['ROOTFiles']['PixelAlive'] = ROOT.TFile.Open(ROOTFiles[0])
            self.FileHandle.append(self.Attributes['ROOTFiles']['PixelAlive'])

            testParametersFilename = "/".join(ROOTFiles[0].split("/")[0:-1]) + "/testParameters.dat"
            NTriggersReadFromFile = False
            if os.path.exists(testParametersFilename):
                testParametersFile = open(testParametersFilename, "r")
                if testParametersFile:
                    testParametersSection = ""
                    for line in testParametersFile:
                        sline = line.strip()
                        if sline[0:2] == "--":
                            testParametersSection = sline[2:].strip()
                        elements = sline.strip().split(" ")
                        if testParametersSection.lower() == "pixelalive" and elements[0].lower() == "ntrig":
                            NTriggersReadFromFile = True
                            self.Attributes['Ntrig']['PixelAlive'] = float(elements[-1])
                    testParametersFile.close()
            if not NTriggersReadFromFile:
                print '\x1b[31mWARNING: testParameters.dat file not found in "%s", using default number of triggers Ntrig = 10\x1b[0m'%FolderName

            # find pxar logfile
            logfilePath = ("%s.log"%ROOTFiles[0][:-5]) if len(ROOTFiles) > 0 and len(ROOTFiles[0]) > 4 else ''
            if os.path.isfile(logfilePath):
                self.logfilePaths.append(logfilePath)
            else:
                files = [f for f in os.listdir(self.RawTestSessionDataPath) if f.endswith('.log')]
                if len(files) == 1:
                    self.logfilePaths.append(files[0])
                else:
                    print "X-ray PixelAlive: either no or multiple .log files found! error statistics are not available. Please name the .log file the same as the .root file to avoid ambiguousness if more than 1 logfiles are present in the folder."

        

        CalDelScanPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_CalDel*_*')
        for Path in CalDelScanPaths:
            ROOTFiles = glob.glob(Path+'/*.root')
            if len(ROOTFiles) > 0:
                self.Attributes['ROOTFiles']['CalDelScan'] = ROOT.TFile.Open(ROOTFiles[0])
                self.FileHandle.append(self.Attributes['ROOTFiles']['CalDelScan'])

            # find pxar logfile
            logfilePath = ("%s.log"%ROOTFiles[0][:-5]) if len(ROOTFiles) > 0 and len(ROOTFiles[0]) > 4 else ''
            if os.path.isfile(logfilePath):
                self.logfilePaths.append(logfilePath)
            else:
                files = [f for f in os.listdir(self.RawTestSessionDataPath) if f.endswith('.log')]
                if len(files) == 1:
                    self.logfilePaths.append(files[0])
                else:
                    print "X-ray CalDelScan: either no or multiple .log files found! error statistics are not available. Please name the .log file the same as the .root file to avoid ambiguousness if more than 1 logfiles are present in the folder."

        self.ResultData['SubTestResultDictList'] = []

        for Rate in self.Attributes['Rates']['HRSCurves']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'Fitting_{Rate}'.format(Rate=Rate),
                'Module': 'Fitting',
                'DisplayOptions': {
                    'Order': 99,
                    'Show': False,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            })

        self.ResultData['SubTestResultDictList'] += [
            {
                'Key': 'Chips',
                'DisplayOptions': {
                    'GroupWithNext': True,
                    'Order': 1,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            },
            {
                'Key': 'Grading',
                'DisplayOptions': {
                    'GroupWithNext': True,
                    'Order': 99,
                    'Show': False,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            },
            {
                'Key': 'Summary',
                'DisplayOptions': {
                    'GroupWithNext': False,
                    'Order': 2,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            }
        ]

        # value per ROC summary plots
        self.ResultData['SubTestResultDictList'].append({
                'Key': 'AliveOverview',
                'Module': 'AliveOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 40,
                },
                'InitialAttributes': {
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'AliveOverview'
                },
            })
        self.ResultData['SubTestResultDictList'].append({
                'Key': 'AliveSummary',
                'Module': 'AliveSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 40,
                },
                'InitialAttributes': {
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'AliveSummary'
                },
            })
        for Rate in self.Attributes['InterpolatedEfficiencyRates']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'EfficiencySummary_{Rate}'.format(Rate=Rate),
                'Module': 'EfficiencySummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 6,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'EfficiencySummary_{Rate}'.format(Rate=Rate)
                },
            })
        for Rate in self.Attributes['Rates']['HRData']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'BumpBondingSummary_{Rate}'.format(Rate=Rate),
                'Module': 'BumpBondingSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 7,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'BumpBondingSummary_{Rate}'.format(Rate=Rate)
                },
            })
        for Rate in self.Attributes['Rates']['HRSCurves']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'NoiseSummary_{Rate}'.format(Rate=Rate),
                'Module': 'NoiseSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 8,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'NoiseSummary_{Rate}'.format(Rate=Rate)
                },
            })

        # value per pixel + distribution summary plots
        for Rate in self.Attributes['Rates']['HRData']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HitOverview_{Rate}'.format(Rate=Rate),
                'Module': 'HitOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 9,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HitOverview_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HitMapDistribution_{Rate}'.format(Rate=Rate),
                'Module': 'HitMapDistribution',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 9,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HitMapDistribution_{Rate}'.format(Rate=Rate)
                },
            })

        for Rate in self.Attributes['Rates']['HRData']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HotPixelOverview_{Rate}'.format(Rate=Rate),
                'Module': 'HotPixelOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 20,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HotPixelOverview_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HotPixelSummary_{Rate}'.format(Rate=Rate),
                'Module': 'HotPixelSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 20,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HotPixelSummary_{Rate}'.format(Rate=Rate)
                },
            })

        for Rate in self.Attributes['Rates']['HRData']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'BumpBondingProblems_{Rate}'.format(Rate=Rate),
                'Module': 'BumpBondingProblems',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 10,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'BumpBondingProblems_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'BumpBondingSummary_{Rate}'.format(Rate=Rate),
                'Module': 'BumpBondingSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 10,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'BumpBondingSummary_{Rate}'.format(Rate=Rate)
                },
            })

        for Rate in self.Attributes['Rates']['HRSCurves']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'ThresholdOverview_{Rate}'.format(Rate=Rate),
                'Module': 'ThresholdOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 30,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'ThresholdOverview_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'ThresholdDistribution_{Rate}'.format(Rate=Rate),
                'Module': 'ThresholdDistribution',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 30,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'ThresholdDistribution_{Rate}'.format(Rate=Rate)
                },
            })

        for Rate in self.Attributes['Rates']['HRSCurves']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'NoiseOverview_{Rate}'.format(Rate=Rate),
                'Module': 'NoiseOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 31,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'NoiseOverview_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'NoiseDistribution_{Rate}'.format(Rate=Rate),
                'Module': 'NoiseDistribution',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 31,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'NoiseDistribution_{Rate}'.format(Rate=Rate)
                },
            })

        for Rate in self.Attributes['Rates']['HREfficiency']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'EfficiencyOverview_{Rate}'.format(Rate=Rate),
                'Module': 'EfficiencyOverview',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 50,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'EfficiencyOverview_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'EfficiencyDistribution_{Rate}'.format(Rate=Rate),
                'Module': 'EfficiencyDistribution',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 50,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'EfficiencyDistribution_{Rate}'.format(Rate=Rate)
                },
            })

        self.ResultData['SubTestResultDictList'].append({
                'Key': 'SummaryROCs',
                'DisplayOptions': {
                    'GroupWithNext': False,
                    'Order': 3,
                    'Width': 4,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            })

        self.ResultData['SubTestResultDictList'].append({
                'Key': 'Logfile',
                'DisplayOptions': {
                    'GroupWithNext': False,
                    'Order': 905,
                    'Width': 1,
                },
            })
        self.ResultData['SubTestResultDictList'].append({
                'Key': 'ConfigFiles',
                'DisplayOptions': {
                    'GroupWithNext': False,
                    'Show': False,
                },
            })
        self.ResultData['SubTestResultDictList'].append({
                'Key': 'Errors',
                'DisplayOptions': {
                    'GroupWithNext': False,
                    'Order': 904,
                    'Width': 1,
                },
            })
        self.ResultData['SubTestResultDictList'].append({
                'Key': 'TestEnvironment',
                'DisplayOptions': {
                    'GroupWithNext': False,
                    'Order': 901,
                    'Width': 1,
                },
            })

        for Rate in self.Attributes['Rates']['RetrimHotPixels']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HotPixelRetrimming_{Rate}'.format(Rate=Rate),
                'Module': 'HotPixelRetrimming',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 60,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HotPixelRetrimming_{Rate}'.format(Rate=Rate)
                },
            })
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'HotPixelRetrimSummary_{Rate}'.format(Rate=Rate),
                'Module': 'HotPixelRetrimSummary',
                'DisplayOptions': {
                    'Width': 1,
                    'Order': 60,
                },
                'InitialAttributes': {
                    'Rate': Rate,
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StorageKey': 'HotPixelRetrimSummary_{Rate}'.format(Rate=Rate)
                },
            })
       

    def OpenFileHandle(self):
        pass

    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()
        pass

    def PrintDatabaseRow(self, Row):
        print '-'*100
        print ' ROW'
        print '-'*100
        for i in Row:
            print ("%s: "%i).ljust(32),Row[i]
        print '-'*100

    def CustomWriteToDatabase(self, ParentID):
        try:
            import PixelDB
        except:
            pass

        selfVerboseBefore = self.verbose
        self.verbose=True
        if self.verbose:
            print 'Write to DB: ',ParentID

        try:
            grade = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ModuleGrade']['Value']
        except KeyError:
            raise

        try:
            PixelDefects = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefects']['Value']
        except KeyError:
            PixelDefects = 'None'

        try:
            ROCsLessThanOnePercent = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCsLessThanOnePercent']['Value']
        except KeyError:
            ROCsLessThanOnePercent = 'None'

        try:
            ROCsMoreThanOnePercent = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCsMoreThanOnePercent']['Value']
        except KeyError:
            ROCsMoreThanOnePercent = 'None'

        try:
            ROCsMoreThanFourPercent = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCsMoreThanFourPercent']['Value']
        except KeyError:
            ROCsMoreThanFourPercent = 'None'

        try:
            NoisyPixels = float(self.ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['NoisyPixels']['Value'])
        except KeyError:
            NoisyPixels = 'None'

        print 'fill row'
        print" ATTRIBUTES", self.Attributes
#        print" PATTRIBUTES", self.ParentObj.Attributes
        
        Comment=''

        Row = {
            'ModuleID': self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'QualificationType': self.ParentObject.Attributes['QualificationType'],
            'Grade': grade,
            'PixelDefects': PixelDefects,
            'ROCsLessThanOnePercent': ROCsLessThanOnePercent,
            'ROCsMoreThanOnePercent': ROCsMoreThanOnePercent,
            'ROCsMoreThanFourPercent': ROCsMoreThanFourPercent,
            'Noise': NoisyPixels,
            'RelativeModuleFinalResultsPath': os.path.relpath(self.TestResultEnvironmentObject.FinalModuleResultsPath,
                                                              self.TestResultEnvironmentObject.GlobalOverviewPath),
            'FulltestSubfolder': os.path.relpath(self.FinalResultsStoragePath,
                                                 self.TestResultEnvironmentObject.FinalModuleResultsPath),
            # needed for PixelDB
            'AbsModuleFulltestStoragePath': self.TestResultEnvironmentObject.FinalModuleResultsPath,
            'AbsFulltestSubfolder': self.FinalResultsStoragePath,
            'InputTarFile': os.environ.get('TARFILE', None),
            'MacroVersion': os.environ.get('MACROVERSION', None),
            
            'TestCenter': self.Attributes['TestCenter'],
            'Hostname': self.Attributes['Hostname'],
            'Operator': self.Attributes['Operator'],
        }

        #adding comment (if any) from manual grading
        if 'Grading' in self.ResultData['SubTestResults'] and self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs'].has_key('GradeComment'):
            Comment += self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['GradeComment']['Value']
        
        # fill final comments
        Comment = Comment.strip().strip('/')
        Row.update({
            'Comments': Comment,
            })

        print 'fill row end'

        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            DebugGlobalDB = True
            GlobalDBRowTemplate = copy.deepcopy(Row)
            del(GlobalDBRowTemplate['Grade'])
            del(GlobalDBRowTemplate['Noise'])
            del(GlobalDBRowTemplate['PixelDefects'])
            del(GlobalDBRowTemplate['ROCsLessThanOnePercent'])
            del(GlobalDBRowTemplate['ROCsMoreThanOnePercent'])
            del(GlobalDBRowTemplate['ROCsMoreThanFourPercent'])

            GradingTestResultObject = self.ResultData['SubTestResults']['Grading']

            # first fill all fields which do not correspond to a specific rate, e.g. ratios of two rates, final grade etc.
            if True:
                HighRateDataModule = copy.deepcopy(Row)

                #GRADE
                del(HighRateDataModule ['Grade'])
                HighRateDataModule ['HRGrade'] = grade

                # N_ROCS_READOUT_PROBLEM <- new
                HighRateDataModule ['ROCsWithReadoutProblems'] = GradingTestResultObject.ResultData['KeyValueDictPairs']['ROCsWithReadoutProblems']['Value']

                # N_COL_NONUNIFORM
                HighRateDataModule ['ROCsWithUniformityProblems'] = GradingTestResultObject.ResultData['KeyValueDictPairs']['ROCsWithUniformityProblems']['Value']

                # ADDR_PIXELS_BAD
                HighRateDataModule ['AddrPixelsBad'] = GradingTestResultObject.ResultData['HiddenData']['TotalDefectPixelsList']['Value']

                # ADDR_PIXELS_HOT
                HighRateDataModule ['AddrPixelsHot'] = GradingTestResultObject.ResultData['HiddenData']['HotPixelsList']['Value']

                # N_HOT_PIXEL
                HighRateDataModule ['NHotPixel'] = len(GradingTestResultObject.ResultData['HiddenData']['HotPixelsList']['Value'])

                # N_BAD_DOUBLECOLUMNS
                HighRateDataModule ['NBadDoubleColumns'] = GradingTestResultObject.ResultData['KeyValueDictPairs']['NBadDoubleColumns']['Value']

                #
                # tommaso
                #
                
                # Temperature
                HighRateDataModule ['TestTemp'] = self.Attributes['TestTemperature']
                HighRateDataModule ['ModuleID'] = self.Attributes['ModuleID']
                
                


                #-------------------------------------------------
                # <--- here comes the code for pixel db upload
                #-------------------------------------------------
                if DebugGlobalDB:
                    self.PrintDatabaseRow(HighRateDataModule)

                ROCNumbers = []
                TotalPixelDefectsLists = []
                HotPixelsLists = []
                RocGrades = []
                NColNonUniform = []
                NBadDoubleColumnsList = []
                ChipsSubTestResult = self.ResultData['SubTestResults']['Chips']
                for i in ChipsSubTestResult.ResultData['SubTestResultDictList']:
                    ChipNo = i['TestResultObject'].Attributes['ChipNo']
                    try:
                        NColNonUniformROC = int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['NumberOfNonUniformColumns']['Value'])
                    except:
                        NColNonUniformROC = -1

                    ROCNumbers.append(ChipNo)
                    TotalPixelDefectsLists.append(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['TotalPixelDefectsList']['Value'])
                    HotPixelsLists.append(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['HotPixelDefectsList']['Value'])
                    RocGrades.append(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCGrade']['Value'])
                    NColNonUniform.append(NColNonUniformROC)
                    NBadDoubleColumnsList.append(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['BadDoubleColumns']['Value'])
          
                # ROC rows
                HighRateDataRoc = {}
                for i in range(0, len(ROCNumbers)):
                    # remove grade from individual rows
                    HighRateDataRoc[i] = copy.deepcopy(GlobalDBRowTemplate)

                    #ROC_POS
                    HighRateDataRoc[i]['RocPos'] = ROCNumbers[i]

                    # ADDR_PIXELS_BAD
                    HighRateDataRoc[i]['AddrPixelsBad'] = TotalPixelDefectsLists[i]

                    # ADDR_PIXELS_HOT
                    HighRateDataRoc[i]['AddrPixelsHot'] = HotPixelsLists[i]

                    # N_HOT_PIXEL
                    HighRateDataRoc[i]['NHotPixel'] = len(HotPixelsLists[i])

                    # N_BAD_DOUBLECOLUMNS
                    HighRateDataRoc[i]['NBadDoubleColumns'] = NBadDoubleColumnsList[i]

                    # GRADE
                    HighRateDataRoc[i]['Grade'] = RocGrades[i]

                    # N_COL_NONUNIFORM
                    HighRateDataRoc[i]['NColNonUniform'] = NColNonUniform[i]

                    #-------------------------------------------------
                    # <--- here comes the code for pixel db upload
                    #-------------------------------------------------
                    if DebugGlobalDB:
                        self.PrintDatabaseRow(HighRateDataRoc[i])
#                        self.testHRCommon(HighRateData, HighRateDataRoc[i])

            # all hitmap rates  ("50", "150")
            HighRateDataAggr = {}
            HighRateDataAggrRoc={}
            print "nonnapapera"
            for Rate in self.Attributes['Rates']['HRData']:
                print 'in the loop', Rate
                # prepare data
                MeasuredHitrates = []
                NonUniformEventBins = []
                BumpBondingDefects = []
                ROCNumbers = []
                ChipsSubTestResult = self.ResultData['SubTestResults']['Chips']
                for i in ChipsSubTestResult.ResultData['SubTestResultDictList']:
                    ChipNo = i['TestResultObject'].Attributes['ChipNo']
                    ROCNumbers.append(ChipNo)
                    MeasuredHitrates.append(float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['RealHitrate']['Value']))
                    NonUniformEventBins.append(int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NumberOfNonUniformEvents_{Rate}'.format(Rate=Rate)]['Value']))
                    BumpBondingDefects.append(int(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['BumpBondingDefects_{Rate}'.format(Rate=Rate)]['Value']))
          
                print "GERdddddd"

                # apply aggregation function
                ModuleMeanHitrate = sum(MeasuredHitrates) / float(len(MeasuredHitrates)) if len(MeasuredHitrates) > 0 else -1
                print "GERdddddddsdsds"
                ModuleNonUniformEventBins = sum(NonUniformEventBins) if len(NonUniformEventBins) > 0 else -1
                ModuleBumpBondingDefects = sum(BumpBondingDefects) if len(BumpBondingDefects) > 0 else -1
                print "GERdddddd0000000000"
                # remove grade from individual rows
                HighRateDataAggr[Rate] = copy.deepcopy(GlobalDBRowTemplate)

                #HITRATENOMINAL
                print "RATE< ETC", Rate
                HighRateDataAggr[Rate]['HitrateNominal'] = Rate
                print"ffffff", ModuleMeanHitrate
                # MEASURED_HITRATE
                HighRateDataAggr[Rate]['MeasuredHitrate'] = ModuleMeanHitrate
                print "GERdddddd1111111111111"
                # N_BINS_LOWHIGH
                HighRateDataAggr[Rate]['NBinsLowHigh'] = ModuleNonUniformEventBins
                print "GERdddddd22222222222222222"
                # N_PIXEL_NO_HIT
                HighRateDataAggr[Rate]['NPixelNoHit'] = ModuleBumpBondingDefects
                print "GERdddddd3333333333333333"
                #-------------------------------------------------
                # <--- here comes the code for pixel db upload
                #-------------------------------------------------
                if DebugGlobalDB:
#                    self.PrintDatabaseRow(HighRateDataAggr[Rate])
                    pass
                print "OOROROORORROROROROO"

                HighRateDataAggrRoc[Rate] = {}

                # ROC rows
                for i in range(0, len(ROCNumbers)):
                    HighRateDataAggrRoc[Rate][i] = {}
                    # remove grade from individual rows
                    print "HEHEHEHEHEHEHEH",i
                    HighRateDataAggrRoc[Rate][i] = copy.deepcopy(GlobalDBRowTemplate)
                    print"PPPPPPP"
                    #HITRATENOMINAL
                    HighRateDataAggrRoc[Rate][i]['HitrateNominal'] = Rate

                    #ROC_POS
                    HighRateDataAggrRoc[Rate][i]['RocPos'] = ROCNumbers[i]

                    # MEASURED_HITRATE
                    HighRateDataAggrRoc[Rate][i]['MeasuredHitrate'] = MeasuredHitrates[i]

                    # N_BINS_LOWHIGH
                    HighRateDataAggrRoc[Rate][i]['NBinsLowHigh'] = NonUniformEventBins[i]

                    # N_PIXEL_NO_HIT
                    HighRateDataAggrRoc[Rate][i]['NPixelNoHit'] = BumpBondingDefects[i]

                    #-------------------------------------------------
                    # <--- here comes the code for pixel db upload
                    #-------------------------------------------------
#                    if DebugGlobalDB:
#                        self.PrintDatabaseRow(HighRateDataAggrRoc[Rate][i])

            # all noise rates
            HighRateDataAllNoise = {}
            HighRateDataAllNoiseRoc = {}
            print "PaperinoIPPO"
            for Rate in self.Attributes['Rates']['HRSCurves']:

                # prepare data
                MeasuredHitrates = []
                NoiseMeans = []
                NoiseWidths = []
                ROCNumbers = []
                NoisePixelsLists = []

                ChipsSubTestResult = self.ResultData['SubTestResults']['Chips']
                for i in ChipsSubTestResult.ResultData['SubTestResultDictList']:
                    ChipNo = i['TestResultObject'].Attributes['ChipNo']
                    ROCNumbers.append(ChipNo)
                    try:
                        MeasuredHitrate = float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['MeasuredHitrate']['Value'])
                    except:
                        MeasuredHitrate = -1

                    NoiseMeans.append(float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['mu']['Value']))
                    NoiseWidths.append(float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['KeyValueDictPairs']['sigma']['Value']))
                    MeasuredHitrates.append(MeasuredHitrate)
                    NoisePixelsLists.append(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['HiddenData']['ListOfNoisyPixels']['Value'])

                # apply aggregation function
                ModuleMeanHitrate = sum(MeasuredHitrates) / float(len(MeasuredHitrates)) if len(MeasuredHitrates) > 0 else -1
                ModuleNoiseMean = sum(NoiseMeans) / float(len(NoiseMeans)) if len(NoiseMeans) > 0 else -1
                ModuleNoiseWidth = sum(NoiseWidths) / float(len(NoiseWidths)) if len(NoiseWidths) > 0 else -1

                # remove grade from individual rows
                HighRateDataAllNoise[Rate] = copy.deepcopy(GlobalDBRowTemplate)

                #HITRATENOMINAL
                HighRateDataAllNoise[Rate]['HitrateNominal'] = Rate

                # MEASURED_HITRATE
                HighRateDataAllNoise[Rate]['MeasuredHitrate'] = ModuleMeanHitrate

                # MEAN_NOISE_ALLPIXELS
                HighRateDataAllNoise[Rate]['MeanNoiseAllPixels'] = ModuleNoiseMean

                # WIDTH_NOISE_ALLPIXELS
                HighRateDataAllNoise[Rate]['WidthNoiseAllPixels'] = ModuleNoiseWidth

                # ADDR_PIXELS_NOISE
                HighRateDataAllNoise[Rate]['AddrPixelsNoise'] = self.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NoiseDefectPixelsList']

                # N_PIXELS_NOISE  (or N_PIXELS_NOISE_ABOVETH)
                HighRateDataAllNoise[Rate]['NPixelsNoise'] = self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['NoiseDefects']

                #-------------------------------------------------
                # <--- here comes the code for pixel db upload
                #-------------------------------------------------
                if DebugGlobalDB:
                    self.PrintDatabaseRow(HighRateDataAllNoise[Rate])


                # ROC rows
                print "PIPPO",Rate
                HighRateDataAllNoiseRoc[Rate] = {}
                for i in range(0, len(ROCNumbers)):
                    # remove grade from individual rows
                    HighRateDataAllNoiseRoc[Rate][i] = copy.deepcopy(GlobalDBRowTemplate)

                    #HITRATENOMINAL
                    HighRateDataAllNoiseRoc[Rate][i]['HitrateNominal'] = Rate

                    #ROC_POS
                    HighRateDataAllNoiseRoc[Rate][i]['RocPos'] = ROCNumbers[i]

                    # MEASURED_HITRATE
                    HighRateDataAllNoiseRoc[Rate][i]['MeasuredHitrate'] = MeasuredHitrates[i]

                    # MEAN_NOISE_ALLPIXELS
                    HighRateDataAllNoiseRoc[Rate][i]['MeanNoiseAllPixels'] = NoiseMeans[i]

                    # WIDTH_NOISE_ALLPIXELS
                    HighRateDataAllNoiseRoc[Rate][i]['WidthNoiseAllPixels'] = NoiseWidths[i]

                    # ADDR_PIXELS_NOISE
                    HighRateDataAllNoiseRoc[Rate][i]['AddrPixelsNoise'] = NoisePixelsLists[i]

                    # N_PIXELS_NOISE  (or N_PIXELS_NOISE_ABOVETH)
                    HighRateDataAllNoiseRoc[Rate][i]['NPixelsNoise'] = len(NoisePixelsLists[i])

                    #-------------------------------------------------
                    # <--- here comes the code for pixel db upload
                    #-------------------------------------------------
#                    if DebugGlobalDB:
#                        self.PrintDatabaseRow(HighRateDataAllNoiseRoc[Rate][i])

            print "PLUTO"
            # all efficiency interpolation rates
            HighRateDataInterp = {}
            HighRateDataInterpRoc = {}
            for Rate in self.Attributes['InterpolatedEfficiencyRates']:

                # prepare data
                MeasuredEfficiencies = []
                ROCNumbers = []

                ChipsSubTestResult = self.ResultData['SubTestResults']['Chips']
                for i in ChipsSubTestResult.ResultData['SubTestResultDictList']:
                    ChipNo = i['TestResultObject'].Attributes['ChipNo']
                    ROCNumbers.append(ChipNo)
                    MeasuredEfficiencies.append(float(ChipsSubTestResult.ResultData['SubTestResults']['Chip%d'%ChipNo].ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['KeyValueDictPairs']['InterpolatedEfficiency{Rate}'.format(Rate=Rate)]['Value']))
          
                # apply aggregation function
                ModuleMeanEfficiency= sum(MeasuredEfficiencies) / float(len(MeasuredEfficiencies)) if len(MeasuredEfficiencies) > 0 else -1

                # remove grade from individual rows
                HighRateDataInterp[Rate] = copy.deepcopy(GlobalDBRowTemplate)

                # HITRATENOMINAL
                HighRateDataInterp[Rate]['HitrateNominal'] = Rate

                # INTERP_EFF_TESTPOINT
                HighRateDataInterp[Rate]['InterpEffTestpoint'] = ModuleMeanEfficiency

                #-------------------------------------------------
                # <--- here comes the code for pixel db upload
                #-------------------------------------------------
                if DebugGlobalDB:
                    self.PrintDatabaseRow(HighRateDataInterp[Rate])

                # ROC rows
                HighRateDataInterpRoc[Rate] = {}
                for i in range(0, len(ROCNumbers)):
                    # remove grade from individual rows
                    HighRateDataInterpRoc[Rate][i] = copy.deepcopy(GlobalDBRowTemplate)

                    #HITRATENOMINAL
                    HighRateDataInterpRoc[Rate][i]['HitrateNominal'] = Rate

                    #ROC_POS
                    HighRateDataInterpRoc[Rate][i]['RocPos'] = ROCNumbers[i]

                    # INTERP_EFF_TESTPOINT
                    HighRateDataInterpRoc[Rate][i]['InterpEffTestpoint'] = MeasuredEfficiencies[i]

                    #-------------------------------------------------
                    # <--- here comes the code for pixel db upload
                    #-------------------------------------------------
#                    if DebugGlobalDB:
#                        self.PrintDatabaseRow(HighRateDataInterpRoc[Rate][i])


#
# Tommaso
#
            print "TOMMASO ALL DATA"
            print "HighRateDataModule",HighRateDataModule
            print "HighRateDataAggr",HighRateDataAggr
            print "HighRateDataAllNoise",HighRateDataAllNoise
            print "HighRateDataInterp",HighRateDataInterp
            print "HighRateDataRoc",HighRateDataRoc
            print "HighRateDataAggrRoc",HighRateDataAggrRoc
            print "HighRateDataAllNoiseRoc",HighRateDataAllNoiseRoc
            print "HighRateDataInterpRoc",HighRateDataInterpRoc
            from PixelDB import *
            # modified by Tommaso
            #
            # try and speak directly with PixelDB
            #

#            fake = int(os.environ.get('FAKE',1))

#            insertedID=7
            pdb = PixelDBInterface(operator="tommaso", center="pisa")
            pdb.connectToDB()

#            if (0 == 0):
            OPERATOR = os.environ['PIXEL_OPERATOR']
            CENTER = os.environ['PIXEL_CENTER']
            s = Session(CENTER, OPERATOR)
            pdb.insertSession(s)
            print "--------------------"
            print "INSERTING INTO DB", self.TestResultEnvironmentObject.FinalModuleResultsPath, s.SESSION_ID
            print "--------------------"
#            pp = pdb.insertTestFullModuleDirPlusMapv96Plus(s.SESSION_ID, Row)

            pdb.insertHR(s.SESSION_ID, HighRateDataModule,  HighRateDataAggr, HighRateDataAllNoise, HighRateDataInterp
                                             ,HighRateDataRoc
                                             ,HighRateDataAggrRoc
                                             ,HighRateDataAllNoiseRoc
                                             ,HighRateDataInterpRoc)
            self.verbose = selfVerboseBefore

        else:
            with self.TestResultEnvironmentObject.LocalDBConnection:
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                    'DELETE FROM ModuleTestResults WHERE ModuleID = :ModuleID AND TestType=:TestType AND QualificationType=:QualificationType AND TestDate <= :TestDate',
                    Row)
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                    '''INSERT INTO ModuleTestResults
                    (
                        ModuleID,
                        TestDate,
                        TestType,
                        QualificationType,
                        Grade,
                        PixelDefects,
                        ROCsLessThanOnePercent,
                        ROCsMoreThanOnePercent,
                        ROCsMoreThanFourPercent,
                        Noise,
                        RelativeModuleFinalResultsPath,
                        FulltestSubfolder,
                        Comments
                        
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :QualificationType,
                        :Grade,
                        :PixelDefects,
                        :ROCsLessThanOnePercent,
                        :ROCsMoreThanOnePercent,
                        :ROCsMoreThanFourPercent,
                        :Noise,
                        :RelativeModuleFinalResultsPath,
                        :FulltestSubfolder,
                        :Comments
                    )
                    ''', Row)
                self.verbose = selfVerboseBefore
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid


