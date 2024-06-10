import requests
from config import _logger, DEBUG, DEBUG_DIR
from response_parser import ResponseParser
from requests.auth import HTTPBasicAuth

class UrlCrawler:
    def __init__(self):
        self.response_parser = ResponseParser()

    # def crawl(self, url, search_terms):
    #     result = {}

    #     # Iterate list of all search terms
    #     for term in search_terms:
    #         _term = term
    #         for to_repl, replacement in url["request"]["replacements"].items():
    #             _term = _term.replace(to_repl, replacement)

    #         if "google" in url:
    #             search_query = url["google"] + url["ajax"](_term)
    #         elif "ajax" in url:
    #             search_query = url["url"] + url["ajax"](_term)
    #         else:
    #             search_query = url["url"] + url["search"](_term)

    #         _logger.info(f"Search Query: {search_query}")

    #         # Crawl results of search and parse found links
    #         if "type" not in url:
    #             response = self._get_request(search_query)
    #         elif url["type"] == "Auth":
    #             response = self._get_request(search_query, HTTPBasicAuth(url["user"], url["pw"]))
    #         else:
    #             response = self._post_request(search_query, url["payload"](_term))

    #         if response:
    #             if DEBUG:
    #                 # TODO fix unicode problem
    #                 f = open(DEBUG_DIR / "debug_response.html", "w", encoding="utf-8")
    #                 f.write(
    #                     response.text
    #                     # .replace(u"\u263a", "")
    #                     # .replace(u"\u26c5", "")
    #                     # .replace(u"\u25ba", "")
    #                     # .replace(u"\u21b5", "")
    #                     # .replace(u"\u2009", "")
    #                     # .replace(u"\u2003", "")
    #                 )
    #                 f.close()

    #             if "google" in url:
    #                 result[term] = self.response_parser.parse_as_text(
    #                     url["url"],
    #                     response.text
    #                         .replace("google.search.cse.api4832({", "{")
    #                         .replace("google.search.cse.api13697({", "{")
    #                         .replace("});", "}")
    #                         .replace("/*O_o*/", "")
    #                 )
    #             elif "ajax" in url:
    #                 result[term] = self.response_parser.parse_as_json(url["url"], response)
    #             else:
    #                 result[term] = self.response_parser.parse_as_html(url["url"], response)
    #         else:
    #             _logger.warning(f"Request did not yield valid information. Did not process {url['name']}.")

    #     return result





    def crawl(self, url, search_terms):
        result = {}

        # Iterate list of all search terms
        for term in search_terms:
            _term = term
            for to_repl, replacement in url["request"]["replacements"].items():
                _term = _term.replace(to_repl, replacement)

            request = url["request"]
            if request["type"] == "get":
                search_query = request["url"] + request["url_payload"](_term)
                response = self._get_request(search_query)
            elif request["type"] == "post":
                search_query = request["url"] + request["url_payload"](_term)
                response = self._post_request(search_query, request["payload"](_term))
            elif request["type"] == "auth":
                search_query = request["url"] + request["url_payload"](_term)
                # TODO
                if "base64" in request:
                    pass
                else:
                    response = self._get_request(
                        search_query,
                        HTTPBasicAuth(request["user"], request["pw"])
                    )
            else:
                # TODO
                raise Exception("This should not happen!")

            _logger.info(f"Search Query: {search_query}")

            if response:
                if DEBUG:
                    f = open(DEBUG_DIR / "debug_response.html", "w", encoding="utf-8")
                    f.write(response.text)
                    f.close()

                exp_response = url["response"]

                if exp_response["type"] == "google":
                    result[term] = self.response_parser.parse_as_text(
                        request["url"],
                        # TODO regex number
                        response.text
                            .replace("google.search.cse.api4832({", "{")
                            .replace("google.search.cse.api13697({", "{")
                            .replace("});", "}")
                            .replace("/*O_o*/", ""),
                        exp_response["list_keys"],
                        exp_response["keys"]
                    )
                elif exp_response["type"] == "json":
                    result[term] = self.response_parser.parse_as_json(
                        request["url"], response, exp_response["list_keys"], exp_response["keys"]
                    )
                elif exp_response["type"] == "html":
                    # TODO improve this
                    if "add_keys" in exp_response:
                        result[term] = self.response_parser.parse_as_html(
                            request["url"], response, exp_response["list_keys"], exp_response["keys"], exp_response["add_keys"]
                        )
                    else:
                        result[term] = self.response_parser.parse_as_html(
                            request["url"], response, exp_response["list_keys"], exp_response["keys"]
                        )
                else:
                    # TODO
                    raise Exception("This should not happen!")
            else:
                _logger.warning(f"Request did not yield valid information. Did not process {url['name']}.")

        return result



    ##########
    # Helper #
    ##########
    def _get_request(self, url, _auth=None):
        r = None
        try:
            # r = requests.get(url, headers={'Accept': 'application/json'})#, timeout=3)
            # https://stackoverflow.com/questions/26745462/
            if _auth:
                # r = requests.get(url, auth=_auth)

                session = requests.Session()
                # session.auth = ("Basic", "c2R3LXJvOnNkdy1ybw==")
                session.auth = ("sdw-ro", "sdw-ro")
                # user sdw-ro
                # pw sdw-ro

                auth2 = session.post(url)
                r = session.get(url)
            else:
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

    def _post_request(self, url, payload):
        r = None
        try:
            # r = requests.get(url, headers={'Accept': 'application/json'})#, timeout=3)
            r = requests.post(url, payload)#, timeout=3)
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

