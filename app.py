from flask import Flask, render_template, redirect, url_for, request, session
from controllers.DangKyNhanVienController import dangkynhanvien
from controllers.TrangChuController import trangchu
from controllers.ModalChiaCaController import modal_chiaca
from controllers.ModalDiemDanhController import checkin_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # cần để sử dụng session

app.register_blueprint(trangchu)
app.register_blueprint(dangkynhanvien)
app.register_blueprint(modal_chiaca)
app.register_blueprint(checkin_bp)

# Trang đăng nhập
@app.route('/', methods=['GET', 'POST'])
def dangnhap():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == 'admin@gmail.com' and password == 'abc123':
            session['logged_in'] = True
            return redirect(url_for('trangchu_index'))
        else:
            return render_template('dangnhap.html', error='Email hoặc mật khẩu sai!')
    return render_template('dangnhap.html', error=None)

# Trang chủ (bảo vệ bằng session)
@app.route('/trangchu')
def trangchu_index():
    if not session.get('logged_in'):
        return redirect(url_for('dangnhap'))
    return render_template('trangchu.html')

# Trang đăng ký nhân viên
@app.route('/dangkynhanvien')
def dangky():
    return render_template('dangkynhanvien.html')

@app.route('/dangxuat')
def dangxuat():
    session.pop('logged_in', None)  # Xóa session đăng nhập
    return redirect(url_for('dangnhap'))  # Quay về trang đăng nhập

if __name__ == '__main__':
    app.run(debug=True)
