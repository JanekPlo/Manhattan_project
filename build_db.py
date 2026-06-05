#!/usr/bin/env python3
"""Buduje i weryfikuje bazę danych z plików SQL.

Wczytuje 01_schema.sql, 02_dane.sql i 03_kwerendy.sql, tworzy plik
baza_proserv.sqlite, a następnie uruchamia cztery kwerendy i wypisuje ich
wyniki w formie tabel. Służy jako automatyczny dowód, że projekt bazy
(struktura, relacje, dane, kwerendy) jest poprawny i spójny.

Użycie:
    python3 build_db.py
"""
import os
import re
import sqlite3
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SQL_DIR = os.path.join(BASE, "sql")
DB_PATH = os.path.join(BASE, "baza_proserv.sqlite")


def read(name):
    with open(os.path.join(SQL_DIR, name), encoding="utf-8") as f:
        return f.read()


def split_statements(sql):
    """Dzieli skrypt na pojedyncze zapytania, pomijając komentarze."""
    lines = [ln for ln in sql.splitlines() if not ln.strip().startswith("--")]
    body = "\n".join(lines)
    return [s.strip() for s in body.split(";") if s.strip()]


def print_table(cursor, rows):
    cols = [d[0] for d in cursor.description]
    widths = [len(c) for c in cols]
    str_rows = []
    for r in rows:
        cells = ["" if v is None else str(v) for v in r]
        str_rows.append(cells)
        widths = [max(w, len(c)) for w, c in zip(widths, cells)]
    sep = "+".join("-" * (w + 2) for w in widths)
    header = "|".join(f" {c:<{w}} " for c, w in zip(cols, widths))
    print(sep)
    print(header)
    print(sep)
    for cells in str_rows:
        print("|".join(f" {c:<{w}} " for c, w in zip(cells, widths)))
    print(sep)
    print(f"({len(rows)} wierszy)\n")


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    # 1. struktura + dane
    conn.executescript(read("01_schema.sql"))
    conn.executescript(read("02_dane.sql"))
    conn.commit()

    # podsumowanie liczby rekordów
    print("=== Liczba rekordów w tabelach ===")
    for t in ("klient", "usluga", "zamowienie", "szczegoly_zamowienia"):
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t:<22} {n}")
    print()

    # kontrola więzów integralności
    problems = conn.execute("PRAGMA foreign_key_check").fetchall()
    print("=== Kontrola więzów integralności (FOREIGN KEY) ===")
    print("  OK – brak naruszeń" if not problems else f"  PROBLEMY: {problems}")
    print()

    # 2. kwerendy
    queries = split_statements(read("03_kwerendy.sql"))
    titles = [
        "KWERENDA PROSTA 1 – klienci z Warszawy",
        "KWERENDA PROSTA 2 – usługi droższe niż 1000 zł",
        "KWERENDA ZŁOŻONA 1 – wartość zamówień z danymi klienta",
        "KWERENDA ZŁOŻONA 2 – ranking usług wg przychodu",
    ]
    for i, q in enumerate(queries):
        title = titles[i] if i < len(titles) else f"KWERENDA {i + 1}"
        print(f"=== {title} ===")
        cur = conn.execute(q)
        print_table(cur, cur.fetchall())

    conn.close()
    print(f"Baza zapisana do: {DB_PATH}")


if __name__ == "__main__":
    sys.exit(main())
