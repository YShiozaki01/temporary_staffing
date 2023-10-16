import sqlite3

DATABASE = "./database/database.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


class DataRegistration:
    def __init__(self, record):
        self.year = record["year"]
        self.month = record["month"]
        self.dept = record["dept_cd"]
        self.vendor = record["vendor_cd"]
        self.human = record["human_cd"]
        self.working_hours = record["working_hours"] if record["working_hours"] else 0
        self.others = record["others"] if record["others"] else ""
        self.remarks = record["remarks"] if record["remarks"] else ""

    # 入力された人材は登録済みかチェック
    def check_registered(self):
        sql = f"""
            SELECT * FROM TTemporary_staffing
            WHERE 請求年 = {self.year} AND 請求月 = {self.month}
            AND 部門 = '{self.dept}' AND 会社 = {self.vendor}
            AND 人材 = {self.human};
            """
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        if len(cur.fetchall()) != 0:
            exist = True
        else:
            exist = False
        return exist
    
    # 入力データをテーブルに登録
    def regist_data(self):
        check = self.check_registered()
        if check:
            sql = f"""
                UPDATE TTemporary_staffing SET 作業時間 = {self.working_hours},
                その他 = '{self.others}', 備考 = '{self.remarks}'
                WHERE 請求年 = {self.year} AND 請求月 = {self.month}
                AND 部門 = '{self.dept}' AND 会社 = {self.vendor}
                AND 人材 = {self.human};
                """
        else:
            sql = f"""
                INSERT INTO TTemporary_staffing(請求年, 請求月, 部門, 会社,
                人材, 作業時間, その他, 備考)
                VALUES({self.year}, {self.month}, '{self.dept}',
                {self.vendor}, {self.human}, {self.working_hours},
                '{self.others}', '{self.remarks}')
                """
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    # 表示用の一覧を取得する
    def input_result(self):
        sql = f"""
            SELECT b.略称名 as 部門名, c.名称 as 会社名,
            d.名称 || ' （' || d.勤務帯 || ' ' || d.業務内容 || '）' as 氏名,
            a.作業時間, a.その他, a.備考
            FROM TTemporary_staffing as a
            LEFT JOIN MDepartment as b on a.部門 = b.コード
            LEFT JOIN MVendor as c on a.会社 = c.コード
            LEFT JOIN MHuman_resources as d on a.人材 = d.コード
            WHERE 請求年 = {self.year} AND 請求月 = {self.month}
            ORDER by a.ID DESC;
            """
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        return result

if __name__ == "__main__":
    test_val = {"year": 2023, "month": 2, "dept_cd": "03",
                "vendor_cd": 2, "human_cd": 1, "working_hours": 0.0,
                "others": "", "remarks": ""}
    dr = DataRegistration(test_val)
    result = dr.input_result()
    for row in result:
        print(row["ID"], row["部門名"], row["会社名"], row["氏名"], row["作業時間"], row["その他"], row["備考"])
