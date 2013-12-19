import AbstractClasses
import ROOT
import os
import AbstractClasses.Helper.BetterConfigParser 
import AbstractClasses.Helper.HtmlParser
import AbstractClasses.Helper.environment
#as BetterConfigParser
import AbstractClasses.Helper.testchain
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
  
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_TestResult'
        self.NameSingle='QualificationGroup'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = self.Attributes['QualificationType'] + " " + self.Attributes['ModuleID']
        if self.Attributes['TestType'] == 'automatic':
            self.ResultData['SubTestResultDictList'] = self.analyseTestIniFile()
        elif self.Attributes['TestType'] == 'singleFulltest':
            print 'add singleFulltest subTestResults'
            self.ResultData['SubTestResultDictList'] = [
                {
                    'Key':'singleFulltest',
                    'Module':'Fulltest',
                    'InitialAttributes':{
                        'StorageKey':    'Fulltest_p17_1',
                        'TestResultSubDirectory': '.',
                        'IncludeIVCurve':False,
                        'IVCurveSubDirectory':    '',
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType':'p17',
                        'TestTemperature':17,
                        'ChipNo':0,
                    },
                    'DisplayOptions':{
                        'Order':1        
                    }
                },
                                                        ]
        self.appendOperationDetails(self.ResultData['SubTestResultDictList'])
   
    def appendOperationDetails(self,testlist):
        Operator = 'UNKNOWN'
        Hostname = 'UNKNOWN'
        TestCenter = 'UNKNOWN'
        if self.initParser:
            if self.initParser.has_option('OperationDetails','Operator'):
                Operator = self.initParser.get('OperationDetails','Operator')
            if self.initParser.has_option('OperationDetails','Hostname'):
                Hostname = self.initParser.get('OperationDetails','Hostname')
            if self.initParser.has_option('OperationDetails','TestCenter'):
                TestCenter = self.initParser.get('OperationDetails','TestCenter')
        
        for i in testlist:
            print i,type(i),i.has_key('InitialAttributes')
            i['InitialAttributes']['Operator'] = Operator
            i['InitialAttributes']['Hostname'] = Hostname
            i['InitialAttributes']['TestCenter'] = TestCenter
            print Operator,Hostname,TestCenter
            
    def analyseTestIniFile(self):
        absPath = self.TestResultEnvironmentObject.ModuleDataDirectory+'/configfiles'
        if not os.path.isdir(absPath):
            raise Exception( 'dir for Tests.ini / elComandante.ini: %s does not exist'%absPath)
            pass
        self.initParser = AbstractClasses.Helper.BetterConfigParser.BetterConfigParser()
        fileName = absPath+'/elComandante.ini'
        fileName2 = absPath+'/Tests.ini'
        if os.path.isfile(fileName):
            self.initParser.read(fileName)
        elif os.path.isfile(fileName2):
            self.initParser.read(fileName2)
        else:
            raise Exception("file %s doesn't exist, cannot extract Tests from ini file"%fileName)
        
        return self.extractTests()
       
        
            
    def extractTests(self):
        if self.initParser:
            print 'Extract Tests from config file'
            testList = []
            tests = self.initParser.get('Tests','Test')
            testList = self.analyseTestList(tests)
    #        print 'done with extraction'
            return testList
            pass
        else:
            raise Exception('Cannot read from configparser')
    def analyseTestList(self,testList):
        tests =[]
        testchain = AbstractClasses.Helper.testchain.parse_test_list(testList)
        test = testchain.next()
        while test:
            env = AbstractClasses.Helper.environment.environment(test.test_str, self.initParser)
            test.environment = env
            test.testname = test.test_str.split("@")[0]
            test = test.next()
        index = 0
        test = testchain.next()
        while test:
            if 'Fulltest' in test.testname:
                tests,test,index = self.appendFulltest(tests,test,index)
            elif 'Cycle' in test.testname:
                tests,test,index = self.appendTemperatureCycle(tests, test, index)
            elif 'XraySpectrum' in test.testname:
                tests,test,index = self.appendXraySpectrum(tests,test,index)
            elif 'HighRateTest' in test.testname or 'HighRatePixelMap' in test.testname or 'HighRateEfficiency' in test.testname:
                # Accept all tests with names 'HighRateTest', 'HighRatePixelMap', and 'HighRateEfficiency' as high rate tests
                # The distinction of the tests is made within the 'appendHighRateTest' function.
                tests, test, index = self.appendHighRateTest(tests, test, index)
            else:
                index += 1
                test = test.next()
                
#        print '\n'
#        for item in tests:
#            for key in item:
#                print key,": ",item[key]
            
#            for key, value in item:
#                print key, value
#            print '\n'
#        for item in testchain:
#            print item
#        for item in testList:
#            item.
#            pass
        
        return tests
    
    def appendTemperatureCycle(self,tests,test,index):
#         print  '%03d'%index, test.testname, test.environment
         tests.append(
                      {
                    'Key':'TemperatureCycle',
                    'Module':'TemperatureCycle',
                    'InitialAttributes':{
                        'StorageKey':    'ModuleFulltest_TemperatureCycle',
                        'TestResultSubDirectory': 'configfiles',
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType':'TemperatureCycle',
                    },
                    'DisplayOptions':{
                        'Order':len(tests)+1        
                    }
                })
         test = test.next()
         index += 1
         return tests,test,index
     
    def appendFulltest(self,tests,test,index):
#        print  '%03d'%index, test.testname, test.environment
        environment = test.environment
        key = 'Module%s_%s'%(test.testname,test.environment.name)
        nKeys = 1
        for item in tests:
            if item['Key'].startswith(key):
                nKeys +=1
        key+='_%s'%(nKeys)        
        directory = '%03d'%index+'_%s_%s'%(test.testname,test.environment.name)
        tests.append( {
            'Key': key,
            'Module':'Fulltest',
            'InitialAttributes':{
                'StorageKey':    key,
                'TestResultSubDirectory': directory,
                'IncludeIVCurve':False,
                'ModuleID':self.Attributes['ModuleID'],
                'ModuleVersion':self.Attributes['ModuleVersion'],
                'ModuleType':self.Attributes['ModuleType'],
                'TestType': '%s_%s'%(test.environment.name,nKeys),
                'TestTemperature':test.environment.temperature,
            },
            'DisplayOptions':{
                'Order':len(tests)+1        
            }
           })
        if test.environment.temperature != 17:
            tests[-1]['InitialAttributes']['recalculateCurrentTo'] = 17
        test = test.next()
        index += 1
        if test and 'IV' in test.testname and test.environment.name == environment.name:
#            print '\tFound corresponding', test.testname, test.environment
            tests[-1]['InitialAttributes']['IncludeIVCurve'] =True
            tests[-1]['InitialAttributes']['IVCurveSubDirectory'] = '%03d_%s_%s'%(index,test.testname,test.environment.name)
            test = test.next()
            index += 1
        return tests,test,index
    
    def appendXraySpectrum(self,tests,test,index):
        environment = test.environment
        key = 'XraySpectrumMethod'
        nKeys = 1
        for item in tests:
            if item['Key'].startswith(key):
                nKeys +=1
        key+='_%s'%(nKeys)        
        directory =  "."
        tests.append( {
            'Key': key,
            'Module':'XrayCalibrationSpectrum',
            'InitialAttributes':{
                'StorageKey':    key,
                'TestResultSubDirectory': directory,
                'IncludeIVCurve':False,
                'ModuleID':self.Attributes['ModuleID'],
                'ModuleVersion':self.Attributes['ModuleVersion'],
                'ModuleType':self.Attributes['ModuleType'],
                'TestType': 'XraySpectrum',
                'TestTemperature':test.environment.temperature,
            },
            'DisplayOptions':{
                'Order':len(tests)+1,
                'Width':2
            }
           })
        while test and 'XraySpectrum' in test.testname:
            tests,test,index = self.appendFluorescenceTarget(tests,test,index)
        
        targetList = [i['InitialAttributes']['Target'] for i in tests[-1]['InitialAttributes']['SubTestResultDictList'] ]
        print 'XraySpectrumMethod with Targets %s'%targetList
        
        return tests,test,index

    # Hard coded initial guess for signal position based on element name
    def GetEnergy(self,elementName):
        if "Fe" in elementName:
            return 6391.02
        elif "Ni" in elementName:
            return 7461.03
        elif "Cu" in elementName:
            return 8027.84
        elif "Br" in elementName:
            return 11877.75
        elif "Mo" in elementName:
            return 17374.29
        elif "Ag" in elementName:
            return 21990.30
        elif "Sn" in elementName:
            return 25044.04
        elif "Ba" in elementName:
            return 31816.615
        else:
            return 0

    def appendFluorescenceTarget(self,tests,test,index):
        environment = test.environment
        key = 'Module%s_%s'%(test.testname,test.environment.name)
        nKeys = 1
        for item in tests:
            if item['Key'].startswith(key):
                nKeys +=1
        key+='_%s'%(nKeys)        
        directory = '%03d' % index + '_%s' % (test.testname)
        if test.environment.temperature >= 0:
            directory += "_p%i" % (test.environment.temperature)
        else:
            directory += "_m%i" % (-test.environment.temperature)
        TargetEnergy= self.GetEnergy(environment.name)
        TargetNElectrons = TargetEnergy / 3.6
        if not tests[-1].has_key('InitialAttributes'):
            tests[-1]['InitialAttributes'] = {}
        if not tests[-1]['InitialAttributes'].has_key('SubTestResultDictList'):
            tests[-1]['InitialAttributes']['SubTestResultDictList']=[]
        tests[-1]['InitialAttributes']['SubTestResultDictList'].append({
               'Key': key,
               'Module':'FluorescenceSpectrum',
               'InitialAttributes':{
                         'StorageKey':    key,
                        'TestResultSubDirectory': directory,
                        'IncludeIVCurve':False,
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType': '%s_%s'%(test.environment.name,nKeys),
                        'TestTemperature':test.environment.temperature,
                        'Target': environment.name,
                        'TargetEnergy': TargetEnergy,
                        'TargetNElectrons': TargetNElectrons,
                        'Operator': 'UNKNOWN',
                        'Hostname': 'UNKNOWN',
                        'TestCenter': 'UNKNOWN',
                },
                'DisplayOptions':{
                        'Order':len(tests[-1]['InitialAttributes']['SubTestResultDictList'])+1        
                }
           })
        test = test.next()
        index +=1
        return tests,test,index 

    ## Appends a high rate test to the list of tests to be analysed
    ##
    ## Creates one single test of type 'HighRateTest' when given any
    ## high rate test. Internally the actual tests are distinguished
    ## by name and made subtests to the 'HighRateTest'.
    def appendHighRateTest(self, tests, test, index):
        key = 'HighRateTest'
        directory = "."

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
                'Module':'HighRateTest',
                'InitialAttributes':{
                    'StorageKey': key,
                    'TestResultSubDirectory': directory,
                    'IncludeIVCurve':False,
                    'ModuleID':self.Attributes['ModuleID'],
                    'ModuleVersion':self.Attributes['ModuleVersion'],
                    'ModuleType':self.Attributes['ModuleType'],
                    'TestType': 'HighRateTest',
                    'TestTemperature':test.environment.temperature,
                },
                'DisplayOptions':{
                    'Order': len(tests) + 1,
                    'Width': 2
                }
            })

            # Set the index to the newly created 'HighRateTest'
            idx = len(tests) - 1

        # Append the actual tests as subtests to the 'HighRateTest'
        # Distinguish by name. A test with name 'HighRateTest' is meant
        # as a generality which stands for
        # - HighRatePixelMap
        # - HighRateEfficiency
        # run together with results in the same ROOT file.
        if 'HighRateTest' in test.testname or 'HighRatePixelMap' in test.testname:
            self.appendHighRatePixelMap(tests[idx], test, index)
        if 'HighRateTest' in test.testname or 'HighRateEfficiency' in test.testname:
            self.appendHighRateEfficiency(tests[idx], test, index)

        # Iterate the test chain
        test = test.next()
        index +=1

        return tests,test,index

    ## Appends a high rate pixel map test to the 'HighRateTest'
    def appendHighRatePixelMap(self, hr_test, test, index):
        # Generate a unique key name for the test
        environment = test.environment
        key = 'Module%s_%s_PixelMap'%(test.testname, test.environment.name)
        nKeys = 1
        try:
            for item in hr_test['InitialAttributes']['SubTestResultDictList']:
                if item['Key'].startswith(key):
                    nKeys +=1
        except KeyError:
            pass
        key+='_%s'%(nKeys)

        # Determine the directory name where the ROOT file with the results is
        #directory = '%03d'%index+'_%s_%s'%(test.testname,test.environment.name)
        directory = '%03d'%index+'_%s_p%i'%(test.testname,test.environment.temperature)

        # Append the test to the 'HighRateTest'
        if not hr_test.has_key('InitialAttributes'):
            hr_test['InitialAttributes'] = {}
        if not hr_test['InitialAttributes'].has_key('SubTestResultDictList'):
            hr_test['InitialAttributes']['SubTestResultDictList']=[]
        hr_test['InitialAttributes']['SubTestResultDictList'].append({
               'Key': key,
               'Module':'HighRatePixelMapModule',
               'InitialAttributes':{
                        'StorageKey': key,
                        'TestResultSubDirectory': directory,
                        'IncludeIVCurve':False,
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType': '%s_%s'%(test.environment.name,nKeys),
                        'TestTemperature':test.environment.temperature,
                        'Target': environment.xray_target,
                        'XrayVoltage': environment.xray_voltage,
                        'XrayCurrent': environment.xray_current
                },
                'DisplayOptions':{
                        'Order': len(hr_test['InitialAttributes']['SubTestResultDictList']) + 1,
                        'Width': 4
                }
           })

    ## Appends a high rate efficiency test to the 'HighRateTest'
    def appendHighRateEfficiency(self, hr_test, test, index):
        # Generate a unique key name for the test
        environment = test.environment
        key = 'Module%s_%s_Efficiency'%(test.testname, test.environment.name)
        nKeys = 1
        try:
            for item in hr_test['InitialAttributes']['SubTestResultDictList']:
                if item['Key'].startswith(key):
                    nKeys +=1
        except KeyError:
            pass
        key+='_%s'%(nKeys)

        # Determine the directory name where the ROOT file with the results is
        #directory = '%03d'%index+'_%s_%s'%(test.testname,test.environment.name)
        directory = '%03d'%index+'_%s_p%i'%(test.testname,test.environment.temperature)

        # Append the test to the 'HighRateTest'
        if not hr_test.has_key('InitialAttributes'):
            hr_test['InitialAttributes'] = {}
        if not hr_test['InitialAttributes'].has_key('SubTestResultDictList'):
            hr_test['InitialAttributes']['SubTestResultDictList']=[]
        hr_test['InitialAttributes']['SubTestResultDictList'].append({
               'Key': key,
               'Module':'HighRateEfficiencyModule',
               'InitialAttributes':{
                        'StorageKey': key,
                        'TestResultSubDirectory': directory,
                        'IncludeIVCurve':False,
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType': '%s_%s'%(test.environment.name,nKeys),
                        'TestTemperature':test.environment.temperature,
                        'Target': environment.xray_target,
                        'XrayVoltage': environment.xray_voltage,
                        'XrayCurrent': environment.xray_current
                },
                'DisplayOptions':{
                        'Order': len(hr_test['InitialAttributes']['SubTestResultDictList']) + 1,
                        'Width': 4
                }
           })

    def PopulateResultData(self):
        
        ModuleResultOverviewObject = AbstractClasses.ModuleResultOverview.ModuleResultOverview(self.TestResultEnvironmentObject)
        ModuleResultOverviewObject.FinalResultsStoragePath = self.FinalResultsStoragePath
        self.ResultData['Table'] = ModuleResultOverviewObject.TableData(self.Attributes['ModuleID'],self.Attributes['TestDate'],GlobalOverviewList = False)
        
    def PostWriteToDatabase(self):
        self.PopulateResultData();
