import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.method = self.Attributes['Method']
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_VcalCalibrationOffset_TestResult"
        self.NameSingle = "VcalCalibrationOffset"
        self.Title = "Offset of {Method} Vcal Calibration".format(Method = self.method)
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.ResultData["SubTestResultDictList"] = []
        self.check_Test_Software()
        self.Attributes['TestedObjectType'] = 'VcalCalibrationOffset'


    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
        self.nRocs = self.ParentObject.nRocs
        offsets = []
        error_offsets = []
        for roc in range(self.nRocs):
            vcal_calibration_module = self.ParentObject.ResultData['SubTestResults']['VcalCalibrationModule']
            key = "VcalCalibration_{Method}_ROC{ROC}".format(Method=self.Attributes['Method'], ROC=roc)
            roc_results = vcal_calibration_module.ResultData['SubTestResults'][key].ResultData
            roc_offset = roc_results['KeyValueDictPairs']['Offset']['Value']
            roc_offset_error = roc_results['KeyValueDictPairs']['Offset']['Sigma']
            if self.verbose:
                print roc, roc_offset, roc_offset_error
            offsets.append(roc_offset)
            error_offsets.append(roc_offset_error)
        vcal_calibration = self.ParentObject.ResultData['SubTestResults']['VcalCalibrationSlope_'+self.method]
        vcal_calibration.SpecialPopulateData(self,offsets,error_offsets,{'Key':'Offset',
                'MarkerColor':ROOT.kPink,
                'LineColor':ROOT.kPink,
                'MarkerStyle':21,
                'YaxisTitle':'Offset [e- / Vcal]',
                'MinY':-2000,
                'MaxY':+2000,})

