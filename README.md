# Công cụ chuyển đổi Azota sang Anki

Một công cụ dòng lệnh (CLI) bằng Python để chuyển đổi file kết quả thi trắc nghiệm HTML từ Azota thành các thẻ flashcard có thể nhập vào Anki (định dạng CSV).

## Tính năng

-   **Tự động phân tích**: Trích xuất câu hỏi, các lựa chọn và đáp án đúng từ trang kết quả Azota.
-   **Tương thích Anki**: Tạo file CSV sẵn sàng để nhập vào Anki (ngăn cách bằng dấu chấm phẩy).
-   **Phát hiện thông minh**: Cảnh báo nếu câu hỏi chưa được tải đầy đủ (các khối skeleton/loading) trong file HTML.
-   **Xử lý hàng loạt**: Xử lý một file cụ thể hoặc tất cả các file trong thư mục đầu vào.

## Yêu cầu

-   Python 3.12+
-   `uv` (khuyên dùng để quản lý gói)

## Cài đặt

1.  Clone repository:
    ```bash
    git clone https://github.com/dngphuu/azota-to-anki.git
    cd azota-to-anki
    ```

2.  Cài đặt các thư viện phụ thuộc:
    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```

## Hướng dẫn sử dụng

1.  **Chuẩn bị đầu vào**:
    -   Mở trang kết quả thi Azota của bạn trên trình duyệt.
    -   **Cuộn xuống cuối trang** để đảm bảo tất cả các câu hỏi đã được tải xong.
    -   Lưu trang dưới dạng HTML (Ctrl+S).
    -   Đặt (các) file HTML đã lưu vào thư mục `input`.

2.  **Chạy công cụ**:
    ```bash
    uv run python azota_to_anki.py
    ```

3.  **Chọn file**:
    -   Công cụ sẽ liệt kê các file HTML có sẵn.
    -   Nhập số thứ tự của file cần xử lý, hoặc gõ `all` để xử lý tất cả.

4.  **Nhập vào Anki**:
    -   Mở Anki.
    -   Vào **File** -> **Import**.
    -   Chọn file `.csv` đã được tạo trong thư mục `output`.
    -   **Cài đặt**:
        -   Dấu ngăn cách (Separator): **Semicolon (;)** (Dấu chấm phẩy)
        -   Cho phép HTML trong các trường (Allow HTML in fields): **Đã chọn**
        -   Ánh xạ Trường 1 sang **Front** (Mặt trước) và Trường 2 sang **Back** (Mặt sau).

## Cấu trúc dự án

```
azota-to-anki/
├── input/          # Đặt các file HTML vào đây
├── output/         # Các file CSV kết quả sẽ xuất hiện ở đây
├── azota_to_anki.py # Script chính
├── requirements.txt
└── README.md
```

## Giấy phép

MIT
