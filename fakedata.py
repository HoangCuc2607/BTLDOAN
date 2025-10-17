import sqlite3
from datetime import date, timedelta
import random

def tao_fake_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 1. Danh sách tên nhân viên giả lập
    nhanvien_list = [
        ("Nguyễn Văn A", "1990-01-15", "Nam", "Hà Nội", "0123456789", "a@example.com"),
        ("Trần Thị B", "1992-05-20", "Nữ", "Hà Nội", "0987654321", "b@example.com"),
        ("Lê Văn C", "1988-03-10", "Nam", "Hà Nội", "0912345678", "c@example.com"),
        ("Phạm Thị D", "1995-07-25", "Nữ", "Hà Nội", "0909876543", "d@example.com"),
        ("Hoàng Văn E", "1991-12-05", "Nam", "Hà Nội", "0934567890", "e@example.com"),
    ]

    # Chèn nhân viên
    for nv in nhanvien_list:
        cursor.execute('''
            INSERT OR IGNORE INTO NhanVien (ho_ten, ngay_sinh, gioi_tinh, dia_chi, so_dien_thoai, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', nv)

    # Lấy danh sách id nhân viên
    cursor.execute('SELECT ma_nhan_vien FROM NhanVien')
    nhanvien_ids = [row[0] for row in cursor.fetchall()]

    # 2. Tạo ca chia cho 5 ngày gần nhất
    for i in range(5):
        ngay = date.today() - timedelta(days=i)
        cursor.execute('''
            INSERT INTO ChiaCa (ngay, gio_bat_dau_ca_sang, gio_ket_thuc_ca_sang,
                                gio_bat_dau_ca_chieu, gio_ket_thuc_ca_chieu,
                                gio_bat_dau_ca_toi, gio_ket_thuc_ca_toi)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (ngay, '08:00', '12:00', '12:00', '16:00', '16:00', '20:00'))
        chia_ca_id = cursor.lastrowid

        # 3. Phân nhân viên ngẫu nhiên cho từng ca
        for ca in ['Sáng', 'Chiều', 'Tối']:
            selected_employees = random.sample(nhanvien_ids, k=random.randint(1, len(nhanvien_ids)))
            for emp_id in selected_employees:
                cursor.execute('''
                    INSERT INTO ChiaCaNhanVien (chia_ca_id, nhanvien_id, ca)
                    VALUES (?, ?, ?)
                ''', (chia_ca_id, emp_id, ca))

    # 4. Tạo bảng điểm danh trống cho 5 ngày gần nhất
    for i in range(5):
        ngay = date.today() - timedelta(days=i)
        for emp_id in nhanvien_ids:
            cursor.execute('''
                INSERT INTO DiemDanh (nhanvien_id, ngay_diem_danh, ca_sang, ca_chieu, ca_toi)
                VALUES (?, ?, ?, ?, ?)
            ''', (emp_id, ngay, None, None, None))

    conn.commit()
    conn.close()
    print("Fake data đã được chèn thành công!")

if __name__ == "__main__":
    tao_fake_data()
