

import pymysql
import logging, logging.config
import subprocess

class DBUtility(object):
    log = logging.getLogger("DBUtility")
    
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
    
    def getDBConn(self):
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password)
        return conn
        
    def getQueryResult(self, sql):
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug('execQuery: %s', sql)
        try:
            conn = self.getDBConn()
#             if conn.isconnected() == True:
            cursor = conn.cursor()
            cursor.execute(sql)
            ret = cursor.fetchall()
            return ret
        except Exception as ex:
            errMsg = "run %s exception %s" % (sql, ex)
            self.log.error(errMsg)
        finally:
            cursor.close()
            conn.close()
            
    def execQuery(self, sql):
        if self.log.isEnabledFor(logging.DEBUG):
            self.log.debug('execQuery: %s', sql)
        try:
            conn = self.getDBConn()
            cursor = conn.cursor()
            ret = cursor.execute(sql)
            conn.commit()
            return ret
        except Exception as ex:
            errMsg = "run %s exception %s" % (sql, ex)
            self.log.error(errMsg)
        finally:
            cursor.close()
            conn.close()