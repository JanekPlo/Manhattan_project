# Projekt bazy danych – system zamówień firmy usługowej „ProServ”

Projekt na przedmiot **57 MC – FIR – Informatyka w zarządzaniu**.
Relacyjna baza danych obsługi zamówień firmy usługowej w MS Access, odtworzona
w aplikacji no-code (Knack/Tadabase), wraz z kwerendami, formularzami i pełnym
sprawozdaniem.

## Struktura projektu

```
.
├── README.md                       # ten plik
├── ProServ.accdb                   # GOTOWA baza MS Access (4 tabele, relacje, dane)
├── build_db.py                     # buduje i weryfikuje bazę z plików SQL
├── baza_proserv.sqlite             # pomocnicza baza do weryfikacji (generowana)
├── sql/
│   ├── 01_schema.sql               # 4 tabele, klucze, relacje, więzy integralności
│   ├── 02_dane.sql                 # dane przykładowe
│   ├── 03_kwerendy.sql             # 4 kwerendy (2 proste, 2 złożone) – wersja ogólna
│   └── kwerendy_ms_access.sql      # te same 4 kwerendy w dialekcie MS Access
├── data/                           # dane w CSV (import do Access/Knack) + instrukcja
│   ├── klient.csv, usluga.csv, zamowienie.csv, szczegoly_zamowienia.csv
│   └── README.md                   # jak zaimportować CSV (Knack i Access)
├── generate_csv.py                 # eksport danych do CSV
└── sprawozdanie/
    ├── sprawozdanie.md             # sprawozdanie (źródło)
    ├── sprawozdanie.docx           # sprawozdanie do druku  ← PRACA DO ODDANIA
    ├── instrukcja_nocode.md        # instrukcja krok po kroku: Knack / Tadabase
    └── build_docx.py               # generator pliku .docx
```

## Co oddać prowadzącemu

1. **`sprawozdanie/sprawozdanie.docx`** – główny dokument pracy.
2. **`ProServ.accdb`** – plik bazy MS Access.

Część no-code wykonuje się w Knack.com (lub Tadabase.io) wg
`sprawozdanie/instrukcja_nocode.md` i dokumentuje zrzutami ekranu w sprawozdaniu.

## Model danych

Cztery tabele w relacjach 1:∞ (oraz wiele-do-wielu przez tabelę pośredniczącą):

```
klient  1───∞  zamowienie  1───∞  szczegoly_zamowienia  ∞───1  usluga
```

## Uruchomienie / weryfikacja

**Baza MS Access:** otwórz `ProServ.accdb` w programie MS Access. Kwerendy
utworzysz, wklejając zapytania z `sql/kwerendy_ms_access.sql`
(Tworzenie → Projekt kwerendy → Widok SQL → wklej → Uruchom).

**Automatyczna weryfikacja** (Python 3, bez dodatkowych bibliotek):

```bash
python3 build_db.py     # tworzy baza_proserv.sqlite i wypisuje wyniki 4 kwerend
```

**Sprawozdanie .docx** (wymaga `pip install python-docx`):

```bash
cd sprawozdanie && python3 build_docx.py
```

## Odpowiedniość MS Access ↔ SQL ↔ no-code

| MS Access | SQL (ten projekt) | Knack/Tadabase |
|---|---|---|
| Autonumerowanie (PK) | `INTEGER PRIMARY KEY AUTOINCREMENT` | wbudowane pole ID |
| Klucz obcy + relacja | `FOREIGN KEY ... REFERENCES` | pole *Connection* |
| Kwerenda wybierająca | `SELECT ... WHERE` | filtr widoku |
| Kwerenda złożona | `JOIN` + `GROUP BY` | pole *Equation/Sum*, widok z grupowaniem |
| Formularz | — | element *Form* |

Szczegóły każdego etapu opisano w `sprawozdanie/sprawozdanie.md`.
