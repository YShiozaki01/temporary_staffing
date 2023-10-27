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


# 入力をTTemporary_staffingに書き込み
def insert_table(data_list):
    # 1)登録済みかチェック
    sql = f"""
        SELECT * FROM TTemporary_staffing 
        WHERE 請求年 = {send_dict['closing_date_year']}
        AND 請求月 = {send_dict['closing_date_month']}
        AND 部門 = '{send_dict['department_code']}'
        AND 会社 = {send_dict['vendor_code']}
        AND 人材 = {send_dict['resource_code']};
        """
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql)
    # 2)もし、同じ内容が登録済みなら更新
    if len(cur.fetchall()) > 0:
        sql = f"""
            SELECT ID FROM TTemporary_staffing 
            WHERE 請求年 = {send_dict['closing_date_year']}
            AND 請求月 = {send_dict['closing_date_month']}
            AND 部門 = '{send_dict['department_code']}'
            AND 会社 = {send_dict['vendor_code']}
            AND 人材 = {send_dict['resource_code']};
            """
        cur.execute(sql)
        result = cur.fetchone()
        id = result[0]
        sql = f"""
            UPDATE TTemporary_staffing
            SET 請求年 = {data_list[0]}, 請求月 = {data_list[1]}, 部門 = '{data_list[2]}',
            会社 = {data_list[3]}, 人材 = {data_list[4]}, 作業時間 = {data_list[5]},
            その他 = '{data_list[6]}', 備考 = '{data_list[7]}' WHERE ID = {id};
            """
        cur.execute(sql)
        conn.commit()
    # 3)もし、同じ内容の登録がなければ追加
    else:
        sql = f"""
            INSERT INTO TTemporary_Staffing(請求年, 請求月, 部門, 会社, 人材, 作業時間, その他, 備考)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?);
            """
        cur.execute(sql, data_list)
        conn.commit()


# 入力データを変数に順次代入
def regist_data():
    send_dict["closing_date_year"] = request.form.get("year")
    send_dict["closing_date_month"] = request.form.get("month")
    if not request.form.get("department") == "":
        send_dict["department_code"] = request.form.get("department")
        send_dict["department_name"] = get_department_name(send_dict["department_code"])
        send_dict["vendor_list"] = get_vendor_list(send_dict["department_code"])
    if not request.form.get("vendor") == "":
        send_dict["vendor_code"] = request.form.get("vendor")
        send_dict["vendor_name"] = get_vendor_name(send_dict["vendor_code"])
        send_dict["resource_list"] = get_resource_list(send_dict["vendor_code"])
    if not request.form.get("resource") == "":
        send_dict["resource_code"] = request.form.get("resource")
        send_dict["resource_name"] = get_resource_name(send_dict["resource_code"])
    send_dict["working_hours"] = request.form.get("working_hours")
    send_dict["others"] = request.form.get("others")
    send_dict["remarks"] = request.form.get("remarks")


# 入力履歴データを生成
def input_history_gen():
    sql = f"""
        SELECT b.名称 as 部門, c.名称 as 会社名, d.名称 as 氏名, a.作業時間, a.その他, a.備考
        FROM TTemporary_staffing as a
        LEFT JOIN MDepartment as b on a.部門 = b.コード
        LEFT JOIN MVendor as c on a.会社 = c.コード
        LEFT JOIN MHuman_resources as d on a.人材 = d.コード
        WHERE a.請求年 = {send_dict['closing_date_year']}
        AND a.請求月 = {send_dict['closing_date_month']}
        ORDER by a.ID DESC;
        """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    send_dict["input_history"] = result


@app.route("/", methods=["GET", "POST"])
def index():
    send_dict["department_list"] = get_department_list()
    return render_template("index.html", send_dict = send_dict)

@app.route("/register", methods=["POST"])
def register():
    regist_data()
    if request.form.get("button") == "entry":
        insert_list = []
        insert_list.append(send_dict["closing_date_year"])
        insert_list.append(send_dict["closing_date_month"])
        insert_list.append(send_dict["department_code"])
        insert_list.append(send_dict["vendor_code"])
        insert_list.append(send_dict["resource_code"])
        insert_list.append(send_dict["working_hours"])
        insert_list.append(send_dict["others"])
        insert_list.append(send_dict["remarks"])
        insert_table(insert_list)
        for element in ["resource_code", "resource_name", "working_hours", "others", "remarks"]:
            del send_dict[element]
        input_history_gen()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000")
