# -*- coding: utf-8 -*-
import gzip
import sys
import datetime
import json
import traceback
import warnings
import os
import ConfigParser
import fnmatch

from Helper.SetEncoder import SetEncoder
from Helper.BetterConfigParser import BetterConfigParser
import subprocess
import traceback
import ROOT

try:
    set
except NameError:
    # noinspection PyShadowingBuiltins,PyDeprecation
    from sets import Set as set
import Helper.ROOTConfiguration as ROOTConfiguration
import glob

class GeneralTestResult(object):
    nRows = 80
    nCols = 52
    nTotalChips = 16

    MoReWebVersion = 'unknown MoReWeb version'

    '''
        Initialization function
        @param ParentObject Reference to the Parent Object
        @param InitialModulePath Starting point of modules
    '''
    
    def __init__(self, TestResultEnvironmentObject, ParentObject=None, InitialModulePath=None,
                 InitialFinalResultsStoragePath=None, InitialAttributes=None, Key=None, DisplayOptions=None):
        ROOTConfiguration.initialise_ROOT()
        self.verbose = False

        # Name of the Test Result, only a-zA-Z0-9_
        self.Name = ''

        # Name of the test result without prefixes
        self.NameSingle = ''
        self.Key = ''

        # Title displayed in HTML, etc
        self.Title = ''
        # options which might be transfered to Attributes?
        self.testSoftware = None
        self.HistoDict = None
        self.version = None
        self.isPROC = False
        self.nRocs = 0
        self.halfModule = 0
        self.CommentFromFile = None
        self.AddCommentsToKeyValueDictPairs = False
        self.CreateJSONIndex = False

        if Key:
            self.Key = Key

        # Attributes like Date, etc.
        self.Attributes = {
            # Date as UNIX timestamp, if 0, the date of the parent object is taken
            'TestDate': 0,
            # Type of the tested object
            'TestedObjectType': '',
            # ID of the tested object
            'TestedObjectID': '',
            # Key for custom storage path
            'StorageKey': '',
            # subDirectory of the test result root-files
            'TestResultSubDirectory': '',
        }

        self.Show = True
        self.Enabled = True
        self.SavePlotFile = True
        self.GzipSVG = TestResultEnvironmentObject.Configuration['GzipSVG']
        
        self.DefaultImageFormat = TestResultEnvironmentObject.Configuration['DefaultImageFormat'].strip().lower()
        if TestResultEnvironmentObject.Configuration.has_key('AdditionalImageFormats'):
            self.AdditionalImageFormats = TestResultEnvironmentObject.Configuration['AdditionalImageFormats'].strip().lower().split(',')
        else:
            self.AdditionalImageFormats = ['root', 'pdf']

        if TestResultEnvironmentObject.Configuration.has_key('OverviewHTMLLink'):
            self.OverviewHTMLLink = TestResultEnvironmentObject.Configuration['OverviewHTMLLink']
        else:
            self.OverviewHTMLLink = None
            
        # Path for current test to folder with root-files
        self.RawTestSessionDataPath = ''

        # Path for current test result files (html, svg, etc)
        self.FinalResultsStoragePath = ''

        # File handle (might be used by sub results)
        self.FileHandle = 0

        # Reference to ROOT canvas
        self.Canvas = None

        # Display Properties as in the ResultData.SubTestResultDictList
        self.DisplayOptions = {
            'Order': 0,
            'Width': 1,
            'GroupWithNext': False,
            'Floating': False,
        }

        # Result array
        self.ResultData = {
            # Key / ValueDict (dict with {Value, Unit, Label}, if Label not specified, the key is used as label) Pairs
            # 'KeyValueDictPairs':{
            # 'MyKey':{
            # 'Value':'25',
            # 'NumericValue':25,
            # 'Unit': 'kg',
            # 'Label': 'My Key'
            # }
            # }
            'KeyValueDictPairs': {},

            # List of keys for sorting
            'KeyList': [],
            # Plot data
            'Plot': {
                'Enabled': 0,
                'ROOTObject': None,
                'Caption': '',
                'ImageFile': '',
                'Format': self.DefaultImageFormat,
                'AdditionalFormats':self.AdditionalImageFormats,
                'ImageFilePDF':'',
            },
            # SubTest Results
            'SubTestResults': {},
            # List of {Key, Module} dict for sorting and special attributes
            'SubTestResultDictList': [],
            # 'SubTestResultDictList':{
            # {
            # 'Key':'Noise'
            # 'Module':'Noise',
            # 'TestResultObject':object,
            # 'InitialAttributes':{'StorageKey':'Blub'},
            # 'DisplayOptions':{'Order':1, 'Width':1,'GroupWithNext':False},
            # }
            # }

            # hidden data, might be needed by other test results but is not displayed
            'HiddenData': {},

            # a data table if needed
            'Table': {
                'HEADER': [],
                'BODY': [],
                'FOOTER': [],
            }

        }
        # Reference to parent object
        self.ParentObject = None
        # Reference to the Test Result Environment
        self.TestResultEnvironmentObject = None
        self.TestResultEnvironmentObject = TestResultEnvironmentObject
        self.Canvas = self.TestResultEnvironmentObject.Canvas
        self.RawTestSessionDataPath = self.TestResultEnvironmentObject.ModuleDataDirectory

        if ParentObject:
            self.ParentObject = ParentObject
            self.RawTestSessionDataPath = self.ParentObject.RawTestSessionDataPath
            self.isPROC = ParentObject.isPROC

        if InitialAttributes:
            self.Attributes.update(InitialAttributes)

        if DisplayOptions:
            self.DisplayOptions.update(DisplayOptions)

        if self.Attributes['TestResultSubDirectory']:
            self.RawTestSessionDataPath += '/' + self.Attributes['TestResultSubDirectory']

        self.Attributes['SpecialPopulateDataParameters'] = {
            'DataKey': None,  # which sub test result to take the data from
            'DefectsKey': None,
            'DataParameterKey': '',  # which part of key value dict pairs
            'YLimitB': None,  # limit for grading
            'YLimitC': None,  # limit for grading
        }

        self.ROOTObjects = []
        self.CustomInit()

        if not self.Title:
            self.Title = self.NameSingle

        # Module Path
        self.ModulePath = self.NameSingle
        
        if InitialModulePath:
            self.ModulePath = InitialModulePath

        if InitialFinalResultsStoragePath:
            self.FinalResultsStoragePath = InitialFinalResultsStoragePath

        self.RelativeFinalResultsStoragePath = ''

        if self.ParentObject:
            self.FinalResultsStoragePath = self.ParentObject.FinalResultsStoragePath
            self.RelativeFinalResultsStoragePath = self.ParentObject.RelativeFinalResultsStoragePath
            self.ModulePath = self.ParentObject.ModulePath + '.' + self.ModulePath

        if self.Attributes['StorageKey']:
            self.FinalResultsStoragePath += '/' + self.Attributes['StorageKey']
            self.RelativeFinalResultsStoragePath += '/' + self.Attributes['StorageKey']
        else:
            self.FinalResultsStoragePath += '/' + self.NameSingle
            self.RelativeFinalResultsStoragePath += '/' + self.NameSingle
        self.SetFinalResultsStoragePath()

        if not os.path.exists(self.FinalResultsStoragePath):
            os.makedirs(self.FinalResultsStoragePath)

        # Load all sub test results in correct order
        i2 = len(self.ResultData['SubTestResultDictList'])
        for i in self.ResultData['SubTestResultDictList']:
            if i.has_key('Module'):
                SubModule = i['Module']
            else:
                SubModule = i['Key']
                i['Module'] = SubModule

            if i.has_key('InitialAttributes'):
                pass
            else:
                i['InitialAttributes'] = {}

            # set the test date for all test results
            i['InitialAttributes'].update({
                'TestDate': self.Attributes['TestDate']
            })

            # Ensure all keys of display properties are set
            DisplayOptions = {
                'Order': i2,
                'Width': 1,
                'Show': True,
                'GroupWithNext': False,
            }

            if i.has_key('DisplayOptions'):
                DisplayOptions.update(i['DisplayOptions'])

            i['DisplayOptions'] = DisplayOptions

            if SubModule.startswith('TestResultClasses'):
                importdir = SubModule
                SubModule = SubModule.split('.')[-1]
            else:
                importdir = self.ModulePath + '.' + SubModule

            # self.ModulePath contains the path under which the module will be saved in hierarchy
            # self.ImportPath contains the path from which the module is copied

            self.ImportPath = None
            try:
                f = __import__(importdir + '.' + SubModule, fromlist=[importdir + '.' + 'TestResult'])
                self.ImportPath = importdir
            except ImportError as inst:
                try:
                    ParentObjectPath = self.ParentObject.ImportPath
                    ModulePath = ParentObjectPath + '.' + SubModule  + '.' + SubModule
                    FromList = ParentObjectPath + '.' + SubModule + '.TestResult'
                    f = __import__(ModulePath, fromlist=[FromList])
                    self.ImportPath = ParentObjectPath + '.' + SubModule
                except:
                    try:
                        f = __import__(importdir + '.TestResult', fromlist=[''])
                    except:
                        print "\x1b[31mImport failed:"
                        print " importdir: ", importdir + '.TestResult'
                        print " fromlist: []"
                        print "\x1b[0m"
                        raise

                    print 'imported', f, 'please change name of file'
            pass

            self.ResultData['SubTestResults'][i['Key']] = f.TestResult(
                self.TestResultEnvironmentObject,
                self,
                None,
                None,
                i['InitialAttributes'],
                i['Key'],
                i['DisplayOptions']
            )

            i['TestResultObject'] = self.ResultData['SubTestResults'][i['Key']]
            i2 += 1

    def check_Test_Software_Pyxar(self):
        self.RawTestSessionDataPath = os.path.abspath(self.RawTestSessionDataPath)
        files = glob.glob(self.RawTestSessionDataPath + '/test.cfg') + \
                glob.glob(self.RawTestSessionDataPath + '/*/test.cfg')
        return len(files) > 0

    def check_Test_Software_Pxar(self):
        data = glob.glob(self.RawTestSessionDataPath + '/*[p,P][x,X][a,A][r,R]*.*') + \
                   glob.glob(self.RawTestSessionDataPath + '/*/*[p,P][x,X][a,A][r,R]*.*')
        if len(data):
            return True

        LogFileNames = glob.glob(self.RawTestSessionDataPath + '/*.log') + glob.glob(self.RawTestSessionDataPath + '/*/*.log')

        for LogFileName in LogFileNames:
            LogFile = open(LogFileName, "r")
            FirstLine = LogFile.readline()
            LogFile.close()
            if FirstLine.lower().find("welcome to pxar") > -1:
                return True

        return False

    def check_Test_Software(self):

        if self.check_Test_Software_Pyxar():
            self.testSoftware = 'pyxar'
        elif self.check_Test_Software_Pxar():
            self.testSoftware = 'pxar'
        else:
            self.testSoftware = 'psi46expert'

        self.HistoDict = BetterConfigParser()
        fileName = 'Configuration/Software/%s.cfg' % self.testSoftware
        self.HistoDict.read(fileName)
        fileName = 'Configuration/Software/global.cfg'
        self.HistoDict.read(fileName)

    def check_for_comments(self):
        dir_name = os.path.abspath(self.RawTestSessionDataPath)
        comment_files = glob.glob(dir_name + '/comment*')
        comment = ''
        comment_short = ''
        for filename in comment_files:
            comment += '{filename}:\n'.format(filename=filename.split('/')[-1])
            with file(filename) as f:
                s = f.read()
            comment += s + '\n\n'
            comment_short += s + ' '
        # if self.ResultData:
        # if not 'KeyVaueDictPairs' in self.ResultData:
        # self.ResultData['KeyValueDictPairs'] = {}
        #
        # if not 'KeyValueList' in self.ResultData:
        # self.ResultData['KeyValueList'] = []
        if comment != '':
            if self.verbose:
                print 'added comment', comment, 'to ', self.Name

            if self.AddCommentsToKeyValueDictPairs:
                self.ResultData['KeyValueDictPairs']['Comment'] = {
                    'Value': comment,
                    'Style': 'font-weight:bold;color:red;' if '!' in comment else 'font-weight:bold;',
                }
                self.ResultData['KeyList'].append('Comment')
            self.CommentFromFile = comment_short

    def check_for_manualGrade(self):
        self.RawTestSessionDataPath = os.path.abspath(self.RawTestSessionDataPath)
        gradefilename = self.RawTestSessionDataPath + '/grade.txt'
        print "checking for manual grading in '%s'"%gradefilename
        grade = ''
        if os.path.isfile(gradefilename):
            try:
                gradefile = open(gradefilename)
                grade = gradefile.read().strip()
                gradefile.close()
                # grade can be given either as number 1,2,3 or as letter A,B,C
                GradeNames = ['A','B','C']
                if grade in GradeNames:
                    grade = 1 + GradeNames.index(grade)
                print "Reading a manual grade "+str(grade)+" specified by the user in "+str(gradefilename)
            except:
                warnings.warn('cannot open manual grade file {file}'.format(file=gradefilename))
        else:
            print " => not found."
        return grade

    def check_for_defects(self):
        self.RawTestSessionDataPath = os.path.abspath(self.RawTestSessionDataPath)
        defectsfilename = self.RawTestSessionDataPath + '/defects.txt'
        print "checking for special defects information in '%s'"%defectsfilename
        Defects = []
        if os.path.isfile(defectsfilename):
            try:
                with open(defectsfilename) as defectsfile:
                    for line in defectsfile:
                        if '#' in line:
                            line = line.split('#')[0]
                        line = line.strip()
                        if len(line) > 0:
                            Defects.append(line)
            except:
                warnings.warn('cannot open defects file {file}'.format(file=defectsfilename))
            print "Reading defects \x1b[31m%s\x1b[0m specified by the user in %s"% (', '.join(Defects), str(defectsfilename))
        else:
            print " => not found."
        return Defects

    def ReadModuleVersion(self):
        if self.verbose:
            print 'Read configParameters'
        self.check_Test_Software()
        config_format = self.HistoDict.get('ConfigParameters', 'configFormat')
        fileNames = self.HistoDict.get('ConfigParameters', 'configParameters').split(',')
        version = 'none'
        nRocs = 0
        halfModule = 0
        if config_format == 'dat':
            lines = []
            for filename in fileNames:
                fileName = '%s/%s' % (self.RawTestSessionDataPath, filename)
                try:
                    f = open(fileName)
                    lines.extend(f.readlines())
                    f.close()
                except:
                    warnings.warn('cannot open config parameters dat file {file}'.format(file=fileName))
            version = 'none'
            for line in lines:
                if line.strip().startswith('rocType'):
                    version = line.split(' ')[-1]
                elif line.strip().startswith('nRocs'):
                    nRocs = int(line.split(' ')[-1])
                    if self.verbose: print '\tnRocs: %s' % nRocs
                elif line.strip().startswith('halfModule'):
                    halfModule = int(line.split(' ')[-1])
                    if self.verbose: print '\thalfModule: %s' % halfModule
        elif config_format == 'cfg':
            config = BetterConfigParser()
            for filename in fileNames:
                fileName = '%s/%s' % (self.RawTestSessionDataPath, filename)
                config.read(fileName)
            try:
                version = config.get('ROC', 'type')
            except (KeyError,ConfigParser.NoOptionError,ConfigParser.NoSectionError):
                warnings.warn('cannot find version name {section}'.format(section=config.sections()))
                if 'ROC' in config.sections():
                    warnings.warn('cannot find type in  ROC-section: {options}'.format(options=config.options('ROC')))
                version = 'none'
            try:
                nRocs = config.getint('Module', 'rocs')
            except (KeyError,ConfigParser.NoOptionError,ConfigParser.NoSectionError):
                nRocs = 0
            try:
                halfModule = config.get('Module', 'halfModule')
            except (KeyError,ConfigParser.NoOptionError,ConfigParser.NoSectionError):
                halfModule = 0
        version = version.rstrip('\n')
        if version and ('proc' in version or 'psi46digplus' in version or 'psi46digl1' in version):
            self.isPROC = True
        if self.verbose:
            print 'Version:    ', version
            print 'nRocs:      ', nRocs
            print 'halfModule: ', halfModule
            print 'isPROC:     ', self.isPROC
        self.version = version
        self.nRocs = nRocs
        self.halfModule = halfModule
        return version, nRocs, halfModule

    '''
        Populates all necessary data
        @final
    '''

    def PopulateAllData(self):
        self.OpenFileHandle()
        for i in self.ResultData['SubTestResultDictList']:
            if i['TestResultObject'].Enabled:
                self.SetCanvasSize()
                try:
                    i['TestResultObject'].PopulateAllData()
                    # i['TestResultObject'].check_for_comments()
                except Exception as inst:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    # Start red color
                    sys.stdout.write("\x1b[31m")
                    sys.stdout.flush()
                    # Print error message
                    print '\x1b[31mException while processing', i['TestResultObject'].FinalResultsStoragePath
                    # Print traceback
                    traceback.print_exception(exc_type, exc_obj, exc_tb)
                    # Stop red color
                    sys.stdout.write("\x1b[0m")
                    sys.stdout.flush()

                    self.TestResultEnvironmentObject.ErrorList.append(
                        {'ModuleID': self.Attributes['TestedObjectID'] if 'TestedObjectID' in self.Attributes else '',
                         'ModulePath': i['TestResultObject'].ModulePath,
                         'ErrorCode': inst,
                         'Message': traceback.format_exception(exc_type, exc_obj, exc_tb)[-1].strip('\n'),
                         'File': traceback.format_exception(exc_type, exc_obj, exc_tb)[-2].strip('\n'),
                         'FinalResultsStoragePath': i['TestResultObject'].FinalResultsStoragePath}
                    )
                    # todo Felix: handel exceptions

        self.SetCanvasSize()
        try:
            self.PopulateResultData()
            #self.SaveCanvas()
            self.check_for_comments()
        except Exception as inst:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # Start red color
            sys.stdout.write("\x1b[31m")
            sys.stdout.flush()
            print '\x1b[31mException while processing', self.FinalResultsStoragePath
            # Print traceback
            traceback.print_exception(exc_type, exc_obj, exc_tb)
            # Stop red color
            sys.stdout.write("\x1b[0m")
            sys.stdout.flush()

            self.TestResultEnvironmentObject.ErrorList.append(
                {'ModuleID': self.Attributes['TestedObjectID'] if 'TestedObjectID' in self.Attributes else '',
                 'ModulePath': self.ModulePath,
                 'ErrorCode': inst,
                 'Message': traceback.format_exception(exc_type, exc_obj, exc_tb)[-1].strip('\n'),
                 'File': traceback.format_exception(exc_type, exc_obj, exc_tb)[-2].strip('\n'),
                 'FinalResultsStoragePath': self.FinalResultsStoragePath}
                # 'FinalResultsStoragePath':i['TestResultObject'].FinalResultsStoragePath}
            )

    def SpecialPopulateData(self, TestResultObject, Parameters):
        # limit for grading
        YLimitB = Parameters['YLimitB']

        NChips = TestResultObject.ParentObject.Attributes['NumberOfChips']
        StartChip = TestResultObject.ParentObject.Attributes['StartChip']

        TestResultObject.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(TestResultObject.GetUniqueID(), '', NChips, StartChip, StartChip + NChips)

        # stores the integral values
        TestResultObject.ResultData['Plot']['ROOTObject_h2'] = ROOT.TH1D(TestResultObject.GetUniqueID(), '', NChips, StartChip, StartChip + NChips)

        Ymin = 0.  # minimum / maximum of y-axis values
        Ymax = 0.

        if not Parameters.has_key('ScaleToLimit') or Parameters['ScaleToLimit']:
            Ymax = YLimitB * 1.1

        Line = ROOT.TLine()
        Sum = 0.
        Mean = 0.

        if TestResultObject.ResultData['Plot']['ROOTObject']:

            NChipResults = 0

            for i in TestResultObject.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                ChipTestResultObject = \
                    self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                ChipNo = ChipTestResultObject.Attributes['ChipNo']
                ChipPosition = ChipNo + 1
                strValue = ''
                try:
                    strValue = ChipTestResultObject.ResultData['SubTestResults'][Parameters['DataKey']].ResultData[
                        'KeyValueDictPairs'][Parameters['DataParameterKey']]['Value']
                    Value = float(strValue)
                    if not 'NoIntegralCheck' in Parameters or not Parameters['NoIntegralCheck']:
                        nValue = float(ChipTestResultObject.ResultData['SubTestResults'][Parameters['DataKey']].ResultData[
                            'KeyValueDictPairs']['N']['Value'])
                    else:
                        nValue = 0
                except KeyError as e:
                    e.message += ' ' + str((Parameters['DataKey'], Parameters['DataParameterKey'], strValue))
                    if Parameters['DataKey'] not in ChipTestResultObject.ResultData['SubTestResults']:
                        e.message += '\n\tMissing: %s, Keys: %s' % (
                            Parameters['DataKey'], ChipTestResultObject.ResultData['SubTestResults'].keys())
                    elif Parameters['DataParameterKey'] not in \
                            ChipTestResultObject.ResultData['SubTestResults'][Parameters['DataKey']].ResultData[
                                'KeyValueDictPairs']:
                        e.message += '\n\tMissing: %s, Keys: %s ' % (Parameters['DataParameterKey'],
                                                                     ChipTestResultObject.ResultData['SubTestResults'][
                                                                         Parameters['DataKey']].ResultData[
                                                                         'KeyValueDictPairs'].keys())
                    raise e
                except TypeError as e:
                    e.message += ' ' + str((Parameters['DataKey'], Parameters['DataParameterKey'], strValue))
                    e.message += '.\n\tParamters: %s' % Parameters
                    e.message += '\n\t Value: %s' % strValue
                    raise e

                except ValueError as e:
                    e.message += ' ' + str((Parameters['DataKey'], Parameters['DataParameterKey'], strValue))
                    e.message += '.\n\tParamters: %s' % Parameters
                    e.message += '\n\t Value: %s' % strValue
                    raise e


                if Parameters.has_key('DataFactor'):
                    Value = Value * Parameters['DataFactor']
                if Parameters.has_key('CalcFunction'):
                    Value = Parameters['CalcFunction'](Value, ChipTestResultObject.ResultData['SubTestResults'][
                        Parameters['DataKey']].ResultData['KeyValueDictPairs'])

                Value = float(Value)
                Sum += Value

                TestResultObject.ResultData['Plot']['ROOTObject'].SetBinContent(ChipPosition, Value)
                TestResultObject.ResultData['Plot']['ROOTObject_h2'].SetBinContent(ChipPosition, nValue)
                if 1.2 * Value > Ymax:
                    Ymax = 1.2 * Value
                elif 1.2 * Value <= Ymin:
                    Ymin = 1.2 * Value
                NChipResults += 1

            Mean = Sum / NChipResults if NChipResults > 0 else 0

            TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerColor(Parameters['MarkerColor'])
            TestResultObject.ResultData['Plot']['ROOTObject'].SetLineColor(Parameters['LineColor'])

            TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerStyle(Parameters['MarkerStyle'])
            TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerSize(0.5)
            TestResultObject.ResultData['Plot']['ROOTObject'].SetTitle("")
            TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(Ymin, Ymax)
            TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC No.")
            TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle(Parameters['YaxisTitle'])
            TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            TestResultObject.ResultData['Plot']['ROOTObject'].Draw('LP')
            lineB = Line.DrawLine(TestResultObject.ParentObject.Attributes['StartChip'], YLimitB,
                                  TestResultObject.ParentObject.Attributes['StartChip'] +
                                  TestResultObject.ParentObject.Attributes['NumberOfChips'], YLimitB)
            lineB.SetLineWidth(2)
            lineB.SetLineStyle(2)
            lineB.SetLineColor(ROOT.kRed)

        ROOT.gPad.SetLogy(0)

        TestResultObject.SaveCanvas()
        TestResultObject.ResultData['Plot']['Caption'] = Parameters['Key']

        RMS = TestResultObject.ResultData['Plot']['ROOTObject'].GetRMS()
        Integral = TestResultObject.ResultData['Plot']['ROOTObject'].Integral(
            TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
            TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()
        )
        Integral_Entries = TestResultObject.ResultData['Plot']['ROOTObject'].GetEntries()

        under = TestResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(0)
        over = TestResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(
            TestResultObject.ResultData['Plot']['ROOTObject'].GetNbinsX() + 1)

        TestResultObject.ResultData['KeyValueDictPairs'] = {
            'mu': {
                'Value': '{0:1.2f}'.format(Mean),
                'Label': 'μ'
            },
        }

        TestResultObject.ResultData['KeyList'] = ['mu']
        if under:
            TestResultObject.ResultData['KeyValueDictPairs']['under'] = {'Value': '{0:1.2f}'.format(under),
                                                                         'Label': '<='}
            TestResultObject.ResultData['KeyList'] += ['under']
        if over:
            TestResultObject.ResultData['KeyValueDictPairs']['over'] = {'Value': '{0:1.2f}'.format(over), 'Label': '>='}
            TestResultObject.ResultData['KeyList'] += ['over']

    def AnalyzeLogfiles(self, logfiles, DetectMessages, ErrorNames):
        KeyValueDictPairs = {}
        KeyList = []
        ErrorObjects = []

        if not type(logfiles) is list:
            logfilesList = [logfiles]
        else:
            logfilesList = logfiles

        for logfile in logfilesList:
            if logfile:
                with open(logfile, 'r') as logfile:
                    for line in logfile:
                        ErrorObject = {}

                        if 'WARNING:' in line and not 'Not unmasking DUT' in line:
                            ErrorObject['type'] = 'warning'
                        if 'ERROR:' in line:
                            ErrorObject['type'] = 'error'
                        if 'CRITICAL:' in line:
                            ErrorObject['type'] = 'critical'

                        ErrorObject['channel'] = None
                        lineParts = line.strip().split()
                        if 'Channel' in lineParts:
                            pos = lineParts.index('Channel')
                            if pos < len(lineParts) - 1:
                                try:
                                    ErrorObject['channel'] = int(lineParts[pos+1])
                                except:
                                    pass

                        if ErrorObject.has_key('type'):
                            Found = False
                            for errorname, keywords in DetectMessages.iteritems():
                                for keyword in keywords:
                                    if keyword in line:
                                        ErrorObject['subtype'] = errorname
                                        Found = True
                                        break
                            if not Found:
                                ErrorObject['subtype'] = 'other'

                            ErrorObjects.append(ErrorObject)

        KeyValueDictPairs['nCriticals'] = {'Label': '# Criticals', 'Value': '%d'%len([True for ErrorObject in ErrorObjects if ErrorObject['type'] == 'critical'])}
        KeyValueDictPairs['nErrors'] = {'Label': '# Errors', 'Value': '%d'%len([True for ErrorObject in ErrorObjects if ErrorObject['type'] == 'error'])}
        KeyValueDictPairs['nWarnings'] = {'Label': '# Warnings', 'Value': '%d'%len([True for ErrorObject in ErrorObjects if ErrorObject['type'] == 'warning'])}

        for ch in range(4):
            KeyValueDictPairs['channel_%d_count'%ch] = {'Label': 'Channel %d'%ch, 'Value': '%d'%len([True for ErrorObject in ErrorObjects if ErrorObject['channel'] == ch])}

        KeyList = (['nCriticals', 'nErrors', 'nWarnings', 'channel_0_count', 'channel_1_count', 'channel_2_count', 'channel_3_count'])

        for errorSubtype, keywords in DetectMessages.iteritems():
            NErrors = len([True for ErrorObject in ErrorObjects if ErrorObject['subtype'] == errorSubtype])
            KeyValueDictPairs['message_%s_count'%errorSubtype] = {'Label': ErrorNames[errorSubtype] if errorSubtype in ErrorNames else errorSubtype, 'Value': '%d'%NErrors}
            if NErrors > 0:
                KeyList.append('message_%s_count'%errorSubtype)

        return {'KeyValueDictPairs': KeyValueDictPairs, 'KeyList': KeyList}


    '''
        Manually close all file handles of the sub tests
        @final
    '''

    def CloseSubTestResultFileHandles(self, Level=0):
        for i in self.ResultData['SubTestResultDictList']:
            if i['TestResultObject'].Enabled:
                i['TestResultObject'].CloseSubTestResultFileHandles(Level + 1)

        if Level:
            if self.FileHandle:

                if not type(self.FileHandle) == list:
                    self.FileHandle = [self.FileHandle]

                for SingleFileHandle in self.FileHandle:
                    try:
                        if "ROOT.TFile" in repr(SingleFileHandle):
                            if self.verbose:
                                print '\x1b[35mclose ROOT file "%s" ...\x1b[0m'%repr(SingleFileHandle)
                            SingleFileHandle.Close()
                        else:
                            if self.verbose:
                                print '\x1b[32mclose file "%s" ...\x1b[0m'%repr(SingleFileHandle)
                            SingleFileHandle.close()
                    except:
                        print '\x1b[33m warning: can not close file "%s" \x1b[0m'%repr(SingleFileHandle)

    '''
        Reads all attributes and writes it to the memory
    '''

    def CustomInit(self):
        pass

    '''
        Opens a file handle just before populating data
    '''

    def OpenFileHandle(self):
        pass

    '''
        Create a unique ID for creating root histograms
    '''

    def GetUniqueID(self):
        return self.TestResultEnvironmentObject.GetUniqueID(self.NameSingle)

    '''
        Sets the storage path
    '''

    def SetFinalResultsStoragePath(self):
        pass

    def CanvasSize(self, canvas):
        canvas.SetCanvasSize(
            self.DisplayOptions['Width'] * self.TestResultEnvironmentObject.Configuration['DefaultValues'][
                'CanvasWidth'],
            self.TestResultEnvironmentObject.Configuration['DefaultValues']['CanvasHeight']
        )
        canvas.Draw()
        canvas.Update()
        return canvas

    '''
        Sets the canvas size
    '''

    def SetCanvasSize(self):
        self.Canvas = self.CanvasSize(self.Canvas)

        # self.Canvas.SetCanvasSize(

    # self.DisplayOptions['Width']*self.TestResultEnvironmentObject.Configuration['DefaultValues']['CanvasWidth'],
    # self.TestResultEnvironmentObject.Configuration['DefaultValues']['CanvasHeight']
    # )
    # self.Canvas.Draw()
    # self.Canvas.Update()

    '''
        Saving the Canvas
    '''
    def SaveCanvas(self):
        if self.SavePlotFile:
            if self.Canvas:
                self.Canvas.SaveAs(self.GetPlotFileName())
                if not self.ResultData['Plot']['Caption']:
                    self.ResultData['Plot']['Caption'] = self.Title
                for Suffix in self.ResultData['Plot']['AdditionalFormats']:
                    if Suffix == 'pdf':
                        self.ResultData['Plot']['ImageFilePDF'] = self.GetPlotFileName(Suffix)
                    if self.ResultData['Plot']['ROOTObject']:
                        self.ResultData['Plot']['ROOTObject'].SetTitle(self.ResultData['Plot']['Caption'])
                    self.Canvas.SaveAs(self.GetPlotFileName(Suffix))
                self.ResultData['Plot']['Enabled'] = 1
                self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
    '''
        Generate the filename including the full path to the plot file according to the format
    '''

    def GetPlotFileName(self,Suffix=''):
        if Suffix == '':
            Suffix = self.ResultData['Plot']['Format']
        return self.FinalResultsStoragePath + '/' + self.NameSingle + '.' + Suffix

    '''
        Get the sub test result list in the display order
    '''

    def GetSortedSubTestResultDictList(self):
        # sort sub test results according to display order
        return sorted(
            self.ResultData['SubTestResultDictList'],
            key=lambda i: i['DisplayOptions']['Order']
        )

    '''
        Reads all test results and writes it to the memory
    '''

    def PopulateResultData(self):
        pass

    '''
        Generates all output files
    '''

    def GenerateFinalOutput(self):
        for i in self.ResultData['SubTestResults']:
            self.ResultData['SubTestResults'][i].GenerateFinalOutput()

        self.GenerateDataFiles()

    '''
        Generate files like Key/Value pairs in JSON format, ASCII-files, HTML-files, etc.
        @final
    '''

    def GenerateDataFiles(self):
        self.GenerateDataFileHTML()
        self.GenerateDataFileJSON()

    '''
        Generate HTML file
        @final
    '''

    def GenerateDataFileHTML(self):
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser

        HTMLFileName = 'TestResult.html'

        FinalHTML = ''
        HTMLTemplate = self.TestResultEnvironmentObject.TestResultHTMLTemplate
        FinalHTML = HTMLTemplate
        Levels = self.ModulePath[:].split('.')

        # Stylesheet

        StylesheetHTMLTemplate = HtmlParser.getSubpart(HTMLTemplate, '###HEAD_STYLESHEET_TEMPLATE###')
        StylesheetHTML = HtmlParser.substituteMarkerArray(
            StylesheetHTMLTemplate,
            {
                '###STYLESHEET###': self.TestResultEnvironmentObject.MainStylesheet +
                                    self.TestResultEnvironmentObject.TestResultStylesheet,
            }
        )
        FinalHTML = HtmlParser.substituteSubpart(
            FinalHTML,
            '###HEAD_STYLESHEETS###',
            StylesheetHTML
        )
        FinalHTML = HtmlParser.substituteSubpart(
            FinalHTML,
            '###HEAD_STYLESHEET_TEMPLATE###',
            ''
        )

        # Clickpath
        ClickPathEntries = []
        ClickPathEntryTemplate = HtmlParser.getSubpart(HTMLTemplate, '###CLICKPATH_ENTRY###')

        LevelPath = ''
        i = 0
        tmpTestResultObject = self

        for Level in Levels[2:]:
            LevelPath = '../' * i
            ClickPathEntries.append(HtmlParser.substituteMarkerArray(
                ClickPathEntryTemplate,
                {
                    '###URL###': HtmlParser.MaskHTML(LevelPath + HTMLFileName),
                    '###LABEL###': HtmlParser.MaskHTML(tmpTestResultObject.Title)
                }
            ))
            if self.ParentObject:
                tmpTestResultObject = tmpTestResultObject.ParentObject

            i += 1
        if not self.OverviewHTMLLink:
            OverviewHTMLLink = os.path.relpath(self.TestResultEnvironmentObject.GlobalOverviewPath + '/Overview.html',
                                               self.FinalResultsStoragePath)
        else:
            OverviewHTMLLink = self.OverviewHTMLLink
        ClickPathEntries.append(HtmlParser.substituteMarkerArray(
            ClickPathEntryTemplate,
            {
                '###URL###': HtmlParser.MaskHTML(OverviewHTMLLink),
                '###LABEL###': 'Overview'
            }
        ))

        ClickPathEntries.reverse()

        CSSClasses = ''

        # Result Data
        FinalHTML = HtmlParser.substituteSubpartArray(
            FinalHTML,
            {
                '###CLICKPATH_ENTRY###': ''.join(ClickPathEntries),
                '###RESULTDATA###': self.GenerateResultDataHTML(self, 0, self.DisplayOptions),
                '###ADDITIONALCSSCLASSES###': CSSClasses,
            }
        )
        # Do it again for the ghost
        FinalHTML = HtmlParser.substituteSubpartArray(
            FinalHTML,
            {
                '###CLICKPATH_ENTRY###': ''.join(ClickPathEntries),
            }
        )

        f = open(self.FinalResultsStoragePath + '/' + HTMLFileName, 'w')
        f.write(FinalHTML)
        f.close()

    '''
        Generate Result Data HTML for usage in HTML files
        @final
    '''

    def GenerateResultDataHTML(self, TestResultObject, RecursionLevel, DisplayOptions):
        HtmlParser = self.TestResultEnvironmentObject.HtmlParser
        HTMLTemplate = self.TestResultEnvironmentObject.TestResultHTMLTemplate
        ResultDataHTML = HtmlParser.getSubpart(HTMLTemplate, '###RESULTDATA###')
        HTMLFileName = 'TestResult.html'

        CSSClasses = self.NameSingle

        ResultDataHTML = HtmlParser.substituteMarker(ResultDataHTML,
                                                     '###RESULTDATAADDITIONALCSSCLASSES###',
                                                     HtmlParser.MaskHTML(CSSClasses)
        )

        RecursionRelativePath = ''
        if RecursionLevel > 0:
            PathParts = TestResultObject.FinalResultsStoragePath.split('/')
            # print PathParts
            RecursionRelativePath = PathParts[-1] + '/'

        # Title
        if not TestResultObject.Title:
            TestResultObject.Title = TestResultObject.NameSingle

        MyObjectTestDate = ''
        VersionInfo = ''
        if RecursionLevel == 0 and TestResultObject.Attributes['TestDate']:
            try:
                MyObjectTestDate = 'Test Date: ' + datetime.datetime.fromtimestamp(
                    float(TestResultObject.Attributes['TestDate'])).strftime("%Y-%m-%d %H:%M") + '<br><span style="font-size:10.5pt;" title="' + self.TestResultEnvironmentObject.MoReWebVersion + '">Analysis date: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + '</span>'
            except:
                print "\x1b[31mERROR: can't read test date from TestResultObject:", TestResultObject, "\x1b[0m"
                MyObjectTestDate = 'Test Date: unknown'
            VersionInfo = self.TestResultEnvironmentObject.MoReWebVersion + " on branch " + self.TestResultEnvironmentObject.MoReWebBranch

        MainTestResultAdditionalClasses = ''

        if RecursionLevel == 0:
            MainTestResultAdditionalClasses += 'MainTestResult Group'
            if self.DisplayOptions['Width'] > 1:
                MainTestResultAdditionalClasses += ' Width' + str(self.DisplayOptions['Width'])

        ResultDataHTML = HtmlParser.substituteMarkerArray(
            ResultDataHTML,
            {
                '###TITLE###': HtmlParser.MaskHTML(TestResultObject.Title),
                '###TESTDATE###': MyObjectTestDate,
                '###MAINTESTRESULTADDITIONALCLASSES###': MainTestResultAdditionalClasses,
                '###VERSIONINFO###': VersionInfo,
            }
        )
        # Plot
        PlotHTML = ''
        if TestResultObject.ResultData['Plot']['Enabled']:
            PlotHTML = HtmlParser.getSubpart(HTMLTemplate, '###PLOT###')
            PlotHTMLTemplate = HtmlParser.getSubpart(HTMLTemplate, '###PLOT###')
            PlotImageHTML = HtmlParser.getSubpart(PlotHTMLTemplate, '###PLOT_IMAGE###')
            '''PlotImageHTML = {
                'SVG':'',
                'PNG':''
            }
            if TestResultObject.ResultData['Plot']['Format'] == 'svg':
                PlotImageHTML['SVG'] = HtmlParser.getSubpart(PlotHTMLTemplate, '###PLOT_IMAGE_SVG###')
            elif TestResultObject.ResultData['Plot']['Format'] == 'png':
                PlotImageHTML['PNG'] = HtmlParser.getSubpart(PlotHTMLTemplate, '###PLOT_IMAGE_PNG###')

            for i in PlotImageHTML:
            '''

            # file operations for svg
            if TestResultObject.ResultData['Plot']['Format'] == 'svg' and RecursionLevel == 0 and self.SavePlotFile:
                f = open(TestResultObject.ResultData['Plot']['ImageFile'], 'r')
                SVGContent = f.read()
                f.close()

                # fix an error in chrome / safari when displaying resized svg
                if SVGContent.find('<svg preserveAspectRatio') == -1:
                    SVGContent = SVGContent.replace('<svg', '<svg preserveAspectRatio="xMinYMin"', 1)

                # remove an invalid space in attribute width and height
                SVGContent = SVGContent.replace('width=" ', 'width="')
                SVGContent = SVGContent.replace('height=" ', 'height="')
                SVGContent = SVGContent.replace('x=" ', 'x="')
                SVGContent = SVGContent.replace('y=" ', 'y="')
                SVGContent = SVGContent.replace('r=" ', 'r="')
                SVGContent = SVGContent.replace('=" ', '="')
                SVGContent = SVGContent.replace('&#786', '&#176')

                if self.GzipSVG and TestResultObject.ResultData['Plot']['ImageFile'].find('.svgz') == -1:
                    os.remove(TestResultObject.ResultData['Plot']['ImageFile'])
                    TestResultObject.ResultData['Plot']['ImageFile'] += 'z'
                    f = gzip.GzipFile(TestResultObject.ResultData['Plot']['ImageFile'], 'w')

                else:
                    f = open(TestResultObject.ResultData['Plot']['ImageFile'], 'w')
                    if os.path.exists(TestResultObject.ResultData['Plot']['ImageFile'] + 'z'):
                        os.remove(TestResultObject.ResultData['Plot']['ImageFile'] + 'z')

                f.write(SVGContent)
                f.close()

            if not TestResultObject.ResultData['Plot']['Caption']:
                TestResultObject.ResultData['Plot']['Caption'] = TestResultObject.Title
            try:
                PlotImageHTML = HtmlParser.substituteMarkerArray(
                    PlotImageHTML,
                    {
                        '###FILENAME###': HtmlParser.MaskHTML(
                            RecursionRelativePath + os.path.basename(TestResultObject.ResultData['Plot']['ImageFile'])),
                        '###PDFFILENAME###': HtmlParser.MaskHTML(
                            RecursionRelativePath + os.path.basename(TestResultObject.ResultData['Plot']['ImageFilePDF'])),
                        '###IMAGELARGECONTAINERID###': HtmlParser.MaskHTML(
                            TestResultObject.Name + '_' + TestResultObject.Key),
                        '###MARGIN_TOP###': str(int(-800. / float(
                            DisplayOptions['Width'] * self.TestResultEnvironmentObject.Configuration['DefaultValues'][
                                'CanvasWidth']) *
                                                    float(
                                                        self.TestResultEnvironmentObject.Configuration['DefaultValues'][
                                                            'CanvasHeight']) / 2.)),
                        '###TITLE###': TestResultObject.ResultData['Plot']['Caption'],
                        '###WIDTH###': str(DisplayOptions['Width']),
                        '###HEIGHT###': str(1),
                    }
                )
            except TypeError:
                print TestResultObject.Name, '_', TestResultObject.Key
                raise TypeError('Canntot convert, ' + str(TestResultObject.Name) + str(TestResultObject.Key))
            # PlotHTML = HtmlParser.substituteSubpart(PlotHTML, '###PLOT_IMAGE_'+i+'###', PlotImageHTML)
            PlotHTML = HtmlParser.substituteSubpart(PlotHTML, '###PLOT_IMAGE###', PlotImageHTML)

        ResultDataHTML = HtmlParser.substituteSubpart(ResultDataHTML, '###PLOT###', PlotHTML)

        # Key Value Dict Pairs
        KeyValueDictPairsRowHTMLTemplate = HtmlParser.getSubpart(HTMLTemplate, '###KEYVALUEDICTPAIRS_ROW###')
        KeyValueDictPairsRows = ''

        for i in TestResultObject.ResultData['KeyList']:
            if not TestResultObject.ResultData['KeyValueDictPairs'].has_key(i):
                warnings.warn('Cannot find Key: {Key} in {Name}'.format(Key=i,Name=self.Name))
                continue
            if not TestResultObject.ResultData['KeyValueDictPairs'][i].has_key('Unit'):
                TestResultObject.ResultData['KeyValueDictPairs'][i]['Unit'] = ''
            html_value = HtmlParser.MaskHTML(str(TestResultObject.ResultData['KeyValueDictPairs'][i]['Value']))
            if TestResultObject.ResultData['KeyValueDictPairs'][i].has_key('Sigma'):
                TestResultObject.ResultData['KeyValueDictPairs'][i]['SigmaOutput'] = ' +/- %s' % \
                                                                                     TestResultObject.ResultData[
                                                                                         'KeyValueDictPairs'][i][
                                                                                         'Sigma']
                html_value += ' &plusmn; ' + HtmlParser.MaskHTML(
                    str(TestResultObject.ResultData['KeyValueDictPairs'][i]['Sigma']))
            else:
                TestResultObject.ResultData['KeyValueDictPairs'][i]['SigmaOutput'] = ''

            if not TestResultObject.ResultData['KeyValueDictPairs'][i].has_key('Label'):
                TestResultObject.ResultData['KeyValueDictPairs'][i]['Label'] = i

            css_style = ''
            if 'Style' in TestResultObject.ResultData['KeyValueDictPairs'][i]:
                css_style = TestResultObject.ResultData['KeyValueDictPairs'][i]['Style']

            KeyValueDictPairsRows += HtmlParser.substituteMarkerArray(
                KeyValueDictPairsRowHTMLTemplate,
                {
                    '###KEY###': HtmlParser.MaskHTML(i),
                    '###LABEL###': HtmlParser.MaskHTML(
                        TestResultObject.ResultData['KeyValueDictPairs'][i]['Label']
                    ),
                    '###STYLE###': css_style,
                    '###VALUE###': html_value,
                    '###UNIT###': HtmlParser.MaskHTML(
                        TestResultObject.ResultData['KeyValueDictPairs'][i]['Unit']
                    ),
                }
            )
        ResultDataHTML = HtmlParser.substituteSubpart(ResultDataHTML,
                                                      '###KEYVALUEDICTPAIRS_ROW###',
                                                      KeyValueDictPairsRows)

        # Table
        TableHTML = ''
        if RecursionLevel == 0 or True:
            TableHTMLTemplate = HtmlParser.getSubpart(HTMLTemplate, '###TABLE###')
            TableHTML = HtmlParser.GenerateTableHTML(TableHTMLTemplate, TestResultObject.ResultData['Table'], {
                '###ADDITIONALCSSCLASS###': '',
                '###ID###': 'Table',
            })

        ResultDataHTML = HtmlParser.substituteSubpart(ResultDataHTML,
                                                      '###TABLE###',
                                                      TableHTML)

        # Sub Test Results
        SubTestResultListHTML = ''

        if RecursionLevel == 0:
            GroupWithNext = False
            i2 = 0
            for i in TestResultObject.GetSortedSubTestResultDictList():
                if i['TestResultObject'].DisplayOptions['Show']:

                    GroupCSSClass = ''

                    if not i['TestResultObject'].DisplayOptions['Floating']:
                        if i2 % 5 == 0:
                            GroupCSSClass += ' WidthNthChild5n'
                        if i2 % 4 == 0:
                            GroupCSSClass += ' WidthNthChild4n'
                        if i2 % 3 == 0:
                            GroupCSSClass += ' WidthNthChild3n'
                        if i2 % 2 == 0:
                            GroupCSSClass += ' WidthNthChild2n'

                        if i['TestResultObject'].DisplayOptions['Width'] > 1:
                            GroupCSSClass += ' Width' + str(i['TestResultObject'].DisplayOptions['Width'])

                    if not GroupWithNext:
                        SubTestResultListHTML += HtmlParser.substituteMarker(
                            HtmlParser.getSubpart(HTMLTemplate, '###SUBTESTRESULTGROUP_START###'),
                            '###SUBTESTRESULTGROUP_ADDITIONALCSSCLASSES###',
                            HtmlParser.MaskHTML(GroupCSSClass)
                        )
                        # only increase the width counter for a group start
                        i2 += i['TestResultObject'].DisplayOptions['Width']

                    SubTestResultListHTML += self.GenerateResultDataHTML(i['TestResultObject'], RecursionLevel + 1,
                                                                         i['TestResultObject'].DisplayOptions)

                    if not i['TestResultObject'].DisplayOptions['GroupWithNext']:
                        # if the last element was in a group but the current not, close the group
                        SubTestResultListHTML += HtmlParser.getSubpart(HTMLTemplate, '###SUBTESTRESULTGROUP_END###')

                    GroupWithNext = i['DisplayOptions']['GroupWithNext']

            # if the last element was in a group, close the group
            if GroupWithNext:
                SubTestResultListHTML += HtmlParser.getSubpart(HTMLTemplate, '###SUBTESTRESULTGROUP_END###')

        else:

            SubTestResultListItemHTMLTemplate = HtmlParser.getSubpart(HTMLTemplate, '###SUBTESTRESULTLIST_ITEM###')
            SubTestResultListHTML = HtmlParser.getSubpart(HTMLTemplate, '###SUBTESTRESULTLIST###')
            SubTestResultListItems = ''

            # Overview link
            SubTestResultOverviewLinkHTML = HtmlParser.getSubpart(SubTestResultListHTML, '###OVERVIEW_LINK###')
            if TestResultObject.ResultData['SubTestResultDictList']:
                SubTestResultOverviewLinkHTML = HtmlParser.substituteMarkerArray(
                    SubTestResultOverviewLinkHTML,
                    {
                        '###URL###': HtmlParser.MaskHTML(
                            os.path.basename(TestResultObject.FinalResultsStoragePath) + '/' + HTMLFileName
                        ),
                    }
                )
            else:
                SubTestResultOverviewLinkHTML = ''

            # Subtests
            for i in TestResultObject.GetSortedSubTestResultDictList():
                if i['DisplayOptions']['Show']:
                    SubTestResultListItems += HtmlParser.substituteMarkerArray(
                        SubTestResultListItemHTMLTemplate,
                        {
                            '###URL###': HtmlParser.MaskHTML(
                                os.path.basename(TestResultObject.FinalResultsStoragePath) + '/' +
                                os.path.basename(i['TestResultObject'].FinalResultsStoragePath) + '/' + HTMLFileName
                            ),
                            '###LABEL###': HtmlParser.MaskHTML(
                                i['TestResultObject'].Title
                            ),
                        }
                    )
            SubTestResultListHTML = HtmlParser.substituteSubpartArray(
                SubTestResultListHTML,
                {
                    '###SUBTESTRESULTLIST_ITEM###': SubTestResultListItems,
                    '###OVERVIEW_LINK###': SubTestResultOverviewLinkHTML,
                }
            )

            if not SubTestResultListItems:
                SubTestResultListHTML = ''


        if 'HTMLContent' in TestResultObject.ResultData:
            ResultDataHTML = ResultDataHTML + TestResultObject.ResultData['HTMLContent']

        ResultDataHTML = HtmlParser.substituteSubpartArray(
            ResultDataHTML,
            {
                '###SUBTESTRESULTLIST###': SubTestResultListHTML,
                '###SUBTESTRESULTGROUP_START###': '',
                '###SUBTESTRESULTGROUP_END###': '',
            }
        )
        return ResultDataHTML

    '''
        Generate file from ResultData['KeyValueDictPairs'] Key/Value pairs in JSON format
        @final
    '''

    def GenerateDataFileJSON(self):
        data = None
        key = None
        DataKeys = ['KeyValueDictPairs', 'HiddenData']
        for DataKey in DataKeys:
            try:
                data = self.ResultData[DataKey]
                for key in data:
                    if type(data[key])==dict and data[key].has_key('Value'):
                        value = data[key]['Value']
                        if type(value) == set:
                            value = list(value)
                            data[key]['Value'] = value
                    elif type(data[key])==dict:
                        data[key] = list(data[key])
                    else:
                        data_value = data[key]
                        data[key] = {'Value': str(data_value)}

                f = open(self.FinalResultsStoragePath + '/'+DataKey+'.json', 'w')
                f.write(json.dumps(self.ResultData[DataKey], sort_keys=True, indent=4, separators=(',', ': '), cls=SetEncoder))
                f.close()
            except (KeyError,IOError,TypeError):
                if data and key in data:
                    if type(data[key])==dict:
                        warnings.warn(
                            'Cannot create JSON for %s, %s' % (type(data[key]['Value']), str(self.ResultData[DataKey])))
                    else:
                        warnings.warn('Cannot create JSON for %s.' % (repr(data)))
                else:
                    warnings.warn('Cannot create JSON for %s.' % (repr(data)))

        if self.CreateJSONIndex:
            self.CreateJSONIndexFile()
    '''
        Generate file from ResultData['KeyValueDictPairs'] Key/Value pairs in ASCII format
        @final
    '''

    def GenerateDataFileASCII(self):
        pass

    '''
        Write all test results to the database
    '''

    def WriteToDatabase(self, ParentID=0):
        ColumnMapping = {}
        ID = 0
        WriteToDBSuccess = True

        try:
            ID = self.CustomWriteToDatabase(ParentID)
        except Exception as inst:
            if ParentID > 0:
                raise
            else:
                # Start red color
                sys.stdout.write("\x1b[31m")
                sys.stdout.flush()
                print 'Error in test (write to database)'
                print inst
                print inst.args
                print sys.exc_info()[0]
                print "\n\n------\n"
                # Print traceback
                exc_type, exc_obj, exc_tb = sys.exc_info()
                traceback.print_exception(exc_type, exc_obj, exc_tb)
                # Reset color
                sys.stdout.write("\x1b[0m")
                sys.stdout.flush()
                WriteToDBSuccess = False

        for i in self.ResultData['SubTestResults']:
            try:
                SubtestWriteToDBSuccess = self.ResultData['SubTestResults'][i].WriteToDatabase(ID)
                WriteToDBSuccess = WriteToDBSuccess and SubtestWriteToDBSuccess
            except Exception as inst:
                # Start red color
                sys.stdout.write("\x1b[31m")
                sys.stdout.flush()
                print 'Error in subtest (write to database)', self.ResultData['SubTestResults'][i].ModulePath, \
                    self.ResultData['SubTestResults'][i].FinalResultsStoragePath
                print inst
                print inst.args
                print sys.exc_info()[0]
                print "\n\n------\n"
                # Print traceback
                exc_type, exc_obj, exc_tb = sys.exc_info()
                traceback.print_exception(exc_type, exc_obj, exc_tb)
                # Reset color
                sys.stdout.write("\x1b[0m")
                sys.stdout.flush()
                WriteToDBSuccess = False

        self.PostWriteToDatabase()
        return WriteToDBSuccess

    def CustomWriteToDatabase(self, ParentID):
        pass

    def PostWriteToDatabase(self):
        pass

    def CreateJSONIndexFile(self):
        # find all .json files in subdirectories
        matches = []
        basePath = '/' + self.FinalResultsStoragePath.strip('/') + '/'
        print "-basePath:", basePath
        for root, dirnames, filenames in os.walk(self.FinalResultsStoragePath):
            for filename in fnmatch.filter(filenames, '*.json'):
                if 'KeyValueDictPairs' in filename or 'HiddenData' in filename:
                    absolutePath = '/' + os.path.join(root, filename).strip('/')
                    relativePath = absolutePath.replace(basePath, '')
                    matches.append([relativePath, absolutePath])
        print "-#files:",len(matches)
        # merge them to one single .json file
        JSONDictionary = {}
        f = open(self.FinalResultsStoragePath + '/Dictionary.json', 'w')
        for jsonFileName, absolutePath in matches:
            try:
                with open(absolutePath) as data_file:
                    JSONData = json.load(data_file)
            except:
                JSONData = {'file': 'missing or corrupted'}
            JSONDictionary[jsonFileName] = JSONData
        f.write(json.dumps(JSONDictionary, sort_keys=True, indent=4, separators=(',', ': '), cls=SetEncoder))
        f.close()

    def CleanUp(self, Level = 0):
        if self.verbose and Level < 1:
            print "\x1b[44m\x1b[97mCalling 'CleanUp' for %s\x1b[0m"%self.Name

        # clean up subtests
        for i in self.ResultData['SubTestResults']:
            SubTestResult = self.ResultData['SubTestResults'][i]
            try:
                SubTestResult.CleanUp(Level + 1)
            except:
                raise

        # clean up own plots
        if self.ResultData['Plot']['ROOTObject']:
            if self.verbose:
                print "\x1b[45m\x1b[97mgarbage collected: %s.%r\x1b[0m"%(self.Name, self.ResultData['Plot']['ROOTObject'])
            self.ResultData['Plot']['ROOTObject'].IsA().Destructor(self.ResultData['Plot']['ROOTObject'])

        if self.ROOTObjects:
            for i in self.ROOTObjects:
                if i:
                    try:
                        if self.verbose:
                            print "\x1b[45m\x1b[97mgarbage collected: %r\x1b[0m"%(i)
                        i.IsA().Destructor(i)
                    except:
                        pass
        self.CloseSubTestResultFileHandles()

    def __del__(self):
        self.CloseSubTestResultFileHandles()
