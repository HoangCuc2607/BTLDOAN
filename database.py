import sqlite3

def tao_co_so_du_lieu():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Bật kiểm tra khóa ngoại
    cursor.execute('PRAGMA foreign_keys = ON;')

    # Bảng NhanVien
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS NhanVien (
        ma_nhan_vien INTEGER PRIMARY KEY AUTOINCREMENT,
        ho_ten TEXT NOT NULL,
        ngay_sinh DATE NOT NULL,
        gioi_tinh TEXT CHECK(gioi_tinh IN ('Nam', 'Nữ', 'Khác')) NOT NULL,
        dia_chi TEXT NOT NULL,
        so_dien_thoai TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')

    # Bảng DiemDanh
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DiemDanh (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nhanvien_id INTEGER NOT NULL,
        ngay_diem_danh DATE NOT NULL,
        ca_sang TEXT CHECK(ca_sang IN ('Đã điểm danh', 'Đến muộn', 'Chưa điểm danh')) DEFAULT NULL,
        ca_chieu TEXT CHECK(ca_chieu IN ('Đã điểm danh', 'Đến muộn', 'Chưa điểm danh')) DEFAULT NULL,
        ca_toi TEXT CHECK(ca_toi IN ('Đã điểm danh', 'Đến muộn', 'Chưa điểm danh')) DEFAULT NULL,
        FOREIGN KEY (nhanvien_id) REFERENCES NhanVien(ma_nhan_vien) ON DELETE CASCADE
    );
    ''')

    # Bảng ChiaCa: lưu thông tin ngày và giờ từng ca
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ChiaCa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ngay DATE NOT NULL,
        gio_bat_dau_ca_sang TIME,
        gio_ket_thuc_ca_sang TIME,
        gio_bat_dau_ca_chieu TIME,
        gio_ket_thuc_ca_chieu TIME,
        gio_bat_dau_ca_toi TIME,
        gio_ket_thuc_ca_toi TIME
    )
    ''')

    # Bảng trung gian ChiaCaNhanVien: nhiều-nhiều với cột ca
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ChiaCaNhanVien (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chia_ca_id INTEGER NOT NULL,
        nhanvien_id INTEGER NOT NULL,
        ca TEXT CHECK(ca IN ('Sáng','Chiều','Tối')) NOT NULL,
        FOREIGN KEY (chia_ca_id) REFERENCES ChiaCa(id) ON DELETE CASCADE,
        FOREIGN KEY (nhanvien_id) REFERENCES NhanVien(ma_nhan_vien) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()
    print("Tạo cơ sở dữ liệu thành công!")

if __name__ == "__main__":
    tao_co_so_du_lieu()
