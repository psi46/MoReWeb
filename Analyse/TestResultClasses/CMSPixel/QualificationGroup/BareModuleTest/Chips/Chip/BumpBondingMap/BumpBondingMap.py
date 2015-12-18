# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBondingMap.BumpBondingMap
class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBondingMap.BumpBondingMap.TestResult):
    def CustomInit(self):
    	# Call Overridden CustomInit()
    	super(TestResult, self).CustomInit()
    	
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BumpBondingMap_TestResult'
        self.NameSingle='BumpBondingMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
