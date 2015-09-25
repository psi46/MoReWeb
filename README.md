Info
=======

see the full changelog at:
http://cmspixel.phys.ethz.ch/MoRe-Web/MoReWeb.html

##### version 0.6.3

HR tests DB upload and Fulltest analysis fixes for special cases

##### version 0.6.2

reduce size of FinalResults folders by changing some chip maps from SVG to PNG.

##### version 0.6.1

includes now BB2 test, takes number of triggers for PixelAlive from testParameters.dat if available and few small fixes for displayed values. Grading is not affected (unless BB2 is used, then bump defects are taken from BB2 now!).

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
