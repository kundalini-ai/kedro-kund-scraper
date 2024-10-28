import pandas as pd
from clearpilldatabase.scraper import ArticleScraper


scraper = ArticleScraper(openai_api_key='<add openai api key>', zenrows_api_key="<add zenrows api key>")

def scrape_articles_node(articles: pd.DataFrame):
    scraped_articles = []
    for article in articles[:10]:
        article_content = scraper.scrape_article(article['link'])
        article['content'] = article_content
        scraped_articles.append(article)
    return scraped_articles
