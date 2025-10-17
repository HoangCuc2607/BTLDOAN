import sqlite3
from datetime import date, datetime

class DiemDanh:
    def __init__(self, id=None, nhanvien_id=None, ngay_diem_danh=None, 
                 ca_sang=None, ca_chieu=None, ca_toi=None):
        self.id = id
        self.nhanvien_id = nhanvien_id
        self.ngay_diem_danh = ngay_diem_danh or date.today()
        self.ca_sang = ca_sang
        self.ca_chieu = ca_chieu
        self.ca_toi = ca_toi

    # Thêm mới điểm danh
    def them_diem_danh(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO DiemDanh (nhanvien_id, ngay_diem_danh, ca_sang, ca_chieu, ca_toi)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.nhanvien_id, self.ngay_diem_danh, self.ca_sang, self.ca_chieu, self.ca_toi))
        conn.commit()
        conn.close()

    # Cập nhật điểm danh cho 1 ca
    @staticmethod
    def cap_nhat_ca(nhanvien_id, ngay_diem_danh, ca, trang_thai):
        """
        ca: 'sang', 'chieu', 'toi'
        trang_thai: 'Đã điểm danh', 'Đến muộn', 'Chưa điểm danh'
        """
        col = f"ca_{ca.lower()}"
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE DiemDanh
            SET {col} = ?
            WHERE nhanvien_id = ? AND ngay_diem_danh = ?
        ''', (trang_thai, nhanvien_id, ngay_diem_danh))
        conn.commit()
        conn.close()

    # Lấy tất cả điểm danh theo ngày
    @staticmethod
    def lay_diem_danh_theo_ngay(ngay_diem_danh):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nhanvien_id, ngay_diem_danh, ca_sang, ca_chieu, ca_toi
            FROM DiemDanh
            WHERE ngay_diem_danh=?
        ''', (ngay_diem_danh,))
        records = cursor.fetchall()
        conn.close()
        return [DiemDanh(*r) for r in records]

    # Lấy tất cả điểm danh theo nhân viên
    @staticmethod
    def lay_diem_danh_theo_nhanvien(nhanvien_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nhanvien_id, ngay_diem_danh, ca_sang, ca_chieu, ca_toi
            FROM DiemDanh
            WHERE nhanvien_id = ?
            ORDER BY ngay_diem_danh DESC
        ''', (nhanvien_id,))
        records = cursor.fetchall()
        conn.close()
        return [DiemDanh(*r) for r in records]

    # Lấy trạng thái 1 ca của nhân viên theo ngày
    @staticmethod
    def lay_trang_thai_ca(nhanvien_id, ngay_diem_danh, ca):
        """
        Trả về giá trị của ca: 'Đã điểm danh', 'Đến muộn', 'Chưa điểm danh' hoặc None
        """
        col = f"ca_{ca.lower()}"
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT {col} FROM DiemDanh
            WHERE nhanvien_id=? AND ngay_diem_danh=?
        ''', (nhanvien_id, ngay_diem_danh))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
