# -*- coding: utf-8 -*-
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.BareModuleTest.Chips.Chip.BareBBScan.BareBBScan

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.BareModuleTest.Chips.Chip.BareBBScan.BareBBScan.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()

    def PopulateResultData(self):
        try:
            super(TestResult, self).PopulateResultData()
        except:
            self.DisplayOptions['Show'] = False