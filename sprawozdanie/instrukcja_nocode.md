# Instrukcja krok po kroku – odtworzenie bazy w aplikacji no-code

Instrukcja opisuje, jak odtworzyć bazę „ProServ” w platformie **Knack.com**
(wersja darmowa/trial). Na końcu podano różnice dla **Tadabase.io**. W trakcie
wykonywania rób **zrzuty ekranu** w miejscach oznaczonych 📸 – posłużą jako
ilustracje w sprawozdaniu.

## Szacowany czas wykonania (≈ 60–90 min)

| Etap | Czas |
|---|---|
| A. Założenie konta i aplikacji | ~5 min |
| B. Cztery obiekty i pola | ~20–25 min |
| C. Relacje (Connection) i pola obliczeniowe | ~10 min |
| D. Import danych z CSV | ~10 min |
| E. Strony i formularze | ~15 min |
| Zrzuty ekranu + testy | ~10 min |
| **Razem** | **~60–90 min** (osoba robiąca to pierwszy raz) |

---

## A. Założenie konta i aplikacji

1. Wejdź na **https://www.knack.com** i kliknij **Start Free Trial**. Załóż
   konto (e-mail + hasło) i potwierdź je z poczty.
2. Po zalogowaniu kliknij **Create New App → Start from Scratch**.
3. Nazwij aplikację **ProServ** i zatwierdź. Otworzy się **Builder** z trzema
   zakładkami u góry: **Database**, **Pages**, **Settings**.
   📸 *Zrzut: pusty Builder aplikacji ProServ.*

---

## B. Utworzenie tabel (obiektów) i pól

W Knack tabela nazywa się **Object**, a kolumna – **Field**. Każdy obiekt ma
automatyczne pole identyfikatora (odpowiednik klucza podstawowego /
autonumerowania w Access).

### B.1. Obiekt `Klient`

1. Zakładka **Database → Add Object**, nazwa **Klient**, **Continue**.
2. Dodaj pola przyciskiem **Add Field** (typ pola w nawiasie):
   - `imie` (Short Text), `nazwisko` (Short Text)
   - `nazwa_firmy` (Short Text)
   - `email` (Email)
   - `telefon` (Phone)
   - `adres` (Short Text), `miasto` (Short Text), `kod_pocztowy` (Short Text)
   - `data_rejestracji` (Date/Time)
3. W polu `email` zaznacz **Must be unique** (odpowiednik indeksu bez duplikatów).
   📸 *Zrzut: lista pól obiektu Klient.*

### B.2. Obiekt `Usluga`

Dodaj obiekt **Usluga** i pola:
- `nazwa_uslugi` (Short Text)
- `kategoria` (Multiple Choice: Web, Marketing, Grafika, IT, Szkolenia)
- `opis` (Paragraph Text)
- `cena_jednostkowa` (Currency)
- `jednostka` (Multiple Choice: szt., godz., m-c)
- `czas_realizacji` (Number)
  📸 *Zrzut: lista pól obiektu Usluga.*

### B.3. Obiekt `Zamowienie`

Dodaj obiekt **Zamowienie** i pola:
- `data_zamowienia` (Date/Time)
- `status` (Multiple Choice: Nowe, W realizacji, Zrealizowane, Anulowane)
- `metoda_platnosci` (Multiple Choice: Przelew, Karta, Gotówka, BLIK)
- `uwagi` (Paragraph Text)

(Pole relacji do klienta dodasz w punkcie C.)

### B.4. Obiekt `Szczegoly_zamowienia`

Dodaj obiekt **Szczegoly_zamowienia** i pola:
- `ilosc` (Number)
- `cena` (Currency)
- `rabat` (Number – wpisuj ułamek, np. 0,1 = 10%)

(Pola relacji do zamówienia i usługi dodasz w punkcie C.)

---

## C. Odtworzenie relacji (klucze obce → pola Connection)

W Knack relację tworzy pole typu **Connection**. Zastępuje ono klucz obcy z
MS Access i automatycznie pilnuje spójności (można wskazać tylko istniejący
rekord – odpowiednik więzów integralności).

1. **Zamowienie → Klient (1:∞).** W obiekcie **Zamowienie** → *Add Field* →
   typ **Connection** → *Connect to* **Klient**. Relacja:
   **„Each Zamowienie connects to one Klient”** oraz
   **„Each Klient connects to many Zamowienie”**. Nazwij pole `klient`.
2. **Szczegoly_zamowienia → Zamowienie (1:∞).** W obiekcie
   **Szczegoly_zamowienia** dodaj Connection do **Zamowienie**
   (many szczegóły → one zamówienie). Nazwij `zamowienie`.
3. **Szczegoly_zamowienia → Usluga (1:∞).** Dodaj Connection do **Usluga**
   (many szczegóły → one usługa). Nazwij `usluga`.

Te trzy relacje odpowiadają dokładnie relacjom z MS Access; punkty 2 i 3 wspólnie
realizują relację **wiele-do-wielu** między zamówieniami a usługami.
📸 *Zrzut: pole Connection przy tworzeniu relacji Zamowienie→Klient.*

### C.1. Pola obliczeniowe (odpowiednik kwerend złożonych)

1. W **Szczegoly_zamowienia** dodaj pole **Equation** o nazwie `wartosc`
   z formułą: `{ilosc} * {cena} * (1 - {rabat})` (wynik typu Currency).
2. W **Zamowienie** dodaj pole **Sum** o nazwie `wartosc_zamowienia`,
   sumujące pole `wartosc` z powiązanych rekordów Szczegoly_zamowienia.
   📸 *Zrzut: konfiguracja pola Sum w obiekcie Zamowienie.*

---

## D. Wprowadzenie danych

Dane wpiszesz ręcznie (zakładka **Database → [obiekt] → Add new record**) albo
zaimportujesz z pliku CSV (**Records → Import**). Wprowadź dane w kolejności:

1. najpierw **Klient** i **Usluga** (tabele nadrzędne),
2. potem **Zamowienie** (wybierając klienta z listy),
3. na końcu **Szczegoly_zamowienia** (wybierając zamówienie i usługę z list).

Wykorzystaj dane z plików `sql/02_dane.sql` lub gotowej bazy `ProServ.accdb`.
📸 *Zrzut: tabela Zamowienie z wprowadzonymi rekordami i kolumną wartość.*

---

## E. Formularze (zakładka Pages)

Knack generuje formularze i widoki na **stronach** (Pages). Najszybciej:

1. **Pages → Add Page**, nazwa **„Klienci”** → dodaj element **Table** (Grid)
   na obiekcie Klient. Przy tabeli włącz opcje **Add / Edit / Delete** – Knack
   sam wygeneruje **formularz dodawania i edycji** klienta.
   📸 *Zrzut: strona „Klienci” z tabelą i przyciskiem Add.*
2. Powtórz dla stron **„Usługi”** (obiekt Usluga) oraz **„Zamówienia”**
   (obiekt Zamowienie).
3. Na stronie **„Zamówienia”** otwórz widok szczegółów zamówienia i dodaj
   pod nim element **Table** dla **Szczegoly_zamowienia** powiązanych z danym
   zamówieniem, z opcją **Add** – tak dodaje się pozycje do zamówienia.
   W formularzu pozycji pola `zamowienie` i `usluga` pojawią się jako **listy
   wyboru** (dzięki relacjom Connection).
   📸 *Zrzut: formularz dodawania pozycji zamówienia z listą wyboru usługi.*
4. Opublikuj aplikację (**Settings → … / Live App**) i przetestuj dodawanie,
   edycję oraz przeglądanie rekordów.
   📸 *Zrzut: działająca aplikacja (Live App) z poziomu użytkownika.*

---

## F. Różnice w Tadabase.io

Procedura jest analogiczna; zmienia się nazewnictwo:

| Pojęcie | Knack | Tadabase |
|---|---|---|
| Tabela | Object | **Table** |
| Pole | Field | **Field** |
| Klucz obcy / relacja | Connection | **Connection field** |
| Pole obliczeniowe | Equation | **Equation / Formula field** |
| Strona z formularzem | Page + Form | **Page + Form / Grid component** |

W Tadabase: **Data Builder** → *New Table* (cztery tabele), pola dodajesz przez
*Add Field*, relacje przez typ **Connection**, a formularze i tabele budujesz w
**Page Builder** (komponenty *Form* oraz *Table*).

---

## G. Lista zrzutów ekranu do wstawienia w sprawozdaniu

Zalecane ilustracje (zgodnie z oznaczeniami 📸 powyżej):

1. Pusty Builder aplikacji ProServ.
2. Lista pól obiektu Klient (oraz Usluga).
3. Tworzenie relacji Connection (Zamowienie → Klient).
4. Konfiguracja pola Sum (wartość zamówienia).
5. Tabela z danymi (np. Zamowienie z kolumną wartość).
6. Formularz dodawania/edycji rekordu.
7. Działająca aplikacja w widoku użytkownika (Live App).
