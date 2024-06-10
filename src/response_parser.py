import dateutil.parser as parser
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from config import IGNORE_ADDS
import json

class ResponseParser:
    def __init__(self):
        pass

    def parse_as_json(self, main_url: str, response, list_keys, keys):
        # Save list of links to a dictionary
        # print(response.text)
        res_json = response.json()

        for key in list_keys:
            res_json = res_json[key]

        return {
            "link_list": self.search_for_links(main_url, res_json, keys)
        }

    def parse_as_text(self, main_url: str, response, keys):
        # Save list of links to a dictionary
        # print(response.text)
        res_json = json.loads(response)

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
                    tmp_obj = tmp_obj[key]
                new_url_obj[field] = str(tmp_obj)

            # TODO add date processing

            if "url" in new_url_obj and not new_url_obj["url"].startswith("https:") and not new_url_obj["url"].startswith("http:"):
                new_url_obj["url"] = main_url + url_obj["url"]

            new_url_list.append(new_url_obj)
        return new_url_list

        #     new_url_obj = {
        #         "date": None,
        #         "title": None,
        #         "url": None,
        #     }
        #     if "url" in url_obj:
        #         new_url_obj["url"] = url_obj["url"]
        #         if not url_obj["url"].startswith("https:") and not url_obj["url"].startswith("http:"):
        #             new_url_obj["url"] = main_url + url_obj["url"]

        #     if "datetime" in url_obj:
        #         new_url_obj["date"] = url_obj["datetime"]
        #     elif "date" in url_obj:
        #         new_url_obj["date"] = url_obj["date"]
        #     elif "publicationDate" in url_obj:
        #         new_url_obj["date"] = url_obj["publicationDate"]
        #     elif "publish_date" in url_obj:
        #         new_url_obj["date"] = str(url_obj["publish_date"])
        #     elif "richSnippet" in url_obj and "metatags" in url_obj["richSnippet"] and "date" in url_obj["richSnippet"]["metatags"]:
        #         new_url_obj["date"] = str(url_obj["richSnippet"]["metatags"]["date"])
        #     elif "content" in url_obj:
        #         # new_url_obj["date"] = url_obj["content"].split(" ")[0]
        #         new_url_obj["date"] = url_obj["contentNoFormatting"].split("...")[0]

        #     # TODO
        #     # new_url_obj["date"] = str(parser.parse(new_url_obj["date"]))

        #     if "title" in url_obj:
        #         new_url_obj["title"] = url_obj["title"]
        #     elif "headline" in url_obj:
        #         new_url_obj["title"] = url_obj["headline"]

        #     # Bild
        #     # new_url_obj["text"] = url_obj["content"]

        #     if new_url_obj["title"] is None:
        #         continue

        #     new_url_list.append(new_url_obj)
        # return new_url_list

    # def _reduce_result(self, main_url: str, url_list):
    #     new_url_list = []

    #     for url_obj in url_list:
    #         new_url_obj = {
    #             "date": None,
    #             "title": None,
    #             "url": None,
    #         }
    #         if "url" in url_obj:
    #             new_url_obj["url"] = url_obj["url"]
    #             if not url_obj["url"].startswith("https:") and not url_obj["url"].startswith("http:"):
    #                 new_url_obj["url"] = main_url + url_obj["url"]

    #         if "datetime" in url_obj:
    #             new_url_obj["date"] = url_obj["datetime"]
    #         elif "date" in url_obj:
    #             new_url_obj["date"] = url_obj["date"]
    #         elif "publicationDate" in url_obj:
    #             new_url_obj["date"] = url_obj["publicationDate"]
    #         elif "publish_date" in url_obj:
    #             new_url_obj["date"] = str(url_obj["publish_date"])
    #         elif "richSnippet" in url_obj and "metatags" in url_obj["richSnippet"] and "date" in url_obj["richSnippet"]["metatags"]:
    #             new_url_obj["date"] = str(url_obj["richSnippet"]["metatags"]["date"])
    #         elif "content" in url_obj:
    #             # new_url_obj["date"] = url_obj["content"].split(" ")[0]
    #             new_url_obj["date"] = url_obj["contentNoFormatting"].split("...")[0]

    #         # TODO
    #         # new_url_obj["date"] = str(parser.parse(new_url_obj["date"]))

    #         if "title" in url_obj:
    #             new_url_obj["title"] = url_obj["title"]
    #         elif "headline" in url_obj:
    #             new_url_obj["title"] = url_obj["headline"]

    #         # Bild
    #         # new_url_obj["text"] = url_obj["content"]

    #         if new_url_obj["title"] is None:
    #             continue

    #         new_url_list.append(new_url_obj)
    #     return new_url_list

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

            if new_url_obj["url"] or new_url_obj["title"]:
                new_url_list.append(new_url_obj)

        return {
            "link_list": new_url_list
        }




    def parse_as_html2(self, main_url: str, response):
        new_url_list = []

        parsed_html = BeautifulSoup(response.text, features="html.parser")

        # print(response.text.replace(u"\u279e", ""))

        # "zeit.de" specific classes
        for elem in parsed_html.body.find_all('div', attrs={'class': 'zon-teaser__container'}):
            url = elem.find('a', attrs={'class': 'zon-teaser__link'})
            title = elem.find('span', attrs={'class': 'zon-teaser__title'}).contents[0]

            new_url_obj = {
                "date": None,
                "title": title,
                "url": None if url is None else url['href'],
            }
            new_url_list.append(new_url_obj)

        # "forschung-und-lehre.de" specific classes
        for elem in parsed_html.body.find_all('div', attrs={'class': 'result-list-item'}):
            url = elem.find('a', href=True)
            title = elem.find('span', attrs={'class': 'result-title'}).a.contents[0]

            if not url['href'].startswith("https:") and not url['href'].startswith("http:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": None,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "ihk-position.de" specific classes
        for elem in parsed_html.body.find_all('h2', attrs={'class': 'elementor-post__title'}):
            url = elem.find('a', href=True)
            title = url.contents[0]

            if not url['href'].startswith("https:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": None,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "profil-dphv.de" specific classes
        for elem in parsed_html.body.find_all('div', attrs={'class': 'fusion-rollover-content'}):
            url = elem.find('a', attrs={'class': 'fusion-rollover-link'}, href=True)
            title = url.contents[0]

            if not url['href'].startswith("https:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": None,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "table.media" specific classes
        for elem in parsed_html.body.find_all('div', attrs={'class': 'u-teaser-card__card'}):
            url = elem.find('a', attrs={'class': 'u-teaser-card__link'}, href=True)
            title = url.find('h3', attrs={'class': 'u-headline u-teaser-card__headline'}).contents[0]

            if not url['href'].startswith("https:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": None,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "bildungsklick.de" specific classes
        for elem in parsed_html.body.find_all('h2', attrs={'class': 'e-header-h2'}):
            url = elem.find('a', href=True)
            if url is None:
                continue
            title = url.contents[0]
            # print(elem)
            # print(title)
            # print(url['href'])

            if not url['href'].startswith("https:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": None,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "wb-web.de" specific classes
        for elem in parsed_html.body.find_all('div', attrs={'class': 'search-result'}):
            url = elem.find('a', attrs={'class': 'search-result-page-link'}, href=True)
            if url is None:
                continue
            title = url.contents[0]
            # print(elem)
            # print(title)
            # print(url['href'])

            if not url['href'].startswith("https:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": None,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "noz.de" specific classes
        for elem in parsed_html.body.find_all('div', attrs={'class': 'article__teaser'}):
            url = elem.find('a', attrs={'class': 'article__teaser__sub-headline--wrapper'}, href=True)
            if url is None:
                continue

            title = url.find('h3', attrs={'class': 'article__teaser__headline'}).contents[0]
            infos = elem.find('div', attrs={'class': 'article__teaser__info'}).find_all('span')
            if len(infos) == 2:
                date = infos[1].contents[0]
            else:
                date = None

            if not url['href'].startswith("https:") and not url['href'].startswith("http:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": date,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "fachportal-paedagogik.de" specific classes
        for elem in parsed_html.body.find_all('span', attrs={'class': 'book-list-item'}):
            url = elem.find('a', href=True)
            if url is None:
                continue

            title = url.contents[0]

            date = elem.find('span', attrs={'class': 'a5-book-list-item-year'}).contents[0]

            if not url['href'].startswith("https:") and not url['href'].startswith("http:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": date,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "taz.de" specific classes
        for elem in parsed_html.body.find_all('li', attrs={'class': 'elaborate'}):
            url = elem.find('a', href=True, attrs={'class': 'article'})
            if url is None:
                continue

            title = url.find('h3').contents[0]

            date = elem.find('li', attrs={'class': 'date'}).contents[0]

            if not url['href'].startswith("https:") and not url['href'].startswith("http:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": date,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "stuttgarter-zeitung.de" specific classes
        for elem in parsed_html.body.find_all('div', attrs={'class': 'item'}):
            url = elem.find('a', href=True, attrs={'class': 'data'})
            if url is None:
                continue

            title = url["title"]

            date = elem.find('time', attrs={'class': 'article-date-time'}).contents[0]

            if not url['href'].startswith("https:") and not url['href'].startswith("http:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": date,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "merkur.de" specific classes
        for elem in parsed_html.body.find_all('div', attrs={'class': ['id-LB-e--XL6_0c', 'id-LB-e--XL6_6']}):
            # Add can be found via attrs id-Teaser-el--proBEEP
            if IGNORE_ADDS and elem.find(attrs={'class': "id-Teaser-el--proBEEP"}):
                continue

            url = elem.find('a', href=True, attrs={'class': 'id-LinkOverlay-link'})
            if url is None:
                continue

            title = url.contents[0]

            # date = elem.find('time', attrs={'class': 'article-date-time'}).contents[0]
            date = None

            if not url['href'].startswith("https:") and not url['href'].startswith("http:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": date,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "bildungsserver.de" specific classes
        for list in parsed_html.body.find_all('div', attrs={'class': "ym-gbox-left"}):
            for elem in list.find_all('dt'):
                url = elem.find('a', href=True)
                if url is None:
                    continue

                title = url.find(attrs={'class': "meta_gesamt_title"}).contents[0]

                # date = elem.find('time', attrs={'class': 'article-date-time'}).contents[0]
                date = None

                if not url['href'].startswith("https:") and not url['href'].startswith("http:"):
                    url['href'] = main_url + url['href']

                new_url_obj = {
                    "date": date,
                    "title": title,
                    "url": url['href'],
                }
                new_url_list.append(new_url_obj)

        # "e-teaching.org" specific classes
        for elem in parsed_html.body.find_all('article', attrs={'class': "row"}):
            url = elem.find('a', attrs={'class': "list-group-item"}, href=True)
            if url is None:
                continue

            title = url.contents[0]

            date = None

            text = elem.find('a', attrs={'class': "page-link"}, href=True).contents[0]

            if not url['href'].startswith("https:") and not url['href'].startswith("http:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": date,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # "fr.de" specific classes
        for elem in parsed_html.body.find_all('div', attrs={'class': "id-LinkOverlay"}):
            url = elem.find('a', attrs={'class': "id-LinkOverlay-link"}, href=True)
            if url is None:
                continue

            title = url.contents[0]

            date = elem.find('span', attrs={'class': "id-DateTime-date"}).contents[0]

            text = elem.find('span', attrs={'class': "id-Teaser-el-content-text-text"}).contents[0]

            if not url['href'].startswith("https:") and not url['href'].startswith("http:"):
                url['href'] = main_url + url['href']

            new_url_obj = {
                "date": date,
                "title": title,
                "url": url['href'],
            }
            new_url_list.append(new_url_obj)

        # print(new_url_list)
        return {
            "link_list": new_url_list
        }

