import sqlite3

class ChiaCaNhanVien:
    def __init__(self, id=None, chia_ca_id=None, nhanvien_id=None, ca=""):
        self.id = id
        self.chia_ca_id = chia_ca_id
        self.nhanvien_id = nhanvien_id
        self.ca = ca  # 'Sáng', 'Chiều', 'Tối'

    # Thêm nhân viên vào ca
    def them_nhan_vien_vao_ca(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ChiaCaNhanVien (chia_ca_id, nhanvien_id, ca)
            VALUES (?, ?, ?)
        ''', (self.chia_ca_id, self.nhanvien_id, self.ca))
        conn.commit()
        conn.close()

    # Cập nhật danh sách nhân viên trong ca (xóa rồi thêm mới)
    @staticmethod
    def cap_nhat_nhan_vien_vao_ca(chia_ca_id, ca, danh_sach_nhan_vien_ids):
        # Xóa nhân viên cũ
        ChiaCaNhanVien.xoa_nhan_vien_theo_ca(chia_ca_id, ca)
        # Thêm nhân viên mới
        for nv_id in danh_sach_nhan_vien_ids:
            cc_nv = ChiaCaNhanVien(chia_ca_id=chia_ca_id, nhanvien_id=nv_id, ca=ca)
            cc_nv.them_nhan_vien_vao_ca()

    # Lấy danh sách nhân viên đã chọn theo ca
    @staticmethod
    def lay_nhan_vien_theo_ca(chia_ca_id, ca):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nhanvien_id FROM ChiaCaNhanVien
            WHERE chia_ca_id=? AND ca=?
        ''', (chia_ca_id, ca))
        records = cursor.fetchall()
        conn.close()
        return [r[0] for r in records]

    # Xóa nhân viên theo ca
    @staticmethod
    def xoa_nhan_vien_theo_ca(chia_ca_id, ca):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM ChiaCaNhanVien
            WHERE chia_ca_id=? AND ca=?
        ''', (chia_ca_id, ca))
        conn.commit()
        conn.close()
