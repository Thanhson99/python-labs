📂 AI_Search_Engine
│── 📂 data                  # Lưu kết quả tìm kiếm & báo cáo
│    ├── algorithms.json     # Lưu thuật toán đã thu thập
│    ├── report.txt          # Báo cáo cuối cùng
│
│── 📂 core                  # Code chính để AI hoạt động
│    ├── search.py           # Tìm kiếm thuật toán trên Google
│    ├── scraper.py          # Trích xuất thuật toán từ trang web
│    ├── evaluator.py        # Kiểm tra hiệu suất thuật toán
│    ├── trainer.py          # Tự học & chọn thuật toán tốt nhất
│    ├── reporter.py         # Ghi báo cáo kết quả
│
│── 📂 utils                 # Công cụ hỗ trợ (log, xử lý văn bản, v.v.)
│    ├── logger.py           # Ghi log
│    ├── text_processor.py   # Xử lý văn bản từ web
│
│── config.py                # Cấu hình API key và cài đặt chung
│── main.py                  # Chạy toàn bộ chương trình
│── requirements.txt         # Danh sách thư viện cần cài đặt
│── README.md                # Hướng dẫn sử dụng


Chi tiết từng file và chức năng

1️⃣ core/search.py 📌 (Tìm kiếm thuật toán trên Google)
    Sử dụng Google Search API để lấy link các bài viết chứa thuật toán.
    Trả về danh sách URL liên quan.
2️⃣ core/scraper.py 📌 (Trích xuất thuật toán từ trang web)
    Lấy nội dung từ URL tìm được.
    Lọc đoạn code từ <code> hoặc <pre> trong HTML.
3️⃣ core/evaluator.py 📌 (Đánh giá hiệu suất thuật toán)
    Chạy thử các thuật toán thu thập được.
    Đo thời gian thực thi để tìm thuật toán nhanh nhất.
4️⃣ core/trainer.py 📌 (AI tự học thuật toán tốt nhất)
    Chạy nhiều thuật toán, so sánh kết quả.
    Chọn thuật toán nhanh nhất để lưu lại.
5️⃣ core/reporter.py 📌 (Ghi báo cáo kết quả)
    Tổng hợp tất cả thuật toán thu thập được.
    Xuất báo cáo ra data/report.txt.
6️⃣ utils/logger.py 📌 (Ghi log)
    Ghi lại tiến trình AI (tìm kiếm, trích xuất, thử nghiệm).
7️⃣ utils/text_processor.py 📌 (Xử lý văn bản từ web)
    Loại bỏ quảng cáo, đoạn không liên quan trong trang web.
8️⃣ config.py 📌 (Cấu hình API Key & setting chung)
    Lưu trữ API Key cho Google Search API.
9️⃣ main.py 📌 (Chạy AI)
    Điều phối toàn bộ các bước tìm kiếm, trích xuất, kiểm tra, báo cáo.

* Run command line:

mkdir AI-search-engine && cd AI-search-engine
pip install -r requirements.txt

* Testing:

python main.py

* Output:

data/report.txt

Ex:

🔍 Tìm thấy 5 thuật toán từ Google:

1️⃣ Thuật toán Bubble Sort từ geeksforgeeks.org
    - Code:
        def bubble_sort(arr): ...
    - Thời gian thực thi: 0.002s

2️⃣ Thuật toán Quick Sort từ tutorialspoint.com
    - Code:
        def quick_sort(arr): ...
    - Thời gian thực thi: 0.001s

✅ Thuật toán tốt nhất: Quick Sort (Nhanh nhất: 0.001s)
