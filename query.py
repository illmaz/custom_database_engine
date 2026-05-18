import ctypes

lib = ctypes.CDLL("./libheap.dylib")

class Row(ctypes.Structure):
    _fields_ = [
        ("is_occupied", ctypes.c_ubyte),
        ("id", ctypes.c_uint),
        ("name", ctypes.c_char * 32),
        ("age", ctypes.c_ubyte)
    ]
    _pack_ = 1

ROWS_PER_PAGE = 4096 // 38

class Page(ctypes.Structure):
    _fields_ = [
        ("rows", Row * ROWS_PER_PAGE)
    ]

BUFFER_SIZE = 3

class BufferSlot(ctypes.Structure):
    _fields_ = [
        ("page_number", ctypes.c_int),
        ("is_used", ctypes.c_int)
    ]

class BufferPool(ctypes.Structure):
    _fields_ = [
        ("pages", Page * BUFFER_SIZE),
        ("slots", BufferSlot * BUFFER_SIZE)
    ]

lib.init_buffer_pool.argtypes = [ctypes.POINTER(BufferPool)]
lib.init_buffer_pool.restype = None
lib.get_page.argtypes = [ctypes.POINTER(BufferPool), ctypes.c_char_p, ctypes.c_int]
lib.get_page.restype = ctypes.POINTER(Page)
lib.insert_row.argtypes = [ctypes.POINTER(Page), ctypes.c_int, Row]
lib.insert_row.restype = None
lib.write_page.argtypes = [ctypes.POINTER(Page), ctypes.c_char_p, ctypes.c_int]
lib.write_page.restype = None
lib.count_pages.argtypes = [ctypes.c_char_p]
lib.count_pages.restype = ctypes.c_int
lib.delete_row.argtypes = [ctypes.POINTER(Page), ctypes.c_int]
lib.delete_row.restype = None

pool = BufferPool()
lib.init_buffer_pool(ctypes.byref(pool))

def insert(row_dict):
    page_count = lib.count_pages(b"heap.db")
    target_page = max(0, page_count - 1)

    row = Row()
    row.is_occupied = 1
    row.id = row_dict["id"]
    row.name = row_dict["name"].encode()
    row.age = row_dict["age"]

    page = lib.get_page(ctypes.byref(pool), b"heap.db", target_page)

    for slot in range(ROWS_PER_PAGE):
        if page.contents.rows[slot].is_occupied == 0:
            lib.insert_row(page, slot, row)
            lib.write_page(page, b"heap.db", target_page)
            return

def select_all():
    page_count = lib.count_pages(b"heap.db")
    results = []
    for page_num in range(page_count):
        page = lib.get_page(ctypes.byref(pool), b"heap.db", page_num)
        for slot in range(ROWS_PER_PAGE):
            row = page.contents.rows[slot]
            if row.is_occupied == 1:
                results.append({
                    "id": row.id,
                    "name": row.name.decode(),
                    "age": row.age
                })
    return results

def select_where(field, value):
    page_count = lib.count_pages(b"heap.db")
    results = []
    for page_num in range(page_count):
        page = lib.get_page(ctypes.byref(pool), b"heap.db", page_num)
        for slot in range(ROWS_PER_PAGE):
            row = page.contents.rows[slot]
            if row.is_occupied == 1:
                row_dict = {
                    "id": row.id,
                    "name": row.name.decode(),
                    "age": row.age
                }
                if row_dict[field] == value:
                    results.append(row_dict)
    return results

def delete(field, value):
    page_count = lib.count_pages(b"heap.db")

    for page_num in range(page_count):
        page = lib.get_page(ctypes.byref(pool), b"heap.db", page_num)
        for slot in range(ROWS_PER_PAGE):
            row = page.contents.rows[slot]
            if row.is_occupied == 1: 
                row_dict = {
                    "id": row.id,
                    "name": row.name.decode(),
                    "age": row.age
                }
                if row_dict[field] == value:
                    lib.delete_row(page, slot)
                    lib.write_page(page, b"heap.db", page_num)
                    return

insert({"id": 1, "name": "Alice", "age": 30})
insert({"id": 2, "name": "Bob", "age": 25})

print("before delete:")
for row in select_all():
    print(row)

delete("name", "Alice")

print("after delete:")
for row in select_all():
    print(row)