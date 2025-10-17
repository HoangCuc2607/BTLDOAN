import sqlite3

class ChiaCa:
    def __init__(self, id=None, ngay="", 
                 gio_bat_dau_ca_sang="", gio_ket_thuc_ca_sang="",
                 gio_bat_dau_ca_chieu="", gio_ket_thuc_ca_chieu="",
                 gio_bat_dau_ca_toi="", gio_ket_thuc_ca_toi=""):
        self.id = id
        self.ngay = ngay
        self.gio_bat_dau_ca_sang = gio_bat_dau_ca_sang
        self.gio_ket_thuc_ca_sang = gio_ket_thuc_ca_sang
        self.gio_bat_dau_ca_chieu = gio_bat_dau_ca_chieu
        self.gio_ket_thuc_ca_chieu = gio_ket_thuc_ca_chieu
        self.gio_bat_dau_ca_toi = gio_bat_dau_ca_toi
        self.gio_ket_thuc_ca_toi = gio_ket_thuc_ca_toi

    # Thêm ca mới
    def them_ca(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ChiaCa (ngay, gio_bat_dau_ca_sang, gio_ket_thuc_ca_sang,
                                gio_bat_dau_ca_chieu, gio_ket_thuc_ca_chieu,
                                gio_bat_dau_ca_toi, gio_ket_thuc_ca_toi)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.ngay, self.gio_bat_dau_ca_sang, self.gio_ket_thuc_ca_sang,
            self.gio_bat_dau_ca_chieu, self.gio_ket_thuc_ca_chieu,
            self.gio_bat_dau_ca_toi, self.gio_ket_thuc_ca_toi))
        self.id = cursor.lastrowid  # <--- quan trọng
        conn.commit()
        conn.close()
        return self.id


    # Cập nhật ca đã tồn tại
    def cap_nhat_ca(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE ChiaCa
            SET gio_bat_dau_ca_sang=?, gio_ket_thuc_ca_sang=?,
                gio_bat_dau_ca_chieu=?, gio_ket_thuc_ca_chieu=?,
                gio_bat_dau_ca_toi=?, gio_ket_thuc_ca_toi=?
            WHERE ngay=?
        ''', (self.gio_bat_dau_ca_sang, self.gio_ket_thuc_ca_sang,
              self.gio_bat_dau_ca_chieu, self.gio_ket_thuc_ca_chieu,
              self.gio_bat_dau_ca_toi, self.gio_ket_thuc_ca_toi,
              self.ngay))
        conn.commit()
        conn.close()

    # Lấy thông tin ca theo ngày
    @staticmethod
    def lay_ca_theo_ngay(ngay):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM ChiaCa WHERE ngay=?
        ''', (ngay,))
        record = cursor.fetchone()
        conn.close()
        if record:
            return ChiaCa(*record)
        return None
    @staticmethod
    def lay_ca_theo_ngay_va_so(ngay, so_ca):
        """
        Lấy ca theo ngày và số ca (1 = sáng, 2 = chiều, 3 = tối)
        Trả về dict {'start': ..., 'end': ...} hoặc None nếu không có
        """
        ca = ChiaCa.lay_ca_theo_ngay(ngay)
        if not ca:
            return None
        if so_ca == 1:
            return {'start': ca.gio_bat_dau_ca_sang, 'end': ca.gio_ket_thuc_ca_sang}
        elif so_ca == 2:
            return {'start': ca.gio_bat_dau_ca_chieu, 'end': ca.gio_ket_thuc_ca_chieu}
        elif so_ca == 3:
            return {'start': ca.gio_bat_dau_ca_toi, 'end': ca.gio_ket_thuc_ca_toi}
        return None
