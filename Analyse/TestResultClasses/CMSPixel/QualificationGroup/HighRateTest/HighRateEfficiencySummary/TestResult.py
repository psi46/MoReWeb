import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRateEfficiencySummary_TestResult"
        self.NameSingle = "HighRateEfficiencySummary"
        self.Title = "Pixel Efficiency Summary"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRateEfficiencySummary'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        # Get the parent object that contains all efficiency tests as sub tests
        hrtest = self.ParentObject

        # Get all the efficiency tests
        efficiency_tests = []
        for test in hrtest.ResultData['SubTestResults']:
            if "_Efficiency_" in test:
                efficiency_tests.append(hrtest.ResultData['SubTestResults'][test])

        # Sort the tests by x-ray temperature, voltage, and current
        # Extremely primitive sorting algorithm
        for i in range(len(efficiency_tests)):
            ta = efficiency_tests[i].Attributes['TestTemperature']
            va = efficiency_tests[i].Attributes['XrayVoltage']
            ia = efficiency_tests[i].Attributes['XrayCurrent']
            for j in range(i, len(efficiency_tests)):
                tb = efficiency_tests[j].Attributes['TestTemperature']
                vb = efficiency_tests[j].Attributes['XrayVoltage']
                ib = efficiency_tests[j].Attributes['XrayCurrent']
                if tb < ta or (tb == ta and vb < va) or (tb == ta and vb == va and ib < ia):
                    # Exchange the two
                    tmp = efficiency_tests[j]
                    efficiency_tests[j] = efficiency_tests[i]
                    efficiency_tests[i] = tmp

        # Get the keys for the table from the 'Chips' TestResult table in the efficiency test
        keys = efficiency_tests[0].ResultData['SubTestResults']['Chips'].ResultData['Table']['HEADER'][0]

        # Create the output table
        self.ResultData['Table'] = {
            'HEADER':[
                [
                    'Test',
                    'Temperature',
                    'X-ray voltage',
                    'X-ray current',
                ]
            ],
            'BODY':[],
            'FOOTER':[],
        }

        # Add the keys from the 'Chips' TestResult table to the header
        self.ResultData['Table']['HEADER'][0].extend(keys[1:])

        # Add the values from each efficiency test
        for test in efficiency_tests:
            line = []

            # Add link to the overview page of the efficiency
            line.append('Pixel Efficiency') # FIXME: should be a link <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

            # Add the Temperature, Voltage, and Current values
            line.append(str(test.Attributes['TestTemperature']) + " C")
            line.append(str(test.Attributes['XrayVoltage']) + " kV")
            line.append(str(test.Attributes['XrayCurrent']) + " mA")

            # Add the values from the 'Total' footer in the 'Chips' TestResult table
            items = test.ResultData['SubTestResults']['Chips'].ResultData['Table']['FOOTER'][0]
            line.extend(items[1:])

            # Add the line to the result table
            self.ResultData['Table']['BODY'].append(line)
