from flask import Blueprint, render_template, request, jsonify
from models.NhanVien import NhanVien
from models.DiemDanh import DiemDanh
from datetime import date

trangchu = Blueprint('trangchu', __name__)

@trangchu.route('/trangchu')
def laydanhsachnhanvien():
    ngay_hien_tai = date.today().strftime('%Y-%m-%d')

    # Lấy toàn bộ danh sách nhân viên
    danh_sach_nhan_vien = NhanVien.lay_danh_sach_nhan_vien()

    # Lấy danh sách điểm danh của ngày hiện tại
    danh_sach_diem_danh = DiemDanh.lay_diem_danh_theo_ngay(ngay_hien_tai)
    diem_danh_dict = {dd.nhanvien_id: dd for dd in danh_sach_diem_danh}

    # Ghép trạng thái từng ca vào nhân viên
    for nv in danh_sach_nhan_vien:
        dd = diem_danh_dict.get(nv.ma_nhan_vien)
        if dd:
            nv.ca_sang = dd.ca_sang or "Chưa điểm danh"
            nv.ca_chieu = dd.ca_chieu or "Chưa điểm danh"
            nv.ca_toi = dd.ca_toi or "Chưa điểm danh"
        else:
            nv.ca_sang = nv.ca_chieu = nv.ca_toi = "Chưa điểm danh"

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
    
# ✅ Route lấy toàn bộ thông tin nhân viên kèm trạng thái điểm danh hôm nay
@trangchu.route('/thong_tin_nhan_vien_day_du', methods=['GET'])
def thong_tin_nhan_vien_day_du():
    today = date.today().isoformat()

    danh_sach_nhan_vien = NhanVien.lay_danh_sach_nhan_vien()
    danh_sach_diem_danh = DiemDanh.lay_diem_danh_theo_ngay(today)

    # Tạo map {nhanvien_id: trang_thai}
    trang_thai_map = {dd.nhanvien_id: dd.trang_thai for dd in danh_sach_diem_danh}

    # Ghép dữ liệu nhân viên + trạng thái điểm danh
    ket_qua = []
    for nv in danh_sach_nhan_vien:
        ket_qua.append({
            'ma_nhan_vien': nv.ma_nhan_vien,
            'ho_ten': nv.ho_ten,
            'so_dien_thoai': nv.so_dien_thoai,
            'dia_chi': nv.dia_chi,
            'gioi_tinh': nv.gioi_tinh,
            'email': nv.email,
            'ngay_sinh': nv.ngay_sinh,
            'trang_thai_diem_danh': trang_thai_map.get(nv.ma_nhan_vien, 'Chưa điểm danh')
        })
    
    return jsonify(ket_qua)