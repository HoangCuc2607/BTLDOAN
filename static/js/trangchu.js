
document.addEventListener('DOMContentLoaded', function() {
    // === Điểm danh ===
    var checkInMenu = document.getElementById('checkInMenu');
    var checkInBtn = document.getElementById('checkInBtn');

    if(checkInMenu) {
        checkInMenu.addEventListener('click', function() {
            var myModal = new bootstrap.Modal(document.getElementById('checkInModal'));
            myModal.show();
        });
    }

    if(checkInBtn) {
        checkInBtn.addEventListener('click', function() {
            var email = document.getElementById('employeeEmail').value;
            if(email) {
                alert("Điểm danh thành công: " + email);
                bootstrap.Modal.getInstance(document.getElementById('checkInModal')).hide();
            } else {
                alert("Vui lòng nhập email!");
            }
        });
    }

    // === Sửa/Xóa nhân viên ===
    var editModal = new bootstrap.Modal(document.getElementById('editModal'));
    var deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    var currentRow = null;


        // document.querySelectorAll('.btn-edit').forEach(function(btn){
        //     btn.addEventListener('click', function() {
        //         var currentRow = btn.closest('tr');
        //         var employeeId = currentRow.dataset.id; // Lấy id nhân viên

        //         // TODO: gọi AJAX hoặc fetch dữ liệu từ server bằng employeeId
        //         // Ví dụ giả lập:
        //         // fetch(`/api/nhanvien/${employeeId}`)
        //         //    .then(res => res.json())
        //         //    .then(data => {
        //         //        document.getElementById('editName').value = data.ho_ten;
        //         //        document.getElementById('editPhone').value = data.so_dien_thoai;
        //         //        document.getElementById('editEmail').value = data.email;
        //         //        ...
        //         //    });

        //         // Hiện modal luôn (tạm thời nếu chưa kết nối backend)
        //         var editModal = new bootstrap.Modal(document.getElementById('editModal'));
        //         editModal.show();
        //     });
        // });

        document.querySelectorAll('.btn-edit').forEach(function(btn){
    btn.addEventListener('click', function() {
        var currentRow = btn.closest('tr');
        var employeeId = currentRow.dataset.id;

        // Gọi backend GET để lấy thông tin nhân viên
        fetch(`/sua_nhan_vien?id=${employeeId}`)
            .then(res => res.json())
            .then(data => {
                if(data.error){
                    alert(data.error);
                    return;
                }

                document.getElementById('editName').value = data.ho_ten;
                document.getElementById('editPhone').value = data.so_dien_thoai;
                document.getElementById('editEmail').value = data.email;
                document.getElementById('editAddress').value = data.dia_chi;
                document.getElementById('editGender').value = data.gioi_tinh;
                document.getElementById('editBirthDate').value = data.ngay_sinh;
                document.getElementById('editModal').dataset.id = employeeId;

                var editModal = new bootstrap.Modal(document.getElementById('editModal'));
                editModal.show();
            })
            .catch(err => console.error(err));
    });
});

    document.getElementById('saveEditBtn').addEventListener('click', function(){
    var employeeId = document.getElementById('editModal').dataset.id;

    var payload = {
        ma_nhan_vien: employeeId,
        ho_ten: document.getElementById('editName').value,
        so_dien_thoai: document.getElementById('editPhone').value,
        email: document.getElementById('editEmail').value,
        dia_chi: document.getElementById('editAddress').value,
        gioi_tinh: document.getElementById('editGender').value,
        ngay_sinh: document.getElementById('editBirthDate').value
    };

    fetch(`/sua_nhan_vien`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if(data.message){
            alert(data.message);
            location.reload(); // tải lại bảng
        } else {
            alert(data.error);
        }
    });
});


 

    document.querySelectorAll('.btn-delete').forEach(function(btn){
    btn.addEventListener('click', function() {
        var currentRow = btn.closest('tr');
        var employeeId = currentRow.dataset.id;

        if(confirm("Bạn có chắc muốn xóa nhân viên này không?")){
            fetch('/xoa_nhan_vien', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ma_nhan_vien: employeeId})
            })
            .then(res => res.json())
            .then(data => {
                if(data.message){
                    alert(data.message);
                    currentRow.remove(); // xóa dòng khỏi bảng
                } else {
                    alert(data.error);
                }
            });
        }
    });
});

});
