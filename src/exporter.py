import csv
import os
from config import OUT_DIR


class Exporter:
    def __init__(self):
        pass

    def export_csv(self, urls_json):
        if not os.path.exists(OUT_DIR):
            os.makedirs(OUT_DIR)

        for medium, results in urls_json.items():

            first = list(results.keys())[0]
            columns = [x for row in results[first]["link_list"] for x in row.keys()]
            columns = list(set(columns))

            file_path = str(OUT_DIR / f"{medium}.csv")
            with open(file_path, 'w', encoding="utf-8") as fou:
                csv_w = csv.writer(fou)
                csv_w.writerow(columns)

                # TODO add term to csv
                for term, term_obj in results.items():
                    for url_obj in term_obj["link_list"]:
                        csv_w.writerow(map(lambda x: url_obj.get(x, ""), columns))

    def export_html(self, urls_json):
        if not os.path.exists(OUT_DIR):
            os.makedirs(OUT_DIR)

        for medium, results in urls_json.items():

            first = list(results.keys())[0]
            # TODO
            # columns = [x for row in results[first]["link_list"] for x in row.keys()]
            # columns = list(set(columns))
            columns = ["date", "title", "url"]

            file_path = str(OUT_DIR / f"{medium}.html")
            with open(file_path, 'w', encoding="utf-8") as fou:
                html_res = ""
                for term, term_obj in results.items():
                    html_res += f"<h1>{term}</h1>"
                    html_res += self._add_html_table(columns, term_obj["link_list"])
                fou.write(html_res)

    def _add_html_table(self, h_row, rows):
        table = "<table>"

        table += self._add_html_th(h_row)
        table += self._add_html_tds(rows)

        table += "</table>"
        return table

    def _add_html_th(self, h_row):
        table_row = "<tr>"
        for e in h_row:
            table_row += f"<th>{e}</th>"

        table_row += "</tr>"
        return table_row

    def _add_html_tds(self, rows):
        table_rows = ""
        for row in rows:
            table_rows += self._add_html_td(row)
        return table_rows

    def _add_html_td(self, row):
        table_row = "<tr>"
        for e in row.values():
            if e is None:
                table_row += f'<td>{e}</td>'
                continue

            if e.startswith("http"):
                table_row += f'<td><a href="{e}">{e}</a></td>'
            else:
                table_row += f'<td>{e}</td>'

        table_row += "</tr>"
        return table_row
