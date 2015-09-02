import AbstractClasses
import copy
import warnings
import ROOT
import os
import sys
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser
from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        # self.verbose = True
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_TestResult"
        self.NameSingle = "XrayCalibration"
        self.Title = "X-ray Calibration - {Method}".format(Method=self.Attributes['Method'])
        self.check_Test_Software()
        self.ReadModuleVersion()
        self.Attributes['NumberOfChips'] = self.nRocs
        self.Attributes["ModuleVersion"] = self.version
        self.Attributes['StartChip'] = 0
        self.Attributes['TargetNames'] = []

        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        target_list = copy.deepcopy(self.Attributes["SubTestResultDictList"])
        # items = len(target_list)
        start_position = 7
        if self.verbose:
            print 'subtestresultdict list:', self.ResultData["SubTestResultDictList"]
        for i in target_list:
            self.Attributes['TargetNames'].append(i['InitialAttributes']['Target'])
            i['InitialAttributes']['Method'] = self.Attributes['Method']
            i['InitialAttributes']['NumberOfChips'] = self.Attributes['NumberOfChips']
            i['InitialAttributes']['StorageKey'] = i['InitialAttributes']['StorageKey'] + '_' + self.Attributes[
                'Method']
            i['Key'] = i['Key'] + '_' + self.Attributes['Method']
            i['DisplayOptions']['Order'] = target_list.index(i) + start_position
            if self.verbose:
                print i['Key'], ':', i['DisplayOptions']['Order']
        self.order_counter = 0
        self.add_calibration_method(target_list)
        self.add_chips()

        for Target in self.Attributes['TargetNames']:
            self.ResultData["SubTestResultDictList"].append({
                "Key": "HitmapOverview_{Target}".format(Target=Target),
                "Module": "HitmapOverview",
                "InitialAttributes": {
                    "StorageKey": "HitmapOverview_{Target}".format(Target=Target),
                    "Target": "{Target}".format(Target=Target),
                    "Method": self.Attributes['Method'],
                },
                "DisplayOptions": {
                    "Order": 100,
                    "Width": 4
                }
            })
            self.ResultData["SubTestResultDictList"].append({
                "Key": "HitmapDistribution_{Target}".format(Target=Target),
                "Module": "HitmapDistribution",
                "InitialAttributes": {
                    "StorageKey": "HitmapDistribution_{Target}".format(Target=Target),
                    "Target": "{Target}".format(Target=Target),
                    'Method': self.Attributes['Method'],
                },
                "DisplayOptions": {
                    "Order": 100,
                    "Width": 1
                }
            })

    def add_chips(self):
        self.ResultData["SubTestResultDictList"].append(
            {
                "Key": "Chips_Xray",
                "Module": "Chips_Xray",
                "InitialAttributes": {
                    "StorageKey": "Chips_Xray",
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StartChip': self.Attributes['StartChip'],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "Chips",
                    "TestTemperature": self.Attributes["TestTemperature"],
                    'SubTestResultDictList': self.ResultData["SubTestResultDictList"],
                    'Operator': self.Attributes['Operator'],
                    'Method': self.Attributes['Method']

                },
                "DisplayOptions": {
                    "Order": -1,
                    "Width": 1
                }
            }
        )

    def add_calibration_method(self, target_test_list):
        if len(target_test_list) == 0:
            return
        for i in target_test_list:
            k = target_test_list.index(i) + self.order_counter + 6
            i['DisplayOptions']['Order'] = k
            i['DisplayOptions']['Width'] = 1
            # print k, i['Key']

        self.ResultData["SubTestResultDictList"].extend(target_test_list)

        self.ResultData["SubTestResultDictList"].append({
            "Key": "VcalCalibrationModule",
            "Module": "VcalCalibrationModule",
            "InitialAttributes": {
                "StorageKey": "VcalCalibrationModule",
                "TestResultSubDirectory": ".",
                "IncludeIVCurve": False,
                "ModuleID": self.Attributes["ModuleID"],
                "ModuleVersion": self.Attributes["ModuleVersion"],
                "ModuleType": self.Attributes["ModuleType"],
                "TestType": "Chips",
                "TestTemperature": self.Attributes["TestTemperature"],
                'ModuleVersion': self.Attributes['ModuleVersion'],
                'NumberOfChips': self.Attributes['NumberOfChips'],
                'StartChip': self.Attributes['StartChip'],
                'Method': self.Attributes['Method'],
            },
            "DisplayOptions": {
                "Order": self.order_counter + 5,
                "Width": 5
            }
        }
        )

        # print self.ResultData["SubTestResultDictList"][-1]["DisplayOptions"]['Order'], \
        # self.ResultData["SubTestResultDictList"][-1]['Key']
        # ['DisplayOptions']['Order'],
        # self.ResultData["SubTestResultDictList"][-1]['Key']
        self.ResultData["SubTestResultDictList"].append(
            {
                "Key": "VcalCalibrationSlope_" + self.Attributes['Method'],
                "Module": "VcalCalibrationSlope",
                "InitialAttributes": {
                    "StorageKey": "VcalCalibrationSlope_" + self.Attributes['Method'],
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "Chips",
                    "TestTemperature": self.Attributes["TestTemperature"],
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StartChip': self.Attributes['StartChip'],
                    'Method': self.Attributes['Method'],
                },
                "DisplayOptions": {
                    "Order": self.order_counter + 1,
                    "Width": 1
                }
            }
        )
        # print self.ResultData["SubTestResultDictList"][-1]["DisplayOptions"]['Order'], \
        # self.ResultData["SubTestResultDictList"][-1]['Key']
        self.ResultData["SubTestResultDictList"].append(
            {
                "Key": "VcalCalibrationOffset_" + self.Attributes['Method'],
                "Module": "VcalCalibrationOffset",
                "InitialAttributes": {
                    "StorageKey": "VcalCalibrationOffset_" + self.Attributes['Method'],
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "Chips",
                    "TestTemperature": self.Attributes["TestTemperature"],
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StartChip': self.Attributes['StartChip'],
                    'Method': self.Attributes['Method'],
                },
                "DisplayOptions": {
                    "Order": self.order_counter + 2,
                    "Width": 1
                }
            }
        )
        # print self.ResultData["SubTestResultDictList"][-1]["DisplayOptions"]['Order'], \
        # self.ResultData["SubTestResultDictList"][-1]['Key']
        self.ResultData["SubTestResultDictList"].append(
            {
                "Key": "VcalCalibrationChi2_" + self.Attributes['Method'],
                "Module": "VcalCalibrationChi2",
                "InitialAttributes": {
                    "StorageKey": "VcalCalibrationChi2_" + self.Attributes['Method'],
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "Chips",
                    "TestTemperature": self.Attributes["TestTemperature"],
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StartChip': self.Attributes['StartChip'],
                    'Method': self.Attributes['Method'],
                },
                "DisplayOptions": {
                    "Order": self.order_counter + 3,
                    "Width": 1
                }
            }
        )
        # print self.ResultData["SubTestResultDictList"][-1]["DisplayOptions"]['Order'], \
        # self.ResultData["SubTestResultDictList"][-1]['Key']
        pos = self.order_counter + 4
        self.ResultData["SubTestResultDictList"].append(
            {
                'Key': 'Dummy_{Position}'.format(Position=pos),
                'Module': 'Dummy',
                'DisplayOptions': {
                    'Order': pos,
                    'Width': 1
                }
            }
        )

        if self.verbose:
            print_list = map(lambda l: [l["DisplayOptions"]['Order'], l['Key']],
                             self.ResultData["SubTestResultDictList"])
            for i in sorted(print_list):
                print i[0], i[1]

        self.check_Test_Software()
        self.Attributes['TestedObjectType'] = 'XrayCalibration'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
        method = self.Attributes['Method']
        slope_key = 'VcalCalibrationSlope_' + method
        try:
            avrgSlope = self.ResultData['SubTestResults'][slope_key].ResultData['KeyValueDictPairs']['avrgSlope'][
                'Value']
        except KeyError:
            avrgSlope = None
            warnings.warn('Cannot find key avrg Slope in  {slopeKey}'.format(slopeKey=slope_key))
            print self.ResultData['SubTestResults'].keys()
        self.ResultData['KeyValueDictPairs'] = {
            'Slope': {
                "Value": avrgSlope,
                # "Sigma": 0,
                "Label": 'avrg Slope',
                "Unit": "",
            }
        }
        self.ResultData['KeyList'].append('Slope')
        self.CloseSubTestResultFileHandles()

    def CustomWriteToDatabase(self, ParentID):
        print 'fill row'
        method = self.Attributes['Method']
        comments = self.ResultData['KeyValueDictPairs'].get('comments', None)
        slope_key = 'VcalCalibrationSlope_' + method
        offset_key = 'VcalCalibrationOffset_' + method
        chi2_key = 'VcalCalibrationChi2_' + method

        try:
            avrgSlope = self.ResultData['SubTestResults'][slope_key].ResultData['KeyValueDictPairs'][
                'avrgSlope']['Value']
            minSlope = self.ResultData['SubTestResults'][slope_key].ResultData['KeyValueDictPairs'][
                'minSlope']['Value']
            maxSlope = self.ResultData['SubTestResults'][slope_key].ResultData['KeyValueDictPairs'][
                'maxSlope']['Value']
            Slopes = self.ResultData['SubTestResults'][slope_key].ResultData['KeyValueDictPairs'][
                'Slopes']['Value']
            avrgOffset = self.ResultData['SubTestResults'][offset_key].ResultData['KeyValueDictPairs'][
                'avrgOffset']['Value']
            minOffset = self.ResultData['SubTestResults'][offset_key].ResultData['KeyValueDictPairs'][
                'minOffset']['Value']
            maxOffset = self.ResultData['SubTestResults'][offset_key].ResultData['KeyValueDictPairs'][
                'maxOffset']['Value']
            Offsets = self.ResultData['SubTestResults'][offset_key].ResultData['KeyValueDictPairs'][
                'Offsets']['Value']
            Chi2 = self.ResultData['SubTestResults'][chi2_key].ResultData['KeyValueDictPairs'][
                'chi2s']['Value']
            target_energies = []
        except KeyError, e:
            print self.ResultData['SubTestResults'].keys(), e
            if slope_key in self.ResultData['SubTestResults']:
                print self.ResultData['SubTestResults'][slope_key].ResultData['KeyValueDictPairs'].keys()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            warnings.warn(exc_type, fname, exc_tb.tb_lineno)
            avrgSlope = 0
            minSlope = 0
            maxSlope = 0
            Slopes = []
            avrgOffset = 0
            minOffset = 0
            maxOffset = 0
            Offsets = []
            Chi2 = []
            target_energies = []
        Row = {
            'ModuleID': self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'QualificationType': self.ParentObject.Attributes['QualificationType'],
            'avrgSlope': avrgSlope,
            'minSlope': minSlope,
            'maxSlope': maxSlope,
            'Slopes': Slopes,
            'avrgOffset': avrgOffset,
            'minOffset': minOffset,
            'maxOffset': maxOffset,
            'Offsets': Offsets,
            'Grade': None,
            'PixelDefects': None,
            'ROCsMoreThanOnePercent': None,
            'Noise': None,
            'Trimming': None,
            'PHCalibration': None,
            'CurrentAtVoltage150V': None,
            'IVSlope': None,
            'Temperature': None,
            'RelativeModuleFinalResultsPath': os.path.relpath(self.TestResultEnvironmentObject.FinalModuleResultsPath,
                                                              self.TestResultEnvironmentObject.GlobalOverviewPath),
            'FulltestSubfolder': os.path.relpath(self.FinalResultsStoragePath,
                                                 self.TestResultEnvironmentObject.FinalModuleResultsPath),
            # needed for PixelDB
            'AbsModuleFulltestStoragePath': self.TestResultEnvironmentObject.FinalModuleResultsPath,
            'AbsFulltestSubfolder': self.FinalResultsStoragePath,
            'InputTarFile': os.environ.get('TARFILE', None),
            'MacroVersion': os.environ.get('MACROVERSION', None),
            #

            'initialCurrent': None,
            'Comments': comments,
            'nCycles': None,
            'CycleTempLow': None,
            'CycleTempHigh': None,

            # Vcalibration Module
            'Vcal_Slope_Module':
                self.ResultData['SubTestResults']['VcalCalibrationModule'].ResultData['KeyValueDictPairs'][
                    'avrg_Slope']['Value'],
            'Vcal_Offset_Module':
                self.ResultData['SubTestResults']['VcalCalibrationModule'].ResultData['KeyValueDictPairs'][
                    'avrg_Slope']['Value'],
            #'Grade':self.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['Grade']['Value']
            ##TODO: target hit rates, grade

            #


            # added by Tommaso
            'TestCenter': self.Attributes['TestCenter'],
            'Hostname': self.Attributes['Hostname'],
            'Operator': self.Attributes['Operator'],
            #
        }

        # VCal target hit rates
        VcalTargetData = {}
        for j in self.ResultData['SubTestResultDictList']:
            if j['Module'] == 'FluorescenceTargetModule':
                VcalTargetTestResult = j['TestResultObject']
                VcalTargetData[VcalTargetTestResult.Attributes['Target']] = {
                    #'Rate':VcalTargetTestResult.ResultData['KeyValueDictPairs']['Rate'] #Measured target hit rate [Vcal],
                }

        print 'fill row end'
        # TODO: Please check if uplaod to DB is ok in this way...
        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
	    print "Global DB"
            from PixelDB import *
            # modified by Tommaso
            #
            # try and speak directly with PixelDB
            #

            pdb = PixelDBInterface(operator="tommaso", center="pisa")
            pdb.connectToDB()
            OPERATOR = os.environ['PIXEL_OPERATOR']
            CENTER = os.environ['PIXEL_CENTER']
	    s = Session(CENTER, OPERATOR,DATE=datetime.fromtimestamp(float(Row["TestDate"])))
            pdb.insertSession(s)
            print "--------------------"
            print "INSERTING XRAY INTO DB", self.TestResultEnvironmentObject.FinalModuleResultsPath, s.SESSION_ID, Row
            print "--------------------"
            anai = pdb.insertTestXRayVCal(s.SESSION_ID, Row)
            if anai is None:
		  print "INSERTION of MODULE PART FAILED!"
  	          sys.exit(33)
 
            insertedID =anai.TEST_ID
            procID =anai.PROCESSING_ID
            insertedFMID =anai.FULLMODULETEST_ID


            ##
            for ChipNo in range(self.nRocs):
                Key = "VcalCalibration_{Method}_ROC{ROC}".format(Method=self.Attributes['Method'], ROC=ChipNo)
                VcalChipTestResultObject = self.ResultData['SubTestResults']['VcalCalibrationModule'].ResultData['SubTestResults'][Key]
                VcalParameters = VcalChipTestResultObject.ResultData['KeyValueDictPairs']
                VcalSlope = VcalParameters['Slope']['Value']
                VcalOffest = VcalParameters['Offset']['Value']
                VcalChi2 = VcalParameters['chi2']['Value']
                ROCGrade = -1
                VcalTargetData = {}
                ROCTargetKey = "FluorescenceTarget_C{ROC}".format(ROC=ChipNo)
                for j in self.ResultData['SubTestResultDictList']:
                    # print j
                    if j['Module'] == 'FluorescenceTargetModule':
                        if j['TestResultObject'].ResultData['SubTestResults'].has_key(ROCTargetKey):
                            try:
                                # print '\tTArget',ChipNo,VcalTargetROCTestResult.Attributes['Target']
                                VcalTargetROCTestResult = j['TestResultObject'].ResultData['SubTestResults'][ROCTargetKey]
                                VcalTargetData[VcalTargetROCTestResult.Attributes['Target']] = {
                                    'Center': VcalTargetROCTestResult.ResultData['KeyValueDictPairs']['Center'],
                                    #Center of Peak [Vcal],
                                    'Rate': VcalTargetROCTestResult.ResultData['KeyValueDictPairs']['Rate']
                                    #Measured target hit rate [Vcal],
                                }
                            except Exception as e:
                                print '\nERROR',e
                                raw_input()
                                raise e
			    print "target",VcalTargetROCTestResult.Attributes['Target']
			    print VcalSlope,VcalOffest,VcalChi2,VcalTargetROCTestResult.ResultData['KeyValueDictPairs']['Rate'],VcalTargetROCTestResult.ResultData['KeyValueDictPairs']['Center'],ROCGrade,ChipNo
			    test = Test_FullModule_XRay_Vcal_Roc_Analysis(
			    		SESSION_ID=s.SESSION_ID,
			   	 	FULLMODULETEST_ID=insertedFMID,
			    		DATA_ID=0,
			    		TARGET=VcalTargetROCTestResult.Attributes['Target'],
					PROCESSING_ID=procID,
					MACRO_VERSION=Row["MacroVersion"], 
					SLOPE=VcalSlope,
					OFFSET=VcalOffest,
					CHi2NDF=VcalChi2,
					TARGET_HIT_RATE= VcalTargetROCTestResult.ResultData['KeyValueDictPairs']['Rate']['Value'],
					TARGET_PEAK_ENERGY=VcalTargetROCTestResult.ResultData['KeyValueDictPairs']['Center']['Value'],
					GRADE=ROCGrade,
					ROC_POS=ChipNo,
					TEST_XRAY_VCAL_MODULE_ID=insertedID,
		            		COMMENT="")

                            ti=pdb.insertObject(test)
                            print "XRAY VCAL per ROC INSERTED FOR", ChipNo, ti.TEST_ID

            if anai is None:
                print "INSERTION FAILED!"
                sys.exit(31)

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
                        ROCsMoreThanOnePercent,
                        Noise,
                        Trimming,
                        PHCalibration,
                        CurrentAtVoltage150V,
                        IVSlope,
                        Temperature,
                        RelativeModuleFinalResultsPath,
                        FulltestSubfolder,
                        initialCurrent,
                        Comments,
                        nCycles,
                        CycleTempLow,
                        CycleTempHigh
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :QualificationType,
                        :Grade,
                        :PixelDefects,
                        :ROCsMoreThanOnePercent,
                        :Noise,
                        :Trimming,
                        :PHCalibration,
                        :CurrentAtVoltage150V,
                        :IVSlope,
                        :Temperature,
                        :RelativeModuleFinalResultsPath,
                        :FulltestSubfolder,
                        :initialCurrent,
                        :Comments,
                        :nCycles,
                        :CycleTempLow,
                        :CycleTempHigh
                    )
                    ''', Row)
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid
