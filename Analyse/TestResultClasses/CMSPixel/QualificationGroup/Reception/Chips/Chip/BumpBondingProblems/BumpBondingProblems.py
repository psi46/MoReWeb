# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBondingProblems.BumpBondingProblems

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBondingProblems.BumpBondingProblems.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()

    def PopulateResultData(self):
        try:
            super(TestResult, self).PopulateResultData()
        except:
            print "No standard BumpBonding test found!"