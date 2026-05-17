import ctypes

lib = ctypes.CDLL("./libheap.dylib")
print("library loaded")

class Row(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint),
        ("name", ctypes.c_char * 32),
        ("age", ctypes.c_ubyte)
    ]
    _pack_ = 1

ROWS_PER_PAGE = 4096 // 37

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

pool = BufferPool()
lib.init_buffer_pool(ctypes.byref(pool))

p0 = lib.get_page(ctypes.byref(pool), b"heap.db", 0)
print(f"id: {p0.contents.rows[0].id}, name: {p0.contents.rows[0].name}, age: {p0.contents.rows[0].age}")

p1 = lib.get_page(ctypes.byref(pool), b"heap.db", 1)
print(f"id: {p1.contents.rows[0].id}, name: {p1.contents.rows[0].name}, age: {p1.contents.rows[0].age}")
