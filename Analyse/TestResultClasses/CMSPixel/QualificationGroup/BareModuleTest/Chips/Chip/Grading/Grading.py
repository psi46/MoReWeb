# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.Grading.Grading
class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.Grading.Grading.TestResult):
    def CustomInit(self):
    	# Call Overridden CustomInit()
    	super(TestResult, self).CustomInit()
    	
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_Grading_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = ''




