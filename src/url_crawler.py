import base64
import re

import requests
from config import DEBUG, DEBUG_DIR, _logger
from requests.auth import HTTPBasicAuth
from response_parser import ResponseParser


class UrlCrawler:
    def __init__(self):
        self.response_parser = ResponseParser()

    def crawl(self, website, search_terms):
        search_results = {}

        # Iterate list of all search terms
        for term in search_terms:
            _term = term
            for to_repl, replacement in website["request"]["replacements"].items():
                _term = _term.replace(to_repl, replacement)

            request = website["request"]
            if request["type"] == "get":
                search_query = request["url"] + request["url_payload"](_term)
                _logger.info(f"Search Query: {search_query}")
                response = self._get_request(search_query)
            elif request["type"] == "post":
                search_query = request["url"] + request["url_payload"](_term)
                _logger.info(f"Search Query: {search_query}, {request['payload'](_term)}")
                response = self._post_request(search_query, request["payload"](_term))
            elif request["type"] == "auth":
                search_query = request["url"] + request["url_payload"](_term)
                _logger.info(f"Search Query: {search_query}")

                if "base64" in request:
                    base64_bytes = request["base64"].encode("ascii")
                    user, pw = base64.b64decode(base64_bytes).decode("ascii").split(":")
                    auth = HTTPBasicAuth(user, pw)
                else:
                    auth = HTTPBasicAuth(request["user"], request["pw"])
                response = self._get_request(search_query, auth)
            else:
                # TODO
                raise Exception("This should not happen!")

            if response:
                if DEBUG:
                    f = open(DEBUG_DIR / "debug_response.html", "w", encoding="utf-8")
                    f.write(response.text)
                    f.close()

                exp_response = website["response"]
                if exp_response["type"] == "google":
                    response = response.text.replace("});", "}").replace("/*O_o*/", "")
                    response = re.sub(r"google.search.cse.api\d*\({", "{", response)

                    search_results[term] = self.response_parser.parse_as_text(
                        request["url"], response, exp_response["list_keys"], exp_response["keys"]
                    )
                elif exp_response["type"] == "json":
                    search_results[term] = self.response_parser.parse_as_json(
                        request["url"], response, exp_response["list_keys"], exp_response["keys"]
                    )
                elif exp_response["type"] == "html":
                    # TODO improve this
                    if "add_keys" in exp_response:
                        search_results[term] = self.response_parser.parse_as_html(
                            request["url"],
                            response,
                            exp_response["list_keys"],
                            exp_response["keys"],
                            exp_response["add_keys"],
                        )
                    else:
                        search_results[term] = self.response_parser.parse_as_html(
                            request["url"],
                            response,
                            exp_response["list_keys"],
                            exp_response["keys"],
                        )
                else:
                    # TODO
                    raise Exception("This should not happen!")
            else:
                _logger.warning(
                    f"Request did not yield valid information. Did not process {website['name']}."
                )

        return search_results

    ##########
    # Helper #
    ##########
    def _get_request(self, url, _auth=None):
        r = None
        try:
            # r = requests.get(url, headers={'Accept': 'application/json'})#, timeout=3)
            # https://stackoverflow.com/questions/26745462/
            if _auth:
                r = requests.get(url, auth=_auth)
            else:
                r = requests.get(url)  # , timeout=3)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            _logger.warning(f"Http Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            _logger.warning(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            _logger.warning(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            _logger.warning(f"OOps: Something Else {err}")

        return r

    def _post_request(self, url, payload):
        r = None
        try:
            # r = requests.get(url, headers={'Accept': 'application/json'})#, timeout=3)
            r = requests.post(url, payload)  # , timeout=3)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            _logger.warning(f"Http Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            _logger.warning(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            _logger.warning(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            _logger.warning(f"OOps: Something Else {err}")

        return r
