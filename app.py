from flask import Flask, render_template, request, redirect,url_for, flash
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = "admin_123"

@app.route("/")
def home():
    conn = sql.connect("user.db")
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("select * from student")
    data = cur.fetchall()
    return render_template("index.html",datas=data)

@app.route("/add_user",methods=['POST','GET'])
def add_user():
    if request.method == "POST":
        s_name = request.form["name"]
        s_age = request.form["age"]
        s_language = request.form["language"]
        s_preference = request.form["preference"]
        conn = sql.connect("user.db")
        cur = conn.cursor()
        cur.execute("insert into student (NAME,AGE,LANGUAGE,PREFERENCE) values (?,?,?,?)",(s_name,s_age,s_language,s_preference))
        conn.commit()
        flash("User Created", "success")
        return redirect(url_for("home"))
    return render_template("add_user.html")

@app.route("/edit_user/<string:id>",methods=["POST","GET"])
def edit_user(id):
    if request.method == "POST":
        s_name = request.form["name"]
        s_age = request.form["age"]
        s_language = request.form["language"]
        s_preference = request.form["preference"]
        conn = sql.connect("user.db")
        cur = conn.cursor()
        cur.execute("update student set NAME=?, AGE=?, LANGUAGE=?, PREFERENCE=? where ID=?",(s_name,s_age,s_language,s_preference,id))
        conn.commit()
        flash("User Updated","success")
        return redirect(url_for("home"))
    conn = sql.connect("user.db")
    conn.row_factory =sql.Row
    cur = conn.cursor()
    cur.execute("select * from student where ID=?",(id,))
    data= cur.fetchone()
    return render_template("edit_user.html", datas=data)


@app.route("/delete_user/<string:id>" , methods=["GET"])
def delete_user(id):
    conn = sql.connect('user.db')
    cur = conn.cursor()
    cur.execute("delete from student where ID=?",(id,))
    conn.commit()
    flash("User Deleted", "warning")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)