import requests
import time
from parsel import Selector
from bs4 import BeautifulSoup
from tech_news.database import create_news


# Requisito 1
def fetch(url, wait = 1):
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
def scrape_updates(html_content):
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
    html_content = fetch("https://blog.betrybe.com/")
    news = []
    while len(news) < amount:
        news += scrape_updates(html_content)
        html_content = fetch(scrape_next_page_link(html_content))
        if not html_content:
            break
    if len(news) > amount:
        news = news[0:amount]
    recent_news = [
        scrape_news(fetch(html_content))
        for html_content in news[0:amount]
    ]

    create_news(recent_news)
    if not recent_news:
        return []
    return recent_news
