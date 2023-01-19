import requests
import time
from parsel import Selector


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
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
