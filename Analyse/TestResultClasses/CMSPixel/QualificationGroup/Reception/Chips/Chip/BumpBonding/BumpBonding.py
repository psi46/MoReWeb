# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBonding.BumpBonding

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBonding.BumpBonding.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()

    def PopulateResultData(self):
        try:
            super(TestResult, self).PopulateResultData()
        except:
            print "No standard BumpBonding test found!"