import csv
import os
from typing import Optional

class MiniDb:
    def __init__(self, filename, fields: list[str]):
        self.filename = filename
        self.seq_file = filename.replace('.csv', '.seq')
        self.fields = fields

        if not os.path.exists(self.seq_file):
            with open(self.seq_file, 'w') as f:
                f.write("0")

        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fields)
                writer.writeheader()

    def insert(self, data: dict) -> dict:
        with open(self.seq_file, 'r+') as f:
            current_id = int(f.read())
            new_id = current_id + 1
            f.seek(0)
            f.write(str(new_id))
            f.truncate()

        data_row = {'id': str(new_id), **data, 'deleted': 'False', 'active': 'True'}
        with open (self.filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writerow(data_row)
        return data_row

    def read_one(self, target_id) -> Optional[dict]:
        with open(self.filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            searched_user = next((u for u in reader if u.get('id') == str(target_id)), None)
            return searched_user

    def read(self):
        with open(self.filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader if row['deleted'] == 'False']

    def update(self, id, new_data) -> Optional[dict]:
        updated = None
        with open(self.filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]
        for row in rows:
            if row['id'] == str(id) and row['deleted'] == 'False':
                row.update(new_data)
                updated = row
                break
        if updated:
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fields)
                writer.writeheader()
                writer.writerows(rows)
            return updated
        else:
            return None

    def delete(self, id) -> bool:
        deleted = False
        with open(self.filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]

        for row in rows:
            if row['id'] == str(id) and row['deleted'] == 'False':
                row['deleted'] = 'True'
                deleted = True
                break
        if deleted:
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fields)
                writer.writeheader()
                writer.writerows(rows)
        return deleted

    def count(self) -> int:
        count = 0
        with open(self.filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['deleted'] == 'False':
                    count += 1
        return count

    def vacuum(self):
        temp_file = self.filename + '.tmp'
        with open(self.filename, 'r', newline='', encoding='utf-8') as f_in, \
            open(temp_file, 'w', newline='', encoding='utf-8') as f_out:
            reader = csv.DictReader(f_in)
            writer = csv.DictWriter(f_out, fieldnames=self.fields)
            writer.writeheader()
            for row in reader:
                if row['deleted'] == 'False':
                    writer.writerow(row)
        os.replace(temp_file, self.filename)
