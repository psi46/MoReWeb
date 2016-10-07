Info
=======

##### version 1.1.0

L1 HR tests: supports analysis of workaround tests of: XPixelAlive, HRScurves, CaldelScan
new test: OnShellQuickTest for modules mounted on half shell, including table of modules on detector
add scripts/decode.py to decode the raw events printed out py pXar logfiles
add scripts/merge_rootfiles.py to combine several pXar rootfiles into one single file

##### version 1.0.4

fix for filling DAC parameters created with recent pxar version into global DB

##### version 1.0.2

fix for Reception tests for global DB

##### version 1.0.1 (DB re-processing with final grading)

few changes for reception tests

##### version 1.0.0

Same grading as in 0.7.3 version, but some small bugs fixed and some changes for global DB

##### version 0.7.3

New bump bonding cut for standard pxar bump bonding test (BB) which can more reliably detect missing bumps if there are >90 per ROC.

##### version 0.7.2

New grading for double column defects (>1% inefficienct pixels per double column => C). Bugfixes for handling incomplete data and "fake test structures" to insert them into the DB.
Improvements for Reception tests analysis, overview page and presentation.


Requirements
=======

    Python 2.6 (2.7 recommended)
    ROOT 5.34.19+ or ROOT 6
    recent Web browser (min Firefox 4, Chrome 18, Safari 3, Opera 9, IE 10)
    optional: MySQLdb python module

MoReWeb
=======
MoReWeb is a software framework to analyze Module / ROC test data acquired using psi46expert or pXar. It can be used to analyse results locally, but it is also the software run on server side of the central BPix DB at Pisa. This software was developed and is currently maintained by ETH Zurich.
It can analyse the output of the following readout softwares:
* pXar
* Pyxar
* PSI46expert

You can find further information on the Twiki Page
https://twiki.cern.ch/twiki/bin/viewauth/CMS/MoReWeb


## Contributors
* Felix Bachmair @veloxid
* Esteban Marín @macjohnny
* Philipp Eller @philippeller
* Vittorio Tavolaro @vtavolar
* Andrea Rizzi @arizzi
* Tommaso Boccali @tommasoboccali
* Andrea Vargas Trevino @andreavargas
* Martin Lipinski  @martinlip
* Pirmin Berger @piberger
