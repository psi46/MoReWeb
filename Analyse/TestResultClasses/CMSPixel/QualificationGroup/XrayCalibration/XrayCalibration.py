import AbstractClasses
import copy
import ROOT
import os
import sys
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        # self.verbose = True
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_TestResult"
        self.NameSingle = "XrayCalibration"
        self.Title = "X-ray Calibration - {Method}".format(Method=self.Attributes['Method'])
        self.check_Test_Software()
        self.ROCtype, self.nRocs, self.halfModule = self.ReadModuleVersion()
        self.Attributes['NumberOfChips'] = self.nRocs
        self.Attributes["ModuleVersion"] = self.ROCtype
        self.Attributes['StartChip'] = 0
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        target_list = copy.deepcopy(self.Attributes["SubTestResultDictList"])
        items = len(target_list)
        start_position = 7
        if self.verbose:
            print 'subtestresultdict list:', self.ResultData["SubTestResultDictList"]
        for i in target_list:
            i['InitialAttributes']['Method'] = self.Attributes['Method']
            i['InitialAttributes']['StorageKey'] = i['InitialAttributes']['StorageKey'] + '_' + self.Attributes[
                'Method']
            i['Key'] = i['Key'] + '_' + self.Attributes['Method']
            i['DisplayOptions']['Order'] = target_list.index(i) + start_position
            if self.verbose:
                print i['Key'], ':', i['DisplayOptions']['Order']
        self.order_counter = 0
        self.add_calibration_method(target_list)
        self.add_chips()

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
        #     self.ResultData["SubTestResultDictList"][-1]['Key']
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
        #     self.ResultData["SubTestResultDictList"][-1]['Key']
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
            print_list = map(lambda i: [i["DisplayOptions"]['Order'], i['Key']],
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
        slope_key = 'VcalCalibrationSlope_' +  self.Attributes['Method']
        avrgSlope = self.ResultData['SubTestResults'][slope_key].ResultData['KeyValueDictPairs'][
                'avrgSlope']['Value']
        self.ResultData['KeyValueDictPairs'] = {
            'Slope': {
                "Value": avrgSlope,
                # "Sigma": 0,
                "Label": 'avrg Slope',
                "Unit": "",
            }
        }
        self.ResultData['KeyList'].append('Slope')

    def CustomWriteToDatabase(self, ParentID):
        print 'fill row'
        method = self.Attributes['Method']
        comments = self.ResultData['KeyValueDictPairs'].get('comments', None)
        slope_key = 'VcalCalibrationSlope_' + method
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
        except:
            print self.ResultData['SubTestResults'].keys()
            if slope_key in self.ResultData['SubTestResults']:
                print self.ResultData['SubTestResults'][slope_key].ResultData['KeyValueDictPairs'].keys()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            avrgSlope = 0
            minSlope = 0
            maxSlope = 0
            Slopes = []
            avrgOffset = 0
            minOffset = 0
            maxOffset = 0
            Offsets = []
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
            'CurrentAtVoltage150': None,
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

            # added by Tommaso
            'TestCenter': self.Attributes['TestCenter'],
            'Hostname': self.Attributes['Hostname'],
            'Operator': self.Attributes['Operator'],
            #
        }

        print 'fill row end'
        # TODO: Please check if uplaod to DB is ok in this way...
        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal'] and False:
            from PixelDB import *
            # modified by Tommaso
            #
            # try and speak directly with PixelDB
            #

            pdb = PixelDBInterface(operator="tommaso", center="pisa")
            pdb.connectToDB()
            OPERATOR = os.environ['PIXEL_OPERATOR']
            CENTER = os.environ['PIXEL_CENTER']
            s = Session(CENTER, OPERATOR)
            pdb.insertSession(s)
            print "--------------------"
            print "INSERTING INTO DB", self.TestResultEnvironmentObject.FinalModuleResultsPath, s.SESSION_ID, Row
            print "--------------------"
            pp = pdb.insertTestFullModuleDirPlusMapv96Plus(s.SESSION_ID, Row)

            if (pp is None):
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
                        CurrentAtVoltage150,
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
                        :CurrentAtVoltage150,
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