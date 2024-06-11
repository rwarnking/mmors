import csv
from config import OUT_DIR


class Exporter:
    def __init__(self):
        pass

    ###############################################################################################
    # CSV exporter
    ###############################################################################################
    def export_csv(self, website, search_results):
        first = list(search_results.keys())[0]
        columns = ["term"]
        columns += [x for row in search_results[first] for x in row.keys()]
        columns = list(set(columns))

        file_path = str(OUT_DIR / f"{website['name']}.csv")
        with open(file_path, 'w', newline="", encoding="utf-8") as fou:
            csv_w = csv.writer(fou)
            csv_w.writerow(columns)

            for term, term_obj in search_results.items():
                filler = [""] * len(columns)
                csv_w.writerow(filler)
                for url_obj in term_obj:
                    url_obj["term"] = term
                    csv_w.writerow(map(lambda x: url_obj.get(x, ""), columns))

    ###############################################################################################
    # HTML exporter
    ###############################################################################################
    def export_html(self, website, search_results):
        if not search_results:
            return

        columns = []
        for key in website["response"]["keys"]:
            columns.append(key)

        file_path = str(OUT_DIR / f"{website['name']}.html")
        with open(file_path, 'w', encoding="utf-8") as fou:
            html_res = ""
            for term, term_obj in search_results.items():
                html_res += f"<h1>{term}</h1>"
                html_res += self._add_html_table(columns, term_obj)
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
