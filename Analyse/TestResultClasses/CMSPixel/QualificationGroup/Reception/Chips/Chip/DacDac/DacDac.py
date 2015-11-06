# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.DacDac.DacDac

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.DacDac.DacDac.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()