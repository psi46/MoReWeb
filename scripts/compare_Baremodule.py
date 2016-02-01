#!/usr/bin/env python
import MySQLdb
import getpass
import pickle
import ast
import time
import datetime

def QueryData():

    User = 'reader'
    Host = 'cmspixelprod.pi.infn.it'
    OutputFileName = 'compare_baremodule.dat'

    Temperature = 'p17_1'
    Center = 'PSI'

    # show only first 10 modules
    Limit = 16 * 10

    SQL = '''
    SELECT inventory_fullmodule.FULLMODULE_ID, test_fullmodule.TIMESTAMP, inventory_fullmodule.BAREMODULE_ID, inventory_fullmodule.BUILTBY, inventory_fullmodule.STATUS, BUMPDEFPIXELS, ROC_POS, nDeadBumps, roc_id, FAILURES, TOTAL_FAILURES, test_data.PFNs
      FROM inventory_fullmodule
      INNER JOIN test_fullmodule ON inventory_fullmodule.LASTTEST_FULLMODULE=test_fullmodule.SUMMARY_ID
      INNER JOIN test_fullmoduleanalysis ON test_fullmodule.LASTANALYSIS_ID=test_fullmoduleanalysis.TEST_ID
      INNER JOIN test_performanceparameters ON test_performanceparameters.FULLMODULEANALYSISTEST_ID=test_fullmoduleanalysis.TEST_ID
      INNER JOIN inventory_baremodule ON inventory_fullmodule.BAREMODULE_ID = inventory_baremodule.BAREMODULE_ID
      INNER JOIN test_baremodule_qa ON inventory_baremodule.LASTTEST_BAREMODULE_QA_BONDING=test_baremodule_qa.TEST_ID
      INNER JOIN test_data ON test_baremodule_qa.DATA_ID=test_data.DATA_ID
      WHERE test_fullmodule.TYPE='FullQualification' AND tempnominal='{Temperature}' AND inventory_fullmodule.STATUS='INSTOCK' AND inventory_fullmodule.BUILTBY='{Center}'
      ORDER BY BUILTBY, inventory_fullmodule.FULLMODULE_ID, tempnominal, ROC_POS
      LIMIT {Limit};
    '''.format(Temperature=Temperature, Center=Center, Limit=Limit)

    try:
        with open('db.auth') as PwFile:
            for line in PwFile:
                LineUser = line.split(':')[0].strip()
                LinePassword = line.split(':')[1].strip()
                if LineUser == User:
                    Password = LinePassword
                    break
    except:
        print("connecting %s@%s"%(User,Host))
        Password = getpass.getpass('MySQL password')

    db = MySQLdb.connect(host=Host, user=User, passwd=Password, db="prod_pixel")
    cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    # execute SQL select statement
    print "\x1b[32mSQL:%s\x1b[0m"%SQL
    cursor.execute(SQL)

    # commit your changes
    db.commit()

    # get the number of rows in the resultset
    numrows = int(cursor.rowcount)
    print "-> #rows = %d"%numrows

    # get and display one row at a time.
    rows = cursor.fetchall()
    with open(OutputFileName, 'wb') as OutputFile:
        print("write data to '%s'"%OutputFileName)
        pickle.dump(rows, OutputFile)

    return rows


def FormatRows(rows):
    FormattedRows = []

    for row in rows:
        ROC = int(row['ROC_POS'])

        FailuresList = ast.literal_eval(row['FAILURES'])
        ROCName = 'ROC%d'%ROC
        if ROCName in FailuresList:
            BaremoduleDefectsROC = len(FailuresList[ROCName])
        else:
            BaremoduleDefectsROC = 0

        FulltestDate = datetime.datetime.fromtimestamp(int(row['TIMESTAMP']))
        BaremoduleDateItems = [int(x) for x in row['PFNs'].split('/')[-1].split('_')[0].split('-')[-3:]]
        BaremoduleDate = datetime.datetime(
            year=BaremoduleDateItems[0],
            month=BaremoduleDateItems[1],
            day=BaremoduleDateItems[2]
        )

        DateDifference = FulltestDate-BaremoduleDate

        FormattedRow = {
            'ModuleID': row['FULLMODULE_ID'],
            'FulltestTimestamp': row['TIMESTAMP'],
            'FulltestDefectsTotal': row['BUMPDEFPIXELS'],
            'ROC': ROC,
            'FulltestDefectsROC': row['nDeadBumps'],
            'BaremoduleDefectsTotal': row['TOTAL_FAILURES'],
            'BaremoduleDefectsROC': BaremoduleDefectsROC,
            'BaremoduleDate': BaremoduleDate.strftime('%Y-%m-%d'),
            'FulltestDate': FulltestDate.strftime('%Y-%m-%d'),
            'DateDelta': DateDifference.days,
        }

        FormattedRows.append(FormattedRow)

    return FormattedRows


Rows = FormatRows(QueryData())
print "\x1b[31m{MODULE:>8}{ROC:>8}{BMD:>12}{FTD:>12}{DELTA:>6}{BM:>8}{FT:>8}\x1b[0m".format(
    MODULE='MODULE',
    ROC='ROC',
    BMD='BM_DATE',
    FTD='FT_DATE',
    DELTA='DAYS',
    BM='BM_DEF',
    FT='FT_DEF',
)

for Row in Rows:
    print "{MODULE:>8}{ROC:>8}{BMD:>12}{FTD:>12}{DELTA:>6}{BM:>8}{FT:>8}".format(
        MODULE=Row['ModuleID'],
        ROC=Row['ROC'],
        BMD=Row['BaremoduleDate'],
        FTD=Row['FulltestDate'],
        DELTA=Row['DateDelta'],
        BM=Row['BaremoduleDefectsROC'],
        FT=Row['FulltestDefectsROC'],
    )
