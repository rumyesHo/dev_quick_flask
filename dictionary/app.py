from flask import Flask, render_template, redirect, flash, request
import requests 
import mysql.connector
import os, logging, sys, datetime

app = Flask(__name__)


class DBRoutines:
# Resources
# https://www.webtrainingroom.com/python/python-mysql
# https://github.com/mysql/mysql-connector-python/tree/master/examples 
# https://stackoverflow.com/questions/27329953/python-using-mysql-connection-from-super-class

  def __init__(self):
    mysqlhost = os.environ['MYSQL_HOST'] 
    mysqluser = os.environ['MYSQL_USER'] 
    mysqlpassword = os.environ['MYSQL_PASSWORD'] 
    mysqlport = os.environ['MYSQL_PORT'] 
    mysqldatabase = os.environ['MYSQL_DB']
    pass

    self.connect2db = mysql.connector.connect(host = mysqlhost, user = mysqluser, password = mysqlpassword, port = mysqlport, database = mysqldatabase)

  def dbconnector(): # under configuration. currently out of use
    mysqlhost = os.environ['MYSQL_HOST']
    mysqluser = os.environ['MYSQL_USER']
    mysqlpassword = os.environ['MYSQL_PASSWORD']
    mysqlport = os.environ['MYSQL_PORT']
    mysqldatabase = os.environ['MYSQL_DB']

    mysql.connector.connect(host = mysqlhost, user = mysqluser, password = mysqlpassword, port = mysqlport, database = mysqldatabase)

 
  def checkEnvTable():
    logger = AppLogging()
    try:
      mysqlhost = os.environ['MYSQL_HOST']
      mysqluser = os.environ['MYSQL_USER']
      mysqlpassword = os.environ['MYSQL_PASSWORD']
      mysqlport = os.environ['MYSQL_PORT']
      mysqldatabase = os.environ['MYSQL_DB']
    except Exception as e:
      message = ("Please, check environment variables, for example:  ")
      logger.debug_logger_test(message)
      print("FUCK")
      sys.exit(1)
        
  def insertstaff(self, val1, val2, val3, val4):
    to_insert = ((val1, val2, val3, val4))
    stmt_insert = "INSERT INTO texts_table (text_language, thetext, source, comments) VALUES (%s, %s, %s, %s)"
    try:
      mycursor = self.connect2db.cursor()
      mycursor.execute(stmt_insert, to_insert)
      #mycursor.executemany(stmt_insert, to_insert)
      self.connect2db.commit()
      a = mycursor.close()
    except mysql.connector.Error as err:
      AppLogging.infologging.debug_logger('Connection is fucked up: ' + err)
    return a

class AppLogging:
  def __init__(self):
    logger = logging.getLogger(__name__)

  def debug_logger(self, message):
    logger = logging.getLogger()
    handler = logging.FileHandler('logfile.info')
    #handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

  def debug_logger_test(self, message):
    logging.basicConfig(filename='logfile.info', level=logging.DEBUG)
    logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logging.info(message)
    logging.warning(message)

  def warning_logger(self, messsage):
    logger = logging.getLogger()
    handler = logging.FileHandler('logfile.info')
    #handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.ERROR)
    
infologging = AppLogging()

def bring_ip():
  import socket
  host_ip = socket.gethostbyname(socket.gethostname())
  return host_ip    

@app.route('/', methods = ['POST', 'GET'])
def hello():
  host_ip = bring_ip()
  infologging.debug_logger(host_ip)
  return render_template('hello.html')

@app.route('/save_text', methods = ['POST', 'GET'])
def save_new_page():
  host_ip = bring_ip()
  return render_template('new-save.html')

@app.route('/save_it_post',methods = ['POST', 'GET'])
def save_it():
  val1 = request.form['language']
  val2 = request.form['thetext']
  val3 = request.form['source']
  val4 = request.form['comments']
  db_ref = DBRoutines()
  db_ref.insertstaff(val1, val2, val3, val4)
  cur_time = datetime.datetime.now()
  return render_template('list-words.html', out1=val1, out2=val2, out3=val3, servertime=cur_time)

@app.route('/print_texts', methods = ['POST', 'GET'])
def print_texts():
#  host_ip = bring_ip()
  return render_template('print-texts.html')


if __name__ == '__main__':
#  DBRoutines.checkEnvTable()
  app.run(debug=True, host='0.0.0.0', port='8090')
