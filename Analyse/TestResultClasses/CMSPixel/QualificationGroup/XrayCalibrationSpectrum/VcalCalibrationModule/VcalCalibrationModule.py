import AbstractClasses
import math
import ROOT


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_QualificationGroup_XrayCalibration_{Method}_VcalCalibrationModule_TestResult".format(
            Method=self.Attributes['Method'])
        self.NameSingle = "VcalCalibrationModule"
        self.Title = 'Vcal Calibration Module - {Method}'.format(Method=self.Attributes['Method'])
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag

        # Determine the number or ROCs
        self.nRocs = self.ParentObject.nRocs
        self.ResultData["SubTestResultDictList"] = []

        for roc in range(self.nRocs):
            if self.verbose:
                print 'add subtest for Roc ', roc, "VcalCalibrationROC" + str(roc)
            self.ResultData["SubTestResultDictList"].append(
                {
                    "Key": "VcalCalibration_{Method}_ROC{ROC}".format(Method=self.Attributes['Method'], ROC=roc),
                    "Module": "VcalCalibrationROC",
                    "InitialAttributes": {
                        "StorageKey": "VcalCalibration_{Method}_ROC{ROC}".format(Method=self.Attributes['Method'],
                                                                                 ROC=roc),
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "Chips",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        "ChipNo": roc,
                        "Method": self.Attributes['Method'],
                    },
                    "DisplayOptions": {
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
            'HEADER': [
                [
                    'ROC', 'Slope', 'Slope Error', 'Offset', 'Offset Error'
                ]
            ],
            'BODY': [],
            'FOOTER': [],
        }

        slopes = []
        offsets = []
        error_slopes = []
        error_offsets = []
        for roc in range(self.nRocs):
            key = "VcalCalibration_{Method}_ROC{ROC}".format(Method=self.Attributes['Method'], ROC=roc)
            roc_results = self.ResultData['SubTestResults'][key].ResultData

            slopes.append(roc_results['KeyValueDictPairs']['Slope']['Value'])
            offsets.append(roc_results['KeyValueDictPairs']['Offset']['Value'])

            error_slopes.append(roc_results['KeyValueDictPairs']['Slope']['Sigma'])
            error_offsets.append(roc_results['KeyValueDictPairs']['Offset']['Sigma'])

        for roc in range (self.nRocs):
            table_line = []
            table_line.append(roc)
            table_line.append("%.1f e- / Vcal" % (slopes[roc]))
            table_line.append("%.1f e- / Vcal" % (error_slopes[roc]))
            table_line.append("%.1f e-" % (offsets[roc]))
            table_line.append("%.1f e-" % (error_offsets[roc]))
            self.ResultData['Table']['BODY'].append(table_line)

        average_offset = reduce(lambda x, y: x + y, offsets)
        average_slope = reduce(lambda x, y: x + y, slopes)
        # for roc in range(self.nRocs):
        # average_slope += slopes[roc]
        # average_offset += offsets[roc]

        average_slope /= self.nRocs
        sigma_slope = math.sqrt(
            reduce(lambda x, y: x + y, map(lambda x: x ** 2, slopes)) / self.nRocs - average_slope ** 2)
        average_offset /= self.nRocs
        sigma_offset = math.sqrt(
            reduce(lambda x, y: x + y, map(lambda x: x ** 2, offsets)) / self.nRocs - average_offset ** 2)

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

        self.ResultData['KeyValueDictPairs'] = {
            'avrg_Slope': {
                'Value': round(average_slope, 3),
                'Label': 'avrg. Slope',
                'Unit': 'nElectrons/VCal',
                'Sigma': round(sigma_slope, 3),
            },
            'avrg_Offset': {
                'Value': round(average_offset, 3),
                'Label': 'avrg. Offset',
                'Unit': 'nElectrons',
                'Sigma': round(sigma_offset, 3),
            },

        }
        # self.ResultData['KeyList'] = ['avrg_Slope', 'avrg_Offset']