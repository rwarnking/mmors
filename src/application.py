from config import EXPORT_CSV, EXPORT_HTML
from exporter import Exporter
from term_list import SEARCH_TERMS
from url_crawler import UrlCrawler
from url_list import SEARCH_SITES


class MainApp:
    def __init__(self):
        pass

    def run(self):
        url_crawler = UrlCrawler()
        exporter = Exporter()

        # Iterate list of all URLs to check
        for website in SEARCH_SITES:
            print(f"Now processing {website['name']}")
            self._validate(website)

            search_results = url_crawler.crawl(website, SEARCH_TERMS)

            if EXPORT_CSV:
                exporter.export_csv(website, search_results)
            if EXPORT_HTML:
                exporter.export_html(website, search_results)

    def _validate(self, website):
        assert "name" in website, f"Missing name in {website}"
        assert "page_url" in website, f"Missing page_url in {website}"
        assert "request" in website, f"Missing request in {website}"
        # TODO further validation
        assert "response" in website, f"Missing response in {website}"


###################################################################################################
# Main
###################################################################################################
if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
