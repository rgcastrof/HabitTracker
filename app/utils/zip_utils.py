import io
import zipfile
import csv

def generate_zip_stream(entities: dict[str, list[dict]]):
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_f:
        for filename, data in entities.items():
            csv_buffer = io.StringIO()
            fields = data[0].keys()
            writer = csv.DictWriter(csv_buffer, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
            zip_f.writestr(f"{filename}.csv", csv_buffer.getvalue())

    zip_buffer.seek(0)
    chunk_size = 1024 * 1024  # 1MB

    while chunk := zip_buffer.read(chunk_size):
        yield chunk
