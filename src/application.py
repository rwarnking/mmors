from url_list import URLS
from term_list import SEARCH_TERMS
from url_crawler import UrlCrawler
from exporter import Exporter

class MainApp:
    def __init__(self):
        pass

    def run(self):
        url_crawler = UrlCrawler()
        results = url_crawler.crawl_list(URLS, SEARCH_TERMS)

        exporter = Exporter()
        exporter.export_csv(results)
        exporter.export_html(results)

###################################################################################################
# Main
###################################################################################################
if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
