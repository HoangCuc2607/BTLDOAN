import sqlite3
from datetime import date

class DiemDanh:
    def __init__(self, id=None, nhanvien_id=None, ngay_diem_danh=None, trang_thai=""):
        self.id = id
        self.nhanvien_id = nhanvien_id
        self.ngay_diem_danh = ngay_diem_danh or date.today()
        self.trang_thai = trang_thai

    def them_diem_danh(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO DiemDanh (nhanvien_id, ngay_diem_danh, trang_thai)
            VALUES (?, ?, ?)
        ''', (self.nhanvien_id, self.ngay_diem_danh, self.trang_thai))
        conn.commit()
        conn.close()

    @staticmethod
    def lay_diem_danh_theo_ngay(ngay_diem_danh):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nhanvien_id, ngay_diem_danh, trang_thai FROM DiemDanh WHERE ngay_diem_danh=?', (ngay_diem_danh,))
        records = cursor.fetchall()
        conn.close()
        return [DiemDanh(*r) for r in records]
