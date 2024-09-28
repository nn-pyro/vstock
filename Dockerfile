# Chọn hình ảnh nền
FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /vstock_chat

# Sao chép tệp requirements.txt vào hình ảnh
COPY requirements.txt .

# Cài đặt các phụ thuộc
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn ứng dụng vào hình ảnh
COPY . .

# Mở cổng cho ứng dụng
EXPOSE 8501

# Lệnh chạy ứng dụng
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
