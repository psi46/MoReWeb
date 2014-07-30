import AbstractClasses
import ROOT


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Xrayt_Chip_TestResult'
        self.NameSingle = 'Chip_Xray'
        self.Title = 'Chip '+str(self.Attributes['ChipNo'])
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
            print 'nChips', self.ParentObject.Attributes['NumberOfChips'], type(
                self.ParentObject.Attributes['NumberOfChips'])
            print 'startChip', self.ParentObject.Attributes['StartChip'], type(
                self.ParentObject.Attributes['StartChip'])
        self.ResultData['SubTestResultDictList'] = []

        methods = set()
        for i in self.Attributes["SubTestResultDictList"]:
            if i['Module'] == 'FluorescenceTargetModule':
                target_key = i['InitialAttributes']['StorageKey']
                target = i['InitialAttributes']['Target']
                key = 'Xray_Target_' + target + '_Chip' + str(self.Attributes['ChipNo'])
                methods.add(i['InitialAttributes']['Method'])
                self.ResultData['SubTestResultDictList'].append(
                    {
                        "Key": key,
                        "Module": "Xray_Target_Chip",
                        "InitialAttributes": {
                            "StorageKey": key,
                            "TestResultSubDirectory": ".",
                            "IncludeIVCurve": False,
                            "ModuleVersion": self.Attributes["ModuleVersion"],
                            'target_key': target_key,
                            "Target": target,
                            "Method":i['InitialAttributes']['Method']
                        },
                        "DisplayOptions": {
                            "Order": 1,
                            "Width": 1
                        }
                    }
                )
        for method in methods:
            key = 'Xray_Calibration_{Method}_Chip{Chip}'.format(Method = method, Chip = self.Attributes['ChipNo'] )
            target_key = 'VcalCalibrationModule'
            self.ResultData['SubTestResultDictList'].append(
                        {
                            "Key": key,
                            "Module": "Xray_Calibration_Chip",
                            "InitialAttributes": {
                                "StorageKey": key,
                                "TestResultSubDirectory": ".",
                                "IncludeIVCurve": False,
                                "ModuleVersion": self.Attributes["ModuleVersion"],
                                'target_key': target_key,
                                "Method":method
                            },
                            "DisplayOptions": {
                                "Order": 1,
                                "Width": 1
                            }
                        }
                    )

    def OpenFileHandle(self):
        self.FileHandle = self.ParentObject.FileHandle

    def PopulateResultData(self):
        pass
