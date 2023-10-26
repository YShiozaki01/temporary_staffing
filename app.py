from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "./database/database.db"

global send_dict
send_dict = {}

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# 部門のリストを作成
def get_department_list():
    sql = "SELECT * FROM MDepartment;"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 業者のリストを作成
def get_vendor_list(department_code):
    sql = f"SELECT コード, 名称 FROM MVendor WHERE 部門 = '{department_code}';"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    return result


@app.route("/", methods=["GET", "POST"])
def index():
    send_dict["department_list"] = get_department_list()
    return render_template("index.html", send_dict = send_dict)

@app.route("/register", methods=["POST"])
def register():
    send_dict["closing_date_year"] = request.form.get("year")
    send_dict["closing_date_month"] = request.form.get("month")
    send_dict["department_code"] = request.form.get("department")
    send_dict["vendor_list"] = get_vendor_list(send_dict["department_code"])
    print(send_dict)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000")
