import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_VcalCalibrationSlope_TestResult"
        self.NameSingle = "VcalCalibrationSlope"
        self.Title = "Slope of Vcal Calibration"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.ResultData["SubTestResultDictList"] = []
        self.check_Test_Software()
        #self.ModuleVersion, self.nRocs, self.halfModule
        #self.nRocs =
        # print   self.ParentObject.ResultData['SubTestResults']

                # , self.ParentObject.ResultData['SubTestResultDictList'][i]
        # ROCtype, nRocs, halfModule = self.ReadModuleVersion()
        # print ROCtype,nRocs,halfModule
        # self.nRocs = self.ParentObject.Attributes['NumberOfChips']
        # Get module information


        self.Attributes['TestedObjectType'] = 'VcalCalibrationSlope'

    def get_n_rocs(self):
        self.nRocs = 0
        for i in self.ParentObject.ResultData['SubTestResultDictList']:
            if i['Key'].startswith('FluorescenceSpectrumModule'):
                self.nRocs = i['TestResultObject'].ResultData['HiddenData']['nRocs']
                break
    def median(self,l):
        s = sorted(l)
        i = len(s)
        if not i%2:
            return (s[(i/2)-1]+s[i/2])/2.0
        return s[i/2]

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
        self.get_n_rocs()
        slopes = []
        for roc in range(self.nRocs):
            vcal_calibration_module = self.ParentObject.ResultData['SubTestResults']['VcalCalibrationModule']
            roc_results = vcal_calibration_module.ResultData['SubTestResults'][
                'VcalCalibrationROC%i' % (roc)].ResultData
            roc_slope = roc_results['KeyValueDictPairs']['Slope']['Value']
            roc_slope_error = roc_results['KeyValueDictPairs']['Slope']['Sigma']
            print roc, roc_slope, roc_slope_error
            slopes.append(roc_slope)
        print slopes,type(slopes)
        raw_input()

        self.SpecialPopulateData(self,slopes,{'Key':'Slope',
                'MarkerColor':ROOT.kPink,
                'LineColor':ROOT.kPink,
                'MarkerStyle':21,
                'YaxisTitle':'Slope [e- / Vcal]',})

    def SpecialPopulateData(self,TestResultObject, array, Parameters):
        print array,type(array)
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), '', TestResultObject.nRocs, 0,
                                                          TestResultObject.nRocs)
        for i in range(len(array)):
            TestResultObject.ResultData['Plot']['ROOTObject'].SetBinContent(i + 1, array[i])
        min_array = min(array)
        max_array= max(array)
        median_array = self.median(array)
        average_array = reduce(lambda x, y: x + y, array) / len(array)
        ymin = min_array
        ymax = max_array
        if ymin > 0:
            ymin *= .8
        else:
            ymin *= 1.2
        if ymax > 0:
            ymax *= 1.2
        else:
            ymax *= .8

        TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerColor(Parameters['MarkerColor'])
        TestResultObject.ResultData['Plot']['ROOTObject'].SetLineColor(Parameters['LineColor'])

        TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerStyle(Parameters['MarkerStyle'])
        TestResultObject.ResultData['Plot']['ROOTObject'].SetMarkerSize(0.5)
        TestResultObject.ResultData['Plot']['ROOTObject'].SetTitle("")
        TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(ymin, ymax)
        TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC No.")
        TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle(Parameters['YaxisTitle'])
        TestResultObject.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
        TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
        TestResultObject.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
        TestResultObject.ResultData['Plot']['ROOTObject'].Draw('LP')
        Line = ROOT.TLine()
        lineB = Line.DrawLine(0, average_array, TestResultObject.nRocs, average_array)
        lineB.SetLineWidth(2);
        lineB.SetLineStyle(2)
        lineB.SetLineColor(ROOT.kRed)

        TestResultObject.ResultData['KeyValueDictPairs'] = {
            'avrg%s'%Parameters['Key'] : {
                "Value" : average_array,
                "Sigma" : 0,
                "Label" : 'avrg %s'%Parameters['Key'],
                "Unit" : "",
            },
            'min%s'%Parameters['Key'] : {
                "Value" : min_array,
                "Sigma" : 0,
                "Label" : 'min %s'%Parameters['Key'],
                "Unit" : "",
            },
            'max%s'%Parameters['Key'] : {
                "Value" : max_array,
                "Sigma" : 0,
                "Label" : 'max %s'%Parameters['Key'],
                "Unit" : "",
            },
            'median%s'%Parameters['Key'] : {
                "Value" : median_array,
                "Sigma" : 0,
                "Label" : 'median %s'%Parameters['Key'],
                "Unit" : "",
            }
        }
        TestResultObject.ResultData['KeyList'].append( 'avrg%s'%Parameters['Key'])
        TestResultObject.ResultData['KeyList'].append('median%s'%Parameters['Key'])
        TestResultObject.ResultData['KeyList'].append('min%s'%Parameters['Key'])
        TestResultObject.ResultData['KeyList'].append('max%s'%Parameters['Key'])

        TestResultObject.Canvas.SaveAs(TestResultObject.GetPlotFileName())
        TestResultObject.ResultData['Plot']['Enabled'] = 1
        TestResultObject.ResultData['Plot']['Caption'] = Parameters['Key']
        TestResultObject.ResultData['Plot']['ImageFile'] = TestResultObject.GetPlotFileName()
        #self.ResultData['Table'] = {
        #    'HEADER':[
        #        [
        #            'ROC', 'Vcal'
        #        ]
        #    ],
        #    'BODY':[],
        #    'FOOTER':[],
        #}

