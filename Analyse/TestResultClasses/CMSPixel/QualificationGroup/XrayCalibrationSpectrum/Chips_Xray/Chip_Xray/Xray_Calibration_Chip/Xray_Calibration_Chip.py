import AbstractClasses
import ROOT
import os
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_QualificationGroup_XrayCalibration_Chips_Chip_Calibration_TestResult"
        self.NameSingle = "XrayCalibrationChipResults"
        self.Title = "X-ray Calibration - Chip Results"
        self.chipNo = self.ParentObject.Attributes['ChipNo']