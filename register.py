import sqlite3

DATABASE = "./database/database.db"


class DataRegistration:
    def __init__(self, record):
        self.year = record["year"]
        self.month = record["month"]
        self.dept = record["dept_cd"]
        self.vendor = record["vendor_cd"]
        self.human = record["human_cd"]
        self.working_hours = record["working_hours"] if record["working_hours"] else 0
        self.others = record["others"] if record["others"] else ""

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
                その他 = '{self.others}'
                WHERE 請求年 = {self.year} AND 請求月 = {self.month}
                AND 部門 = '{self.dept}' AND 会社 = {self.vendor}
                AND 人材 = {self.human};
                """
        else:
            sql = f"""
                INSERT INTO TTemporary_staffing(請求年, 請求月, 部門, 会社,
                人材, 作業時間, その他)
                VALUES({self.year}, {self.month}, '{self.dept}',
                {self.vendor}, {self.human}, {self.working_hours},
                '{self.others}')
                """
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
