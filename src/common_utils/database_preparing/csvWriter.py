import csv

DELIMITER = "#"

class CsvWriter:
    def __init__(self, filename):
        self.filename = filename

    def write_tags_and_text(self, tags, text):
        row = []
        for tag in tags:
            row.append(tag)
        row.append(text)
        with open(self.filename, encoding="utf-8", mode="a", newline='') as file:
            csv_writer = csv.writer(file, delimiter=DELIMITER)
            csv_writer.writerow(row)
