def contains_valid_url(item):
    return "url" in item and item["url"].startswith(("http://", "https://"))
