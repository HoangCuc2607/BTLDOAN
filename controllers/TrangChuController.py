from flask import Blueprint, render_template, request, jsonify
from models.NhanVien import NhanVien

trangchu = Blueprint('trangchu', __name__)

@trangchu.route('/')
def laydanhsachnhanvien():
    # Lấy danh sách nhân viên từ database
    danh_sach_nhan_vien = NhanVien.lay_danh_sach_nhan_vien()
    return render_template('trangchu.html', danh_sach_nhan_vien=danh_sach_nhan_vien)

# Route lấy thông tin 1 nhân viên dựa vào id (GET)
@trangchu.route('/sua_nhan_vien', methods=['GET', 'POST'])
def sua_nhan_vien():
    if request.method == 'GET':
        # Lấy id từ query param
        ma_nhan_vien = request.args.get('id')
        if not ma_nhan_vien:
            return jsonify({'error': 'Không có id nhân viên'}), 400
        
        nv = NhanVien.lay_thong_tin_nhan_vien(ma_nhan_vien)
        if nv:
            return jsonify({
                'ma_nhan_vien': nv.ma_nhan_vien,
                'ho_ten': nv.ho_ten,
                'so_dien_thoai': nv.so_dien_thoai,
                'dia_chi': nv.dia_chi,
                'gioi_tinh': nv.gioi_tinh,
                'email': nv.email,
                'ngay_sinh': nv.ngay_sinh
            })
        else:
            return jsonify({'error': 'Không tìm thấy nhân viên'}), 404

    elif request.method == 'POST':
        # Lấy dữ liệu từ form hoặc JSON
        data = request.json
        ma_nhan_vien = data.get('ma_nhan_vien')
        ho_ten = data.get('ho_ten')
        so_dien_thoai = data.get('so_dien_thoai')
        dia_chi = data.get('dia_chi')
        gioi_tinh = data.get('gioi_tinh')
        email = data.get('email')
        ngay_sinh = data.get('ngay_sinh')

        success = NhanVien.cap_nhat_nhan_vien_theo_id(ma_nhan_vien, ho_ten, so_dien_thoai, dia_chi, gioi_tinh, email, ngay_sinh)
        if success:
            return jsonify({'message': 'Cập nhật thành công'})
        else:
            return jsonify({'error': 'Cập nhật thất bại'}), 400
        
@trangchu.route('/xoa_nhan_vien', methods=['POST'])
def xoa_nhan_vien():
    """
    Xóa nhân viên dựa trên ma_nhan_vien gửi từ client.
    Yêu cầu JSON: { "ma_nhan_vien": 1 }
    """
    data = request.json
    ma_nhan_vien = data.get('ma_nhan_vien')
        
    if not ma_nhan_vien:
        return jsonify({'error': 'Thiếu ma_nhan_vien'}), 400

    try:
        NhanVien.xoa_nhan_vien(ma_nhan_vien)
        return jsonify({'message': 'Xóa nhân viên thành công'})
    except Exception as e:
        return jsonify({'error': f'Xóa thất bại: {str(e)}'}), 500