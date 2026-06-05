#!/usr/bin/env python3
"""Eksportuje dane z bazy do plików CSV (katalog data/).

Pliki CSV nadają się do importu zarówno do MS Access, jak i do Knack.com.
Dane pobierane są z baza_proserv.sqlite (budowanej przez build_db.py), dzięki
czemu są zawsze zgodne z resztą projektu. Pliki zapisywane są w kodowaniu
UTF-8 z BOM (utf-8-sig), aby polskie znaki poprawnie otwierały się w Excelu.

Użycie:
    python3 build_db.py        # najpierw zbuduj bazę
    python3 generate_csv.py
"""
import csv
import os
import sqlite3
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "baza_proserv.sqlite")
OUT = os.path.join(BASE, "data")

TABLES = ["klient", "usluga", "zamowienie", "szczegoly_zamowienia"]


def main():
    if not os.path.exists(DB):
        print("Buduję bazę (build_db.py)...")
        subprocess.run([sys.executable, os.path.join(BASE, "build_db.py")], check=True,
                       stdout=subprocess.DEVNULL)
    os.makedirs(OUT, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    for t in TABLES:
        rows = conn.execute(f"SELECT * FROM {t}").fetchall()
        path = os.path.join(OUT, f"{t}.csv")
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            if rows:
                w.writerow(rows[0].keys())
                for r in rows:
                    w.writerow(["" if v is None else v for v in r])
            else:
                # pusta tabela – nadal zapisujemy nagłówki z PRAGMA
                cols = [c[1] for c in conn.execute(f"PRAGMA table_info({t})").fetchall()]
                w.writerow(cols)
        print(f"  zapisano data/{t}.csv ({len(rows)} wierszy)")
    conn.close()


if __name__ == "__main__":
    main()
