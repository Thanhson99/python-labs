from difflib import SequenceMatcher

def is_similar(text1, text2, threshold=0.85):
    """Kiểm tra hai đoạn văn bản có giống nhau không (dựa trên mức độ giống nhau)."""
    return SequenceMatcher(None, text1, text2).ratio() > threshold

def remove_duplicates(news_list):
    """Loại bỏ các tin tức trùng lặp dựa trên title, link hoặc nội dung tương tự."""
    seen_titles = set()  # Lưu tiêu đề đã xuất hiện
    seen_links = set()   # Lưu link đã xuất hiện
    filtered_news = []   # Danh sách tin đã lọc

    for news in news_list:
        title = news["title"].strip()
        link = news["link"].strip()
        summary = news["summary"].strip()

        # Nếu tiêu đề hoặc link đã tồn tại → bỏ qua
        if title in seen_titles or link in seen_links:
            continue

        # Kiểm tra xem có bài viết nào trước đó quá giống không
        is_duplicate = any(is_similar(summary, existing["summary"]) for existing in filtered_news)
        if is_duplicate:
            continue

        # Nếu là bài mới, thêm vào danh sách
        seen_titles.add(title)
        seen_links.add(link)
        filtered_news.append(news)

    return filtered_news
