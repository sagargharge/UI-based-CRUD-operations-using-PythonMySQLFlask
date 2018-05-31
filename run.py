from flask import Flask, render_template,request,redirect,url_for,jsonify
import pymysql
import json
import collections


conn=pymysql.connect(host="localhost",user="root",password="password",db="employee")
c=conn.cursor()

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/Login')
def login():
	return render_template("login.html")

@app.route('/About')
def about():
	return render_template("about.html")

@app.route('/createForm')
def createform():
	c.execute("CREATE TABLE IF NOT EXISTS emp1 (id int PRIMARY KEY AUTO_INCREMENT, fname  char(20) NOT NULL, lname  char(20), email varchar(40), age int, gender char(1), salary float, UNIQUE (email) )")
	return render_template('insert.html')

@app.route('/insert',methods=['POST','GET'])
def insert():
	if request.method=='POST':
		fname=request.form['f_name']
		lname=request.form['l_name']
		email=request.form['email']
		age=request.form['ag']
		gender=request.form['gndr']
		salary=request.form['sal']
		c.execute("""INSERT into emp1(fname,lname,email,age,gender,salary) VALUES (%s,%s,%s,%s,%s,%s)""",(fname,lname,email,age,gender,salary))
		conn.commit()
	return redirect(url_for('disp',name=fname))

@app.route('/disp/<name>')
def disp(name):
	return render_template("link.html",name =name)

@app.route('/listForm')
def select():
	c.execute("SELECT * from emp1")
	data=c.fetchall()
	return render_template('show.html', data = data)

@app.route('/updateForm')
def update():
	return render_template('update_id.html')

@app.route('/updateid',methods=['POST','GET'])
def update_details():
	if request.method=='POST':
		update_data=request.form['upid']
		query="SELECT id,fname,lname,email,age,gender,salary from emp1 WHERE id=%s"
		param=update_data
		c.execute(query,param)
		data1=c.fetchall()
	return render_template('show_update.html',data1=data1)

@app.route('/update_det', methods=['POST','GET'])
def details_update():
	if request.method=='POST':
		i=request.form['i_d']
		fn=request.form['f_n']
		ln=request.form['l_n']
		em=request.form['eml']
		ag=request.form['age']
		gen=request.form['gdr']
		sal=request.form['sl']
		query="UPDATE emp1 set fname=%s,lname=%s,email=%s,age=%s,gender=%s,salary=%s where id=%s"
		par=(fn,ln,em,ag,gen,sal,i)
		c.execute(query,par)
		conn.commit()

	return render_template('link1.html',name=fn)

@app.route('/deleteForm')
def show_delete():
	return render_template("delete_id.html")

@app.route('/deleteid',methods=['POST','GET'])
def delete_data():
	if request.method=='POST':
		delete1=request.form['upid']
		qry="DELETE from emp1 where id=%s"
		c.execute(qry,delete1)
		conn.commit()
	return render_template("link2.html",id=delete1)

@app.route('/listjsonForm')
def temp():
	c.execute("""
				SELECT id,fname,lname,email,age,gender,salary
				FROM emp1
			""")
	rows= c.fetchall()

	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['Employee_ID'] = row[0]
		d['First_Name'] = row[1]
		d['Last_Name'] = row[2]
		d['E-mail'] = row[3]
		d['Age'] = row[4]
		d['Gender'] = row[5]
		d['Salary'] = row[6]
		objects_list.append(d)
		j = json.dumps(objects_list)
	return render_template("show_json.html",d=j)


app.run()
