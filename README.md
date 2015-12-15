News
=======

Dec 15, 2015:

- new improved BB2 cuts merged into master branch, thanks @andreavargas
- development branch v0.7 which contains: new checks for bad double columns, FQ analysis speed up, more Readback test analysis, support for single test analysis and some improved plots -> will be merged into master branch in January 2016


Info
=======

see the full changelog at:
http://cmspixel.phys.ethz.ch/MoRe-Web/MoReWeb.html

##### version 0.6.7

**IV grading**

Also grade on measured value of leakage current at -20 degrees (with the same criteria than at +17). This will affect grading of modules that have both a higher leakage current at -20 than at +17 and a leakage current at -20 larger than 10 uA. (Not seen any so far, but one module would almost fulfil these criteria)

##### version 0.6.6

**manual grading possible**

how to: add a file grade.txt inside the 00\*\_Fulltest\_\* subfolder which contains the grade as letter (A,B,C) or number (1,2,3). (To add a comment: add a file called comment.txt to the main qualification directory, e.g. M\*\_FullQualification\_...)

...

##### version 0.6.4

**new grading for IV curves!**

All FullQualifications should be re-analyzed with the new version! Re-fitting is not necessary if it has been done already with version v0.6.3.

...

##### version 0.6.0
Grading adjustments and bugfixes.
All test should be re-analyzed (incl. re-fitting) with the new version with:

    ./Controller.py -r -f
    
to create the production overview page, run

    ./Controller.py -p
    
##### Please test this feature and report any bugs or other feedback!




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
