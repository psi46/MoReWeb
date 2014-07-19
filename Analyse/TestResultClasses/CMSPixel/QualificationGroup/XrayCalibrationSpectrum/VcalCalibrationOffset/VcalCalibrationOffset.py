import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_VcalCalibrationOffset_TestResult"
        self.NameSingle = "VcalCalibrationOffset"
        self.Title = "Offset of Vcal Calibration"
        self.verbose = False
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.ResultData["SubTestResultDictList"] = []
        self.check_Test_Software()
        self.Attributes['TestedObjectType'] = 'VcalCalibrationOffset'

    def get_n_rocs(self):
        self.nRocs = 0
        for i in self.ParentObject.ResultData['SubTestResultDictList']:
            if i['Key'].startswith('FluorescenceSpectrumModule'):
                self.nRocs = i['TestResultObject'].ResultData['HiddenData']['nRocs']
                break


    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
        self.get_n_rocs()
        offsets = []
        error_offsets = []
        for roc in range(self.nRocs):
            vcal_calibration_module = self.ParentObject.ResultData['SubTestResults']['VcalCalibrationModule']
            roc_results = vcal_calibration_module.ResultData['SubTestResults'][
                'VcalCalibrationROC%i' % (roc)].ResultData
            roc_offset = roc_results['KeyValueDictPairs']['Offset']['Value']
            roc_offset_error = roc_results['KeyValueDictPairs']['Offset']['Sigma']
            if self.verbose:
                print roc, roc_offset, roc_offset_error
            offsets.append(roc_offset)
            error_offsets.append(roc_offset_error)
        for i in  self.ParentObject.ResultData['SubTestResultDictList']:
            print i
        vcal_calibration = self.ParentObject.ResultData['SubTestResults']['VcalCalibrationSlope']
        vcal_calibration.SpecialPopulateData(self,offsets,error_offsets,{'Key':'Offset',
                'MarkerColor':ROOT.kPink,
                'LineColor':ROOT.kPink,
                'MarkerStyle':21,
                'YaxisTitle':'Offset [e- / Vcal]',})

