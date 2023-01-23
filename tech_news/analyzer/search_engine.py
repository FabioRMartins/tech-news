from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    search = []
    tech_news = search_news({"title": {"$regex": title, "$options": "i"}})
    if not tech_news:
        return []
    for news in tech_news:
        search.append((news['title'], news['url']))
    return search


# Requisito 7
def search_by_date(date):
    try:
        date_information = datetime.fromisoformat(date).strftime("%d/%m/%Y")
        tech_news = search_news({"timestamp": {"$regex": date_information, "$options": "i"}})
        search = []
        if not tech_news:
            return []
        for news in tech_news:
            search.append((news["title"], news["url"]))
        return search
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    tech_news = search_news({"tags": {"$regex": tag, "$options": "i"}})
    if not tech_news:
        return []
    search = []
    for news in tech_news:
        search.append((news['title'], news['url']))
    return search


# Requisito 9
def search_by_category(category):
