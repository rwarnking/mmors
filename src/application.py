from url_list import URLS
from term_list import SEARCH_TERMS
from url_crawler import UrlCrawler
from exporter import Exporter

class MainApp:
    def __init__(self):
        pass

    def run(self):
        url_crawler = UrlCrawler()
        # Iterate list of all URLs to check
        # results = {}

        for url in URLS:
            print(f"Now processing {url['name']}")

            # results[url["name"]] = url_crawler.crawl(url, SEARCH_TERMS)
            result = url_crawler.crawl(url, SEARCH_TERMS)

            exporter = Exporter()
            # exporter.export_csv(result)
            exporter.export_html(url["name"], result)

###################################################################################################
# Main
###################################################################################################
if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
