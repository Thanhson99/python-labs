from difflib import SequenceMatcher

def is_similar(text1, text2, threshold=0.85):
    """Check whether two text blocks are similar by similarity score."""
    return SequenceMatcher(None, text1, text2).ratio() > threshold

def remove_duplicates(news_list):
    """Remove duplicate news items based on title, link, or similar content."""
    seen_titles = set()  # Store seen titles
    seen_links = set()   # Store seen links
    filtered_news = []   # Filtered news list

    for news in news_list:
        title = news["title"].strip()
        link = news["link"].strip()
        summary = news["summary"].strip()

        # Skip if title or link already exists
        if title in seen_titles or link in seen_links:
            continue

        # Check whether previous items are too similar
        is_duplicate = any(is_similar(summary, existing["summary"]) for existing in filtered_news)
        if is_duplicate:
            continue

        # Add item when it is new
        seen_titles.add(title)
        seen_links.add(link)
        filtered_news.append(news)

    return filtered_news
