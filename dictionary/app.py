from flask import Flask, render_template, redirect, flash, request
import requests 
import mysql.connector
import os, logging

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

    self.connect2db = mysql.connector.connect(host = mysqlhost, user = mysqluser, password = mysqlpassword, port = mysqlport, database = mysqldatabase)

#    self.connect2db = mysql.connector.connect(host=os.environ['MYSQL_HOST'], user=os.environ['MYSQL_USER'],password=os.environ['MYSQL_PASSWORD'], port=['MYSQL_PORT'], database=os.environ['MYSQL_DB'])

  def insertstaff(self, val1, val2, val3, val4):
    mycursor = self.connect2db.cursor()
    to_insert = ((val1, val2, val3, val4))
    stmt_insert = "INSERT INTO texts_table (text_language, thetext, source, comments) VALUES (%s, %s, %s, %s)"
    mycursor.execute(stmt_insert, to_insert)
    #mycursor.executemany(stmt_insert, to_insert)
    self.connect2db.commit()
    a = mycursor.close()
    return print(a)

class AppLogging:
  def __init__(self):
    logging.getLogger(__name__).addHandler(logging.NullHandler())
#    self.name = name

  def InfoLog(self, message):
    logging.basicConfig( level=logging.DEBUG, filename='example.log')
    
#    logging.basicConfig( level=logging.INFO, filename='example.log')
    
    pass
    
infologging = AppLogging()

def bring_ip():
  import socket
  host_ip = socket.gethostbyname(socket.gethostname())
  return host_ip    


@app.route('/', methods = ['POST', 'GET'])
def hello():
  host_ip = bring_ip()
  infologging.InfoLog(host_ip)
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
  return render_template('list-words.html', out1=val1, out2=val2, out3=val3, out4=val4)

@app.route('/print_texts', methods = ['POST', 'GET'])
def print_texts():
#  host_ip = bring_ip()
  return render_template('print-texts.html')


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port='8090')
