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


# 人材のリストを作成
def get_resource_list(vendor_code):
    sql = f"""SELECT コード, 名称 || '　(' || 勤務帯 || ' ' || 業務内容 || ' @' || 基本単価 || ')' as 人材情報
        FROM MHuman_resources WHERE 業者コード = {vendor_code} and 削除 is NULL ORDER BY 名称;"""
    print(sql)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 部門名称を取得
def get_department_name(department_code):
    sql = f"SELECT 名称 FROM MDepartment WHERE コード = '{department_code}';"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    name = result["名称"]
    return name


# 業者名称を取得
def get_vendor_name(vendor_code):
    sql = f"SELECT 名称 FROM MVendor WHERE コード = {vendor_code};"
    print(sql)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    name = result["名称"]
    return name


# 人材名を取得
def get_resource_name(resource_code):
    sql = f"""SELECT 名称 || '　(' || 勤務帯 || ' ' || 業務内容 || ' @' || 基本単価 || ')' as 人材情報
        FROM MHuman_resources WHERE コード = {resource_code};"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    name = result["人材情報"]
    return name


@app.route("/", methods=["GET", "POST"])
def index():
    send_dict["department_list"] = get_department_list()
    return render_template("index.html", send_dict = send_dict)

@app.route("/register", methods=["POST"])
def register():
    send_dict["closing_date_year"] = request.form.get("year")
    send_dict["closing_date_month"] = request.form.get("month")
    send_dict["department_code"] = request.form.get("department")
    if not send_dict["department_code"] is None:
        send_dict["department_name"] = get_department_name(send_dict["department_code"])
        send_dict["vendor_list"] = get_vendor_list(send_dict["department_code"])
    send_dict["vendor_code"] = request.form.get("vendor")
    if not send_dict["vendor_code"] is None:
        send_dict["vendor_name"] = get_vendor_name(send_dict["vendor_code"])
        send_dict["resource_list"] = get_resource_list(send_dict["vendor_code"])
    send_dict["resource_code"] = request.form.get("resource")
    if not send_dict["resource_code"] is None:
        send_dict["resource_name"] = get_resource_name(send_dict["resource_code"])
    send_dict["working_hours"] = request.form.get("working_hours")
    send_dict["others"] = request.form.get("others")
    send_dict["remarks"] = request.form.get("remarks")
    print(send_dict)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000")
