from flask import Flask, render_template, redirect, flash, request
import requests
import mysql.connector

app = Flask(__name__)


class DBRoutines:
# Resources
# https://www.webtrainingroom.com/python/python-mysql
# https://github.com/mysql/mysql-connector-python/tree/master/examples 
# https://stackoverflow.com/questions/27329953/python-using-mysql-connection-from-super-class

  def __init__(self):
    self.connect2db = mysql.connector.connect(host="127.0.0.1", user="admin", password="mysql", port="3306", database="mytexts")

  config = {
       'host': '127.0.0.1',
       'port': 3306,
       'database': 'my_texts',
       'user': 'admin',
       'password': 'mysql',
       'charset': 'utf8',
       'use_unicode': True,
       'get_warnings': True,
   }

#  def connect2db(self, config):
#    cnx = mysql.connector.connect(**config)
#    #cur = cnx.cursor()
#    return cnx

  def insertstaff(self, val1, val2, val3, val4):
    mycursor = self.connect2db.cursor()
    to_insert = ((val1, val2, val3, val4))
    stmt_insert = "INSERT INTO texts_table (text_language, thetext, source, comments) VALUES (%s, %s, %s, %s)"
    mycursor.execute(stmt_insert, to_insert)
    #mycursor.executemany(stmt_insert, to_insert)
    self.connect2db.commit()
    a = mycursor.close()
    return print(a)

def bring_ip():
  import socket
  host_ip = socket.gethostbyname(socket.gethostname())
  return host_ip    


@app.route('/', methods = ['POST', 'GET'])
def hello():
  host_ip = bring_ip()
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
