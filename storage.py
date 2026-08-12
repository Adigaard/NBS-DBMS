import json
import os
import zlib
from engine import Table
DB_FILE = "aiga_database.bin"  # no longer .json, since it's now compressed bytes

def save_database(table_list, table_index):
    data_dump = {"table_index": table_index, "tables": []}

    for t in table_list:
        records = t.display()
        if records is None:
            records = []
        dt_str = "int" if t.datatype == int else "str" if t.datatype == str else None
        data_dump["tables"].append({
            "col_name": t.col_name,
            "datatype": dt_str,
            "records": records
        })

    # 1. Serialize: dict -> JSON string -> bytes
    json_string = json.dumps(data_dump)
    raw_bytes = json_string.encode('utf-8')

    # 2. Compress: this is your "compressor"
    compressed_bytes = zlib.compress(raw_bytes)

    # 3. Write compressed bytes to disk (note "wb" — write binary)
    with open(DB_FILE, "wb") as f:
        f.write(compressed_bytes)

    print(f"Saved. Raw size: {len(raw_bytes)} bytes -> Compressed: {len(compressed_bytes)} bytes")
#decompressor funtion
def load_database():
    if not os.path.exists(DB_FILE):
        return [], {}

    # 1. Read compressed bytes from disk (note "rb" — read binary)
    with open(DB_FILE, "rb") as f:
        compressed_bytes = f.read()

    # 2. Decompress back to raw bytes
    raw_bytes = zlib.decompress(compressed_bytes)

    # 3. Deserialize: bytes -> JSON string -> dict
    json_string = raw_bytes.decode('utf-8')
    data_dump = json.loads(json_string)

    table_index = data_dump["table_index"]
    table_list = []
    for t_data in data_dump["tables"]:
        new_table = Table(8)
        new_table.col_name = t_data["col_name"]
        new_table.datatype = int if t_data["datatype"] == "int" else str if t_data["datatype"] == "str" else None
        for record in t_data["records"]:
            new_table.insert(record)
        table_list.append(new_table)

    return table_list, table_index