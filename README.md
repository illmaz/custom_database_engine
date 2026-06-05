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
Adds the buffer pool. `BufferPool` and `BufferSlot` structs, `init_buffer_pool`, and `get_page` — which checks memory first and only goes to disk on a cache miss. Uses LRU eviction when all slots are full.

**Phase 5 — `query.py`, `repl.py`, and `btree.py`**
Python query layer on top of the C engine. Loads `libheap.dylib` via `ctypes`, defines the structs in Python to match C, and exposes `insert`, `select_all`, `select_where`, `select_by_id`, and `delete`. Includes a B-tree index for O(log n) id lookups, an interactive REPL, and a test suite.

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

**Interactive REPL**
```bash
gcc -shared -fPIC -o libheap.dylib heap.c
python3 repl.py
```

**Tests**
```bash
python3 test_query.py
```

**Benchmark**
```bash
gcc -shared -fPIC -o libheap.dylib heap.c
python3 benchmark.py
```

## Benchmark

500 rows, looking up id=499 (worst case for a full scan), averaged over 100 runs.

`select_where("id", 499)` — full scan, O(n) — 0.213 ms

`select_by_id(499)` — B-tree index, O(log n) — 0.003 ms

**81.7x faster** with the B-tree index.

## Example — Python

```python
insert({"id": 1, "name": "Alice", "age": 30})
insert({"id": 2, "name": "Bob",   "age": 25})

select_all()
# [{'id': 1, 'name': 'Alice', 'age': 30}, {'id': 2, 'name': 'Bob', 'age': 25}]

select_where("name", "Alice")
# [{'id': 1, 'name': 'Alice', 'age': 30}]

select_by_id(2)
# {'id': 2, 'name': 'Bob', 'age': 25}

delete("name", "Alice")
select_all()
# [{'id': 2, 'name': 'Bob', 'age': 25}]
```

## Example — REPL

```
> insert 1 Alice 30
inserted.
> insert 2 Bob 25
inserted.
> select all
{'id': 1, 'name': 'Alice', 'age': 30}
{'id': 2, 'name': 'Bob', 'age': 25}
> select id 2
{'id': 2, 'name': 'Bob', 'age': 25}
> select where name Alice
{'id': 1, 'name': 'Alice', 'age': 30}
> delete name Alice
deleted.
> select all
{'id': 2, 'name': 'Bob', 'age': 25}
```

## Known limitations

- B-tree index lives in memory only — does not persist to disk between sessions, rebuilt on startup by scanning the heap
- `delete` does not remove entries from the B-tree index — stale entries accumulate but `select_by_id` handles them correctly by checking `is_occupied`
- `delete` only removes the first matching row
- `select_where` on non-id fields still does a full scan
- Single process only, no concurrency