# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.IanaLoss.IanaLoss

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.IanaLoss.IanaLoss.TestResult):
    def CustomInit(self):
        super(TestResult, self).CustomInit()