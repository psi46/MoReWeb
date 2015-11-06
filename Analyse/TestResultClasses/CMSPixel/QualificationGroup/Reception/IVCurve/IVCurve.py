# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.IVCurve.IVCurve

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.IVCurve.IVCurve.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()