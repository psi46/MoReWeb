# -*- coding: utf-8 -*-
import os


def fileExists(fileName):
        return os.path.isfile(fileName)

def get_factor_of_unit(unitstring, unit):
        if not unitstring.endswith(unit):
            warnings.warn('Cannot extract Unit prefix for unit %s in unitstring  %s' % (unit, unitstring))
            return 1
        unitprefix = unitstring[:-len(unit)]
        unitprefix = unitprefix.strip()
        if 'T' == unitprefix:
            return 1e12
        elif 'G' == unitprefix:
            return 1e9
        elif 'M' == unitprefix:
            return 1e6
        elif 'k' == unitprefix:
            return 1e3
        elif 'h' == unitprefix:
            return 1e2
        elif '' == unitprefix:
            return 1
        elif 'd' == unitprefix:
            return 1e-1
        elif 'c' == unitprefix:
            return 1e-2
        elif 'm' == unitprefix:
            return 1e-3
        elif 'mu' in unitprefix or 'μ' == unitprefix:
            return 1e-6
        elif 'n' == unitprefix:
            return 1e-9
        elif 'p' == unitprefix:
            return 1e-12
        elif 'f' == unitprefix:
            return 1e-15
        else:
            warnings.warn('Cannot extract Unit prefix for unit %s in unitstring  %s' % (unit, unitstring))
            return 1
        return 1