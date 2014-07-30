import AbstractClasses
import copy
import ROOT
import os
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_TestResult"
        self.NameSingle = "XrayCalibrationSpectrum"
        self.Title = "X-ray Calibration"
        self.check_Test_Software()
        self.ROCtype, self.nRocs, self.halfModule = self.ReadModuleVersion()
        self.Attributes['NumberOfChips'] = self.nRocs
        self.Attributes["ModuleVersion"] = self.ROCtype
        self.Attributes['StartChip'] = 0
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        do_spectrum_method = True
        do_scurve_method = False
        specturm_method_testlist = copy.deepcopy(self.Attributes["SubTestResultDictList"])
        scurve_method_testlist = copy.deepcopy(self.Attributes["SubTestResultDictList"])
        items = len(specturm_method_testlist)
        start_position = 7
        if self.verbose:
            print 'subtestresultdict list:', self.ResultData["SubTestResultDictList"]
        for i in specturm_method_testlist:
            i['InitialAttributes']['Method'] = 'Spectrum'
            i['InitialAttributes']['StorageKey'] = i['InitialAttributes']['StorageKey'] + '_Spectrum'
            i['Key'] = i['Key'] + '_Spectrum'
            i['DisplayOptions']['Order'] = specturm_method_testlist.index(i) + start_position
            if self.verbose:
                print i['Key'], ':', i['DisplayOptions']['Order']

        start_position = 8 + len(specturm_method_testlist)
        for i in scurve_method_testlist:
            i['InitialAttributes']['Method'] = 'SCurve'
            i['InitialAttributes']['StorageKey'] = i['InitialAttributes']['StorageKey'] + '_SCurve'
            i['Key'] = i['Key'] + '_SCurve'
            i['DisplayOptions']['Order'] = scurve_method_testlist.index(i) + start_position
            if self.verbose:
                print i['Key'], ':', i['DisplayOptions']['Order']
        self.order_counter = 0
        if do_spectrum_method:
            self.add_calibration_method(specturm_method_testlist)
            # self.ResultData["SubTestResultDictList"].extend(specturm_method_testlist)
        if do_scurve_method:
            self.add_calibration_method(scurve_method_testlist)
            # self.ResultData["SubTestResultDictList"].extend(scurve_method_testlist)
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
                    'Method': 'Spectrum'

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
        method = target_test_list[-1]['InitialAttributes']['Method']
        for i in target_test_list:
            k = target_test_list.index(i) + self.order_counter + 6
            i['DisplayOptions']['Order'] = k
            i['DisplayOptions']['Width'] = 1
            print k, i['Key']

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
                'Method': method,
            },
            "DisplayOptions": {
                "Order": self.order_counter + 5,
                "Width": 5
            }
        }
        )

        print self.ResultData["SubTestResultDictList"][-1]["DisplayOptions"]['Order'], \
        self.ResultData["SubTestResultDictList"][-1]['Key']
        # ['DisplayOptions']['Order'],
        # self.ResultData["SubTestResultDictList"][-1]['Key']
        self.ResultData["SubTestResultDictList"].append(
            {
                "Key": "VcalCalibrationSlope_" + method,
                "Module": "VcalCalibrationSlope",
                "InitialAttributes": {
                    "StorageKey": "VcalCalibrationSlope_" + method,
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
                    'Method': method,
                },
                "DisplayOptions": {
                    "Order": self.order_counter + 1,
                    "Width": 1
                }
            }
        )
        print self.ResultData["SubTestResultDictList"][-1]["DisplayOptions"]['Order'], \
        self.ResultData["SubTestResultDictList"][-1]['Key']
        self.ResultData["SubTestResultDictList"].append(
            {
                "Key": "VcalCalibrationOffset_" + method,
                "Module": "VcalCalibrationOffset",
                "InitialAttributes": {
                    "StorageKey": "VcalCalibrationOffset_" + method,
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "Chips",
                    "TestTemperature": self.Attributes["TestTemperature"],
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StartChip': self.Attributes['StartChip'],
                    'Method': method,
                },
                "DisplayOptions": {
                    "Order": self.order_counter + 2,
                    "Width": 1
                }
            }
        )
        print self.ResultData["SubTestResultDictList"][-1]["DisplayOptions"]['Order'], \
        self.ResultData["SubTestResultDictList"][-1]['Key']
        self.ResultData["SubTestResultDictList"].append(
                {
                    "Key": "VcalCalibrationChi2_"+method,
                    "Module": "VcalCalibrationChi2",
                    "InitialAttributes": {
                        "StorageKey": "VcalCalibrationChi2_"+method,
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "Chips",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        'NumberOfChips': self.Attributes['NumberOfChips'],
                        'StartChip': self.Attributes['StartChip'],
                        'Method': method,
                    },
                    "DisplayOptions": {
                        "Order": self.order_counter + 3,
                        "Width": 1
                    }
                }
            )
        print self.ResultData["SubTestResultDictList"][-1]["DisplayOptions"]['Order'], \
        self.ResultData["SubTestResultDictList"][-1]['Key']

        # ntargets = len(specturm_method_testlist)
        # n_dummies = ntargets % 5 - 1
        # for i in range(n_dummies):
        #     pos = start_position + ntargets + i
        #     specturm_method_testlist.append(
        #         {
        #             'Key': 'Dummy_{Position}'.format(Position=pos),
        #             'Module': 'Dummy',
        #             'DisplayOptions': {
        #                 'Order': pos,
        #             }
        #         }
        #     )


        if self.verbose:
            print_list = map(lambda i: [i["DisplayOptions"]['Order'], i['Key']],
                             self.ResultData["SubTestResultDictList"])
            for i in sorted(print_list):
                print i[0], i[1]

        self.check_Test_Software()
        self.Attributes['TestedObjectType'] = 'XrayCalibrationSpectrum'


    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

    def CustomWriteToDatabase(self, ParentID):
        pass