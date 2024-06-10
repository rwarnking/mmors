from url_list import URLS
from term_list import SEARCH_TERMS
from url_crawler import UrlCrawler
from exporter import Exporter
from config import EXPORT_CSV, EXPORT_HTML

class MainApp:
    def __init__(self):
        pass

    def run(self):
        url_crawler = UrlCrawler()
        exporter = Exporter()

        # Iterate list of all URLs to check
        for url in URLS:
            print(f"Now processing {url['name']}")
            self._validate(url)

            result = url_crawler.crawl(url, SEARCH_TERMS)

            if EXPORT_CSV:
                exporter.export_csv(url, result)
            if EXPORT_HTML:
                exporter.export_html(url, result)

    def _validate(self, url):
        assert "name" in url, f"Missing name in {url}"
        assert "page_url" in url, f"Missing page_url in {url}"
        assert "request" in url, f"Missing request in {url}"
        # TODO further validation
        assert "response" in url, f"Missing response in {url}"

###################################################################################################
# Main
###################################################################################################
if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
