from modules.news.deduplicator import remove_duplicates

def generate_summary(news_list):
    """Summarize news into one post"""
    news_list = remove_duplicates(news_list)  # Remove duplicate articles

    if not news_list:
        return "⚠️ No relevant news is available right now!"

    summary_text = "🚀 *Latest Crypto Bulletin:*\n\n"
    for news in news_list[:5]:  # Keep only the first 5 items
        summary_text += f"🔹 *{news['title']}*\n_{news['summary']}_\n🔗 [Read more]({news['link']})\n\n"

    return summary_text
