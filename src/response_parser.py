import dateutil.parser as parser
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

class ResponseParser:
    def __init__(self):
        pass

    def parse_as_json(self, main_url: str, response):
        # Save list of links to a dictionary
        # print(response.text)
        res_json = response.json()

        return {
            "link_list": self.search_for_links(main_url, res_json)
        }

    def search_for_links(self, main_url: str, res_json):
        url_list = []
        self._walk_trough_json(res_json, url_list)
        url_list = self._reduce_result(main_url, url_list)
        # print(url_list)
        return url_list

    def _reduce_result(self, main_url: str, url_list):
        new_url_list = []

        for url_obj in url_list:
            new_url_obj = {
                "date": None,
                "title": None,
                "url": None,
            }
            if "url" in url_obj:
                new_url_obj["url"] = url_obj["url"]
                if not url_obj["url"].startswith("https:"):
                    new_url_obj["url"] = main_url + url_obj["url"]

            if "datetime" in url_obj:
                new_url_obj["date"] = url_obj["datetime"]
            elif "date" in url_obj:
                new_url_obj["date"] = url_obj["date"]
            elif "publicationDate" in url_obj:
                new_url_obj["date"] = url_obj["publicationDate"]
            elif "publish_date" in url_obj:
                new_url_obj["date"] = str(url_obj["publish_date"])

            # TODO
            # new_url_obj["date"] = str(parser.parse(new_url_obj["date"]))

            if "title" in url_obj:
                new_url_obj["title"] = url_obj["title"]
            elif "headline" in url_obj:
                new_url_obj["title"] = url_obj["headline"]

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

    def parse_as_html(self, main_url: str, response):
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

            if not url['href'].startswith("https:"):
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

        # print(new_url_list)
        return {
            "link_list": new_url_list
        }

