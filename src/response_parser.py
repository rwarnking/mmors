import dateutil.parser as parser
from dateutil.parser import ParserError
from dateutil import tz
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from config import IGNORE_ADDS, LocaleParserInfo
import json

class ResponseParser:
    def __init__(self):
        pass

    def parse_as_json(self, main_url: str, response, list_keys, keys):
        # Save list of links to a dictionary
        # print(response.text)
        res_json = response.json()

        for key in list_keys:
            if key not in res_json:
                return {"link_list": []}
            res_json = res_json[key]

        return {
            "link_list": self.search_for_links(main_url, res_json, keys)
        }

    def parse_as_text(self, main_url: str, response, list_keys, keys):
        # Save list of links to a dictionary
        res_json = json.loads(response)

        for key in list_keys:
            if key not in res_json:
                return {"link_list": []}
            res_json = res_json[key]

        return {
            "link_list": self.search_for_links(main_url, res_json, keys)
        }

    def search_for_links(self, main_url: str, res_json, keys):
        # url_list = []
        # self._walk_trough_json(res_json, url_list)
        url_list = self._reduce_result(main_url, res_json, keys)
        # print(url_list)
        return url_list

    def _reduce_result(self, main_url: str, url_list, data_fields):
        new_url_list = []

        for url_obj in url_list:
            new_url_obj = {}

            for field, keys in data_fields.items():
                tmp_obj = url_obj
                for key in keys:
                    if key not in tmp_obj:
                        # TODO
                        print(f"Warning: Key ({key}) not found")
                        tmp_obj = None
                        break
                    tmp_obj = tmp_obj[key]
                new_url_obj[field] = str(tmp_obj)

            if "url" in new_url_obj and not new_url_obj["url"].startswith("https:") and not new_url_obj["url"].startswith("http:"):
                new_url_obj["url"] = main_url + url_obj["url"]

            if "date" in new_url_obj and new_url_obj["date"]:
                try:
                    new_url_obj["date"] = parser.parse(
                        new_url_obj["date"],
                        parserinfo=LocaleParserInfo()
                    ).isoformat(sep=" ")
                except ParserError:
                    # TODO
                    print(f"Error parsing {new_url_obj['date']}")

            new_url_list.append(new_url_obj)
        return new_url_list

    def _walk_trough_json(self, json, url_list):
        if type(json) is dict:
            for e in json.values():
                if type(e) is dict and "url" in e:
                    if not e["url"].endswith(".jpeg"):
                        url_list.append(e)
                self._walk_trough_json(e, url_list)
        elif type(json) is list:
            for e in json:
                if type(e) is dict and "url" in e:
                    if not e["url"].endswith(".jpeg"):
                        url_list.append(e)
                self._walk_trough_json(e, url_list)

    def parse_as_html(self, main_url: str, response, list_keys, keys, add_keys=[]):
        new_url_list = []

        parsed_html = BeautifulSoup(response.text, features="html.parser")

        # TODO multiple list_keys
        for elem in parsed_html.body.find_all(
            list_keys[0]["type"],
            attrs={'class': list_keys[0]["class"]}
        ):
            new_url_obj = {}

            if IGNORE_ADDS:
                for add_key in add_keys:
                    if elem.find(attrs={'class': add_key}):
                        continue

            for key, value in keys.items():
                if key == "elem":
                    continue

                if value["scope"] == "one":
                    result = elem.find(
                        value["type"],
                        attrs={'class': value["class"]}
                    )
                elif value["scope"] == None:
                    result = elem
                else:
                    raise Exception("Error")

                # print(result)
                new_url_obj[key] = None if not result else value["access"](result)

            if new_url_obj["url"] and not new_url_obj["url"].startswith("https:") and not new_url_obj["url"].startswith("http:"):
                new_url_obj["url"] = main_url + new_url_obj["url"]

            if "date" in new_url_obj and new_url_obj["date"]:
                try:
                    new_url_obj["date"] = parser.parse(
                        new_url_obj["date"],
                        parserinfo=LocaleParserInfo(),
                        fuzzy=True
                    ).isoformat(sep=" ")
                except ParserError:
                    # TODO
                    print(f"Error parsing {new_url_obj['date']}")

            if new_url_obj["url"] or new_url_obj["title"]:
                new_url_list.append(new_url_obj)

        return {
            "link_list": new_url_list
        }
