import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_TestResult"
        self.NameSingle = "HighRateTest"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag

        # Add all the high rate tests to the list of subtests to be
        # analysed.
        # nTest is greater than 1 because the results of the subtests
        # should be displayed below the summary tables.
        nTest = 4
        PixelMaps = []
        for test in self.Attributes['SubTestResultDictList']:
            test['DisplayOptions']['Order'] = nTest
            nTest += 1
            if test["Module"] == "HighRatePixelMapModule":
                self.ResultData["SubTestResultDictList"].append(test)
                # Make a list of high rate pixel map tests
                PixelMaps.append(test)
            elif test["Module"] == "HighRateEfficiencyModule":
                self.ResultData["SubTestResultDictList"].append(test)

        if self.verbose:
            print "Unsorted pixel map list:"
            for a in PixelMaps:
                print a["Key"], a["InitialAttributes"]["TestTemperature"], a["InitialAttributes"]["XrayVoltage"], a["InitialAttributes"]["XrayCurrent"]

        # Order PixelMaps by Temperature, then by XrayVoltage and XrayCurrent
        # Extremely primitive sorting algorithm
        for i in range(len(PixelMaps)):
            ta = PixelMaps[i]['InitialAttributes']['TestTemperature']
            va = PixelMaps[i]['InitialAttributes']['XrayVoltage']
            ia = PixelMaps[i]['InitialAttributes']['XrayCurrent']
            for j in range(i + 1, len(PixelMaps)):
                tb = PixelMaps[j]['InitialAttributes']['TestTemperature']
                vb = PixelMaps[j]['InitialAttributes']['XrayVoltage']
                ib = PixelMaps[j]['InitialAttributes']['XrayCurrent']
                if tb < ta or (tb == ta and vb < va) or (tb == ta and vb == va and ib < ia):
                    # Exchange the two
                    tmp = PixelMaps[j]
                    PixelMaps[j] = PixelMaps[i]
                    PixelMaps[i] = tmp

        if self.verbose:
            print "Sorted pixel map list:"
            for a in PixelMaps:
                print a["Key"], a["InitialAttributes"]["TestTemperature"], a["InitialAttributes"]["XrayVoltage"], a["InitialAttributes"]["XrayCurrent"]

        # Pick a voltage and temperature that have two different current settings
        idx = len(PixelMaps) - 1
        top = len(PixelMaps) - 1
        count = 0
        temperature = None
        voltage = None
        current = None
        while idx >= 0:
            if PixelMaps[idx]['InitialAttributes']['XrayVoltage'] != voltage or PixelMaps[idx]['InitialAttributes']['TestTemperature'] != temperature:
                if count > 1:
                    break
                top = idx
                temperature = PixelMaps[idx]['InitialAttributes']['TestTemperature']
                voltage = PixelMaps[idx]['InitialAttributes']['XrayVoltage']
                current = PixelMaps[idx]['InitialAttributes']['XrayCurrent']
                count = 1
            if PixelMaps[idx]['InitialAttributes']['XrayCurrent'] != current:
                count += 1
            idx -= 1

        # Require 2 pixel maps that have the same voltage and same temperature
        if count > 1:
            # Select the pixel maps with the highest and lowest current
            PixelMapA = PixelMaps[idx + 1]['Key']
            PixelMapB = PixelMaps[top]['Key']
            directory = PixelMaps[idx + 1]["InitialAttributes"]["TestResultSubDirectory"]
            ModuleVersion, nRocs, halfModule = self.ReadModuleConfigParams(directory)

            # Add the DCol test
            self.ResultData['SubTestResultDictList'].append(
                {
                    "Key": "HighRateDColEfficiencyModule",
                    "InitialAttributes": {
                        "StorageKey": "HighRateDColEfficiencyModule",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "ModuleNRocs": nRocs,
                        "TestType": "HighRateTest",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        "PixelMapA": PixelMapA,
                        "PixelMapB": PixelMapB,
                    },
                    "DisplayOptions":{
                        "Order": 3,
                        "Width": 5
                    }
                }
            )
            nTest += 1

        # Add a pixel map summary test
        self.ResultData['SubTestResultDictList'].append(
            {
                "Key": "HighRatePixelMapSummary",
                "InitialAttributes": {
                    "StorageKey": "HighRatePixelMapSummary",
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "HighRateTest",
                    "TestTemperature": self.Attributes["TestTemperature"],
                },
                "DisplayOptions":{
                    "Order": 1,
                    "Width": 5
                }
            }
        )
        nTest += 1

        # Add an efficiency summary test
        self.ResultData['SubTestResultDictList'].append(
            {
                "Key": "HighRateEfficiencySummary",
                "InitialAttributes": {
                    "StorageKey": "HighRateEfficiencySummary",
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "HighRateTest",
                    "TestTemperature": self.Attributes["TestTemperature"],
                },
                "DisplayOptions":{
                    "Order": 2,
                    "Width": 5
                }
            }
        )
        nTest += 1

        self.Attributes['TestedObjectType'] = 'HighRateTest'

    def ReadModuleConfigParams(self, subdir):
        fileName = self.RawTestSessionDataPath + "/" + subdir + '/configParameters.dat'
        f = open(fileName)
        lines = f.readlines()
        for line in lines:
            if line.strip().startswith('rocType'):
                version = line.split(' ')[-1]
            elif line.strip().startswith('nRocs'):
                nRocs = int(line.split(' ')[-1])
            elif line.strip().startswith('halfModule'):
                halfModule = int(line.split(' ')[-1])
        f.close()
        return (version, nRocs, halfModule)

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
