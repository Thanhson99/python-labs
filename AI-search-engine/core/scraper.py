import requests
from bs4 import BeautifulSoup

def scrape_algorithm(url):
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return {"url": url, "code": "Không thể lấy dữ liệu.", "time": "N/A"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Tìm code trong <pre>, <code>, hoặc class chứa code
    code_blocks = soup.find_all(["pre", "code"], class_=lambda x: x and "code" in x.lower())

    if not code_blocks:
        return {"url": url, "code": "Không tìm thấy code, có thể chỉ là bài viết mô tả.", "time": "N/A"}

    extracted_code = "\n".join([block.get_text() for block in code_blocks])
    
    return {"url": url, "code": extracted_code[:5000], "time": "0.0000"}
