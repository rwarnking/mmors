import requests
from config import _logger
from response_parser import ResponseParser


class UrlCrawler:
    def __init__(self):
        pass

    def crawl(self, url, search_terms):
        response_parser = ResponseParser()
        result = {}

        # Iterate list of all search terms
        for term in search_terms:
            _term = term.replace(" ", url["separator"])

            if "ajax" in url:
                search_query = url["url"] + url["ajax"](_term)
            else:
                search_query = url["url"] + url["search"](_term)

            # Crawl results of search and parse found links
            response = self._get_request(search_query)

            if "ajax" in url:
                result[term] = response_parser.parse_as_json(url["url"], response)
            else:
                result[term] = response_parser.parse_as_html(url["url"], response)

        return result

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
            print("Http Error:", errh)
            _logger.warning("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            _logger.warning("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            _logger.warning("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            _logger.warning("OOps: Something Else", err)

        return r
