import requests

def fetch_url_content(url):
    try:
        # Gửi yêu cầu GET đến URL
        response = requests.get(url)
        # Kiểm tra mã trạng thái HTTP
        response.raise_for_status()  # Nếu không phải 200, sẽ gây ra một lỗi
        # Trả về nội dung của phản hồi
        return response.text
    except requests.exceptions.RequestException as e:
        # Xử lý lỗi nếu có vấn đề khi truy cập URL
        print(f"Error accessing {url}: {e}")
        return None

if __name__ == "__main__":
    url = input("Enter URL: ")
    content = fetch_url_content(url)
    if content:
        print(content)
