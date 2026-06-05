# Projekt bazy danych – system zamówień firmy usługowej „ProServ”

Projekt na przedmiot **57 MC – FIR – Informatyka w zarządzaniu**.
Relacyjna baza danych obsługi zamówień firmy usługowej, odtworzona dodatkowo w
aplikacji no-code, wraz z formularzami i pełnym sprawozdaniem.

## Struktura projektu

```
.
├── README.md                     # ten plik
├── build_db.py                   # buduje i weryfikuje bazę z plików SQL
├── baza_proserv.sqlite           # gotowa baza (generowana przez build_db.py)
├── sql/
│   ├── 01_schema.sql             # 4 tabele, klucze, relacje, więzy integralności
│   ├── 02_dane.sql               # dane przykładowe
│   └── 03_kwerendy.sql           # 4 kwerendy (2 proste, 2 złożone)
├── nocode-app/
│   └── index.html                # działająca aplikacja no-code z formularzami
└── sprawozdanie/
    ├── sprawozdanie.md           # sprawozdanie (źródło)
    ├── sprawozdanie.docx         # sprawozdanie do druku
    └── build_docx.py             # generator pliku .docx
```

## Model danych

Cztery tabele w relacjach 1:∞ (oraz wiele-do-wielu przez tabelę pośredniczącą):

```
klient  1───∞  zamowienie  1───∞  szczegoly_zamowienia  ∞───1  usluga
```

## Uruchomienie

**Baza danych i kwerendy** (wymaga Pythona 3, bez dodatkowych bibliotek):

```bash
python3 build_db.py
```

Skrypt tworzy `baza_proserv.sqlite`, sprawdza więzy integralności i wypisuje
wyniki czterech kwerend.

**Aplikacja no-code** – otwórz `nocode-app/index.html` w przeglądarce.
Pozwala dodawać, edytować i przeglądać klientów, usługi i zamówienia
(z dynamicznymi pozycjami). Dane zapisywane są lokalnie w przeglądarce.

**Sprawozdanie .docx** (wymaga `pip install python-docx`):

```bash
cd sprawozdanie && python3 build_docx.py
```

## Odpowiedniość MS Access ↔ SQL ↔ no-code

| MS Access | SQL (ten projekt) | Knack/Tadabase |
|---|---|---|
| Autonumerowanie (PK) | `INTEGER PRIMARY KEY AUTOINCREMENT` | pole ID |
| Klucz obcy + relacja | `FOREIGN KEY ... REFERENCES` | pole *Connection* |
| Kwerenda wybierająca | `SELECT ... WHERE` | filtr widoku |
| Kwerenda złożona | `JOIN` + `GROUP BY` | pole *Equation/Sum*, widok z grupowaniem |
| Formularz | — | element *Form* |

Szczegóły każdego etapu opisano w `sprawozdanie/sprawozdanie.md`.
