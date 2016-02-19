# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PixelMap.PixelMap

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PixelMap.PixelMap.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()
        self.verbose = False