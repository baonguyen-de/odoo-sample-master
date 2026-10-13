# Hướng dẫn Sao lưu (Backup) và Phục hồi (Restore) Dữ liệu Odoo qua CLI

Odoo cung cấp một công cụ dòng lệnh (CLI) mạnh mẽ để quản lý cơ sở dữ liệu. 

---

## Phần 1: Hướng dẫn Sao lưu (Backup)

Lệnh `db dump` cho phép bạn sao lưu toàn bộ dữ liệu của Odoo, bao gồm cả PostgreSQL database và Filestore (các tệp đính kèm, hình ảnh, tài liệu), thành một tệp `.zip` duy nhất.

### 1. Môi trường Docker Container

Trong môi trường Docker, Odoo và PostgreSQL thường chạy ở 2 container khác nhau. Do đó, khi gọi CLI từ container Odoo, bạn cần truyền thêm các tham số kết nối đến database (host, user, password) **trước** lệnh `dump`.

**Bước 1: Chạy lệnh sao lưu bên trong container Odoo**

Cú pháp chung:
```bash
docker exec -it <tên_container_odoo> odoo db --db_host <tên_host_db> -r <user_db> -w <mật_khẩu_db> dump <tên_database> <đường_dẫn_lưu_file_trong_container>
```

**Ví dụ thực tế:** 
Nếu container Odoo tên là `sample-odoo-1`, host của database là `db`, user/pass là `odoo`/`odooodoo`, và bạn muốn backup database tên là `sample` vào thư mục `/tmp/`:
```bash
docker exec -it sample-odoo-1 odoo db --db_host db -r odoo -w odooodoo dump sample /tmp/sample_backup.zip
```
*Lưu ý: Lệnh này sẽ tạo ra file `sample_backup.zip` nằm **bên trong** container.*

**Bước 2: Lấy file backup từ container ra máy tính thật (Host Machine)**

Để lấy file `.zip` vừa tạo ra ngoài, sử dụng lệnh `docker cp`:
```bash
docker cp sample-odoo-1:/tmp/sample_backup.zip ./sample_backup.zip
```
Lúc này, file `sample_backup.zip` đã nằm an toàn trên thư mục hiện tại của máy bạn.

### 2. Môi trường Chạy từ Source Code (Mã nguồn)

Khi bạn tải mã nguồn Odoo về chạy trực tiếp trên môi trường Linux/Ubuntu, lệnh thực thi chính là `odoo-bin`.

**Cú pháp cơ bản:**
```bash
./odoo-bin db dump <tên_database> <đường_dẫn_lưu_file.zip>
```

**Ví dụ:**
```bash
./odoo-bin db dump sample /tmp/sample_backup.zip
```

**Cú pháp nâng cao (Nếu cần chỉ định Host/User/Password):**
Giống như Docker, nếu PostgreSQL của bạn đòi hỏi mật khẩu hoặc khác host, bạn cũng truyền các biến kết nối **trước** lệnh `dump`:
```bash
./odoo-bin db --db_host localhost -r odoo -w odooodoo dump sample /tmp/sample_backup.zip
```

---

## Phần 2: Hướng dẫn Phục hồi (Restore)

Để khôi phục (restore) một database trong Odoo qua CLI, chúng ta sẽ sử dụng lệnh `load`. Quá trình này về cơ bản là ngược lại với lệnh `dump`.

### 1. Môi trường Docker Container

Đối với Docker, file backup của bạn (ví dụ `sample_backup.zip`) đang nằm ở máy tính thật (host). Bạn cần phải copy nó vào bên trong container Odoo trước khi chạy lệnh khôi phục.

**Bước 1: Copy file backup từ máy tính vào container Odoo**
Giả sử file backup của bạn đang nằm ở thư mục hiện tại:
```bash
docker cp ./sample_backup.zip sample-odoo-1:/tmp/sample_backup.zip
```

**Bước 2: Chạy lệnh khôi phục (load) bên trong container**
Giống lệnh dump, bạn vẫn cần truyền thông số kết nối Database (host, user, password) **trước** lệnh `load`. 

Cú pháp chung:
```bash
docker exec -it <tên_container_odoo> odoo db --db_host <tên_host_db> -r <user_db> -w <mật_khẩu_db> load <tên_database_mới> <đường_dẫn_file_backup_trong_container>
```

**Ví dụ:** Khôi phục ra một database mới tên là `sample_restored`:
```bash
docker exec -it sample-odoo-1 odoo db --db_host db -r odoo -w odooodoo load sample_restored /tmp/sample_backup.zip
```
*Lưu ý: Bạn có thể đặt tên database giống với tên cũ để ghi đè, nhưng nếu database cũ vẫn đang tồn tại hoặc đang có kết nối, bạn sẽ gặp lỗi. Tốt nhất là tạo một tên database mới hoặc dùng lệnh `drop` để xóa database cũ trước.*

### 2. Môi trường Chạy từ Source Code (Mã nguồn)

Trên môi trường chạy trực tiếp (như Ubuntu/Linux), bạn có thể trỏ thẳng tới file backup đang nằm trên máy tính mà không cần bước copy.

**Cú pháp cơ bản:**
```bash
./odoo-bin db load <tên_database_mới> <đường_dẫn_file_backup.zip>
```

**Ví dụ:**
```bash
./odoo-bin db load sample_restored /tmp/sample_backup.zip
```

**Nếu cần chỉ định Host/User/Password của PostgreSQL:**
```bash
./odoo-bin db --db_host localhost -r odoo -w odooodoo load sample_restored /tmp/sample_backup.zip
```

---

## Mẹo Bổ sung
- Lệnh `drop` để xóa database cũ nếu cần (nhớ thêm cờ kết nối database như `--db_host`):
  ```bash
  docker exec -it sample-odoo-1 odoo db --db_host db -r odoo -w odooodoo drop <tên_database_cần_xóa>
  ```
- Nếu bạn chỉ muốn backup cấu trúc Database (SQL) mà **không kèm** Filestore (giúp file nhẹ hơn, nhưng sẽ mất ảnh/đính kèm), bạn có thể thêm cờ `--no-filestore` ở cuối lệnh `dump`.
- Định dạng file sao lưu mặc định là chuẩn nén `.zip` chứa file `dump.sql` và thư mục `filestore` trừ khi bạn thay đổi sang `--format=dump`.

---

## Tài liệu tham khảo
- [Tài liệu chính thức Odoo 19: Command-line interface - Manage a database](https://www.odoo.com/documentation/19.0/developer/reference/cli.html#db-manage-a-database)
