import requests
import time
from parsel import Selector
from bs4 import BeautifulSoup


# Requisito 1
def fetch(url: str, wait: int = 1) -> str:
    time.sleep(1)
    try:
        response = requests.get(url, timeout=wait, header={
            "user-agent": "Fake user-agent"
        })
        response.raise_for_status()
    except (requests.HTTPError, requests.ReadTimeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_updates(html_content: str) -> list:
    selector = Selector(html_content)
    scrape_news = []
    if not selector.css("div.cs-overlay"):
        return []
    for news in selector.css("div.cs-overlay"):
        scrape_news.append(news.css("a::attr(href)").get())
    return scrape_news


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    if not selector.css("a.next::attr(href)"):
        return None
    return selector.css("a.next::attr(href)").get()


# Requisito 4
def scrape_news(html_content):
    selector = Selector(html_content)

    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css("h1::text").get().strip()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css("span.author a::text").get()
    comments_count = len(selector.css("div.comment-list li"))
    summary = BeautifulSoup(selector.css(
        "div.entry-content p"
        ).get(), "html.parser").get_text().strip()
    tags = selector.css("section.post-tags a::text").getall()
    category = selector.css("span.label::text").get()
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "comments_count": comments_count,
        "summary": summary,
        "tags": tags,
        "category": category
    }


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
