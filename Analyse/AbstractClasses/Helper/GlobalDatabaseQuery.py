import os
import ConfigParser

try:
    import getpass
    import MySQLdb
except:
    pass

class GlobalDatabaseQuery():

    def __init__(self):
        self.User = None
        self.Host = None
        self.Password = None
        self.dbName = None
        self.DBMacroVersion = None
        self.db = None

        self.Configuration = ConfigParser.ConfigParser()
        self.Configuration.read(['Configuration/GlobalDatabase.cfg'])
        try:
            self.User = self.Configuration.get('GlobalDatabase', 'User')
            self.Host = self.Configuration.get('GlobalDatabase', 'Host')
            self.dbName = self.Configuration.get('GlobalDatabase', 'Database').strip()
            self.DBMacroVersion = self.Configuration.get('GlobalDatabase', 'MacroVersion').strip()
        except:
            print 'Configuration/GlobalDatabase.cfg does not contain all information needed: User, Host, Database, MacroVersion'

    def Connect(self):
        if self.db is None and self.Host is not None:

            try:
                Password = self.Configuration.get('GlobalDatabase', 'Password').strip()
            except:
                print("connecting %s@%s"%(self.User, self.Host))
                Password = getpass.getpass('MySQL password: ')
                print("...")

            try:
                print 'Connect to DB:'
                print ' host:', self.Host
                print ' user:', self.User
                print ' password:', '********' if Password else 'None'
                print ' database:', self.dbName
                self.db = MySQLdb.connect(host=self.Host, user=self.User, passwd=Password, db=self.dbName)
                if not os.path.isfile('db.auth'):
                    with open('db.auth', 'w') as PwFile:
                        PwFile.write('%s:%s'%(self.User, Password))
                print "-> connected."
            except:
                print "-> connection failed!"
                self.db = None
            Password = None

    def QuerySQL(self, SQLQuery, UseDict = True):

        if self.db is None:
            self.Connect()

        if self.db:
            if UseDict:
                cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            else:
                cursor = self.db.cursor()

            # execute SQL select statement
            print "\x1b[32mSQL:%s\x1b[0m"%SQLQuery
            cursor.execute(SQLQuery)

            # commit your changes
            self.db.commit()

            # get and display one row at a time.
            rows = cursor.fetchall()
        else:
            rows = None

        return rows

    def GetFulltestPixelDefects(self, ModuleID, tempnominal = 'p17_1'):

        SQLQuery = '''
SELECT inventory_fullmodule.FULLMODULE_ID, tempnominal, ROC_POS, Total, nDeadPixel, nDeadBumps
FROM inventory_fullmodule
INNER JOIN test_fullmodule ON inventory_fullmodule.LASTTEST_FULLMODULE=test_fullmodule.SUMMARY_ID
INNER JOIN test_fullmoduleanalysis ON test_fullmodule.TEST_ID=test_fullmoduleanalysis.FULLMODULETEST_ID
INNER JOIN test_performanceparameters ON test_performanceparameters.FULLMODULEANALYSISTEST_ID=test_fullmoduleanalysis.TEST_ID
WHERE inventory_fullmodule.FULLMODULE_ID = '{ModuleID}' AND tempnominal='{tempnominal}' AND test_fullmoduleanalysis.MACRO_VERSION = '{MacroVersion}' AND TYPE='FullQualification' AND STATUS='INSTOCK'
ORDER BY ROC_POS'''.format(MacroVersion=self.DBMacroVersion, tempnominal=tempnominal, ModuleID=ModuleID)
        return self.QuerySQL(SQLQuery)

    def GetFullQualificationResult(self, ModuleID):

        SQLQuery = '''
SELECT inventory_fullmodule.FULLMODULE_ID, GRADE, BAREMODULE_ID, HDI_ID, TBM_ID, BUILTON, BUILTBY, STATUS, tempnominal, I150, IVSLOPE, PIXELDEFECTS
FROM inventory_fullmodule
INNER JOIN test_fullmodule ON inventory_fullmodule.LASTTEST_FULLMODULE=test_fullmodule.SUMMARY_ID
INNER JOIN test_fullmoduleanalysis ON test_fullmodule.TEST_ID=test_fullmoduleanalysis.FULLMODULETEST_ID
WHERE inventory_fullmodule.FULLMODULE_ID = '{ModuleID}' AND test_fullmoduleanalysis.MACRO_VERSION = '{MacroVersion}' AND TYPE='FullQualification' AND STATUS='INSTOCK'
ORDER BY tempnominal ;'''.format(MacroVersion=self.DBMacroVersion, ModuleID=ModuleID)
        return self.QuerySQL(SQLQuery)

