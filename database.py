import sqlite3

def tao_co_so_du_lieu():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Bật kiểm tra khóa ngoại
    cursor.execute('PRAGMA foreign_keys = ON;')

    # Tạo bảng NhanVien
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

    # Tạo bảng DiemDanh
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DiemDanh (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nhanvien_id INTEGER NOT NULL,
        ngay_diem_danh DATE NOT NULL,
        trang_thai TEXT CHECK(trang_thai IN ('Đã điểm danh', 'Chưa điểm danh', 'Đến muộn')),
        FOREIGN KEY (nhanvien_id) REFERENCES NhanVien(ma_nhan_vien) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()
    print("Tạo cơ sở dữ liệu thành công!")

if __name__ == "__main__":
    tao_co_so_du_lieu()
