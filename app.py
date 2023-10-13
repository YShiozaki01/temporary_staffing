from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "./database/database.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# リストを取得
def get_pulldown_list(name, dept_cd, vendor_cd):
    sql_dept = """
        SELECT コード, 名称 FROM MDepartment;
        """
    sql_vendor = f"""
        SELECT コード, 名称 FROM MVendor WHERE 部門 like '{dept_cd}';
        """
    sql_human = f"""
        SELECT コード, 名称 FROM MHuman_resources WHERE 業者コード like {vendor_cd};
        """
    if name == "dept":
        sql = sql_dept
    elif name == "vendor":
        sql = sql_vendor
    elif name == "human":
        sql = sql_human
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    dept_list = cur.fetchall()
    return dept_list


# 表示用の名称を取得
def get_display_name(name, code):
    if name == "dept":
        table_name = "MDepartment"
    elif name == "vendor":
        table_name = "MVendor"
    elif name == "human":
        table_name = "MHuman_resources"
    sql = f"""
        SELECT * FROM {table_name} WHERE コード = '{code}';
        """
    print(sql)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    display_name = result["名称"]
    return display_name


@app.route("/", methods=["get", "post"])
def index():
    record = {}
    record["dept_cd"] = "%"
    record["vendor_cd"] = 0
    record["human_cd"] = 0
    record["dept_list"] = get_pulldown_list("dept", record["dept_cd"], record["vendor_cd"])
    record["dept_name"] = ""
    record["vendor_list"] = get_pulldown_list("vendor", record["dept_cd"], record["vendor_cd"])
    record["vendor_name"] = ""
    record["human_list"] = get_pulldown_list("human", record["dept_cd"], record["vendor_cd"])
    record["human_name"] = ""
    if request.form.get("dpt1") == "submit1":
        record["dept_cd"] = request.form.get("code_dept")
        print(record["dept_cd"])
    if request.form.get("dpt2") == "submit2":
        record["dept_name"] = get_display_name("dept", record["dept_cd"])
        record["vendor_list"] = get_pulldown_list("vendor", record["dept_cd"], record["vendor_cd"])
        record["vendor_cd"] = request.form.get("code_vendor") if request.form.get("code_vendor") else ""
        # record["vendor_name"] = get_display_name("vendor", record["vendor_cd"])
        # record["human_list"] = get_pulldown_list("human", record["dept_cd"], record["vendor_cd"])
    print(f"部門: {record['dept_name']}, 業者: {record['vendor_name']}")
    return render_template("index.html", record=record)
