from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import json

# Configure app
app = Flask(__name__)

global yearMonth
yearMonth = {}

# データベースに接続して連想配列で取得
def get_db_connection():
    connection = sqlite3.connect("./database/database.db")
    connection.row_factory = sqlite3.Row
    return connection


# 入力済みテーブル表示用のデータを生成
def get_history(year, month):
    sql = f"""
        SELECT b.名称 as 部門, c.名称 as 会社名, d.名称 as 氏名,
        a.作業時間, a.その他, a.備考
        FROM TTemporary_staffing as a
        LEFT JOIN MDepartment as b on a.部門 = b.コード
        LEFT JOIN MVendor as c on a.会社 = c.コード
        LEFT JOIN MHuman_resources as d on a.人材 = d.コード
        WHERE a.請求年 = {year} AND a.請求月 = {month}
        ORDER by a.ID DESC;
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    return result


# 入力済みのデータかチェック
def check_exist(year, month, code):
    conn = sqlite3.connect("./database/database.db")
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM TTemporary_staffing
                WHERE 請求年 = {year} AND 請求月 = {month}
                AND 人材 = {code}""")
    if len(cur.fetchall()) > 0:
        result = True
    else:
        result = False
    return result


@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT コード, 名称 FROM MDepartment;")
    departmentList = cur.fetchall()
    # テーブル表示用のデータを取得
    if "year" in yearMonth:
        inputHist = get_history(yearMonth["year"], yearMonth["month"])
    else:
        inputHist = ""
    return render_template("index.html", departmentList=departmentList,
                           inputHist=inputHist)


@app.route("/get_vendors", methods=["POST"])
def get_vendors():
    keyword = request.form.get("departmentCode")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT コード, 名称 FROM MVendor WHERE 部門 = '{keyword}';")
    result = cur.fetchall()
    vendors = dict(result)
    return jsonify(vendors)


@app.route("/get_resources", methods=["POST"])
def get_resources():
    keyword = request.form.get("keyword")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"""SELECT コード, 名称 || ' 【' || 勤務帯 || ' ' || 業務内容 || ' ' || 基本単価 || '】' as 人材
                FROM MHuman_resources WHERE 業者コード = {keyword};""")
    result = cur.fetchall()
    vendors = dict(result)
    return jsonify(vendors)


@app.route("/get_resources_name", methods=["POST"])
def get_resources_name():
    strKeywords = request.form.get("keyword")
    dictKw = json.loads(strKeywords)
    sql = f"""
        SELECT コード, 名称 || ' 【' || 勤務帯 || ' ' || 業務内容 || ' ' || 基本単価 || '】' as 人材
        FROM MHuman_resources WHERE 業者コード = {int(dictKw["key1"])} AND 名称 like '%{dictKw["key2"]}%';
        """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    vendors = dict(result)
    return jsonify(vendors)


@app.route("/regist", methods=["POST"])
def regist():
    if request.method == "POST":
        closingYear = request.form.get("year")
        closingMonth = request.form.get("month")
        selectDepartment = request.form.get("select_dept")
        selectVendor = request.form.get("select_vendor")
        selectHumanResources = request.form.get("select_resource")
        workingHours = request.form.get("working_hours")
        others = request.form.get("others")
        remarks = request.form.get("remarks")
        # データベースに接続
        conn = sqlite3.connect("./database/database.db")
        cur = conn.cursor()
        # もし入力済みでなければ新規追加
        if not check_exist(closingYear, closingMonth, selectHumanResources):
            sql = f"""
                INSERT INTO TTemporary_staffing(請求年, 請求月, 部門, 会社, 人材, 作業時間, その他, 備考)
                VALUES({closingYear}, {closingMonth}, '{selectDepartment}', {selectVendor}, {selectHumanResources},
                {workingHours if workingHours else 0}, '{others if others else ''}', '{remarks if remarks else ''}');
            """
            cur.execute(sql)
            conn.commit()
        # 登録済みなら内容を更新
        else:
            sql = f"""
                UPDATE TTemporary_staffing SET 作業時間 = {workingHours if workingHours else 0},
                その他 = '{others if others else ''}', 備考 = '{remarks if remarks else ''}'
                WHERE 請求年 = {closingYear} AND 請求月 = {closingMonth} AND 人材 = {selectHumanResources};
            """
            print(sql)
            cur.execute(sql)
            conn.commit()
        yearMonth["year"] = closingYear
        yearMonth["month"] = closingMonth
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000")
