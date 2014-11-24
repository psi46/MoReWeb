# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PHCalibrationTan.PHCalibrationTan
class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PHCalibrationTan.PHCalibrationTan.TestResult):
    
    def CustomInit(self):
    	# Call Overridden CustomInit()
    	super(TestResult, self).CustomInit()
    	
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PHCalibrationTan_TestResult'
        self.NameSingle = 'PHCalibrationTan'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
