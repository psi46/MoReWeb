import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_VcalCalibrationModule_TestResult"
        self.NameSingle = "VcalCalibrationModule"
        self.verbose = False
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag

        # Determine the number or ROCs
        for a in self.ParentObject.ResultData['SubTestResults']:
            if 'ModuleXraySpectrum' in a:
                self.nRocs = self.ParentObject.ResultData['SubTestResults'][a].nRocs
                break

        self.ResultData["SubTestResultDictList"] = []

        for roc in range(self.nRocs):
            self.ResultData["SubTestResultDictList"].append(
                {
                    "Key": "VcalCalibrationROC" + str(roc),
                    "Module": "VcalCalibrationROC",
                    "InitialAttributes": {
                        "StorageKey": "VcalCalibrationROC" + str(roc),
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "Chips",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        "ChipNo": roc,
                    },
                    "DisplayOptions":{
                        "Order": 1,
                        "Width": 1
                    }
                }
            )

        self.Attributes['TestedObjectType'] = "VcalCalibrationModule"

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        self.ResultData['Table'] = {
            'HEADER':[
                [
                    'ROC', 'Slope', 'Slope Error', 'Offset', 'Offset Error'
                ]
            ],
            'BODY':[],
            'FOOTER':[],
        }

        slopes = []
        offsets = []
        for roc in range(self.nRocs):
            roc_results = self.ResultData['SubTestResults']['VcalCalibrationROC%i' % (roc)].ResultData
            table_line = []
            table_line.append(roc)
            table_line.append("%.1f e- / Vcal" % (roc_results['KeyValueDictPairs']['Slope']['Value']))
            table_line.append("%.1f e- / Vcal" % (roc_results['KeyValueDictPairs']['Slope']['Sigma']))
            table_line.append("%.1f e-" % (roc_results['KeyValueDictPairs']['Offset']['Value']))
            table_line.append("%.1f e-" % (roc_results['KeyValueDictPairs']['Offset']['Sigma']))
            slopes.append(roc_results['KeyValueDictPairs']['Slope']['Value'])
            offsets.append(roc_results['KeyValueDictPairs']['Offset']['Value'])
            self.ResultData['Table']['BODY'].append(table_line)

        average_slope = 0;
        average_offset = 0;
        for roc in range(self.nRocs):
            average_slope += slopes[roc]
            average_offset += offsets[roc]

        average_slope /= self.nRocs
        average_offset /= self.nRocs

        table_line = []
        table_line.append("Average")
        table_line.append("%.1f e- / Vcal" % (average_slope))
        table_line.append("")
        table_line.append("%.1f e-" % (average_offset))
        table_line.append("")
        self.ResultData['Table']['FOOTER'].append(table_line)

        slopes.sort()
        offsets.sort()
        median_slope = slopes[self.nRocs / 2]
        median_offset = offsets[self.nRocs / 2]

        table_line = []
        table_line.append("Median")
        table_line.append("%.1f e- / Vcal" % (median_slope))
        table_line.append("")
        table_line.append("%.1f e-" % (median_offset))
        table_line.append("")
        self.ResultData['Table']['FOOTER'].append(table_line)
