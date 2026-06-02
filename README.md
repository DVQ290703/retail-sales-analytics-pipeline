## Cách chạy dự án

### 1. Clone repository

```bash
git clone <repository-url>
cd retail-data-pipeline
```

### 2. Tạo môi trường ảo

```bash
python -m venv venv
```

Windows:

```bash
source venv/Scripts/activate
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 4. Chuẩn bị dữ liệu

Tải bộ dữ liệu Online Retail và đặt vào:

```text
data/raw/online_retail.xlsx
```

### 5. Chạy ETL Pipeline

```bash
python src/pipeline.py
```

Kết quả:

```text
data/processed/cleaned_online_retail.csv
retail_dw.duckdb
```

### 6. Xây dựng Data Warehouse

```bash
python src/build_dw.py
```

### 7. Kiểm tra các bảng

```bash
python src/check_dw.py
```

### 8. Tạo báo cáo phân tích

```bash
python src/analytics_report.py
```

Kết quả được lưu tại:

```text
reports/output/
```