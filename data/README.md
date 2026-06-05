# Pliki CSV z danymi – instrukcja importu

Pliki CSV zawierają te same dane co `ProServ.accdb` i baza SQL. Kodowanie:
**UTF-8 z BOM** (poprawne polskie znaki w Excelu). Kolumny odpowiadają polom
tabel; kolumny `id_*` to klucze (podstawowe i obce).

| Plik | Tabela | Wierszy |
|---|---|---|
| `klient.csv` | klient | 7 |
| `usluga.csv` | usluga | 8 |
| `zamowienie.csv` | zamowienie | 8 |
| `szczegoly_zamowienia.csv` | szczegoly_zamowienia | 13 |

> **Kolejność importu jest ważna** (z powodu relacji): najpierw `klient` i
> `usluga`, potem `zamowienie`, na końcu `szczegoly_zamowienia`.

---

## Import do Knack.com

Najpierw utwórz obiekty i pola wg `sprawozdanie/instrukcja_nocode.md`. Następnie
w każdym obiekcie: **Records → Import → CSV**.

Aby zaimportować również relacje (pola Connection), wykorzystaj kolumny `id_*`:

1. **Klient** – zaimportuj `klient.csv`. Zmapuj kolumnę `id_klienta` na zwykłe
   pole liczbowe (np. dodaj w obiekcie pole `id_klienta` typu Number). Reszta
   kolumn mapuje się na odpowiednie pola.
2. **Usluga** – zaimportuj `usluga.csv` (analogicznie, z polem `id_uslugi`).
3. **Zamowienie** – zaimportuj `zamowienie.csv`. Kolumnę `id_klienta` zmapuj na
   pole **Connection `klient`** i wybierz dopasowanie **„match on field:
   id_klienta”** (Knack połączy zamówienie z właściwym klientem po numerze).
4. **Szczegoly_zamowienia** – zaimportuj `szczegoly_zamowienia.csv`. Kolumnę
   `id_zamowienia` zmapuj na Connection `zamowienie` (match on `id_zamowienia`),
   a `id_uslugi` na Connection `usluga` (match on `id_uslugi`).

Po imporcie możesz ukryć pomocnicze pola `id_*` w widokach – relacje już działają.

---

## Import do MS Access

Plik `ProServ.accdb` zawiera już komplet danych, więc import nie jest konieczny.
Gdyby trzeba było odtworzyć dane od zera:

1. **Dane zewnętrzne → Nowe źródło danych → Z pliku → Plik tekstowy**.
2. Wskaż plik CSV, wybierz **„Rozdzielany”**, separator **przecinek**,
   stronę kodową **Unicode (UTF-8)**, zaznacz **„Pierwszy wiersz zawiera nazwy
   pól”**.
3. Importuj w kolejności: `klient`, `usluga`, `zamowienie`,
   `szczegoly_zamowienia` (do istniejących tabel, aby zachować typy i relacje).

---

## Regeneracja plików CSV

```bash
python3 build_db.py        # buduje baza_proserv.sqlite
python3 generate_csv.py    # eksportuje katalog data/*.csv
```
