# custom-engine

A toy database engine built from scratch in C and Python, written by a data engineer who wanted to understand how storage engines actually work under the hood, and to learn C along the way.

## Why I built this

I work with data pipelines daily but always treated databases as a black box. I wanted to understand how rows become bytes, how pages are managed in memory, and how a query layer sits on top of raw storage — so I built one myself, phase by phase.

## Phase map

**Phase 1 — `db_phase1.py`**
Pure Python. Manually serializes a row into binary using `struct`, writes it to a flat file, and reads it back. No C, no pages — just raw bytes.

**Phase 2 — `page.c`**
C implementation of a single page with fixed-size rows. Introduces the `Row` and `Page` structs, `insert_row`, `write_page`, and `read_page`. Compiled to a standalone binary.

**Phase 3 — `heap.c`**
Extends the page into a full heap file. Multiple pages stored back to back on disk. Adds `open_or_create`, page-number-aware `write_page` and `read_page`, and `count_pages`.

**Phase 4 — `heap.c` continued**
Adds the buffer pool. `BufferPool` and `BufferSlot` structs, `init_buffer_pool`, and `get_page` — which checks memory first and only goes to disk on a cache miss.

**Phase 5 — `query.py`**
Python query layer on top of the C engine. Loads `libheap.dylib` via `ctypes`, defines the structs in Python to match C, and exposes `insert`, `select_all`, and `select_where`.

## How to compile and run

**Phase 2 — C page binary**
```bash
gcc page.c -o page
./page
```

**Phase 3–5 — shared library and Python query layer**
```bash
gcc -shared -fPIC -o libheap.dylib heap.c
python3 query.py
```

## Example

```python
insert({"id": 1, "name": "Alice", "age": 30})
insert({"id": 2, "name": "Bob",   "age": 25})

select_all()
# [{'id': 1, 'name': 'Alice', 'age': 30}, {'id': 2, 'name': 'Bob', 'age': 25}]

select_where("name", "Alice")
# [{'id': 1, 'name': 'Alice', 'age': 30}]
```

## Known limitations

- Buffer pool holds 3 pages — no eviction when full
- No delete yet
- No index — `select_where` does a full scan
- Single process only, no concurrency