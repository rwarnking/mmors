from url_list import URLS
from term_list import SEARCH_TERMS
from url_crawler import UrlCrawler
from exporter import Exporter

class MainApp:
    def __init__(self):
        pass

    def run(self):
        url_crawler = UrlCrawler()
        exporter = Exporter()

        # Iterate list of all URLs to check
        # results = {}

        for url in URLS:
            print(f"Now processing {url['name']}")
            self._validate(url)

            # results[url["name"]] = url_crawler.crawl(url, SEARCH_TERMS)
            result = url_crawler.crawl(url, SEARCH_TERMS)

            # exporter.export_csv(result)
            exporter.export_html(url["name"], result)

    def _validate(self, url):
        assert "name" in url, f"Missing name in {url}"
        assert "url" in url, f"Missing url in {url}"
        assert "search" in url or "ajax" in url, f"Missing ajax or search in {url}"
        assert "separator" in url, f"Missing separator in {url}"

###################################################################################################
# Main
###################################################################################################
if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
