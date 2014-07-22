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

        ntargets = len(specturm_method_testlist)
        n_dummies = ntargets % 5 - 1
        for i in range(n_dummies):
            pos = start_position + ntargets + i
            specturm_method_testlist.append(
                {
                    'Key': 'Dummy_{Position}'.format(Position=pos),
                    'Module': 'Dummy',
                    'DisplayOptions': {
                        'Order': pos,
                    }
                }
            )

        start_position = 8 + len(specturm_method_testlist)
        for i in scurve_method_testlist:
            i['InitialAttributes']['Method'] = 'SCurve'
            i['InitialAttributes']['StorageKey'] = i['InitialAttributes']['StorageKey'] + '_SCurve'
            i['Key'] = i['Key'] + '_SCurve'
            i['DisplayOptions']['Order'] = scurve_method_testlist.index(i) + start_position
            if self.verbose:
                print i['Key'], ':', i['DisplayOptions']['Order']
        if do_spectrum_method:
            self.ResultData["SubTestResultDictList"].extend(specturm_method_testlist)
        if do_scurve_method:
            self.ResultData["SubTestResultDictList"].extend(scurve_method_testlist)
        if do_spectrum_method:
            self.ResultData["SubTestResultDictList"].append(
                {
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
                        'Method': 'Spectrum'
                    },
                    "DisplayOptions": {
                        "Order": 5,
                        "Width": 5
                    }
                }
            )
        if do_scurve_method:
            self.ResultData["SubTestResultDictList"].append(
                {
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
                        'Method': 'Spectrum'
                    },
                    "DisplayOptions": {
                        "Order": 6,
                        "Width": 5
                    }
                }
            )
        if do_spectrum_method:
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
                        # self.Attributes["SubTestResultDictList"],
                        'Operator': self.Attributes['Operator'],
                        'Method': 'Spectrum'

                    },
                    "DisplayOptions": {
                        "Order": 0,
                        "Width": 1
                    }
                }
            )
        if do_spectrum_method:
            self.ResultData["SubTestResultDictList"].append(
                {
                    "Key": "VcalCalibrationSlope",
                    "Module": "VcalCalibrationSlope",
                    "InitialAttributes": {
                        "StorageKey": "VcalCalibrationSlope",
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
                        'Method': 'Spectrum'
                    },
                    "DisplayOptions": {
                        "Order": 2,
                        "Width": 1
                    }
                }
            )
        if do_spectrum_method:
            self.ResultData["SubTestResultDictList"].append(
                {
                    "Key": "VcalCalibrationOffset",
                    "Module": "VcalCalibrationOffset",
                    "InitialAttributes": {
                        "StorageKey": "VcalCalibrationOffset",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "Chips",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        'NumberOfChips': self.Attributes['NumberOfChips'],
                        'StartChip': self.Attributes['StartChip'],
                        'Method': 'Spectrum'
                    },
                    "DisplayOptions": {
                        "Order": 2,
                        "Width": 1
                    }
                }
            )
        if do_scurve_method:
            self.ResultData["SubTestResultDictList"].append(
                {
                    "Key": "VcalCalibrationSlope",
                    "Module": "VcalCalibrationSlope",
                    "InitialAttributes": {
                        "StorageKey": "VcalCalibrationSlope",
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
                        'Method': 'SCurve'
                    },
                    "DisplayOptions": {
                        "Order": 2,
                        "Width": 1
                    }
                }
            )
        if do_scurve_method:
            self.ResultData["SubTestResultDictList"].append(
                {
                    "Key": "VcalCalibrationOffset",
                    "Module": "VcalCalibrationOffset",
                    "InitialAttributes": {
                        "StorageKey": "VcalCalibrationOffset",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "Chips",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        'NumberOfChips': self.Attributes['NumberOfChips'],
                        'StartChip': self.Attributes['StartChip'],
                        'Method': 'SCurve'
                    },
                    "DisplayOptions": {
                        "Order": 2,
                        "Width": 1
                    }
                }
            )
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