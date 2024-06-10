URLS = [
    {
        "name": "sueddeutsche",
        "page_url": "https://www.sueddeutsche.de",
        "search_url": lambda x: f"/suche?search={x}",
        "request": {
            "type": "get",
            "url": "https://www.sueddeutsche.de",
            "url_payload": lambda x: f"/api/public/search/teasers?term={x}",
            "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
            },
        },
        "response": {
            "type": "json",
            "list_keys": ["teasers"],
            "keys": {
                "date": ["content", "date"],
                "title": ["content", "title"],
                "url": ["content", "url"],
                "desc": ["content", "teaserText"],
                "topic": ["trackingdata", "main_topic"],
                "section": ["trackingdata", "section"],
            }
        }
    },
    # TODO tagesschau returns also images and videos that are ignored here
    {
        "name": "tagesschau",
        "page_url": "https://www.tagesschau.de",
        "search_url": lambda x: f"/suche#/?searchText={x}",
        "request": {
            "type": "get",
            "url": "https://www.tagesschau.de",
            "url_payload": lambda x: f"/json/search?searchText={x}",
            "replacements": {
                " ": "%20",
                "/": "",
            },
        },
        "response": {
            "type": "json",
            "list_keys": ["documentTypes", 0, "items"],
            "keys": {
                "date": ["datetime"],
                "title": ["headline"],
                "url": ["url"],
                "desc": ["description"],
            }
        }
    },
    {
        "name": "spiegel",
        "page_url": "https://www.spiegel.de",
        "search_url": lambda x: f"/suche/?suchbegriff={x}",
        "request": {
            "type": "get",
            "url": "https://www.spiegel.de",
            "url_payload": lambda x: f"/services/sitesearch/search?segments=spon%2Cspon_paid%2Cspon_international%2Cmmo%2Cmmo_paid%2Chbm%2Chbm_paid%2Celf%2Celf_paid&q={x}",
            "replacements": {
                " ": "%2B",
                "/": "%2F",
                ":": "%3A",
            },
        },
        "response": {
            "type": "json",
            "list_keys": ["results"],
            "keys": {
                "date": ["publish_date"],
                "title": ["title"],
                "url": ["url"],
                "desc": ["intro"],
                "access": ["access_level"],
            }
        }
    },
    {
        "name": "faz",
        "page_url": "https://www.faz.net",
        "search_url": lambda x: f"/suche/{x}",
        "request": {
            "type": "get",
            "url": "https://www.faz.net",
            "url_payload": lambda x: f"/api/faz-content-search?page=1&paid_content=include&q={x}&rows=20&sort_by=date&sort_order=desc",
            "replacements": {
                " ": "+",
                "/": "%2F",
            },
        },
        "response": {
            "type": "json",
            "list_keys": ["docs"],
            "keys": {
                "date": ["date"],
                "title": ["title"],
                "url": ["url"],
                "desc": ["teaser"],
                "access": ["faz_plus"],
                "section": ["section"],
            }
        }
    },
    {
        "name": "zeit",
        "page_url": "https://www.zeit.de",
        "search_url": lambda x: f"/suche/index?q={x}",
        "request": {
            "type": "get",
            "url": "https://www.zeit.de",
            "url_payload": lambda x: f"/suche/index?q={x}",
            "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "div",
                    "class": "zon-teaser__container",
                },
            ],
            "keys": {
                "date": {
                    "scope": "one",
                    "type": "time",
                    "class": "zon-teaser__datetime",
                    "access": lambda x: x.get_text()
                },
                "title": {
                    "scope": "one",
                    "type": "span",
                    "class": "zon-teaser__title",
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "zon-teaser__link",
                    "access": lambda x: x["href"]
                },
                "desc": {
                    "scope": "one",
                    "type": "p",
                    "class": "zon-teaser__summary",
                    "access": lambda x: x.get_text()
                },
                "access": {
                    "scope": "one",
                    "type": "svg",
                    "class": "zplus-logo",
                    "access": lambda x: x["aria-label"]
                },
            }
        },
    },
    {
        "name": "welt",
        "page_url": "https://www.welt.de",
        "search_url": lambda x: f"/suche?q={x}",
        "request": {
            "type": "get",
            "url": "https://www.welt.de",
            "url_payload": lambda x: f"/api/search/{x}?offset=0&restrictBy=y1",
            "replacements": {
                " ": "%20",
                "/": "",
            },
        },
        "response": {
            "type": "json",
            "list_keys": ["items"],
            "keys": {
                "date": ["publicationDate"],
                "title": ["headline"],
                "url": ["url"],
                "desc": ["intro"],
                "access": ["premium"],
                "section": ["rootSection"],
            }
        }
    },
    {
        "name": "ihk-position",
        "page_url": "https://www.ihk-position.de",
        "search_url": lambda x: f"/?s={x}",
        "request": {
            "type": "get",
            "url": "https://www.ihk-position.de",
            "url_payload": lambda x: f"/?s={x}",
            "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "div",
                    "class": "elementor-post__card",
                },
            ],
            "keys": {
                "date": {
                    "scope": "one",
                    "type": "span",
                    "class": "elementor-post-date",
                    "access": lambda x: x.get_text()
                },
                "title": {
                    "scope": "one",
                    "type": "a",
                    "class": None,
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": None,
                    "access": lambda x: x["href"]
                },
            }
        },
    },
    {
        "name": "profil-dphv",
        "page_url": "https://www.profil-dphv.de",
        "search_url": lambda x: f"/?s={x}",
        "request": {
            "type": "get",
            "url": "https://www.profil-dphv.de",
            "url_payload": lambda x: f"/?s={x}",
            "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "article",
                    "class": "fusion-post-medium",
                },
            ],
            "keys": {
                "date": {
                    "scope": "one",
                    "type": "span",
                    "class": "updated",
                    "access": lambda x: x.get_text()
                },
                "title": {
                    "scope": "one",
                    "type": "a",
                    "class": "fusion-rollover-link",
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "fusion-rollover-link",
                    "access": lambda x: x["href"]
                },
                "desc": {
                    "scope": "one",
                    "type": "div",
                    "class": "fusion-post-content-container",
                    "access": lambda x: x.p.get_text()
                },
            }
        },
    },
    # TODO add page variable
    {
        "name": "table.media",
        "page_url": "https://table.media",
        "search_url": lambda x: f"/suche/?s={x}&page=1",
        "request": {
            "type": "get",
            "url": "https://table.media",
            "url_payload": lambda x: f"/suche/?s={x}&page=1",
            "replacements": {
                " ": "+",
                "/": "",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "article",
                    "class": "u-teaser-card",
                },
            ],
            "keys": {
                "date": {
                    "scope": None,
                    "type": "",
                    "class": "",
                    "access": lambda x: x["postdate"]
                },
                "title": {
                    "scope": "one",
                    "type": "h3",
                    "class": "u-headline u-teaser-card__headline",
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "u-teaser-card__link",
                    "access": lambda x: x["href"]
                },
                "desc": {
                    "scope": "one",
                    "type": "p",
                    "class": "u-teaser-card__text",
                    "access": lambda x: x.get_text()
                },
                "section": {
                    "scope": "one",
                    "type": "a",
                    "class": "u-teaser-card__kicker",
                    "access": lambda x: x.span.get_text()
                },
            }
        },
    },
    {
        "name": "bildungsklick",
        "page_url": "https://bildungsklick.de",
        "search_url": lambda x: f"/suche?tx_elastica_pi1%5BdateFrom%5D=&tx_elastica_pi1%5BdateTo%5D=&tx_elastica_pi1%5Bfacets%5D%5Bnews%5D=&tx_elastica_pi1%5Bkeyword%5D={x}&tx_elastica_pi1%5Bsorting%5D=0&tx_elastica_pi1%5Bvideo%5D=&cHash=f8efd2f1fd21f0ea34021c56c65f8c78",
        "request": {
            "type": "get",
            "url": "https://bildungsklick.de",
            "url_payload": lambda x: f"/suche?tx_elastica_pi1%5BdateFrom%5D=&tx_elastica_pi1%5BdateTo%5D=&tx_elastica_pi1%5Bfacets%5D%5Bnews%5D=&tx_elastica_pi1%5Bkeyword%5D={x}&tx_elastica_pi1%5Bsorting%5D=0&tx_elastica_pi1%5Bvideo%5D=&cHash=f8efd2f1fd21f0ea34021c56c65f8c78",
            "replacements": {
                " ": "%20",
                "/": "",
                ":": "%3A",
                "(": "",
                ")": "",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "section",
                    "class": "m-news-list__item",
                },
            ],
            "keys": {
                "date": {
                    "scope": "one",
                    "type": "span",
                    "class": "m-news-swiper__date",
                    "access": lambda x: x.get_text()
                },
                "title": {
                    "scope": "one",
                    "type": "a",
                    "class": "",
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "",
                    "access": lambda x: x["href"]
                },
                "desc": {
                    "scope": "one",
                    "type": "p",
                    "class": "bodytext",
                    "access": lambda x: x.get_text()
                },
                "section": {
                    "scope": "one",
                    "type": "span",
                    "class": "e-header-kicker__obtrusive",
                    "access": lambda x: x.get_text()
                },
                "type": {
                    "scope": "one",
                    "type": "span",
                    "class": "m-news-swiper__category",
                    "access": lambda x: x.get_text()
                },
            }
        },
    },
    {
        "name": "wb-web",
        "page_url": "https://wb-web.de",
        "search_url": lambda x: f"/suche.html?search={x}",
        "request": {
            "type": "get",
            "url": "https://wb-web.de",
            "url_payload": lambda x: f"/suche.html?search={x}",
            "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "div",
                    "class": "search-result",
                },
            ],
            "keys": {
                "title": {
                    "scope": "one",
                    "type": "a",
                    "class": "search-result-page-link",
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "search-result-page-link",
                    "access": lambda x: x["href"]
                },
                "desc": {
                    "scope": "one",
                    "type": "p",
                    "class": "search-result-hightlight-text",
                    "access": lambda x: x.get_text()
                },
                "type": {
                    "scope": "one",
                    "type": "div",
                    "class": "search-result-meta",
                    "access": lambda x: x.get_text()
                },
            }
        },
    },
    # TODO date and section have a problem with kolumnen (try term "blau rot")
    {
        "name": "noz",
        "page_url": "https://noz.de",
        "search_url": lambda x: f"/suche?q={x}",
        "request": {
            "type": "get",
            "url": "https://noz.de",
            "url_payload": lambda x: f"/suche?q={x}",
            "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "div",
                    "class": "article__teaser",
                },
            ],
            "keys": {
                "date": {
                    "scope": "one",
                    "type": "div",
                    "class": "article__teaser__info",
                    "access": lambda x: x.select('div > span')[1].get_text()
                },
                "title": {
                    "scope": "one",
                    "type": "h3",
                    "class": "article__teaser__headline",
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "article__teaser__sub-headline--wrapper",
                    "access": lambda x: x["href"]
                },
                "section": {
                    "scope": "one",
                    "type": "div",
                    "class": "article__teaser__info",
                    "access": lambda x: x.span.get_text()
                },
            }
        },
    },
    {
        "name": "fachportal-paedagogik",
        "page_url": "https://www.fachportal-paedagogik.de",
        "search_url": lambda x: f"/suche/trefferliste.html?searchIn%5B%5D=fis&searchIn%5B%5D=fdz&searchIn%5B%5D=fin&feldname1=Freitext&bool1=AND&suche=einfach&feldinhalt1={x}&ur_wert_feldinhalt1einfach={x}",
        "request": {
            "type": "get",
            "url": "https://www.fachportal-paedagogik.de",
            "url_payload": lambda x: f"/suche/trefferliste.html?searchIn%5B%5D=fis&searchIn%5B%5D=fdz&searchIn%5B%5D=fin&feldname1=Freitext&bool1=AND&suche=einfach&feldinhalt1={x}&ur_wert_feldinhalt1einfach={x}",
            "replacements": {
                " ": "+and+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "span",
                    "class": "book-list-item",
                },
            ],
            "keys": {
                "date": {
                    "scope": "one",
                    "type": "span",
                    "class": "a5-book-list-item-year",
                    "access": lambda x: x.get_text()
                },
                "title": {
                    "scope": "one",
                    "type": "a",
                    "class": "",
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "",
                    "access": lambda x: x["href"]
                },
            }
        },
    },
    {
        "name": "taz",
        "page_url": "https://taz.de",
        "search_url": lambda x: f"/!s={x}",
        "request": {
            "type": "get",
            "url": "https://taz.de",
            "url_payload": lambda x: f"/!s={x}",
            "replacements": {
                " ": "+",
                "/": "",
                ":": "%253A",
                "(": "%2528",
                ")": "%2529",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "li",
                    "class": "elaborate",
                },
            ],
            "keys": {
                "date": {
                    "scope": "one",
                    "type": "li",
                    "class": "date",
                    "access": lambda x: x.get_text()
                },
                "title": {
                    "scope": "one",
                    "type": "h3",
                    "class": "",
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "article",
                    "access": lambda x: x["href"]
                },
                "desc": {
                    "scope": "one",
                    "type": "p",
                    "class": "snippet",
                    "access": lambda x: x.get_text()
                },
                # "type": {
                #     "scope": "one",
                #     "type": "div",
                #     "class": "extension",
                #     "access": lambda x: x.find(lambda y: y.name == "p" and "Ressort:" in y.text).get_text()
                # },
            }
        },
    },
    {
        "name": "stuttgarter-zeitung",
        "page_url": "https://www.stuttgarter-zeitung.de",
        "search_url": lambda x: f"/suche?_charset_=UTF-8&searchSort=desc&searchText={x}",
        "request": {
            "type": "get",
            "url": "https://www.stuttgarter-zeitung.de",
            "url_payload": lambda x: f"/suche?_charset_=UTF-8&searchSort=desc&searchText={x}",
            "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "div",
                    "class": "item",
                },
            ],
            "keys": {
                "date": {
                    "scope": "one",
                    "type": "time",
                    "class": "article-date-time",
                    "access": lambda x: x.get_text()
                },
                "title": {
                    "scope": "one",
                    "type": "a",
                    "class": "data",
                    "access": lambda x: x["title"]
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "data",
                    "access": lambda x: x["href"]
                },
                "desc": {
                    "scope": "one",
                    "type": "div",
                    "class": "appetizer-text",
                    "access": lambda x: None if len (x.span.contents) < 1 else x.span.get_text()
                },
                "access": {
                    "scope": "one",
                    "type": "a",
                    "class": "data",
                    "access": lambda x: x["data-paidcontent"]
                },
            }
        },
    },
    {
        "name": "merkur",
        "page_url": "https://merkur.de",
        "search_url": lambda x: f"/suche/?tt=1&tx=&sb=&td=&fd=&qr={x}",
        "request": {
            "type": "get",
            "url": "https://merkur.de",
            "url_payload": lambda x: f"/suche/?tt=1&tx=&sb=&td=&fd=&qr={x}",
            "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "div",
                    "class": ['id-LB-e--XL6_0c', 'id-LB-e--XL6_6'],
                },
            ],
            "keys": {
                "title": {
                    "scope": "one",
                    "type": "a",
                    "class": "id-LinkOverlay-link",
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "id-LinkOverlay-link",
                    "access": lambda x: x["href"]
                },
                "desc": {
                    "scope": "one",
                    "type": "span",
                    "class": "id-Teaser-el-content-text-text",
                    "access": lambda x: x.get_text()
                },
                "section": {
                    "scope": "one",
                    "type": "span",
                    "class": "id-Teaser-el-content-meta-item-category",
                    "access": lambda x: x.get_text()
                },
            },
            "add_keys": ["id-Teaser-el--proBEEP"]
        },
    },
    {
        "name": "bildungsserver",
        "page_url": "https://www.bildungsserver.de",
        "search_url": lambda x: f"/metasuche/metasuche.html?feldinhalt1={x}&feldname1=Freitext&gruppen%5B%5D=Deutscher+Bildungsserver&fisOnline=y&sucheMitBoost=y&fieldLenNorm=n&bool1=AND&DBS=1&art=einfach",
        "request": {
            "type": "get",
            "url": "https://www.bildungsserver.de",
            "url_payload": lambda x: f"/metasuche/metasuche.html?feldinhalt1={x}&feldname1=Freitext&gruppen%5B%5D=Deutscher+Bildungsserver&fisOnline=y&sucheMitBoost=y&fieldLenNorm=n&bool1=AND&DBS=1&art=einfach",
            "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "dt",
                    "class": "",
                },
            ],
            "keys": {
                # "date": {
                #     "scope": "one",
                #     "type": "time",
                #     "class": "article-date-time",
                #     "access": lambda x: x.get_text()
                # },
                "title": {
                    "scope": "one",
                    "type": "a",
                    "class": "",
                    "access": lambda x: x.span.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "",
                    "access": lambda x: x["href"]
                },
                # "desc": {
                #     "scope": "one",
                #     "type": "div",
                #     "class": "a5-search-list-dbs-content",
                #     "access": lambda x: x.get_text()
                # },
                # "type": {
                #     "scope": "one",
                #     "type": "p",
                #     "class": "a5-search-list-dbs-place",
                #     "access": lambda x: x.strong.get_text()
                # },
            },
        },
    },
    {
        "name": "forschung-und-lehre",
        "page_url": "https://www.forschung-und-lehre.de",
        "search_url": lambda x: f"/suchergebnis?id=88&tx_kesearch_pi1%5Bsword%5D={x}&tx_kesearch_pi1%5Bpage%5D=1&tx_kesearch_pi1%5BresetFilters%5D=0&tx_kesearch_pi1%5BsortByField%5D=score&tx_kesearch_pi1%5BsortByDir%5D=desc",
        "request": {
            "type": "get",
            "url": "https://www.forschung-und-lehre.de",
            "url_payload": lambda x: f"/suchergebnis?id=88&tx_kesearch_pi1%5Bsword%5D={x}&tx_kesearch_pi1%5Bpage%5D=1&tx_kesearch_pi1%5BresetFilters%5D=0&tx_kesearch_pi1%5BsortByField%5D=score&tx_kesearch_pi1%5BsortByDir%5D=desc",
            "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "div",
                    "class": "result-list-item",
                },
            ],
            "keys": {
                "title": {
                    "scope": "one",
                    "type": "span",
                    "class": "result-title",
                    "access": lambda x: x.a.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "",
                    "access": lambda x: x["href"]
                },
                "desc": {
                    "scope": "one",
                    "type": "span",
                    "class": "result-teaser",
                    "access": lambda x: x.get_text()
                },
            },
        },
    },
    {
        "name": "e-teaching",
        "page_url": "https://www.e-teaching.org",
        "search_url": lambda x: "/global_search",
        "request": {
            "type": "post",
            "url": "https://www.e-teaching.org",
            "url_payload": lambda x: "/global_search",
            "payload": lambda x: {"query": x},
            "replacements": {
                "(": " ",
                ")": " ",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "article",
                    "class": "row",
                },
            ],
            "keys": {
                "title": {
                    "scope": "one",
                    "type": "a",
                    "class": "list-group-item",
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "list-group-item",
                    "access": lambda x: x["href"]
                },
                "desc": {
                    "scope": "one",
                    "type": "a",
                    "class": "page-link",
                    "access": lambda x: x.get_text()
                },
            },
        },
    },
    # TODO this is a problem since it changes regularly
    # cse_tok=AB-tC_6FkFxkHXZgRV_VzcjMT2zK%3A1718005954739
    {
        "name": "focus",
        "page_url": "https://www.focus.de",
        "search_url": lambda x: f"/suche/?q={x}",
        "request": {
            "type": "get",
            "url": "https://cse.google.com",
            "url_payload": lambda x: f"/cse/element/v1?rsz=filtered_cse&num=10&hl=de&source=gcsc&gss=.de&cselibv=8435450f13508ca1&cx=006046384882075175371%3Axnjsrxzqupw&q={x}&safe=off&cse_tok=AB-tC_6FkFxkHXZgRV_VzcjMT2zK%3A1718005954739&sort=&exp=cc%2Cpos%2Cdtsq-3&fexp=72519171%2C72519168&callback=google.search.cse.api1996",
             "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
                "ä": "%C3%A4",
            },
        },
        "response": {
            "type": "google",
            "list_keys": ["results"],
            "keys": {
                "date": ["richSnippet", "metatags", "date"],
                "title": ["title"],
                "url": ["url"],
                "desc": ["richSnippet", "metatags", "ogDescription"],
                # "type": ["richSnippet", "metatags", "ogType"],
            }
        }
    },
    {
        "name": "spektrum",
        "page_url": "https://www.spektrum.de",
        "search_url": lambda x: f"/suche/#/q/{x}",
        "request": {
            "type": "auth",
            "user": "sdw-ro",
            "pw": "sdw-ro",
            # "base64": "c2R3LXJvOnNkdy1ybw==",
            "url": "https://solr.spektrum.de",
            "url_payload": lambda x: f"/solr/sdw/select?q={x}",
             "replacements": {
                " ": "%20",
                "/": "\/",
            },
        },
        "response": {
            "type": "json",
            "list_keys": ["response", "docs"],
            "keys": {
                "title": ["title"],
                "url": ["link"],
                "desc": ["description"],
                "type": ["artikeltyp"],
                "publication": ["erschienen"],
            }
        }
    },
    {
        "name": "fr",
        "page_url": "https://www.fr.de",
        "search_url": lambda x: f"/suche/?tt=1&tx=&sb=&td=&fd=&qr={x}",
        "request": {
            "type": "get",
            "url": "https://www.fr.de",
            "url_payload": lambda x: f"/suche/?tt=1&tx=&sb=&td=&fd=&qr={x}",
             "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "html",
            "list_keys": [
                {
                    "scope": "all",
                    "type": "div",
                    "class": "id-LinkOverlay",
                },
            ],
            "keys": {
                "date": {
                    "scope": "one",
                    "type": "time",
                    "class": "id-DateTime",
                    "access": lambda x: x["datetime"]
                },
                "title": {
                    "scope": "one",
                    "type": "h3",
                    "class": "id-Teaser-el-content-headline",
                    "access": lambda x: x.get_text()
                },
                "url": {
                    "scope": "one",
                    "type": "a",
                    "class": "id-LinkOverlay-link",
                    "access": lambda x: x["href"]
                },
                "desc": {
                    "scope": "one",
                    "type": "span",
                    "class": "id-Teaser-el-content-text-text",
                    "access": lambda x: x.get_text()
                },
            },
        },
    },
    # TODO this is a problem since it changes regularly
    # cse_tok=AB-tC_5_bjNJ_0NmfesFwf9iejgs%3A1718009560670
    {
        "name": "bild",
        "page_url": "https://bild.de",
        "search_url": lambda x: f"/suche.bild.html#gsc.tab=0&gsc.q={x}&gsc.sort=date",
        "request": {
            "type": "get",
            "url": "https://cse.google.com",
            "url_payload": lambda x: f"/cse/element/v1?rsz=filtered_cse&num=10&hl=de&source=gcsc&gss=.de&cselibv=8435450f13508ca1&cx=5178ff0c134dc483f&q={x}&safe=off&cse_tok=AB-tC_5_bjNJ_0NmfesFwf9iejgs%3A1718009560670&lr=&cr=&gl=de&filter=1&sort=date&as_oq=&as_sitesearch=www.bild.de%2F*&exp=cc&fexp=72519171%2C72519168&callback=google.search.cse.api13697",
            "replacements": {
                " ": "+",
                "/": "%2F",
                ":": "%3A",
                "(": "%28",
                ")": "%29",
            },
        },
        "response": {
            "type": "google",
            "list_keys": ["results"],
            "keys": {
                "title": ["title"],
                "url": ["url"],
                "content": ["content"],
                "desc": ["richSnippet", "metatags", "ogDescription"],
                # "type": ["richSnippet", "metatags", "ogType"],
            }
        }
    },
]
