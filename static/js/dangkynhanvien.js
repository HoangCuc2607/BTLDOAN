document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');

    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Ngăn form submit mặc định

        // Lấy dữ liệu từ form
        const ho_ten = form.querySelector('input[type="text"]').value;
        const so_dien_thoai = form.querySelector('input[placeholder="0123456789"]').value;
        const dia_chi = form.querySelector('input[placeholder^="Số nhà"]').value;
        const ngay_sinh = form.querySelector('input[type="date"]').value;
        const email = form.querySelector('input[type="email"]').value;
        const gioi_tinh = form.querySelector('select').value;

        // Gửi dữ liệu lên server
        fetch('/dang_ky_nhan_vien', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ho_ten, so_dien_thoai, dia_chi, ngay_sinh, email, gioi_tinh })
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                form.reset(); // reset form sau khi thêm thành công
            } else if (data.error) {
                alert("Lỗi: " + data.error);
            }
        })
        .catch(err => console.error(err));
    });
});
