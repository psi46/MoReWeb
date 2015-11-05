# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.ReadbackCal.ReadbackCal

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.ReadbackCal.ReadbackCal.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()