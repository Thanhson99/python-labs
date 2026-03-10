from modules.news.deduplicator import remove_duplicates

def generate_summary(news_list):
    """Tổng hợp tin tức thành 1 bài viết"""
    news_list = remove_duplicates(news_list)  # Loại bỏ bài trùng

    if not news_list:
        return "⚠️ Hiện tại không có tin tức mới nào phù hợp!"

    summary_text = "🚀 *Bản tin Crypto mới nhất:*\n\n"
    for news in news_list[:5]:  # Chỉ lấy 5 bài đầu
        summary_text += f"🔹 *{news['title']}*\n_{news['summary']}_\n🔗 [Đọc thêm]({news['link']})\n\n"

    return summary_text
