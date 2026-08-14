# NBS DBMS — A Lightweight Hash + BST Database Engine

NBS DBMS is a small, dependency-free, command-line database management system written in pure Python. It lets you create tables, insert/search/edit/delete records, list all records in sorted order, and persist everything to disk in a compressed binary file — all from an interactive REPL.

The engine is built from scratch on top of a **hash table whose buckets are binary search trees (BSTs)** instead of the usual linked lists, plus a **zlib-compressed JSON storage layer** for saving and loading the database.

---

## 1. Project Structure

```
nbs_dbms/
├── main.py        # CLI / REPL — the user-facing interface
├── engine.py       # Table class — hashing, insert/search/delete/edit/display
├── bst_file.py     # bs_tree / TreeNode — the BST used inside each hash bucket
└── storage.py      # save_datwrite completely in one file
```

Each file has one job. `main.py` never touches the tree directly, `engine.py` never touches the disk, and `storage.py` never touches the tree directly — it always goes through `engine.py`. This separation keeps the interface, the data structure, and the persistence logic independent of each other.

---

## 2. What Each File Does

### 2.1 `main.py` — The Interface Layer

This is the entry point (`python main.py`). It runs a REPL (read–eval–print loop) that:

1. Loads the database from disk on startup via `storage.load_database()`.
2. Prints a `dbms>>` prompt (or `dbms>>tablename>>` once you're inside a table).
3. Reads a line of input, splits it on whitespace, and treats the first word as the **command** and the rest as **arguments**.
4. Dispatches to the matching block of logic (`CREATE_TABLE`, `INSERT`, `SEARCH`, etc.) via a long `if / elif` chain.
5. Wraps the whole loop in `try/except` so a bad command (`IndexError`, `ValueError`) or `Ctrl+C` doesn't crash the program — it either prints a friendly error or saves the database before exiting.
6. On `EXIT`, calls `storage.save_database()` before terminating.

**Key idea used to optimize it:** the interface holds no data of its own — `curr_table` is just a reference to a `Table` object living inside the `table` list. So switching between commands (`INSERT`, `SEARCH`, `DELETE`...) inside a table never re-fetches or re-parses anything; it's operating directly on the live object. Validation (argument count, datatype checks, duplicate-key checks) is also pushed to the top of each command block so invalid input is rejected in O(1) *before* any tree operation is attempted, saving wasted hashing/tree work.

### 2.2 `bst_file.py` — The BST (Bucket Storage)

Defines two things:

- **`TreeNode`** — a plain node holding `val` (the primary key), `lst` (the full record), and `left` / `right` pointers.
- **`bs_tree`** — an unbalanced binary search tree with `insert`, `delete_fn`, `search_fn`, `min_node_fn`, `max_node_fn`, `GetHeight`, `clean`, and `inorder`.

This BST is what sits **inside every hash bucket** (see 2.3) instead of a simple Python list/linked-list, so that even within one bucket, records stay ordered and searchable in better-than-linear time.

**Key ideas used to optimize it:**
- **Iterative insert/search** (no recursion) — avoids Python's recursion overhead and the ~1000-frame recursion limit, so a bucket can hold arbitrarily many records without a stack-overflow risk.
- **Morris inorder traversal** (`inorder()`) — instead of the classic recursive/stack-based inorder traversal (O(n) extra space), it temporarily rethreads the tree's `right` pointers to simulate a stack, giving **O(1) extra space** for a full sorted dump of a bucket. This matters because `inorder()` is called on *every* bucket whenever you run `DISPLAY`.
- **`delete_fn` avoids full recursive restructuring** — it patches pointers in place (attaching the deleted node's left subtree under the in-order successor) rather than rebuilding the subtree, keeping deletion close to O(h) where h is the tree height.

### 2.3 `engine.py` — The Table / Storage Engine

Defines the `Table` class, which is really a **hybrid hash table** where every bucket is a `bs_tree` from `bst_file.py`, rather than a plain chained list. This is the core data-structure trick of the whole project.

**Key ideas used to optimize it:**
- **Custom polynomial rolling hash** (`my_hash`) — `h = h*31 + ord(ch)` mod `2^32`, the same style of hash used in Java's `String.hashCode()`. Cheap to compute, and spreads string/int keys fairly evenly across buckets.
- **Hash + BST hybrid buckets** — a pure hash table with linked-list chaining degrades to O(n) search under heavy collisions. Here, each bucket is itself a BST, so even a "bad" bucket with many collisions still searches/inserts in roughly O(log k) for k items in that bucket, rather than O(k).
- **Automatic resizing (`double_array`)** — when *any single bucket* reaches 256 nodes, the whole table doubles its bucket count and every record is re-hashed and reinserted. This is a classic **load-factor control** technique (similar to how Python dicts / Java HashMaps resize) that keeps buckets small and searches fast, at the amortized cost of an occasional O(n) rehash.
- **K-way merge with a min-heap for `DISPLAY`** (`merge_k_sorted`) — each bucket's `inorder()` already returns a *sorted* list of records. Instead of concatenating all buckets and sorting the whole thing (O(n log n) with a big constant), `engine.py` uses Python's `heapq` to merge all already-sorted bucket lists in **O(n log b)**, where `b` is the number of buckets — the same algorithmic idea used in external/merge sort and in merging sorted runs across shards of a real database.
- **Lazy datatype detection** — the table doesn't require you to declare a column datatype up front; it infers `int` vs `str` from the first inserted primary key and then enforces consistency, avoiding a rigid schema-definition step for a small CLI tool.

### 2.4 `storage.py` — The Persistence Layer

Handles saving/loading the whole database to a single file (`nbs_database.bin`):

- **`save_database`** walks every table, exports `col_name`, `datatype`, and every record (via `Table.display()`, i.e. the sorted, merged output from `engine.py`), builds one big dict, serializes it to JSON, then **compresses it with `zlib`** before writing it to disk.
- **`load_database`** reverses the process: reads the compressed bytes, `zlib.decompress`s them, `json.loads`s the string back into a dict, then rebuilds each `Table` object and re-inserts every record (which naturally rebuilds the hash buckets and BSTs from scratch).

**Key ideas used to optimize it:**
- **Compress-on-write** — JSON is verbose (repeated keys, whitespace), so compressing it with `zlib` before hitting disk significantly shrinks the file size and I/O time, at a small CPU cost. The benchmark below shows roughly a **3.5x size reduction**.
- **Single-file, single-write persistence** — rather than writing one file per table or doing incremental disk writes on every command, the whole database is flushed once (on `EXIT` or `Ctrl+C`), which avoids repeated disk I/O overhead during normal operation.
- **Schema-light rebuild on load** — instead of persisting the tree structure itself, only the *records* are persisted; the BST/hash structure is deterministically rebuilt by replaying inserts. This keeps the on-disk format simple (just JSON) and structure-agnostic — you could change the tree/hash implementation entirely and old save files would still load correctly.

---

## 3. Command Syntax Reference

All commands are typed at the `dbms>>` prompt and are case-insensitive (the first word is upper-cased internally).

| Command | Syntax | What it does |
|---|---|---|
| `CREATE_TABLE` | `CREATE_TABLE <table_name> COLUMNS <col1> <col2> ...` | Creates a new table with the given column names. The 3rd token onward becomes `col_name`; token index 2 is expected to be a keyword slot (e.g. `COLUMNS`) per the `command_parts[3:]` slicing. Fails if the table already exists or fewer than 4 tokens are given. |
| `ENTER_TABLE` | `ENTER_TABLE <table_name>` | Opens a table for record-level operations (`INSERT`, `SEARCH`, etc.). Fails if a table is already open or the table doesn't exist. |
| `SHOW_TABLE` | `SHOW_TABLE` | Lists the names of all created tables. |
| `EXIT_TABLE` | `EXIT_TABLE` | Closes the currently open table and returns to the top-level `dbms>>` prompt. |
| `INSERT` | `INSERT <val1> <val2> ... <valN>` | Inserts a record into the currently open table. Number of values must match the number of columns. Numeric-looking values are auto-cast to `int`. Rejects duplicate primary keys (first value). |
| `DISPLAY` | `DISPLAY` | Prints every record in the open table, sorted by primary key, as a formatted `| col | col | ...` table. |
| `SEARCH` | `SEARCH <key>` | Looks up a record by primary key and prints it. Datatype of `<key>` must match the table's inferred datatype. |
| `DELETE` | `DELETE <key>` | Deletes the record with the given primary key. |
| `EDIT` | `EDIT <column_name> TO <new_value> for <key>` (6 tokens total) | Edits a field of an existing record. If the edited column is the primary key (index 0), it re-hashes the record by deleting and re-inserting it under the new key. |
| `EXIT` | `EXIT` | Saves the database to disk (compressed) and quits. |

> Note: `EDIT` and `CREATE_TABLE` are positional/token-count based (`command_parts[1]`, `command_parts[3]`, `command_parts[5]`, etc.) rather than keyword-parsed, so extra/missing words will shift the meaning of arguments — stick to the exact token count shown above.

**Example session:**
```
dbms>> CREATE_TABLE students COLUMNS id name marks
dbms>> ENTER_TABLE students
dbms>>students>> INSERT 1 Alice 88
dbms>>students>> INSERT 2 Bob 91
dbms>>students>> DISPLAY
|  id | name | marks |

|  1 |  Alice |  88 |

|  2 |  Bob |  91 |

dbms>>students>> SEARCH 2
|  2 |  Bob |  91 |
dbms>>students>> EDIT marks TO 95 FOR 2
dbms>>students>> DELETE 1
dbms>>students>> EXIT_TABLE
dbms>> EXIT
Compressing and saving data...
Saved. Raw size: 189 bytes -> Compressed: 142 bytes
```

---

## 4. Benchmarks

Measured on the reference implementation with `time.perf_counter()`, Python 3, single-threaded, keys inserted in randomized order (seed=42), 3 records per row (`id`, `name`, `value`).

| Records (N) | Insert time (total) | Insert (per op) | 2,000 random searches | Search (per op) | `DISPLAY` (full sorted dump) | Final bucket count |
|---:|---:|---:|---:|---:|---:|---:|
| 1,000 | 7.1 ms | 7.1 µs | 2.46 ms | 1.23 µs | 0.55 ms | 8 |
| 5,000 | 112.4 ms | 22.5 µs | 6.57 ms | 3.28 µs | 4.39 ms | 64 |
| 20,000 | 390.5 ms | 19.5 µs | 11.45 ms | 5.73 µs | 21.0 ms | 128 |

**Persistence (N = 10,000 records):**

| Operation | Time | Notes |
|---|---|---|
| `save_database` | ~28.9 ms | Serialize + zlib compress + write |
| `load_database` | ~259.3 ms | Read + decompress + parse + rebuild all trees via re-insert |
| Raw JSON size | 262,337 bytes | Before compression |
| Compressed file size | 74,211 bytes | **~3.5x smaller on disk** |

**Takeaways:**
- Search stays in the **single-digit-microsecond** range even at 20K records because the hash spreads records across many small BSTs — each lookup only walks a shallow tree inside one bucket, not the whole dataset.
- `load_database` is much slower than `save_database` because loading **replays every insert** (rebuilding the hash+BST structure from scratch), whereas saving just walks and serializes existing sorted data — this is the expected cost trade-off of not persisting the tree structure directly (see §2.4).
- Insert time per-op briefly rises then stabilizes around 19–22 µs/op — the bumps line up with `double_array()` resize events, which are individually O(n) but happen rarely (amortized O(1) per insert overall).

*(Re-run `bench.py`, included below, on your own machine to reproduce or extend these numbers — absolute timings will vary by hardware.)*

---

## 5. Installation & Setup

### Requirements
- Python 3.7+ (no third-party packages — only the standard library: `os`, `sys`, `json`, `zlib`, `heapq`, `collections`)

### Steps

1. **Get the files.** Place `main.py`, `engine.py`, `bst_file.py`, and `storage.py` in the same directory.

2. **(Optional) Verify your Python version:**
   ```bash
   python3 --version
   ```

3. **Run the DBMS:**
   ```bash
   python3 main.py
   ```
   This starts the interactive `dbms>>` prompt.

4. **Use the commands** from the [syntax reference](#3-command-syntax-reference) above to create tables, insert data, and query it.

5. **Exit and persist:**
   ```
   dbms>> EXIT
   ```
   This writes `nbs_database.bin` (a zlib-compressed JSON blob) into the current working directory. The next time you run `python3 main.py` from that same directory, your tables and records will be loaded back automatically.

6. **Force-quit safety net:** pressing `Ctrl+C` at any point also triggers a save before exiting, so data loss from an accidental interrupt is minimized.

No installation of external dependencies, virtual environments, or build steps is required — it's a single `python3 main.py` away from running.
