import io
import zipfile
import csv

def get_database_data():
    with open("users.csv", 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def generate_zip_stream():
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_f:
        with zip_f.open("users.csv", mode='w') as csv_file:
            writer = io.TextIOWrapper(csv_file, encoding='utf-8', newline='')
            csv_writer = None

            for row in get_database_data():  # Essa função retorna os dados do seu mini banco
                if csv_writer is None:
                    fieldnames = list(row.keys())
                    csv_writer = csv.DictWriter(writer, fieldnames=fieldnames)
                    csv_writer.writeheader()
                csv_writer.writerow(row)
            writer.flush()

    zip_buffer.seek(0)
    chunk_size = 1024 * 1024  # 1MB

    while chunk := zip_buffer.read(chunk_size):
        yield chunk
