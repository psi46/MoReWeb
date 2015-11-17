# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.ReadbackParameter.ReadbackParameter

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.ReadbackParameter.ReadbackParameter.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()