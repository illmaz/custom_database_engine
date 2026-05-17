import struct

ROW_FORMAT = "!I32sB"
ROW_SIZE = struct.calcsize(ROW_FORMAT)

print(f"ROW_SIZE = {ROW_SIZE} bytes")

def serialize_row(row):
    name_bytes = row["name"].encode("utf-8")
    return struct.pack(ROW_FORMAT, row["id"], name_bytes, row["age"])

row = {"id": 1, "name": "Alice", "age": 30}
print(serialize_row(row))

with open("phase1.db", "wb") as f:
    f.write(serialize_row(row))

def deserialize_row(data):
    id_, name_byte, age = struct.unpack(ROW_FORMAT, data) 
    name = name_byte.rstrip(b"\x00").decode("utf-8")
    return {"id": id_, "name": name, "age": age}

def read_row(filepath):
    with open(filepath, "rb") as f: 
        data = f.read(ROW_SIZE)
        return deserialize_row(data)

result = read_row("phase1.db")
print(result)  