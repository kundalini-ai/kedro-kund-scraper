from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from openai import OpenAI, BadRequestError
from bs4 import BeautifulSoup
from clearpilldatabase import middleware_manager
from zenrows import ZenRowsClient
import sys

class ArticleScraper:
    def __init__(self, openai_api_key, zenrows_api_key):
        self.client = OpenAI(api_key=openai_api_key)
        self.zenrows = ZenRowsClient(zenrows_api_key)

    def fetch_html_fallback (self, url): # ugly, todo 
        response = self.zenrows.get(url, params={"js_render":"true", "premium_proxy": "true"})
        if response.status_code != 200:
            print('[*] ZenRows failed too!')
            raise ValueError
        return response.text

    def fetch_html(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=300)
            context = browser.new_context()
            page = context.new_page()

            stealth_sync(page)

            page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br'
            })

            resource = page.goto(url)

            middleware_cls = middleware_manager.MiddlewareManager.detect(resource)
            if middleware_cls == False:
                print('[*] No middleware detected, proceeding')

                if (resource.status != 200):
                    print('[*] Received status {}. Using ZenRows as a fallback'.format(resource.status))
                    browser.close()
                    return self.fetch_html_fallback(url)

                page.wait_for_load_state()
                html = page.content()
                browser.close()
                return html
            else:
                middleware = middleware_cls(page)
                print('[*] {} middleware detected'.format(str(middleware)))
                try:
                    return middleware.handle()
                except middleware_manager.MiddlewareHandlingException:
                    print('[*] Failed to bypass/solve middleware locally. Using ZenRows')
                    browser.close()
                    return self.fetch_html_fallback(url)
                    

    def extract_body_content(self, html):
        soup = BeautifulSoup(html, 'lxml')

        # Usuwanie elementów stylu
        for style in soup(["style", "script", "link", "meta", "noscript"]):
            style.decompose()

        # remove inline css, other unrelevant attributes and empty elements
        for tag in soup.find_all(True):
            del tag['style'], tag['target'], tag['rel']
            if not tag.contents and not tag.string:
                tag.decompose()
                continue

            for attr in [attr for attr in tag.attrs if attr.startswith('data-')]:
                del tag[attr]


        body = soup.body
        return str(body)

    def extract_article_content(self, html):
        response = self.client.chat.completions.create(
            model='gpt-4-turbo',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",
                 "content": f"Extract the main article content from the following HTML:\n\n{html}. Return only article content and nothing else."}
            ],
        )
        return response.choices[0].message.content

    def scrape_article(self, article_url):
        html = self.fetch_html(article_url)
        print('[*] Source fetched successfully')
        body_content = self.extract_body_content(html)
        try:
            article_content = self.extract_article_content(body_content)
        except BadRequestError as exc:
            return exc.message

        return article_content

if __name__ == '__main__':
    # Przykład użycia
    scraper = ArticleScraper(openai_api_key='<add openai api key>', zenrows_api_key="<add zenrows api key>")
    #article = scraper.scrape_article('https://example.com/article')
    article = scraper.scrape_article(sys.argv[1])
    print(article)
