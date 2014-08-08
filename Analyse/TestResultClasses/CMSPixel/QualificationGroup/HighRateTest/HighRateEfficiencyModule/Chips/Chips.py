import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRateEfficiencyModule_Chips_TestResult"
        self.NameSingle = "Chips"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.ResultData["SubTestResultDictList"] = []
        nRocs = self.Attributes['ModuleNRocs']
        for roc in range(nRocs):
            self.ResultData["SubTestResultDictList"].append(
                {
                    "Key": "Chip" + str(roc),
                    "Module": "Chip",
                    "InitialAttributes": {
                        "StorageKey": "Chip" + str(roc),
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "Chips",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        #"SubTestResultDictList": self.Attributes["SubTestResultDictList"],
                        "ChipNo": roc,
                        'XrayVoltage': self.Attributes["XrayVoltage"],
                        'XrayCurrent': self.Attributes["XrayCurrent"],
                    },
                    "DisplayOptions":{
                        "Order": 1,
                        "Width": 1
                    }
                }
            )

        self.Attributes['TestedObjectType'] = 'Chips'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        self.ResultData['Table'] = {
            'HEADER':[
                [
                    'ROC',
                ]
            ],
            'BODY':[],
            'FOOTER':[],
        }
        chip = self.ResultData['SubTestResults']['Chip' + str(0)]
        summary = chip.ResultData['SubTestResults']['HighRateEffSummary']
        keys = summary.ResultData['KeyList']
        totals = []
        units = []
        for key in keys:
            label = summary.ResultData['KeyValueDictPairs'][key]['Label']
            self.ResultData['Table']['HEADER'][0].append(label)
            totals.append(0)
            units.append(summary.ResultData['KeyValueDictPairs'][key]['Unit'])

        nRocs = self.Attributes['ModuleNRocs']
        for roc in range(nRocs):
            chip = self.ResultData['SubTestResults']['Chip' + str(roc)]
            summary = chip.ResultData['SubTestResults']['HighRateEffSummary']
            keys = summary.ResultData['KeyList']
            keyvalues = summary.ResultData['KeyValueDictPairs']
            self.ResultData['Table']['BODY'].append(["ROC " + str(roc)])
            idx = 0
            for key in keys:
                value = keyvalues[key]['Value']
                unit = keyvalues[key]['Unit']
                unit = " " + unit
                if unit == " [1]":
                    unit = ""
                self.ResultData['Table']['BODY'][roc].append("%s%s" % (str(value), unit))
                totals[idx] += value
                idx += 1

        self.ResultData['Table']['FOOTER'].append(["Total"])
        idx = 1
        for i in range(len(totals)):
            value = totals[i]
            unit = units[i]
            unit = " " + unit
            if unit == " [1]":
                unit = ""
            if keys[i] == "Rate" or keys[i] == "Core efficiency" or keys[i] == "Mean efficiency":
                value /= nRocs
            self.ResultData['Table']['FOOTER'][0].append("%s%s" % (str(value), unit))
