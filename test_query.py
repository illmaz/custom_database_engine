import ctypes
import unittest
import os

from query import insert, select_all, select_where, delete

class TestEngine(unittest.TestCase):


    def test_insert_and_select_all(self):
        insert({"id": 1, "name": "Alice", "age": 30})
        insert({"id": 2, "name": "Bob", "age": 25})
        rows = select_all()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["name"], "Alice")
        self.assertEqual(rows[1]["name"], "Bob")

    def test_select_where(self):
        insert({"id": 1, "name": "Alice", "age": 30})
        insert({"id": 2, "name": "Bob", "age": 30})
        rows = select_where("name", "Alice")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "Alice")

    def test_delete(self):
        insert({"id": 1, "name": "Alice", "age": 30})
        insert({"id": 2, "name": "Bob", "age": 25})
        delete("name", "Alice")
        rows = select_all()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "Bob")
    
    def test_round_trip(self):
        insert({"id": 1, "name": "Alice", "age": 30})
        delete("name", "Alice")
        rows = select_all()
        self.assertEqual(len(rows), 0)
        insert({"id": 2, "name": "Charlie", "age": 22})
        rows = select_all()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "Charlie")
    
    def setUp(self):
        if os.path.exists("heap.db"):
            os.remove("heap.db")
        from query import pool, lib, BufferPool, index 
        lib.init_buffer_pool(ctypes.byref(pool))
        index.root.keys = []
        index.root.values = []
        index.root.children = []
        index.root.is_leaf = True

    def test_select_by_id(self):
        from query import select_by_id
        insert({"id": 1, "name": "Alice", "age": 30})
        insert({"id": 2, "name": "Bob", "age": 25})
        row = select_by_id(1)
        self.assertIsNotNone(row)
        self.assertEqual(row["name"], "Alice")
        row = select_by_id(9)
        self.assertIsNone(row)

if __name__ == "__main__":
    unittest.main()