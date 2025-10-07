import csv
import os

class MiniDb:
    def __init__(self, filename, fields: list[str]):
        self.filename = filename
        self.seq_file = filename.replace('.csv', '.seq')
        self.fields = ['id'] + fields + ['deleted']

        if not os.path.exists(self.seq_file):
            with open(self.seq_file, 'w') as f:
                f.write("0")

        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fields)
                writer.writeheader()
