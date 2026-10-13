# Note code — Docker khi dev Odoo

Cheatsheet dùng trong workshop. Copy lệnh, **đổi tên database** cho đúng DB của mình, rồi chạy.

Thông tin môi trường mẫu:

| Thứ | Giá trị |
|-----|---------|
| Container Odoo | `19-odoo-1` |
| Web | http://localhost:8869 |
| DB host (trong Docker) | `db` |
| DB user | `odoo` |
| DB password | `odooodoo` |
| Custom addons | `./custom_addons` |

Tên database **không cố định**. Ví dụ workshop: `PAT_290526`, `demo-elearning`. Đổi `-d TÊN_DB` cho khớp DB mình đang dùng.

---

## 1. Bật / tắt môi trường

```bash
# Bật Odoo + PostgreSQL (chạy nền)
docker compose up -d

# Tắt (giữ data)
docker compose down

# Tắt và XÓA hết data (DB, filestore) — chỉ dùng khi muốn làm lại từ đầu
docker compose down -v
```

Lần đầu: mở http://localhost:8869 → tạo database → Apps → cài module.

---

## 2. Xem log khi lỗi

Khi Odoo không lên, module update fail, hoặc màn hình trắng — xem log trước.

```bash
# Theo dõi log realtime (Ctrl+C để thoát, container vẫn chạy)
docker logs -f 19-odoo-1
```

```bash
# Chỉ lấy 100 dòng log gần nhất (không theo dõi)
docker logs --tail 100 19-odoo-1
```

Nếu không nhớ tên container:

```bash
docker compose ps
```

---

## 3. Update module (lệnh dùng nhiều nhất khi dev)

Chạy **thêm 1 process Odoo** trong container đang sống: load module → ghi thay đổi vào DB → process đó tắt (`--stop-after-init`). Web server chính vẫn chạy.

```bash
docker exec -it 19-odoo-1 odoo \
  -d PAT_290526 \
  -u all \
  --stop-after-init \
  --db_host=db \
  --db_user=odoo \
  --db_password=odooodoo
```

Giải thích từng cờ:

| Cờ | Ý nghĩa |
|----|---------|
| `docker exec -it 19-odoo-1` | Chạy lệnh trong container Odoo |
| `odoo` | Gọi binary Odoo |
| `-d PAT_290526` | Database cần update. **Đổi thành DB của mình** |
| `-u all` | Upgrade **tất cả** module đã cài |
| `--stop-after-init` | Update xong thì thoát process này (không chiếm cổng) |
| `--db_host=db` | Host Postgres trong docker-compose (service `db`) |
| `--db_user=odoo` | User DB |
| `--db_password=odooodoo` | Password DB |

Chỉ update 1 module (nhanh hơn `-u all`):

```bash
docker exec -it 19-odoo-1 odoo \
  -d PAT_290526 \
  -u ps_accounting_sample \
  --stop-after-init \
  --db_host=db \
  --db_user=odoo \
  --db_password=odooodoo
```

`-u` nhận technical name trong `__manifest__.py` (thư mục module), không phải tên hiện trên Apps.

---

## 4. Khi nào restart Docker, khi nào chỉ update module

### Sửa file Python (`models/*.py`, `__manifest__.py`, `__init__.py`, ...)

Python được load lúc process Odoo **start**. Sửa xong cần restart container, rồi update module để DB nhận field / model mới.

```bash
docker compose down
docker compose up -d
```

Đợi Odoo lên (hoặc `docker logs -f 19-odoo-1`), rồi:

```bash
docker exec -it 19-odoo-1 odoo \
  -d PAT_290526 \
  -u all \
  --stop-after-init \
  --db_host=db \
  --db_user=odoo \
  --db_password=odooodoo
```

Cách ngắn hơn (không `down` hết stack):

```bash
docker compose restart odoo
```

Rồi chạy lệnh `-u` như trên.

### Sửa XML (views, menu, security CSV, demo data)

Thường **không cần** restart. Chỉ `-u` module.

```bash
docker exec -it 19-odoo-1 odoo \
  -d PAT_290526 \
  -u ps_accounting_sample \
  --stop-after-init \
  --db_host=db \
  --db_user=odoo \
  --db_password=odooodoo
```

Xong thì **hard refresh** trình duyệt (`Ctrl+Shift+R`).

---

## 5. Copy-paste theo tình huống

### A. Sửa Python → restart + update all

```bash
docker compose down
docker compose up -d

docker exec -it 19-odoo-1 odoo -d PAT_290526 -u all --stop-after-init --db_host=db --db_user=odoo --db_password=odooodoo
```

### B. Sửa XML / views → chỉ update module

```bash
docker exec -it 19-odoo-1 odoo -d PAT_290526 -u ps_accounting_sample --stop-after-init --db_host=db --db_user=odoo --db_password=odooodoo
```

### C. Lỗi, cần đọc log

```bash
docker logs -f 19-odoo-1
```

### D. DB khác (ví dụ workshop elearning)

```bash
docker exec -it 19-odoo-1 odoo -d demo-elearning -u all --stop-after-init --db_host=db --db_user=odoo --db_password=odooodoo
```

Đổi `PAT_290526` / `demo-elearning` thành tên DB trên màn hình login Odoo.

---

## 6. Lỗi hay gặp

| Hiện tượng | Việc nên làm |
|------------|----------------|
| `database does not exist` | Sai `-d`. Vào http://localhost:8869 xem đúng tên DB |
| Container not found `19-odoo-1` | Chưa `docker compose up -d`, hoặc tên khác → `docker compose ps` |
| Sửa Python rồi F5 vẫn không đổi | Chưa restart container |
| Sửa XML rồi F5 vẫn không đổi | Chưa `-u` module, hoặc chưa hard refresh |
| Update xong web chết / không vào được | Xem `docker logs -f 19-odoo-1`, sửa traceback, restart lại |

Module mới **chưa từng Install** thì `-u` không đủ. Vào **Apps** (bật Developer Mode nếu cần) → Install, hoặc:

```bash
docker exec -it 19-odoo-1 odoo \
  -d PAT_290526 \
  -i ps_accounting_sample \
  --stop-after-init \
  --db_host=db \
  --db_user=odoo \
  --db_password=odooodoo
```

`-i` = install, `-u` = upgrade module đã cài.
