# Hướng dẫn Sao lưu và Phục hồi Dữ liệu Odoo qua Giao diện Web

Ngoài công cụ dòng lệnh (CLI), Odoo cung cấp sẵn một giao diện web trực quan, thân thiện giúp người dùng dễ dàng thực hiện việc sao lưu (backup) và phục hồi (restore) cơ sở dữ liệu chỉ với vài cú click chuột.

---

## 1. Truy cập Trình quản lý Cơ sở dữ liệu (Database Manager)

Để thực hiện bất kỳ thao tác quản lý database nào qua giao diện, bạn cần truy cập vào trang Database Manager của Odoo.

1. Mở trình duyệt web.
2. Truy cập vào đường dẫn sau:
   ```
   http://<tên-miền-hoặc-ip>:<cổng>/web/database/manager
   ```
   **Ví dụ:** Nếu bạn đang chạy hệ thống cục bộ (như ở các bước trước), đường dẫn sẽ là: `http://localhost:8869/web/database/manager`

---

## 2. Hướng dẫn Sao lưu (Backup) Database

Tại trang Database Manager, bạn sẽ thấy danh sách các database đang có trên hệ thống của mình.

1. Tìm tên database bạn muốn sao lưu (ví dụ: `sample`).
2. Bấm vào nút **Backup** nằm ngay bên cạnh tên database đó.
3. Một cửa sổ (pop-up) sẽ hiện ra yêu cầu bạn điền thông tin:
   - **Master Password:** Nhập mật khẩu quản trị hệ thống Odoo của bạn (đây là mật khẩu bảo vệ trình quản lý database, được thiết lập khi cài đặt Odoo).
   - **Backup Format (Định dạng sao lưu):** 
     - Chọn `zip (includes filestore)`: Lựa chọn tốt nhất, sao lưu cả dữ liệu database lẫn các file đính kèm/hình ảnh.
     - Chọn `pg_dump custom format (without filestore)`: Chỉ sao lưu dữ liệu database, file sẽ nhẹ hơn nhưng mất file đính kèm.
4. Bấm nút **Backup**. 
5. Đợi một lát (thời gian tùy thuộc vào dung lượng database), trình duyệt sẽ tự động tải xuống file backup (thường là file `.zip`).

---

## 3. Hướng dẫn Phục hồi (Restore) Database

Để khôi phục lại dữ liệu từ một file backup có sẵn (.zip hoặc .dump), bạn cũng thực hiện trên trang Database Manager.

1. Tại trang chính của Database Manager, tìm và bấm vào nút **Restore Database** (thường nằm ở phía trên cùng hoặc dưới cùng danh sách database).
2. Điền các thông tin yêu cầu trong cửa sổ hiện ra:
   - **Master Password:** Nhập mật khẩu quản trị hệ thống Odoo.
   - **File:** Chọn file backup từ máy tính của bạn (ví dụ: `sample_backup.zip`).
   - **Database Name:** Đặt tên cho database mới sẽ được phục hồi (có thể là tên cũ để ghi đè, hoặc tốt nhất là đặt tên mới để an toàn, ví dụ: `sample_restored`).
   - **This database is a copy:** (Tùy chọn) Đánh dấu check vào ô này nếu bạn đang phục hồi bản sao để làm môi trường test. Điều này giúp Odoo vô hiệu hóa các cronjob gửi email hoặc đồng bộ dữ liệu để tránh xung đột với hệ thống thật.
3. Bấm nút **Continue** (hoặc Restore).
4. Odoo sẽ tải file lên và tiến hành giải nén, khôi phục dữ liệu. Khi quá trình hoàn tất, bạn sẽ thấy tên database mới xuất hiện trong danh sách.

---

## 4. Lưu ý Quan trọng
- **Master Password:** Hãy lưu trữ Master Password cẩn thận, vì không có nó bạn sẽ không thể thực hiện các thao tác quản lý database qua giao diện web.
- **Giới hạn dung lượng tải lên:** Nếu file backup quá lớn (vài GB), việc restore qua giao diện web có thể bị lỗi do timeout hoặc giới hạn cấu hình proxy/server (như Nginx, Apache). Trong trường hợp đó, bạn bắt buộc phải dùng phương pháp **CLI** đã được hướng dẫn ở bài trước.