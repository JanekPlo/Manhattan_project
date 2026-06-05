# Sprawozdanie z realizacji projektu bazy danych

**Przedmiot:** 57 MC – FIR – Informatyka w zarządzaniu
**Temat:** Projekt i implementacja relacyjnej bazy danych systemu obsługi zamówień firmy usługowej oraz jej odtworzenie w aplikacji no-code
**System przykładowy:** „ProServ” – firma świadcząca usługi cyfrowe (web, marketing, IT, grafika, szkolenia)

---

## Spis treści

1. [Wprowadzenie i cel projektu](#1-wprowadzenie-i-cel-projektu)
2. [Krok 1 – Utworzenie bazy danych i czterech tabel w MS Access](#2-krok-1--utworzenie-bazy-danych-i-czterech-tabel-w-ms-access)
3. [Krok 2 – Definicja relacji, kluczy głównych i obcych](#3-krok-2--definicja-relacji-kluczy-głównych-i-obcych)
4. [Krok 3 – Wypełnienie tabel danymi przykładowymi](#4-krok-3--wypełnienie-tabel-danymi-przykładowymi)
5. [Krok 4 – Cztery kwerendy (dwie proste, dwie złożone)](#5-krok-4--cztery-kwerendy-dwie-proste-dwie-złożone)
6. [Krok 5 – Odtworzenie struktury w aplikacji no-code](#6-krok-5--odtworzenie-struktury-w-aplikacji-no-code)
7. [Krok 6 – Formularze do wprowadzania i przeglądania danych](#7-krok-6--formularze-do-wprowadzania-i-przeglądania-danych)
8. [Krok 7 – Podsumowanie i wnioski](#8-krok-7--podsumowanie-i-wnioski)
9. [Załączniki – zawartość projektu](#9-załączniki--zawartość-projektu)

---

## 1. Wprowadzenie i cel projektu

Celem projektu było zaprojektowanie i zaimplementowanie relacyjnej bazy danych
obsługującej proces przyjmowania i realizacji zamówień w firmie usługowej, a
następnie odtworzenie tej samej struktury w aplikacji typu **no-code** wraz z
formularzami do obsługi danych. Projekt obejmuje pełny cykl pracy z bazą danych:
od modelu pojęciowego, przez fizyczną strukturę tabel, relacje i więzy
integralności, dane testowe i kwerendy analityczne, aż po warstwę aplikacyjną
(formularze) dostępną dla użytkownika końcowego.

Jako dziedzinę przyjęto firmę **ProServ**, świadczącą usługi cyfrowe. Model danych
oparto na czterech tabelach wymaganych w treści zadania:

| Tabela | Rola w systemie |
|---|---|
| `klient` | dane klientów (indywidualnych i firmowych) |
| `usluga` | katalog oferowanych usług wraz z cenami |
| `zamowienie` | nagłówki zamówień składanych przez klientów |
| `szczegoly_zamowienia` | pozycje zamówień – usługi wraz z ilością, ceną i rabatem |

Taki podział odpowiada klasycznemu, znormalizowanemu modelowi „zamówienie –
pozycje zamówienia”, w którym jedno zamówienie może obejmować wiele usług, a ta
sama usługa może występować w wielu zamówieniach (relacja **wiele-do-wielu**
rozwiązana tabelą pośredniczącą `szczegoly_zamowienia`).

> **Uwaga metodyczna.** Zadanie zakładało wykonanie bazy w MS Access oraz w
> aplikacji no-code. Bazę wykonano w MS Access (plik **`ProServ.accdb`**,
> format Access 2016, dołączony do pracy), a warstwę no-code odtworzono w
> platformie **Knack.com**, której procedurę odtworzenia opisano krok po kroku
> w załączniku `instrukcja_nocode.md`. Dodatkowo strukturę bazy zapisano w
> postaci skryptów SQL, co pozwala odtworzyć i automatycznie zweryfikować całość
> (skrypt `build_db.py`). Mapowanie typów danych MS Access ↔ SQL ↔ Knack
> opisano w kolejnych krokach.

---

## 2. Krok 1 – Utworzenie bazy danych i czterech tabel w MS Access

W programie MS Access bazę tworzy się poleceniem **Plik → Nowy → Pusta baza
danych programu Access**, zapisując ją jako `ProServ.accdb`. Następnie w widoku
projektu (**Projekt tabeli**) definiuje się kolejne tabele, ich pola, typy danych
oraz klucze podstawowe.

Poniżej przedstawiono strukturę każdej z czterech tabel wraz z typami danych
używanymi w MS Access. W nawiasach podano odpowiadające im typy w zapisie SQL
zastosowane w skryptach projektu.

### 2.1. Tabela `klient`

| Pole | Typ danych (MS Access) | Uwagi |
|---|---|---|
| **id_klienta** | Autonumerowanie | klucz podstawowy |
| imie | Krótki tekst | wymagane |
| nazwisko | Krótki tekst | wymagane |
| nazwa_firmy | Krótki tekst | puste dla klienta indywidualnego |
| email | Krótki tekst | wymagane, unikalne (indeks bez duplikatów) |
| telefon | Krótki tekst | |
| adres | Krótki tekst | |
| miasto | Krótki tekst | |
| kod_pocztowy | Krótki tekst | maska wprowadzania 00-000 |
| data_rejestracji | Data/godzina | wartość domyślna `=Date()` |

### 2.2. Tabela `usluga`

| Pole | Typ danych (MS Access) | Uwagi |
|---|---|---|
| **id_uslugi** | Autonumerowanie | klucz podstawowy |
| nazwa_uslugi | Krótki tekst | wymagane |
| kategoria | Krótki tekst | np. Web, Marketing, IT |
| opis | Długi tekst (Memo) | |
| cena_jednostkowa | Waluta | reguła poprawności `>=0` |
| jednostka | Krótki tekst | szt. / godz. / m-c |
| czas_realizacji | Liczba (całkowita) | orientacyjny czas w dniach |

### 2.3. Tabela `zamowienie`

| Pole | Typ danych (MS Access) | Uwagi |
|---|---|---|
| **id_zamowienia** | Autonumerowanie | klucz podstawowy |
| **id_klienta** | Liczba (długa całkowita) | **klucz obcy** → `klient` |
| data_zamowienia | Data/godzina | wartość domyślna `=Date()` |
| status | Krótki tekst | lista: Nowe / W realizacji / Zrealizowane / Anulowane |
| metoda_platnosci | Krótki tekst | lista: Przelew / Karta / Gotówka / BLIK |
| uwagi | Długi tekst (Memo) | |

### 2.4. Tabela `szczegoly_zamowienia`

| Pole | Typ danych (MS Access) | Uwagi |
|---|---|---|
| **id_szczegolu** | Autonumerowanie | klucz podstawowy |
| **id_zamowienia** | Liczba (długa całkowita) | **klucz obcy** → `zamowienie` |
| **id_uslugi** | Liczba (długa całkowita) | **klucz obcy** → `usluga` |
| ilosc | Liczba (całkowita) | `>0`, wartość domyślna 1 |
| cena | Waluta | cena usługi w chwili zamówienia |
| rabat | Liczba (pojedyncza) | 0–1 (np. 0,10 = 10%) |

**Mapowanie typów MS Access ↔ SQL** zastosowane w skryptach projektu:

| MS Access | SQL (skrypty projektu) |
|---|---|
| Autonumerowanie (klucz podstawowy) | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| Krótki / Długi tekst | `TEXT` |
| Waluta / Liczba | `REAL` |
| Data/godzina | `DATE` |
| Reguła poprawności | `CHECK (...)` |
| Indeks bez duplikatów | `UNIQUE` |

Pełna definicja struktury znajduje się w pliku **`sql/01_schema.sql`**.

---

## 3. Krok 2 – Definicja relacji, kluczy głównych i obcych

Relacje między tabelami w MS Access definiuje się w oknie **Narzędzia bazy danych
→ Relacje**, przeciągając klucz podstawowy jednej tabeli na klucz obcy drugiej i
zaznaczając opcję **„Wymuszaj więzy integralności”** (opcjonalnie z kaskadową
aktualizacją i usuwaniem powiązanych rekordów).

W projekcie zdefiniowano trzy relacje typu **jeden-do-wielu (1:∞)**:

| Relacja | Strona „1” | Strona „wiele” | Klucz obcy |
|---|---|---|---|
| Klient → Zamówienia | `klient.id_klienta` | `zamowienie` | `zamowienie.id_klienta` |
| Zamówienie → Pozycje | `zamowienie.id_zamowienia` | `szczegoly_zamowienia` | `szczegoly_zamowienia.id_zamowienia` |
| Usługa → Pozycje | `usluga.id_uslugi` | `szczegoly_zamowienia` | `szczegoly_zamowienia.id_uslugi` |

Dwie ostatnie relacje wspólnie realizują relację **wiele-do-wielu** między
zamówieniami a usługami: jedno zamówienie może zawierać wiele usług, a jedna
usługa może występować w wielu zamówieniach.

### Diagram związków encji (ERD)

```
        ┌──────────────────┐                 ┌──────────────────────┐
        │      KLIENT      │                 │        USLUGA        │
        ├──────────────────┤                 ├──────────────────────┤
        │ PK id_klienta    │                 │ PK id_uslugi         │
        │    imie          │                 │    nazwa_uslugi      │
        │    nazwisko      │                 │    kategoria         │
        │    nazwa_firmy   │                 │    cena_jednostkowa  │
        │    email         │                 │    jednostka         │
        │    ...           │                 │    czas_realizacji   │
        └────────┬─────────┘                 └───────────┬──────────┘
                 │ 1                                      │ 1
                 │                                        │
                 │ ∞                                      │ ∞
        ┌────────┴─────────┐   1        ∞   ┌────────────┴───────────────┐
        │    ZAMOWIENIE    ├───────────────►│   SZCZEGOLY_ZAMOWIENIA      │
        ├──────────────────┤                ├────────────────────────────┤
        │ PK id_zamowienia │                │ PK id_szczegolu            │
        │ FK id_klienta    │                │ FK id_zamowienia           │
        │    data_zamowien.│                │ FK id_uslugi               │
        │    status        │                │    ilosc                   │
        │    metoda_platn. │                │    cena                    │
        │    uwagi         │                │    rabat                   │
        └──────────────────┘                └────────────────────────────┘
```

**Więzy integralności** zapewniają spójność danych:

- nie można dodać zamówienia dla nieistniejącego klienta,
- nie można dodać pozycji odwołującej się do nieistniejącego zamówienia lub usługi,
- usunięcie zamówienia kaskadowo usuwa jego pozycje (`ON DELETE CASCADE`),
- usunięcie klienta lub usługi powiązanej z zamówieniami jest blokowane
  (`ON DELETE RESTRICT`), co chroni dane historyczne.

Poprawność więzów została potwierdzona automatycznie poleceniem
`PRAGMA foreign_key_check` (wynik: **brak naruszeń**).

---

## 4. Krok 3 – Wypełnienie tabel danymi przykładowymi

Każdą tabelę wypełniono realistycznymi danymi odzwierciedlającymi typowe
przypadki użycia systemu. Dane wprowadzono skryptem **`sql/02_dane.sql`**.

| Tabela | Liczba rekordów | Zakres danych |
|---|---|---|
| `klient` | 7 | klienci indywidualni i firmowi z różnych miast |
| `usluga` | 8 | usługi z 5 kategorii (Web, Marketing, Grafika, IT, Szkolenia) |
| `zamowienie` | 8 | zamówienia o różnych statusach i metodach płatności |
| `szczegoly_zamowienia` | 13 | wielopozycyjne zamówienia, część z rabatami |

Dane celowo zaprojektowano tak, aby umożliwić testowanie różnych scenariuszy:

- klienci indywidualni (bez nazwy firmy) oraz firmowi,
- zamówienia o statusach: Nowe, W realizacji, Zrealizowane, Anulowane,
- zamówienie anulowane bez pozycji (test obsługi pustych grup w kwerendach),
- pozycje z rabatami (5%, 10%, 15%) do weryfikacji obliczeń wartości,
- jeden klient z dwoma zamówieniami (test agregacji na poziomie klienta).

---

## 5. Krok 4 – Cztery kwerendy (dwie proste, dwie złożone)

Wszystkie kwerendy zapisano w pliku **`sql/03_kwerendy.sql`** i uruchomiono na
zbudowanej bazie. Poniżej opis każdej z nich wraz z rzeczywistym wynikiem.

### 5.1. Kwerenda prosta nr 1 – klienci z wybranego miasta

Filtruje tabelę `klient` według kryterium `miasto = 'Warszawa'` i sortuje wynik.
W MS Access odpowiada to kwerendzie wybierającej z kryterium wpisanym w polu
`miasto`.

```sql
SELECT id_klienta, imie, nazwisko, nazwa_firmy, telefon, miasto
FROM   klient
WHERE  miasto = 'Warszawa'
ORDER BY nazwisko, imie;
```

**Wynik:**

| id_klienta | imie | nazwisko | nazwa_firmy | telefon | miasto |
|---|---|---|---|---|---|
| 1 | Anna | Kowalska | | 601234567 | Warszawa |
| 4 | Tomasz | Zieliński | TechBud sp. z o.o. | 224556677 | Warszawa |

### 5.2. Kwerenda prosta nr 2 – usługi droższe niż 1000 zł

Wyświetla z tabeli `usluga` pozycje droższe niż 1000 zł, posortowane malejąco po
cenie.

```sql
SELECT nazwa_uslugi, kategoria, cena_jednostkowa, jednostka
FROM   usluga
WHERE  cena_jednostkowa > 1000
ORDER BY cena_jednostkowa DESC;
```

**Wynik:**

| nazwa_uslugi | kategoria | cena_jednostkowa | jednostka |
|---|---|---|---|
| Sklep internetowy | Web | 7900,00 | szt. |
| Projekt strony WWW | Web | 3500,00 | szt. |
| Audyt informatyczny | IT | 2500,00 | szt. |
| Logo i identyfikacja | Grafika | 1800,00 | szt. |
| Pozycjonowanie SEO | Marketing | 1200,00 | m-c |

### 5.3. Kwerenda złożona nr 1 – wartość zamówień z danymi klienta

Łączy trzy tabele (`zamowienie`, `klient`, `szczegoly_zamowienia`), oblicza
wartość każdego zamówienia z uwzględnieniem rabatu
(`ilosc × cena × (1 − rabat)`), zlicza pozycje i grupuje wynik po zamówieniu.
Złączenie zewnętrzne (`LEFT JOIN`) zapewnia, że zamówienie anulowane bez pozycji
również pojawia się w zestawieniu.

```sql
SELECT z.id_zamowienia AS nr_zamowienia,
       k.imie || ' ' || k.nazwisko AS klient,
       k.nazwa_firmy AS firma,
       z.data_zamowienia, z.status,
       COUNT(sz.id_szczegolu) AS liczba_pozycji,
       ROUND(SUM(sz.ilosc * sz.cena * (1 - sz.rabat)),2) AS wartosc_zamowienia
FROM      zamowienie z
JOIN      klient k ON k.id_klienta = z.id_klienta
LEFT JOIN szczegoly_zamowienia sz ON sz.id_zamowienia = z.id_zamowienia
GROUP BY  z.id_zamowienia, k.imie, k.nazwisko, k.nazwa_firmy,
          z.data_zamowienia, z.status
ORDER BY  wartosc_zamowienia DESC;
```

**Wynik:**

| nr | klient | firma | data | status | poz. | wartość |
|---|---|---|---|---|---|---|
| 3 | Tomasz Zieliński | TechBud sp. z o.o. | 2024-04-02 | W realizacji | 3 | 11 110,00 |
| 6 | Marek Wójcik | Wójcik Transport | 2024-05-25 | W realizacji | 2 | 10 710,00 |
| 2 | Piotr Nowak | Nowak Consulting | 2024-03-15 | Zrealizowane | 3 | 5 820,00 |
| 1 | Anna Kowalska | | 2024-03-01 | Zrealizowane | 2 | 5 120,00 |
| 4 | Magdalena Wiśniewska | | 2024-04-20 | Zrealizowane | 1 | 3 500,00 |
| 5 | Katarzyna Lewandowska | | 2024-05-08 | Nowe | 1 | 1 800,00 |
| 7 | Anna Kowalska | | 2024-06-10 | Nowe | 1 | 750,00 |
| 8 | Piotr Nowak | Nowak Consulting | 2024-06-18 | Anulowane | 0 | |

### 5.4. Kwerenda złożona nr 2 – ranking usług wg przychodu

Łączy `usluga`, `szczegoly_zamowienia` i `zamowienie`, grupuje po usłudze i
wylicza kilka miar jednocześnie: liczbę zamówień, liczbę sprzedanych sztuk oraz
przychód. Pomija zamówienia anulowane (`WHERE z.status <> 'Anulowane'`).

```sql
SELECT u.nazwa_uslugi, u.kategoria,
       COUNT(DISTINCT sz.id_zamowienia) AS liczba_zamowien,
       SUM(sz.ilosc) AS sztuk_sprzedanych,
       ROUND(SUM(sz.ilosc * sz.cena * (1 - sz.rabat)),2) AS przychod
FROM   usluga u
JOIN   szczegoly_zamowienia sz ON sz.id_uslugi = u.id_uslugi
JOIN   zamowienie z ON z.id_zamowienia = sz.id_zamowienia
WHERE  z.status <> 'Anulowane'
GROUP BY u.id_uslugi, u.nazwa_uslugi, u.kategoria
ORDER BY przychod DESC;
```

**Wynik:**

| nazwa_uslugi | kategoria | liczba_zamowien | sztuk | przychód |
|---|---|---|---|---|
| Pozycjonowanie SEO | Marketing | 2 | 9 | 9 540,00 |
| Sklep internetowy | Web | 1 | 1 | 7 110,00 |
| Projekt strony WWW | Web | 2 | 2 | 7 000,00 |
| Kampania Google Ads | Marketing | 2 | 8 | 6 390,00 |
| Logo i identyfikacja | Grafika | 2 | 2 | 3 420,00 |
| Audyt informatyczny | IT | 1 | 1 | 2 500,00 |
| Wsparcie techniczne | IT | 2 | 15 | 2 250,00 |
| Szkolenie z obsługi CMS | Szkolenia | 1 | 1 | 600,00 |

---

## 6. Krok 5 – Odtworzenie struktury w aplikacji no-code

Zgodnie z wymaganiem, tę samą strukturę odtworzono w środowisku no-code –
w platformie **Knack.com** (analogicznie można wykonać w **Tadabase.io**).
Poniżej opisano procedurę; pełną instrukcję „klik po kliku” wraz z listą
zrzutów ekranu zawiera załącznik **`instrukcja_nocode.md`**.

### 6.1. Procedura odtworzenia w Knack.com

1. **Założenie aplikacji** – po zalogowaniu wybieramy *Create New App* i nadajemy
   nazwę „ProServ”. Knack tworzy aplikację z pustą bazą (*Database*).
2. **Utworzenie obiektów (tabel).** W zakładce *Database* dodajemy cztery obiekty
   odpowiadające tabelom: `Klient`, `Usluga`, `Zamowienie`,
   `Szczegoly zamowienia`. Knack automatycznie tworzy pole identyfikatora
   (odpowiednik klucza podstawowego / Autonumerowania).
3. **Dodanie pól.** Dla każdego obiektu odwzorowujemy pola z MS Access, dobierając
   typy pól Knack:

   | Typ w MS Access | Typ pola w Knack |
   |---|---|
   | Krótki tekst | Short Text |
   | Długi tekst (Memo) | Paragraph Text |
   | Waluta | Currency |
   | Liczba | Number |
   | Data/godzina | Date/Time |
   | Lista wartości (status) | Multiple Choice |

4. **Odtworzenie relacji.** Zamiast klasycznych kluczy obcych Knack używa pól typu
   **Connection**:
   - w obiekcie `Zamowienie` dodajemy pole *Connection* do obiektu `Klient`
     (relacja *many Zamowienia to one Klient*),
   - w obiekcie `Szczegoly zamowienia` dodajemy dwa pola *Connection*: do
     `Zamowienie` oraz do `Usluga`.

   Dzięki temu zachowana zostaje ta sama logika relacji 1:∞ i wiele-do-wielu co
   w MS Access.
5. **Pola obliczeniowe.** Wartość pozycji (`ilosc × cena × (1 − rabat)`) realizuje
   się polem typu *Equation*, a sumę wartości zamówienia – polem *Sum* po
   powiązanych pozycjach (odpowiednik kwerendy złożonej).

### 6.2. Odwzorowanie pojęć MS Access w Knack

Kluczem do poprawnego odtworzenia bazy jest świadome odwzorowanie pojęć:

| MS Access | Knack | Uwaga |
|---|---|---|
| Tabela | Object (obiekt) | jeden obiekt = jedna tabela |
| Pole + typ danych | Field + typ pola | np. Waluta → Currency |
| Klucz podstawowy (Autonumer) | wbudowane pole ID rekordu | tworzone automatycznie |
| Klucz obcy + relacja | pole **Connection** | pilnuje spójności (więzy integralności) |
| Kwerenda złożona (agregacja) | pole **Equation** / **Sum** | wartość pozycji i suma zamówienia |
| Indeks bez duplikatów | opcja **Must be unique** | np. pole `email` |

Po wykonaniu tych kroków w Knack istnieją cztery obiekty z identycznym zestawem
pól jak w MS Access oraz trzy relacje (Connection) odpowiadające relacjom z bazy
Access. Zrzuty ekranu z gotowej aplikacji (rysunki 1–7 wg listy w
`instrukcja_nocode.md`) dokumentują strukturę, relacje, dane i formularze.

---

## 7. Krok 6 – Formularze do wprowadzania i przeglądania danych

W aplikacji no-code utworzono intuicyjne formularze umożliwiające pełną obsługę
danych (operacje **CRUD**: tworzenie, odczyt, aktualizacja, usuwanie). W Knack
formularze tworzy się w sekcji *Pages*, dodając elementy *Form* (dodawanie/edycja)
oraz *Table/Grid* (przeglądanie); szczegółowy sposób ich utworzenia opisano w
punkcie E załącznika `instrukcja_nocode.md`. Przygotowano następujące formularze
i widoki:

| Funkcja | Formularz / widok |
|---|---|
| Dodawanie i edycja klienta | formularz z polami imię, nazwisko, firma, e-mail, telefon, adres |
| Dodawanie i edycja usługi | formularz z ceną, kategorią, jednostką, czasem realizacji |
| Tworzenie zamówienia | formularz z **listą wyboru klienta** (relacja) oraz dynamiczną listą pozycji |
| Dodawanie pozycji zamówienia | wybór usługi z listy, podanie ilości, ceny i rabatu |
| Przeglądanie danych | widoki listowe z wyszukiwarką i wartościami wyliczanymi |

Najważniejsze cechy formularzy zapewniające intuicyjność:

- **Pola relacyjne jako listy rozwijane** – przy tworzeniu zamówienia klient i
  usługi wybierane są z listy, co eliminuje błędy i wymusza poprawność więzów
  integralności (nie można wskazać nieistniejącego rekordu).
- **Automatyczne podpowiedzi** – po wybraniu usługi formularz podpowiada jej cenę
  katalogową, którą można nadpisać (cena z chwili zamówienia).
- **Walidacja danych** – pola wymagane, kontrola formatu e-mail, ilość > 0,
  rabat w zakresie 0–100%.
- **Ochrona spójności** – próba usunięcia klienta lub usługi powiązanej z
  zamówieniami jest blokowana komunikatem, a usunięcie zamówienia kaskadowo
  usuwa jego pozycje (odpowiednik więzów `RESTRICT`/`CASCADE`).
- **Wartości wyliczane na bieżąco** – wartość pozycji i suma zamówienia liczone
  są automatycznie.

---

## 8. Krok 7 – Podsumowanie i wnioski

W ramach projektu zrealizowano wszystkie etapy określone w treści zadania:

1. ✅ Utworzono bazę danych z czterema poprawnie zaprojektowanymi tabelami.
2. ✅ Zdefiniowano relacje oraz klucze główne i obce z więzami integralności.
3. ✅ Wypełniono tabele realistycznymi danymi testowymi (7 + 8 + 8 + 13 rekordów).
4. ✅ Utworzono cztery kwerendy: dwie proste (filtrowanie) i dwie złożone
   (złączenia, grupowanie, agregacja, obliczenia z rabatem).
5. ✅ Odtworzono identyczną strukturę tabel i relacji w środowisku no-code.
6. ✅ Przygotowano intuicyjne formularze do dodawania, edycji i przeglądania
   danych.
7. ✅ Udokumentowano każdy etap w niniejszym sprawozdaniu.

**Wnioski.** Zastosowanie znormalizowanego modelu danych z tabelą pośredniczącą
`szczegoly_zamowienia` pozwoliło elastycznie obsłużyć zamówienia wielopozycyjne i
relację wiele-do-wielu między zamówieniami a usługami. Więzy integralności
gwarantują spójność danych niezależnie od warstwy aplikacyjnej. Przeniesienie tego
samego modelu do środowiska no-code okazało się bezpośrednie: relacje MS Access
(klucze obce) odpowiadają polom *Connection* w Knack, a kwerendy złożone –
polom obliczeniowym i widokom z grupowaniem. Potwierdza to, że dobrze
zaprojektowany model relacyjny jest niezależny od narzędzia i stanowi trwałą
podstawę systemu informatycznego w zarządzaniu.

---

## 9. Załączniki – zawartość projektu

| Plik / katalog | Opis |
|---|---|
| **`ProServ.accdb`** | **gotowa baza danych MS Access** (4 tabele, relacje, dane) |
| `sql/01_schema.sql` | definicja struktury czterech tabel, kluczy i relacji (DDL) |
| `sql/02_dane.sql` | przykładowe dane testowe |
| `sql/03_kwerendy.sql` | cztery kwerendy (2 proste, 2 złożone) – wersja ogólna/SQLite |
| `sql/kwerendy_ms_access.sql` | te same kwerendy w dialekcie MS Access (do wklejenia) |
| `data/*.csv` | dane czterech tabel w formacie CSV (import do Access/Knack) |
| `build_db.py` | skrypt budujący i weryfikujący bazę z plików SQL |
| `generate_csv.py` | eksport danych do plików CSV |
| `baza_proserv.sqlite` | pomocnicza, zbudowana baza do automatycznej weryfikacji |
| `sprawozdanie/instrukcja_nocode.md` | instrukcja krok po kroku odtworzenia w Knack/Tadabase |
| `sprawozdanie/sprawozdanie.md` | niniejsze sprawozdanie (źródło) |
| `sprawozdanie/sprawozdanie.docx` | sprawozdanie w formacie do druku |
| `README.md` | instrukcja uruchomienia projektu |

**Sposób weryfikacji projektu:**

- Plik **`ProServ.accdb`** otwiera się bezpośrednio w programie MS Access –
  zawiera cztery tabele, relacje z wymuszonymi więzami integralności oraz dane.
  Cztery kwerendy tworzy się, wklejając zapytania z pliku
  `sql/kwerendy_ms_access.sql` (Widok SQL → Uruchom).
- Niezależną weryfikację poprawności struktury, danych i kwerend zapewnia skrypt:

```bash
python3 build_db.py        # buduje bazę i wypisuje wyniki czterech kwerend
```

- Część no-code wykonuje się w Knack.com (lub Tadabase.io) zgodnie z załącznikiem
  `instrukcja_nocode.md`; gotową aplikację dokumentuje się zrzutami ekranu.
