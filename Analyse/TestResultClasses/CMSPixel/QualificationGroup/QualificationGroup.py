import AbstractClasses
import ROOT
import copy
import os
import os.path
import AbstractClasses.Helper.BetterConfigParser
import AbstractClasses.Helper.HtmlParser
import AbstractClasses.Helper.environment
# as BetterConfigParser
import AbstractClasses.Helper.testchain
import warnings


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_TestResult'
        self.NameSingle = 'QualificationGroup'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = self.Attributes['QualificationType'] + " " + self.Attributes['ModuleID']
        self.initParser = None

        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        if self.Attributes['TestType'] == 'automatic':
            self.ResultData['SubTestResultDictList'] = self.analyseTestIniFile()
        elif self.Attributes['TestType'] == 'singleFulltest':
            print 'add singleFulltest subTestResults'
            self.ResultData['SubTestResultDictList'] = [
                {
                    'Key': 'singleFulltest',
                    'Module': 'Fulltest',
                    'InitialAttributes': {
                        'StorageKey': 'Fulltest_p17_1',
                        'TestResultSubDirectory': '.',
                        'IncludeIVCurve': False,
                        'IVCurveSubDirectory': '',
                        'ModuleID': self.Attributes['ModuleID'],
                        'ModuleVersion': self.Attributes['ModuleVersion'],
                        'ModuleType': self.Attributes['ModuleType'],
                        'TestType': 'p17',
                        'TestTemperature': 17,
                        'ChipNo': 0,
                    },
                    'DisplayOptions': {
                        'Order': 1
                    }
                },
            ]
        elif self.Attributes['TestType'] == 'bareModuletest':
            print 'add bareModuletest subTestResults'
            self.ResultData['SubTestResultDictList'] = [
                {
                    'Key': 'bareModuletest',
                    'Module': 'BareModuleTest',
                    'InitialAttributes': {
                        'StorageKey': 'BareModule_p17_1',
                        'TestResultSubDirectory': '.',
                        'IncludeIVCurve': False,
                        'IVCurveSubDirectory': '',
                        'ModuleID': self.Attributes['ModuleID'],
                        'ModuleVersion': self.Attributes['ModuleVersion'],
                        'ModuleType': self.Attributes['ModuleType'],
                        'TestType': 'p17',
                        'TestTemperature': 17,
                        'ChipNo': 0,
                    },
                    'DisplayOptions': {
                        'Order': 1
                    }
                },     
            ]

        self.appendOperationDetails(self.ResultData['SubTestResultDictList'])

    def appendOperationDetails(self, testlist):
        Operator = 'UNKNOWN'
        Hostname = 'UNKNOWN'
        TestCenter = 'UNKNOWN'
        if self.initParser:
            if self.initParser.has_option('OperationDetails', 'Operator'):
                Operator = self.initParser.get('OperationDetails', 'Operator')
            if self.initParser.has_option('OperationDetails', 'Hostname'):
                Hostname = self.initParser.get('OperationDetails', 'Hostname')
            if self.initParser.has_option('OperationDetails', 'TestCenter'):
                TestCenter = self.initParser.get('OperationDetails', 'TestCenter')
        if testlist:
            for i in testlist:
                i['InitialAttributes']['Operator'] = Operator
                i['InitialAttributes']['Hostname'] = Hostname
                i['InitialAttributes']['TestCenter'] = TestCenter
                if self.verbose:
                    print i['Key'], i['InitialAttributes']['Operator'], i['InitialAttributes']['Hostname'], \
                    i['InitialAttributes']['TestCenter']

    def analyseTestIniFile(self):
        absPath = self.TestResultEnvironmentObject.ModuleDataDirectory + '/configfiles'
        if not os.path.isdir(absPath):
            raise Exception('dir for Tests.ini / elComandante.ini: %s does not exist' % absPath)
            pass
        self.initParser = AbstractClasses.Helper.BetterConfigParser.BetterConfigParser()
        fileName = absPath + '/elComandante.ini'
        fileName2 = absPath + '/Tests.ini'
        if os.path.isfile(fileName):
            self.initParser.read(fileName)
        elif os.path.isfile(fileName2):
            self.initParser.read(fileName2)
        else:
            raise Exception("file %s doesn't exist, cannot extract Tests from ini file" % fileName)

        return self.extractTests()


    def extractTests(self):
        if self.initParser:
            print 'Extract Tests from config file'
            test_list = []
            tests = self.initParser.get('Tests', 'Test')
            test_list = self.analyse_test_list(tests)
            print 'done with extraction'
            return test_list
            pass
        else:
            raise Exception('Cannot read from configparser')

    def analyse_test_list(self, testList):
        tests = []
        testchain = AbstractClasses.Helper.testchain.parse_test_list(testList)
        test = testchain.next()
        Testnames = []
        while test:
            env = AbstractClasses.Helper.environment.environment(test.test_str, self.initParser)
            test.environment = env
            test.testname = test.test_str.split("@")[0]
            Testnames.append(test.test_str.split("@")[0])
            test = test.next()
        index = 0
        test = testchain.next()
        if not ('HREfficiency' in Testnames): 
            tests, test, index = self.appendTemperatureGraph(tests, test, index)
        HRTestAdded = False
        while test:
            if 'fulltest' in test.testname.lower():
                print '\t-> appendFulltest'
                tests, test, index = self.appendFulltest(tests, test, index)
            elif 'cycle' in test.testname.lower():
                print '\t-> appendTemperatureCycle'
                tests, test, index = self.appendTemperatureCycle(tests, test, index)
            elif 'xrayspectrum' in test.testname.lower() or 'xraypxar' in test.testname.lower():
                print '\t-> appendXraySpectrum'
                tests, test, index = self.appendXrayCalibration(tests, test, index)
            elif (
                    ('hrefficiency' in test.testname.lower()
                        or 'hrdata' in test.testname.lower()
                        or 'hrscurves' in test.testname.lower()
                    )
                    and not HRTestAdded
                ):
                # Accept all tests with names 'HREfficiency'
                print '\t-> appendXRayHighRateTest'
                tests, test, index = self.appendXRayHighRateTest(tests, test, index)
                HRTestAdded = True
            elif 'powercycle' in test.testname:
                test = test.next()
            elif 'leakagecurrentpon' in test.testname.lower():
                print '\t-> appendLeakageCurrentPON'
                tests, test, index = self.appendLeakageCurrentPON(tests, test, index)
            else:
                if self.verbose:
                    print '\t-> cannot convert ', test.testname
                index += 1
                test = test.next()
        self.appendOperationDetails(self.ResultData['SubTestResultDictList'])
        return tests

    def appendTemperatureGraph(self, tests, test, index):
        if os.path.isfile(self.RawTestSessionDataPath+'/'+'temperature.log'):
            tests.append(
                {
                    'Key': 'Temperature',
                    'Module': 'Temperature',
                    'InitialAttributes': {
                        'StorageKey': 'ModuleQualification_Temperature',
                        'TestResultSubDirectory': 'logfiles',
                        'ModuleID': self.Attributes['ModuleID'],
                        'ModuleVersion': self.Attributes['ModuleVersion'],
                        'ModuleType': self.Attributes['ModuleType'],
                        'TestType': 'Temperature',
                    },
                    'DisplayOptions': {
                        'Order': len(tests) + 1,
                        'Width': 5,
                    }
                })
        return tests, test, index


    def appendTemperatureCycle(self, tests, test, index):
        #         print  '%03d'%index, test.testname, test.environment
        tests.append(
            {
                'Key': 'TemperatureCycle',
                'Module': 'TemperatureCycle',
                'InitialAttributes': {
                    'StorageKey': 'ModuleFulltest_TemperatureCycle',
                    'TestResultSubDirectory': 'configfiles',
                    'ModuleID': self.Attributes['ModuleID'],
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                    'ModuleType': self.Attributes['ModuleType'],
                    'TestType': 'TemperatureCycle',
                },
                'DisplayOptions': {
                    'Order': len(tests) + 1
                }
            })
        test = test.next()
        index += 1
        return tests, test, index

    def appendFulltest(self, tests, test, index):
        #        print  '%03d'%index, test.testname, test.environment
        environment = test.environment
        key = 'Module%s_%s' % (test.testname, test.environment.name)
        nKeys = 1
        for item in tests:
            if item['Key'].startswith(key):
                nKeys += 1
        key += '_%s' % (nKeys)
        directory = '%03d' % index + '_%s_%s' % (test.testname, test.environment.name)
        tests.append({
            'Key': key,
            'Module': 'Fulltest',
            'InitialAttributes': {
                'StorageKey': key,
                'TestResultSubDirectory': directory,
                'IncludeIVCurve': False,
                'ModuleID': self.Attributes['ModuleID'],
                'ModuleVersion': self.Attributes['ModuleVersion'],
                'ModuleType': self.Attributes['ModuleType'],
                'TestType': '%s_%s' % (test.environment.name, nKeys),
                'TestTemperature': test.environment.temperature,
            },
            'DisplayOptions': {
                'Order': len(tests) + 1
            }
        })
        if test.environment.temperature != 17:
            tests[-1]['InitialAttributes']['recalculateCurrentTo'] = 17
        test = test.next()
        index += 1
        if test and 'IV' in test.testname and test.environment.name == environment.name:
            #            print '\tFound corresponding', test.testname, test.environment
            tests[-1]['InitialAttributes']['IncludeIVCurve'] = True
            tests[-1]['InitialAttributes']['IVCurveSubDirectory'] = '%03d_%s_%s' % (
            index, test.testname, test.environment.name)
            test = test.next()
            index += 1
        return tests, test, index

    def appendXrayCalibration(self, tests, test, index):
        # environment = test.environment
        key = 'XrayCalibration{Method}'
        nKeys = 1
        for item in tests:
            if item['Key'].startswith(key):
                nKeys += 1
        key += '_%s' % (nKeys)
        directory = './%03d' % index + '_%s' % (test.testname)
        if test.environment.temperature >= 0:
            directory += "_p%i" % (test.environment.temperature)
        else:
            directory += "_m%i" % (-test.environment.temperature)

        tests.append({
            'Key': key,
            'Module': 'XrayCalibration',
            'InitialAttributes': {
                'StorageKey': key,
                'TestResultSubDirectory': directory,
                'IncludeIVCurve': False,
                'ModuleID': self.Attributes['ModuleID'],
                'ModuleVersion': self.Attributes['ModuleVersion'],
                'ModuleType': self.Attributes['ModuleType'],
                'TestType': 'XrayCalibration_{Method}',
                'TestTemperature': test.environment.temperature,
                'Method': 'Spectrum'
            },
            'DisplayOptions': {
                'Order': len(tests) + 1,
                'Width': 2
            }
        })
        while test:
            if 'xrayspectrum' in test.testname.lower() or 'xraypxar' in test.testname.lower():
                tests, test, index = self.appendFluorescenceTarget(tests, test, index)
            else:
                break
        targetList = [i['InitialAttributes']['Target'] for i in tests[-1]['InitialAttributes']['SubTestResultDictList']]
        print '\t    XraySpectrumMethod with Targets %s' % targetList
        self.appendOperationDetails(tests)
        self.appendOperationDetails(tests[-1]['InitialAttributes']['SubTestResultDictList'])
        xray_test = copy.deepcopy(tests[-1])
        xray_test2 = copy.deepcopy(tests[-1])
        self.check_Test_Software()
        if self.HistoDict.getboolean('XrayCalibration','SpectrumMethod'):
            tests[-1] = self.set_analysis_method(xray_test,'Spectrum')
        self.check_Test_Software()
        print 'softwareVersion:',self.testSoftware
        if self.testSoftware == 'pxar' and self.HistoDict.getboolean('XrayCalibration','SCurveMethod'):
            xray_test2 = self.set_analysis_method(xray_test2,'SCurve')
            tests.append(xray_test2)
        for i in tests:
            print i['Key'],i['Module'],i['InitialAttributes']['StorageKey']
        return tests, test, index

    def appendFluorescenceTarget(self, tests, test, index):
        environment = test.environment
        key = 'FluorescenceTargetModule_%s' % (test.environment.name)

        nKeys = 1
        for item in tests:
            if item['Key'].startswith(key):
                nKeys += 1
        key += '_%s' % (nKeys)
        directory = '../%03d' % index + '_%s' % (test.testname)
        if test.environment.temperature >= 0:
            directory += "_p%i" % (test.environment.temperature)
        else:
            directory += "_m%i" % (-test.environment.temperature)
        if not tests[-1].has_key('InitialAttributes'):
            tests[-1]['InitialAttributes'] = {}
        if not tests[-1]['InitialAttributes'].has_key('SubTestResultDictList'):
            tests[-1]['InitialAttributes']['SubTestResultDictList'] = []
        tests[-1]['InitialAttributes']['SubTestResultDictList'].append({
            'Key': key,
            'Module': 'FluorescenceTargetModule',
            'InitialAttributes': {
                'StorageKey': key,
                'TestResultSubDirectory': directory,
                'IncludeIVCurve': False,
                'ModuleID': self.Attributes['ModuleID'],
                'ModuleVersion': self.Attributes['ModuleVersion'],
                'ModuleType': self.Attributes['ModuleType'],
                'TestType': '%s_%s' % (test.environment.name, nKeys),
                'TestTemperature': test.environment.temperature,
                'Target': environment.name,
                'Operator': 'UNKNOWN',
                'Hostname': 'UNKNOWN',
                'TestCenter': 'UNKNOWN',
            },
            'DisplayOptions': {
                'Order': len(tests[-1]['InitialAttributes']['SubTestResultDictList']) + 20
            }
        })
        test = test.next()
        index += 1
        return tests, test, index

    def set_analysis_method(self,test,method):
        test['Key'] = test['Key'].format(Method=method)
        test['InitialAttributes']['StorageKey'] = test['InitialAttributes']['StorageKey'].format(Method=method)
        test['InitialAttributes']['Method'] = method
        test['InitialAttributes']['TestType'] = test['InitialAttributes']['TestType'].format(Method=method)
        for i in test['InitialAttributes']['SubTestResultDictList']:
            i['Key'] = i['Key'].format(Method=method)
            i['InitialAttributes']['StorageKey'] = i['InitialAttributes']['StorageKey'].format(Method=method)
            i['InitialAttributes']['Method'] = method
        return test

    ## Appends a high rate test to the list of tests to be analysed
    ##
    ## Creates one single test of type 'HighRateTest' when given any
    ## high rate test. Internally the actual tests are distinguished
    ## by name and made subtests to the 'HighRateTest'.
    def appendXRayHighRateTest(self, tests, test, index):
        key = 'XRayHRQualification'
        
        # Find the index of a previously created 'HighRateTest'
        idx = -1
        for i in range(len(tests)):
            if tests[i]["Key"] == key:
                idx = i
                break

        # If no 'HighRateTest' exists yet, create one
        if idx < 0:
            tests.append({
                'Key': key,
                'Module': 'XRayHRQualification',
                'InitialAttributes': {
                    'StorageKey': key,
                    'IncludeIVCurve': False,
                    'ModuleID': self.Attributes['ModuleID'],
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                    'ModuleType': self.Attributes['ModuleType'],
                    'TestType': 'XRayHRQualification',
                    'TestTemperature': test.environment.temperature,
                },
                'DisplayOptions': {
                    'Order': len(tests) + 1,
                    'Width': 2
                }
            })

            # Set the index to the newly created 'HighRateTest'
            idx = len(tests) - 1

        self.check_Test_Software()
        
        # Append the actual tests as subtests to the 'HighRateTest'
        # Distinguish by name. A test with name 'HighRateTest' is meant
        # as a generality which stands for
        # - HighRatePixelMap
        # - HighRateEfficiency
        # run together with results in the same ROOT file.
        #if 'HighRateTest' in test.testname or 'HighRatePixelMap' in test.testname:
        #    self.appendHighRatePixelMap(tests[idx], test, index)
        #if 'HighRateTest' in test.testname or 'HighRateEfficiency' in test.testname:
        #    self.appendHighRateEfficiency(tests[idx], test, index)

        # Iterate the test chain
        test = test.next()
        index += 1

        return tests, test, index

    def appendLeakageCurrentPON(self, tests, test, index):
        key = 'LeakageCurrentPON'
        idx = -1
        for i in range(len(tests)):
            if tests[i]["Key"] == key:
                idx = i
                break

        # If no 'LeakageCurrentPON' test exists yet, create one
        if idx < 0:
            tests.append({
                'Key': key,
                'Module': 'LeakageCurrentPON',
                'InitialAttributes': {
                    'StorageKey': key,
                    'IncludeIVCurve': False,
                    'ModuleID': self.Attributes['ModuleID'],
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                    'ModuleType': self.Attributes['ModuleType'],
                    'TestType': 'LeakageCurrentPON',
                    'TestTemperature': test.environment.temperature,
                },
                'DisplayOptions': {
                    'Order': len(tests) + 1,
                    'Width': 2
                }
            })

            idx = len(tests) - 1

        test = test.next()
        index += 1

        return tests, test, index

    def PopulateResultData(self):

        ModuleResultOverviewObject = AbstractClasses.ModuleResultOverview.ModuleResultOverview(
            self.TestResultEnvironmentObject)
        ModuleResultOverviewObject.FinalResultsStoragePath = self.FinalResultsStoragePath
        self.ResultData['Table'] = ModuleResultOverviewObject.TableData(self.Attributes['ModuleID'],
                                                                        self.Attributes['TestDate'],
                                                                        GlobalOverviewList=False)

    def PostWriteToDatabase(self):
        self.PopulateResultData();
