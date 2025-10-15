from flask import Flask, render_template
from controllers.DangKyNhanVienController import dangkynhanvien
from controllers.TrangChuController import trangchu


app = Flask(__name__)
app.register_blueprint(trangchu)
app.register_blueprint(dangkynhanvien)
@app.route('/')
def trangchu():
    return render_template('trangchu.html')

@app.route('/dangkynhanvien')
def dangky():
    return render_template('dangkynhanvien.html')

# Đăng ký blueprint
if __name__ == '__main__':
    app.run(debug=True)
