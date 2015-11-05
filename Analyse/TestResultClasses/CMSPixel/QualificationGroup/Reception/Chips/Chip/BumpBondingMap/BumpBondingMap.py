# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBondingMap.BumpBondingMap

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBondingMap.BumpBondingMap.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()