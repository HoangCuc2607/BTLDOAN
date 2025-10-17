from flask import Blueprint, request, jsonify
from models.NhanVien import NhanVien
from models.ChiaCa import ChiaCa
from models.DiemDanh import DiemDanh
from datetime import datetime

checkin_bp = Blueprint('checkin', __name__)

@checkin_bp.route('/diem_danh', methods=['POST'])
def diem_danh():
    data = request.json
    email = data.get('email')
    ca_num = data.get('ca')  # 1 = sáng, 2 = chiều, 3 = tối
    ngay = data.get('ngay')

    if not email or not ca_num or not ngay:
        return jsonify({'error': 'Thiếu dữ liệu'}), 400

    # Lấy thông tin nhân viên theo email
    nv = NhanVien.lay_theo_email(email)
    if not nv:
        return jsonify({'error': 'Không tìm thấy nhân viên'}), 404

    # Lấy ca theo ngày và số ca
    ca_info = ChiaCa.lay_ca_theo_ngay_va_so(ngay, ca_num)
    if not ca_info:
        return jsonify({'error': 'Ca chưa được thiết lập cho ngày này'}), 400

    # Chuyển giờ sang datetime.time
    start_time = datetime.strptime(ca_info['start'], "%H:%M").time()
    end_time = datetime.strptime(ca_info['end'], "%H:%M").time()
    now_time = datetime.now().time()

    # Xác định trạng thái điểm danh
    if now_time <= start_time:
        trang_thai = "Đã điểm danh"
    elif start_time < now_time <= end_time:
        trang_thai = "Đến muộn"
    else:
        trang_thai = "Chưa điểm danh"

    # Kiểm tra xem đã có bản ghi điểm danh cho ngày này chưa
    dd = DiemDanh.lay_diem_danh_theo_nhanvien(nv.ma_nhan_vien)
    dd_ngay = next((d for d in dd if d.ngay_diem_danh == ngay), None)
    if not dd_ngay:
        # Nếu chưa có, tạo mới
        new_dd = DiemDanh(nhanvien_id=nv.ma_nhan_vien, ngay_diem_danh=ngay)
        new_dd.them_diem_danh()

    # Cập nhật trạng thái ca
    ca_map = {1: 'sang', 2: 'chieu', 3: 'toi'}
    DiemDanh.cap_nhat_ca(nv.ma_nhan_vien, ngay, ca_map[ca_num], trang_thai)

    return jsonify({'message': 'Điểm danh thành công', 'trang_thai': trang_thai})
