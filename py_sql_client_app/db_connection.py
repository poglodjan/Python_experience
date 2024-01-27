import configparser
import pymssql
import psycopg2
from psycopg2 import Error

# configuracja bazy danych
cnf = configparser.ConfigParser()
cnf.read("cnf.ini")

cnx_mssql = pymssql.connect(user = cnf['mssqlDB']['user'],
                            password = cnf['mssqlDB']['pass'],
                            server = cnf['mssqlDB']['server'],
                            database=cnf['mssqlDB']['db'])


