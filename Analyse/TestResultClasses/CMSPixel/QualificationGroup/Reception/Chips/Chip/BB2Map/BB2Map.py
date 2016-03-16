# -*- coding: utf-8 -*-
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.BareModuleTest.Chips.Chip.BareBBMap.BareBBMap

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.BareModuleTest.Chips.Chip.BareBBMap.BareBBMap.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()

    def PopulateResultData(self):
        try:
            super(TestResult, self).PopulateResultData()
        except:
            self.DisplayOptions['Show'] = False
