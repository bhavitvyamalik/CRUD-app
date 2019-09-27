from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         phone = request.form['phone']
         
         with sql.connect("dbtest1.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO students (name,addr,city,phone) VALUES (?,?,?,?);",(nm,addr,city,phone))
            print('hello')            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
      	return render_template("result.html",msg = msg)
      	con.close()

@app.route('/list')
def list():
   con = sql.connect("dbtest1.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

@app.route('/update')
def update_func():
   return render_template('update.html')

@app.route('/update1',methods = ['POST', 'GET'])
def update1():
   if request.method == 'POST':
      
      nm = request.form['nm']
      addr = request.form['add']
      city = request.form['city']
      phone = request.form['phone']
      print(phone)
      
      with sql.connect("dbtest1.db") as con:
         cur = con.cursor()
         
         cur.execute("DELETE from students where phone='{}';".format(phone) )           
         cur.execute("INSERT INTO students (name,addr,city,phone) VALUES (?,?,?,?);",(nm,addr,city,phone))            
         con.commit()
         msg = "Record successfully updated"
   
      
      
      return render_template("result.html",msg = msg)
      con.close()

@app.route('/delete')
def delete_func():
   return render_template('delete.html')


@app.route('/deleteFUNCTION', methods = ['POST'])
def deleteFUNCTION():
   if request.method == 'POST': 
      phone = request.form['phone']
      with sql.connect("dbtest1.db") as con:
         cur = con.cursor()

      cur.execute("DELETE from students where phone='{}';".format(phone) )           
      con.commit()

   rows = cur.fetchall();
   return render_template("list.html",rows = rows)


if __name__ == '__main__':
   app.run(debug = True)