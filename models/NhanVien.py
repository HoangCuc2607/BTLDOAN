import sqlite3

class NhanVien:
    def __init__(self, ma_nhan_vien=None, ho_ten="", so_dien_thoai="", dia_chi="", gioi_tinh="", email="", ngay_sinh=""):
        self.ma_nhan_vien = ma_nhan_vien
        self.ho_ten = ho_ten
        self.so_dien_thoai = so_dien_thoai
        self.dia_chi = dia_chi
        self.gioi_tinh = gioi_tinh
        self.email = email
        self.ngay_sinh = ngay_sinh

    def them_nhan_vien(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO NhanVien (ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.ho_ten, self.so_dien_thoai, self.dia_chi, self.gioi_tinh, self.email, self.ngay_sinh))
        conn.commit()
        conn.close()

    @staticmethod
    def lay_danh_sach_nhan_vien():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ma_nhan_vien, ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh
            FROM NhanVien
        ''')
        records = cursor.fetchall()
        conn.close()
        return [NhanVien(*r) for r in records]

    @staticmethod
    def cap_nhat_nhan_vien(ma_nhan_vien, ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE NhanVien
            SET ho_ten=?, so_dien_thoai=?, dia_chi=?, gioi_tinh=?, email=?, ngay_sinh=?
            WHERE ma_nhan_vien=?
        ''', (ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh, ma_nhan_vien))
        conn.commit()
        conn.close()

    @staticmethod
    def xoa_nhan_vien(ma_nhan_vien):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM NhanVien WHERE ma_nhan_vien = ?', (ma_nhan_vien,))
            conn.commit()
        except sqlite3.Error as e:
            print("Lỗi khi xóa nhân viên:", e)
        finally:
            conn.close()

    @staticmethod
    def lay_thong_tin_nhan_vien(ma_nhan_vien):
        """
        Lấy thông tin 1 nhân viên theo id.
        Trả về đối tượng NhanVien hoặc None nếu không tìm thấy.
        """
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ma_nhan_vien, ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh
            FROM NhanVien
            WHERE ma_nhan_vien = ?
        ''', (ma_nhan_vien,))
        record = cursor.fetchone()
        conn.close()
        if record:
            return NhanVien(*record)
        return None

    @staticmethod
    def cap_nhat_nhan_vien_theo_id(ma_nhan_vien, ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh):
        """
        Cập nhật thông tin 1 nhân viên theo id.
        Trả về True nếu thành công, False nếu lỗi.
        """
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE NhanVien
                SET ho_ten=?, so_dien_thoai=?, dia_chi=?, gioi_tinh=?, email=?, ngay_sinh=?
                WHERE ma_nhan_vien=?
            ''', (ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh, ma_nhan_vien))
            conn.commit()
            return cursor.rowcount > 0  # True nếu có dòng bị update
        except sqlite3.Error as e:
            print("Lỗi khi cập nhật nhân viên:", e)
            return False
        finally:
            conn.close()
