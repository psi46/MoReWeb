# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.BareModuleTest.Chips.Chip.BareBBMap.BareBBMap
class TestResult(TestResultClasses.CMSPixel.QualificationGroup.BareModuleTest.Chips.Chip.BareBBMap.BareBBMap.TestResult):
    def CustomInit(self):
        # Call Overridden CustomInit()
        super(TestResult, self).CustomInit()

        #self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BareBBMap_TestResult'
        #self.NameSingle='BareBBMap'
        #self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_BareModuleTest_ROC'
