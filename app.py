from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from register import DataRegistration

app = Flask(__name__)

# DATABASE = "./database/database.db"
DATABASE = "./database/database.db"

global record
global record2
record = {}
record2 = {}


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# リストを取得
def get_pulldown_list(name):
    dept_cd = record["dept_cd"] if "dept_cd" in record else "%"
    vendor_cd = record["vendor_cd"] if "vendor_cd" in record else 0
    keyword = record["keyword"] if "keyword" in record else "%"
    sql_dept = """
        SELECT コード, 名称 FROM MDepartment;
        """
    sql_vendor = f"""
        SELECT コード, 名称 FROM MVendor WHERE 部門 = '{dept_cd}';
        """
    sql_human = f"""
        SELECT コード, 名称 || ' 【' || 業務内容 || ' ' || 基本単価 || '】'
        as 人材
        FROM MHuman_resources
        WHERE 業者コード = {vendor_cd};
        """
    sql_human_2 = f"""
        SELECT コード, 名称 || ' 【' || 業務内容 || ' ' || 基本単価 || '】'
        as 人材
        FROM MHuman_resources
        WHERE 業者コード = {vendor_cd} AND 名称 like '%{keyword}%';
        """
    if name == "dept":
        sql = sql_dept
    elif name == "vendor":
        sql = sql_vendor
    elif name == "human":
        sql = sql_human
    elif name == "human2":
        sql = sql_human_2
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    pulldown_list = cur.fetchall()
    return pulldown_list


# 表示用の名称を取得
def get_display_name(name):
    if name == "dept":
        table_name = "MDepartment"
        code = record["dept_cd"]
    elif name == "vendor":
        table_name = "MVendor"
        code = record["vendor_cd"]
    elif name == "human":
        table_name = "MHuman_resources"
        code = record["human_cd"]
    sql = f"""
        SELECT * FROM {table_name} WHERE コード = '{code}';
        """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    display_name = result["名称"]
    return display_name


# 人材の情報を取得
def get_human_info(code):
    sql = f"""
        SELECT * FROM MHuman_resources WHERE コード = '{code}';
        """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    return result


@app.route("/", methods=["get", "post"])
def index():
    record["dept_list"] = get_pulldown_list("dept")
    return render_template("index.html", record=record)


@app.route("/select_1", methods=["get", "post"])
def select_1():
    record["year"] = request.form.get("year")
    record["month"] = request.form.get("month")
    record["dept_cd"] = request.form.get("code_dept")
    if "dept_cd" in record:
        record["dept_name"] = get_display_name("dept")
        record["vendor_list"] = get_pulldown_list("vendor")
    return render_template("index.html", record=record)


@app.route("/select_2", methods=["get", "post"])
def select_2():
    record["vendor_cd"] = request.form.get("code_vendor")
    if "vendor_cd" in record:
        record["vendor_name"] = get_display_name("vendor")
        record["human_list"] = get_pulldown_list("human")
    return render_template("index.html", record=record)


@app.route("/keyword", methods=["post"])
def keyword():
    record["keyword"] = request.form.get("keywd")
    record["human_list"] = get_pulldown_list("human2")
    return render_template("index.html", record=record)


@app.route("/select_3", methods=["get", "post"])
def select_3():
    input_result = ""
    if request.form.get("btn") == "s":
        record["human_cd"] = request.form.get("code_human")
        if "human_cd" in record:
            record["human_name"] = get_display_name("human")
            human_info = get_human_info(record["human_cd"])
            record2["info_1"] = human_info["勤務帯"]
            record2["info_2"] = human_info["業務内容"]
            record2["info_3"] = human_info["基本単価"]
        start_flg = True
    elif request.form.get("btn") == "c":
        start_flg = False
        del record["human_cd"]
        record["human_list"] = get_pulldown_list("human")
        if "keyword" in record:
            del record["keyword"]
        record2.clear()
    elif request.form.get("btn") == "r":
        start_flg = False
        record["working_hours"] = request.form.get("working_hours")
        record["others"] = request.form.get("others")
        record["remarks"] = request.form.get("remarks")
        dr = DataRegistration(record)
        dr.regist_data()
        input_result = dr.input_result()
    return render_template("index.html", record=record,
                           record2=record2, start_flg=start_flg,
                           input_result=input_result)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000")
