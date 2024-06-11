import dateutil.parser as parser
from dateutil.parser import ParserError

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

import json

from config import IGNORE_ADDS, LocaleParserInfo


class ResponseParser:
    def __init__(self):
        pass

    def parse_as_json(self, main_url: str, response, list_keys, data_fields):
        # Save list of links to a dictionary
        # print(response.text)
        res_json = response.json()

        # Access the list of search results
        for key in list_keys:
            # This converts the res_json to a list
            if key not in res_json:
                return []
            res_json = res_json[key]

        return self._extract_data(main_url, res_json, data_fields)

    def parse_as_text(self, main_url: str, response, list_keys, data_fields):
        # Save list of links to a dictionary
        res_json = json.loads(response)

        # Access the list of search results
        for key in list_keys:
            # This converts the res_json to a list
            if key not in res_json:
                return []
            res_json = res_json[key]

        return self._extract_data(main_url, res_json, data_fields)

    def _extract_data(self, main_url: str, result_list, data_fields):
        extracted_results = []

        for s_result in result_list:
            extracted = {}

            for field, keys in data_fields.items():
                tmp_obj = s_result
                for key in keys:
                    if key not in tmp_obj:
                        # TODO
                        print(f"Warning: Key ({key}) not found")
                        tmp_obj = None
                        break
                    tmp_obj = tmp_obj[key]
                extracted[field] = str(tmp_obj)

            if (
                "url" in extracted
                and not extracted["url"].startswith("https:")
                and not extracted["url"].startswith("http:")
            ):
                extracted["url"] = main_url + s_result["url"]

            if "date" in extracted and extracted["date"]:
                try:
                    extracted["date"] = parser.parse(
                        extracted["date"],
                        parserinfo=LocaleParserInfo(),
                    ).isoformat(sep=" ")
                except ParserError:
                    # TODO
                    print(f"Error parsing {extracted['date']}")

            extracted_results.append(extracted)
        return extracted_results

    # def _walk_trough_json(self, json, url_list):
    #     if type(json) is dict:
    #         for e in json.values():
    #             if type(e) is dict and "url" in e:
    #                 if not e["url"].endswith(".jpeg"):
    #                     url_list.append(e)
    #             self._walk_trough_json(e, url_list)
    #     elif type(json) is list:
    #         for e in json:
    #             if type(e) is dict and "url" in e:
    #                 if not e["url"].endswith(".jpeg"):
    #                     url_list.append(e)
    #             self._walk_trough_json(e, url_list)

    def parse_as_html(self, main_url: str, response, list_keys, data_fields, add_keys=[]):
        extracted_results = []

        parsed_html = BeautifulSoup(response.text, features="html.parser")

        # TODO multiple list_keys
        for elem in parsed_html.body.find_all(
            list_keys[0]["type"], attrs={"class": list_keys[0]["class"]}
        ):
            extracted = {}

            if IGNORE_ADDS:
                for add_key in add_keys:
                    if elem.find(attrs={"class": add_key}):
                        continue

            for key, value in data_fields.items():
                if key == "elem":
                    continue

                if value["scope"] == "one":
                    _result = elem.find(value["type"], attrs={"class": value["class"]})
                elif value["scope"] is None:
                    _result = elem
                else:
                    raise Exception("Error")

                extracted[key] = None if not _result else value["access"](_result)

            if (
                extracted["url"]
                and not extracted["url"].startswith("https:")
                and not extracted["url"].startswith("http:")
            ):
                extracted["url"] = main_url + extracted["url"]

            if "date" in extracted and extracted["date"]:
                try:
                    extracted["date"] = parser.parse(
                        extracted["date"], parserinfo=LocaleParserInfo(), fuzzy=True,
                    ).isoformat(sep=" ")
                except ParserError:
                    # TODO
                    print(f"Error parsing {extracted['date']}")

            if extracted["url"] or extracted["title"]:
                extracted_results.append(extracted)

        return extracted_results
