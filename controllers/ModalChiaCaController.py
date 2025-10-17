from flask import Blueprint, request, jsonify
from models.ChiaCa import ChiaCa
from models.ChiaCaNhanVien import ChiaCaNhanVien

modal_chiaca = Blueprint('modal_chiaca', __name__)

# Lưu hoặc cập nhật ca và nhân viên
@modal_chiaca.route('/luu_chia_ca', methods=['POST'])
def luu_chia_ca():
    data = request.json
    ngay = data.get('ngay')
    gio_ca_sang = data.get('ca_sang')  # {'bat_dau':..., 'ket_thuc':..., 'nhanvien_ids':[...]}
    gio_ca_chieu = data.get('ca_chieu')
    gio_ca_toi = data.get('ca_toi')

    # 1. Lưu/Cập nhật ca
    ca_hien_tai = ChiaCa.lay_ca_theo_ngay(ngay)
    if ca_hien_tai:
        ca_hien_tai.gio_bat_dau_ca_sang = gio_ca_sang['bat_dau']
        ca_hien_tai.gio_ket_thuc_ca_sang = gio_ca_sang['ket_thuc']
        ca_hien_tai.gio_bat_dau_ca_chieu = gio_ca_chieu['bat_dau']
        ca_hien_tai.gio_ket_thuc_ca_chieu = gio_ca_chieu['ket_thuc']
        ca_hien_tai.gio_bat_dau_ca_toi = gio_ca_toi['bat_dau']
        ca_hien_tai.gio_ket_thuc_ca_toi = gio_ca_toi['ket_thuc']
        ca_hien_tai.cap_nhat_ca()
        chia_ca_id = ca_hien_tai.id
    else:
        ca_moi = ChiaCa(
            ngay=ngay,
            gio_bat_dau_ca_sang=gio_ca_sang['bat_dau'],
            gio_ket_thuc_ca_sang=gio_ca_sang['ket_thuc'],
            gio_bat_dau_ca_chieu=gio_ca_chieu['bat_dau'],
            gio_ket_thuc_ca_chieu=gio_ca_chieu['ket_thuc'],
            gio_bat_dau_ca_toi=gio_ca_toi['bat_dau'],
            gio_ket_thuc_ca_toi=gio_ca_toi['ket_thuc']
        )
        ca_moi.them_ca()
        chia_ca_id = ca_moi.id  # Nếu muốn, có thể lấy lại id từ DB

    # 2. Lưu nhân viên cho từng ca
    ChiaCaNhanVien.cap_nhat_nhan_vien_vao_ca(chia_ca_id, 'Sáng', gio_ca_sang['nhanvien_ids'])
    ChiaCaNhanVien.cap_nhat_nhan_vien_vao_ca(chia_ca_id, 'Chiều', gio_ca_chieu['nhanvien_ids'])
    ChiaCaNhanVien.cap_nhat_nhan_vien_vao_ca(chia_ca_id, 'Tối', gio_ca_toi['nhanvien_ids'])

    return jsonify({'message': 'Lưu chia ca thành công'})


# Lấy dữ liệu ca theo ngày (để load modal)
@modal_chiaca.route('/lay_chia_ca/<ngay>', methods=['GET'])
def lay_chia_ca(ngay):
    ca = ChiaCa.lay_ca_theo_ngay(ngay)
    if not ca:
        return jsonify({'error': 'Chưa có ca nào cho ngày này'}), 404

    data = {
        'ca_sang': {
            'bat_dau': ca.gio_bat_dau_ca_sang,
            'ket_thuc': ca.gio_ket_thuc_ca_sang,
            'nhanvien_ids': ChiaCaNhanVien.lay_nhan_vien_theo_ca(ca.id, 'Sáng')
        },
        'ca_chieu': {
            'bat_dau': ca.gio_bat_dau_ca_chieu,
            'ket_thuc': ca.gio_ket_thuc_ca_chieu,
            'nhanvien_ids': ChiaCaNhanVien.lay_nhan_vien_theo_ca(ca.id, 'Chiều')
        },
        'ca_toi': {
            'bat_dau': ca.gio_bat_dau_ca_toi,
            'ket_thuc': ca.gio_ket_thuc_ca_toi,
            'nhanvien_ids': ChiaCaNhanVien.lay_nhan_vien_theo_ca(ca.id, 'Tối')
        }
    }

    return jsonify(data)
