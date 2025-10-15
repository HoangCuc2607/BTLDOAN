
from flask import Blueprint, request, jsonify
from models.NhanVien import NhanVien

dangkynhanvien = Blueprint('dangkynhanvien', __name__)

@dangkynhanvien.route('/dang_ky_nhan_vien', methods=['POST'])
def dang_ky_nhan_vien():
    data = request.json
    try:
        nv = NhanVien(
            ho_ten=data.get('ho_ten'),
            so_dien_thoai=data.get('so_dien_thoai'),
            dia_chi=data.get('dia_chi'),
            gioi_tinh=data.get('gioi_tinh'),
            email=data.get('email'),
            ngay_sinh=data.get('ngay_sinh')
        )
        nv.them_nhan_vien()
        return jsonify({'message': 'Thêm nhân viên thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
