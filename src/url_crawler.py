import requests
from config import _logger
from response_parser import ResponseParser


class UrlCrawler:
    def __init__(self):
        pass

    def crawl_list(self, urls, search_terms):
        response_parser = ResponseParser()
        results = {}

        # Iterate list of all URLs to check
        for url in urls:
            # print(url)

            results[url["name"]] = {}
            # Iterate list of all search terms
            for term in search_terms:
                # print(term)

                if "ajax" in url:
                    search_query = url["url"] + url["ajax"](term)
                else:
                    search_query = url["url"] + url["search"](term)

                # Crawl results of search and parse found links
                response = self._get_request(search_query)

                if "ajax" in url:
                    results[url["name"]][term] = response_parser.parse_as_json(url["url"], response)
                else:
                    results[url["name"]][term] = response_parser.parse_as_html(url["url"], response)

        return results

    ##########
    # Helper #
    ##########
    def _get_request(self, url):
        r = None
        try:
            # r = requests.get(url, headers={'Accept': 'application/json'})#, timeout=3)
            r = requests.get(url)#, timeout=3)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            _logger.warning("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            _logger.warning("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            _logger.warning("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            _logger.warning("OOps: Something Else", err)

        return r
