import logging
from core.search import search_algorithms
from core.scraper import scrape_algorithm
from core.evaluator import measure_execution_time
from core.reporter import generate_report
import json
import os

# Cấu hình log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Tạo thư mục lưu dữ liệu nếu chưa có
os.makedirs("data", exist_ok=True)

def main():
    logging.info("Bắt đầu tìm kiếm thuật toán...")
    urls = search_algorithms()
    
    algorithms = []
    for url in urls:
        logging.info(f"Đang lấy thuật toán từ {url}")
        code = scrape_algorithm(url)
        exec_time = measure_execution_time(code)
        algorithms.append({"url": url, "code": code, "time": exec_time})
    
    algorithms.sort(key=lambda x: x["time"])
    
    with open("data/algorithms.json", "w") as f:
        json.dump(algorithms, f, indent=4)
    
    generate_report(algorithms)
    
    logging.info("Hoàn thành! Xem kết quả trong data/report.txt")

if __name__ == "__main__":
    main()
