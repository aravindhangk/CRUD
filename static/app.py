from flask import Flask,render_template,url_for,redirect,request
from flask_mysqldb import MySQL
app=Flask(__name__)

#MySQL connection

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="root"
app.config["MYSQL_DB"]="crud"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

#Loading Home Page

@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * from users"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)
    
 #New User
@app.route("/addUser",methods=['GET','POST'])
def addUser():
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        con=mysql.connection.cursor()
        sql="insert into users(NAME,CITY,AGE) value (%s,%s,%s)"
        con.execute(sql,[name,city,age])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))   
    return render_template("addUser.html")
#update User
@app.route("/editUser/<string:id>", methods=['GET','POST'])
def editUser(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        sql="update users set NAME=%s, CITY=%s,AGE=%s where ID=%s"
        con.execute(sql,[name,city,age,id])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
        con=mysql.connection.cursor()
    sql="select * from users where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("editUser.html",datas=res)
#Delete User
@app.route("/deleteUser/<string:id>",methods=['GET','POST'])
def deleteUser(id):
    con=mysql.connection.cursor()
    sql="delete from users where ID=%s"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for("home"))

if(__name__=='__main__'):
    app.run(host="172.16.100.160", port=8000, debug=True)