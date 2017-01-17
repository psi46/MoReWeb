#!/usr/bin/env python
import os
import getpass
import urllib


# requirements
#
# 1) MySQLdb python module: e.g. install with with the command: 'pip install MySQL-python'
# 2) DB password


# how to run
#
# 1) ./IVcurves_download.py
# 2) ./IVcurves_plot.py


try:
    import MySQLdb
except:
    print "\x1b[31merror: can't load Python module 'MySQLdb' \x1b[0m"
    print "\x1b[31m -> run: pip install MySQL-python\x1b[0m"

sqlQueryMountedModule = '''
SELECT inventory_fullmodule.FULLMODULE_ID, MOUNT_POSITION, GRADE, inventory_fullmodule.BUILTON, inventory_fullmodule.BUILTBY, inventory_fullmodule.STATUS, tempnominal, I150, IVSLOPE, PFNs
FROM inventory_fullmodule
    INNER JOIN test_fullmodule ON inventory_fullmodule.LASTTEST_FULLMODULE=test_fullmodule.SUMMARY_ID
    INNER JOIN test_fullmoduleanalysis ON test_fullmodule.LASTANALYSIS_ID=test_fullmoduleanalysis.TEST_ID
    INNER JOIN test_data ON test_data.DATA_ID = test_fullmoduleanalysis.DATA_ID
WHERE inventory_fullmodule.STATUS = 'MOUNTED';
'''

databaseHostAddress = 'cmspixelprod.pi.infn.it'
Password = getpass.getpass('MySQL password: ')
db = MySQLdb.connect(host='cmspixelprod.pi.infn.it', user='reader', passwd=Password, db='prod_pixel') 
if not db:
    print "connection failed!"
    exit(2)

cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
cursor.execute(sqlQueryMountedModule)
db.commit()
rows = cursor.fetchall()

print rows

try:
    os.mkdir('ivcurves')
except:
    pass

for row in rows:
    localPath = 'ivcurves/' + row['MOUNT_POSITION'] + '_' + row['tempnominal'] + '.root'
    if not os.path.isfile(localPath):
        print "downloading ",localPath, "..."
        remotePath = 'http://' + databaseHostAddress + '/' + row['PFNs'].split(':')[1] + '/IVCurve/IVCurve.root'

        try:
            a=urllib.urlopen(remotePath)
            if a.getcode() != 200:
                raise Exception("404 - not found.")

            urllib.urlretrieve(remotePath, localPath)
        except:
            print "\x1b[31mdownload failed!\x1b[0m"




