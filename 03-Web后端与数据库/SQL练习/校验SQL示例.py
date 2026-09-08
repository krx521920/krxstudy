"""Execute marked SQL from the notes, using only isolated in-memory SQLite DBs.

Run with Python 3.10+ from any working directory. No third-party dependencies.
No database file, network connection, note modification, or production access.
"""

from contextlib import closing
from math import isclose
from pathlib import Path
import re
import sqlite3


HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
VAULT = NOTES.parent
FIXTURE = (HERE / "订单样例.sql").read_text(encoding="utf-8-sig")
TITLES = [
    "SQL与关系型数据库学习地图",
    "SQL基础查询与多表关联",
    "关系型数据库设计：建模、约束与范式",
    "SQL复杂统计与报表设计",
    "SQL窗口函数：排名、累计与同期比较",
    "SQL数据清洗与质量校验",
    "SQL事务、锁与并发一致性",
    "SQL索引、执行计划与性能优化",
    "B+树与数据库索引原理",
    "数据库事务日志、主从复制与故障恢复",
    "SQL订单实战：样例数据与练习",
]

EXPECTED = {
    "latest_paid": [(109, 3, 5000), (108, 2, 5000), (106, 1, 20000)],
    "customer_counts": [(1, 3), (2, 2), (3, 2), (4, 0), (5, 0)],
    "never_paid": [(4,), (5,)],
    "big_customers": [(1, 40000)],
    "repeated_buyers": [(1,), (2,), (3,)],
    "cte_steps": [(2,)],
    "recursive_numbers": [(1,), (2,), (3,), (4,), (5,)],
    "status_summary": [(10, 7, 2, 82000)],
    "order_metrics": [(7, 3, 820.0, 820.0 / 7)],
    "fanout_wrong": [(4, 60000)],
    "net_order_total": [(82000, 5000, 77000)],
    "daily_report": [
        ("2026-08-01", 1, 15000), ("2026-08-02", 2, 25000),
        ("2026-08-03", 0, 0), ("2026-08-04", 2, 32000),
        ("2026-08-05", 0, 0), ("2026-08-06", 2, 10000),
        ("2026-08-07", 0, 0),
    ],
    "category_report": [("外设", 80000), ("配件", 2000)],
    "share_of_customer": [
        (101, 1, 15000, 40000), (102, 1, 5000, 40000),
        (106, 1, 20000, 40000), (103, 2, 20000, 25000),
        (108, 2, 5000, 25000), (105, 3, 12000, 17000),
        (109, 3, 5000, 17000),
    ],
    "ranks": [
        (103, 20000, 1, 1, 1), (106, 20000, 2, 1, 1),
        (101, 15000, 3, 3, 2), (105, 12000, 4, 4, 3),
        (102, 5000, 5, 5, 4), (108, 5000, 6, 5, 4),
        (109, 5000, 7, 5, 4),
    ],
    "latest_per_customer": [(1, 106), (2, 108), (3, 109)],
    "customer_running": [
        (101, 1, 15000), (102, 1, 20000), (106, 1, 40000),
        (103, 2, 20000), (108, 2, 25000),
        (105, 3, 12000), (109, 3, 17000),
    ],
    "daily_lag": [
        ("2026-08-01", 15000, None, None),
        ("2026-08-02", 25000, 15000, 2 / 3),
        ("2026-08-03", 0, 25000, -1.0),
        ("2026-08-04", 32000, 0, None),
        ("2026-08-05", 0, 32000, -1.0),
        ("2026-08-06", 10000, 0, None),
        ("2026-08-07", 0, 10000, -1.0),
    ],
    "rolling_week": [
        ("2026-08-01", 15000, 1, 150.0),
        ("2026-08-02", 40000, 2, 200.0),
        ("2026-08-03", 40000, 3, 400 / 3),
        ("2026-08-04", 72000, 4, 180.0),
        ("2026-08-05", 72000, 5, 144.0),
        ("2026-08-06", 82000, 6, 820 / 6),
        ("2026-08-07", 82000, 7, 820 / 7),
    ],
    "contact_classification": [
        (1, "alice@example.com", "accepted_candidate"),
        (2, "alice@example.com", "accepted_candidate"),
        (3, None, "missing_email"), (4, None, "missing_email"),
        (5, "bob@example.com", "accepted_candidate"),
        (6, "bob@example.com", "accepted_candidate"),
        (7, "not-an-email", "invalid_email"),
        (8, "carol@example.com", "accepted_candidate"),
    ],
    "clean_contacts": [
        (2, "alice@example.com", "Alice Li"),
        (6, "bob@example.com", "Bob New"),
        (8, "carol@example.com", "Carol"),
    ],
    "order_amount_mismatches": [],
    "excessive_refunds": [],
    "indexed_customer_orders": [
        (106, "2026-08-04", 20000), (102, "2026-08-02", 5000),
        (101, "2026-08-01", 15000),
    ],
    "keyset_page": [
        (105, "2026-08-04"), (103, "2026-08-02"), (102, "2026-08-02"),
    ],
}
MUTATIONS = {"reserve_one", "optimistic_update"}


def fresh_db():
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys = ON")
    assert db.execute("PRAGMA foreign_keys").fetchone() == (1,)
    db.executescript(FIXTURE)
    return db


def assert_rows(actual, expected, label):
    assert len(actual) == len(expected), (label, actual, expected)
    for got, want in zip(actual, expected):
        assert len(got) == len(want), (label, got, want)
        for value, reference in zip(got, want):
            if isinstance(reference, float):
                assert isinstance(value, (int, float)) and isclose(
                    value, reference, rel_tol=1e-10, abs_tol=1e-10
                ), (label, got, want)
            else:
                assert value == reference, (label, got, want)


def collect_examples():
    examples = {}
    vault_stems = {p.stem for p in VAULT.rglob("*.md")}
    for title in TITLES:
        note = NOTES / f"{title}.md"
        content = note.read_text(encoding="utf-8-sig")
        assert len(re.findall(r"^```", content, re.M)) % 2 == 0, note
        assert "verified: 2026-09-08" in content, note
        for target in re.findall(r"\[\[([^\]|#]+)(?:[^\]]*)\]\]", content):
            assert target in vault_stems, (note.name, "unresolved link", target)
        for sql in re.findall(r"```sql\s*\n(.*?)\n```", content, re.S):
            tag = re.search(r"^-- lab: ([a-z_]+)\s*$", sql, re.M)
            if tag:
                name = tag.group(1)
                assert name not in examples, ("duplicate tag", name)
                examples[name] = sql
    assert set(examples) == set(EXPECTED) | MUTATIONS, (
        "example inventory differs", set(examples) ^ (set(EXPECTED) | MUTATIONS)
    )
    return examples


def check_constraint(sql):
    with closing(fresh_db()) as db:
        try:
            db.execute(sql)
        except sqlite3.IntegrityError:
            db.rollback()
        else:
            raise AssertionError(f"Invalid data was accepted: {sql}")


def main():
    assert sqlite3.sqlite_version_info >= (3, 25, 0), "Window functions required"
    print(f"SQLite {sqlite3.sqlite_version}; isolated in-memory fixtures only")
    examples = collect_examples()
    for name, sql in examples.items():
        with closing(fresh_db()) as db:
            if name in MUTATIONS:
                assert db.execute(sql).rowcount == 1, name
                assert db.execute("SELECT stock, version FROM inventory").fetchone() == (0, 1)
                assert db.execute(sql).rowcount == 0, name
                db.rollback()
                assert db.execute("SELECT stock, version FROM inventory").fetchone() == (1, 0)
            else:
                assert_rows(db.execute(sql).fetchall(), EXPECTED[name], name)
        print(f"PASS {name}")

    invalid_writes = [
        "INSERT INTO customers VALUES (1, 'Duplicate', 'Test')",
        "INSERT INTO orders VALUES (999,999,'2026-08-01',NULL,'pending',100)",
        "UPDATE inventory SET stock = -1 WHERE product_id = 10",
        "UPDATE orders SET status = 'unknown' WHERE order_id = 101",
        "UPDATE orders SET paid_day = NULL WHERE order_id = 101",
        "UPDATE orders SET amount_cents = NULL WHERE order_id = 101",
        "INSERT INTO order_items VALUES (101,1,10,1,10000)",
        "INSERT INTO refunds VALUES (999,101,'2026-08-07',0)",
    ]
    for sql in invalid_writes:
        check_constraint(sql)
    print(f"PASS {len(invalid_writes)} invalid-write constraint checks")

    with closing(fresh_db()) as db:
        db.execute("BEGIN")
        assert db.execute(examples["reserve_one"]).rowcount == 1
        db.execute("INSERT INTO customers VALUES (6, 'Rollback', 'Test')")
        db.rollback()
        assert db.execute("SELECT stock, version FROM inventory").fetchone() == (1, 0)
        assert db.execute("SELECT COUNT(*) FROM customers WHERE customer_id=6").fetchone() == (0,)
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
        assert db.execute("PRAGMA integrity_check").fetchone() == ("ok",)
    print("PASS multi-statement rollback, foreign keys, and SQLite integrity")

    with closing(fresh_db()) as db:
        db.execute("UPDATE orders SET amount_cents=15001 WHERE order_id=101")
        assert_rows(db.execute(examples["order_amount_mismatches"]).fetchall(), [(101,)], "detect mismatch")
        db.execute("INSERT INTO refunds VALUES (9,101,'2026-08-07',20000)")
        assert_rows(db.execute(examples["excessive_refunds"]).fetchall(), [(101,)], "detect over-refund")
    print("PASS quality rules detect deliberately corrupted practice data")

    with closing(fresh_db()) as db:
        query = examples["indexed_customer_orders"]
        before = db.execute(query).fetchall()
        db.execute("CREATE INDEX idx_orders_customer_status_day ON orders(customer_id,status,paid_day DESC,order_id DESC)")
        assert_rows(db.execute(query).fetchall(), before, "index preserves result")
        plan = db.execute("EXPLAIN QUERY PLAN " + query).fetchall()
        print("OBSERVED SQLite plan:", " | ".join(row[3] for row in plan))
    print(f"PASS {len(TITLES)} notes: link targets, fences, example inventory")
    print(f"SUCCESS: {len(examples)} marked SQL examples plus safety/quality checks")
    print("Not tested: MySQL/PostgreSQL dialects, real concurrent locks, crash recovery, replication, production speed.")


if __name__ == "__main__":
    main()
