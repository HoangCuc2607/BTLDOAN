import sqlite3
from datetime import date, timedelta
import random

def tao_fake_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Danh sách tên giả lập
    nhanvien_list = [
        ("Nguyễn Văn A", "1990-01-15", "Nam", "Hà Nội", "0123456789", "a@example.com"),
        ("Trần Thị B", "1992-05-20", "Nữ", "Hà Nội", "0987654321", "b@example.com"),
        ("Lê Văn C", "1988-03-10", "Nam", "Hà Nội", "0912345678", "c@example.com"),
        ("Phạm Thị D", "1995-07-25", "Nữ", "Hà Nội", "0909876543", "d@example.com"),
        ("Hoàng Văn E", "1991-12-05", "Nam", "Hà Nội", "0934567890", "e@example.com"),
    ]

    # Chèn dữ liệu nhân viên
    for nv in nhanvien_list:
        cursor.execute('''
            INSERT OR IGNORE INTO NhanVien (ho_ten, ngay_sinh, gioi_tinh, dia_chi, so_dien_thoai, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', nv)

    # Lấy danh sách id nhân viên vừa thêm
    cursor.execute('SELECT ma_nhan_vien FROM NhanVien')
    nhanvien_ids = [row[0] for row in cursor.fetchall()]

    # Tạo điểm danh cho 5 ngày gần nhất
    for nhanvien_id in nhanvien_ids:
        for i in range(5):
            ngay = date.today() - timedelta(days=i)
            trang_thai = random.choice(['Đã điểm danh', 'Chưa điểm danh', 'Đến muộn'])
            cursor.execute('''
                INSERT INTO DiemDanh (nhanvien_id, ngay_diem_danh, trang_thai)
                VALUES (?, ?, ?)
            ''', (nhanvien_id, ngay, trang_thai))

    conn.commit()
    conn.close()
    print("Fake data đã được chèn thành công!")

if __name__ == "__main__":
    tao_fake_data()
