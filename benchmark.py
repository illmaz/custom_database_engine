import os
import time
import ctypes
from query import insert, select_where, select_by_id

if os.path.exists("heap.db"):
    os.remove("heap.db")

from query import index, pool, lib
index.root.keys = []
index.root.values = []
index.root.children = []
index.root.is_leaf = True
lib.init_buffer_pool(ctypes.byref(pool))

print("inserting 500 rows...")
for i in range(1, 501):
    insert({"id": i, "name": f"User{i}", "age": i % 100})

target_id = 499

start = time.perf_counter()
for _ in range(100):
    select_where("id", target_id)
scan_time = (time.perf_counter() - start) / 100

start = time.perf_counter()
for _ in range(100):
    select_by_id(target_id)
index_time = (time.perf_counter() - start) / 100

print(f"select_where (full scan):  {scan_time * 1000:.3f} ms")
print(f"select_by_id (B-tree):     {index_time * 1000:.3f} ms")
print(f"speedup: {scan_time / index_time:.1f}x faster")