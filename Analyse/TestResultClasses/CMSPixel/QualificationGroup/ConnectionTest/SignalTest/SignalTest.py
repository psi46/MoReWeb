# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.OnShellQuickTest.SignalTest.SignalTest
class TestResult(TestResultClasses.CMSPixel.QualificationGroup.OnShellQuickTest.SignalTest.SignalTest.TestResult):
    def CustomInit(self):
        # Call Overridden CustomInit()
        super(TestResult, self).CustomInit()