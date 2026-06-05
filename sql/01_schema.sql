-- =============================================================================
--  System obsługi zamówień firmy usługowej "ProServ"
--  Plik: 01_schema.sql  —  definicja struktury bazy danych (DDL)
-- =============================================================================
--  Zadanie: 57 MC - FIR - Informatyka w zarządzaniu
--
--  Baza składa się z czterech tabel:
--      1. klient                – dane klientów
--      2. usluga                – katalog świadczonych usług
--      3. zamowienie            – nagłówki zamówień
--      4. szczegoly_zamowienia  – pozycje zamówień (tabela łącząca M:N)
--
--  Skrypt napisano w dialekcie SQLite (do automatycznej weryfikacji), ale
--  jest świadomie zgodny z MS Access. Mapowanie typów danych SQLite -> MS Access:
--
--      INTEGER PRIMARY KEY AUTOINCREMENT  ->  Autonumerowanie (Klucz podstawowy)
--      TEXT                               ->  Krótki tekst / Długi tekst (Memo)
--      REAL                               ->  Liczba (Pojedyncza/Podwójna) / Waluta
--      DATE / TEXT (RRRR-MM-DD)           ->  Data/godzina
--
--  W MS Access relacje i więzy integralności ustawia się w oknie "Relacje"
--  (zakładka Narzędzia bazy danych -> Relacje) z włączoną opcją
--  "Wymuszaj więzy integralności". Poniżej te same więzy zapisano jako
--  klauzule FOREIGN KEY.
-- =============================================================================

PRAGMA foreign_keys = ON;

-- usuwamy tabele w kolejności odwrotnej do zależności (jeśli istnieją)
DROP TABLE IF EXISTS szczegoly_zamowienia;
DROP TABLE IF EXISTS zamowienie;
DROP TABLE IF EXISTS usluga;
DROP TABLE IF EXISTS klient;

-- -----------------------------------------------------------------------------
-- 1. Tabela KLIENT
--    Przechowuje dane kontaktowe i adresowe klientów firmy.
--    Klucz podstawowy: id_klienta (autonumerowanie).
-- -----------------------------------------------------------------------------
CREATE TABLE klient (
    id_klienta       INTEGER PRIMARY KEY AUTOINCREMENT,
    imie             TEXT    NOT NULL,
    nazwisko         TEXT    NOT NULL,
    nazwa_firmy      TEXT,                              -- NULL dla klienta indywidualnego
    email            TEXT    NOT NULL UNIQUE,
    telefon          TEXT,
    adres            TEXT,
    miasto           TEXT,
    kod_pocztowy     TEXT,
    data_rejestracji DATE    NOT NULL DEFAULT (date('now'))
);

-- -----------------------------------------------------------------------------
-- 2. Tabela USLUGA
--    Katalog usług oferowanych przez firmę wraz z ceną jednostkową.
--    Klucz podstawowy: id_uslugi (autonumerowanie).
-- -----------------------------------------------------------------------------
CREATE TABLE usluga (
    id_uslugi        INTEGER PRIMARY KEY AUTOINCREMENT,
    nazwa_uslugi     TEXT    NOT NULL,
    kategoria        TEXT,
    opis             TEXT,
    cena_jednostkowa REAL    NOT NULL CHECK (cena_jednostkowa >= 0),
    jednostka        TEXT    DEFAULT 'szt.',           -- np. szt., godz., m-c
    czas_realizacji  INTEGER                            -- orientacyjny czas w dniach
);

-- -----------------------------------------------------------------------------
-- 3. Tabela ZAMOWIENIE
--    Nagłówek zamówienia. Każde zamówienie należy do jednego klienta.
--    Klucz obcy: id_klienta -> klient(id_klienta)   [relacja 1 : wiele]
-- -----------------------------------------------------------------------------
CREATE TABLE zamowienie (
    id_zamowienia    INTEGER PRIMARY KEY AUTOINCREMENT,
    id_klienta       INTEGER NOT NULL,
    data_zamowienia  DATE    NOT NULL DEFAULT (date('now')),
    status           TEXT    NOT NULL DEFAULT 'Nowe'
                             CHECK (status IN ('Nowe','W realizacji','Zrealizowane','Anulowane')),
    metoda_platnosci TEXT    CHECK (metoda_platnosci IN ('Przelew','Karta','Gotówka','BLIK')),
    uwagi            TEXT,
    FOREIGN KEY (id_klienta) REFERENCES klient (id_klienta)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 4. Tabela SZCZEGOLY_ZAMOWIENIA
--    Pozycje zamówienia – realizuje relację wiele-do-wielu pomiędzy
--    tabelami zamowienie i usluga. Każdy wiersz to jedna usługa w zamówieniu.
--    Klucze obce: id_zamowienia -> zamowienie, id_uslugi -> usluga
-- -----------------------------------------------------------------------------
CREATE TABLE szczegoly_zamowienia (
    id_szczegolu     INTEGER PRIMARY KEY AUTOINCREMENT,
    id_zamowienia    INTEGER NOT NULL,
    id_uslugi        INTEGER NOT NULL,
    ilosc            INTEGER NOT NULL DEFAULT 1 CHECK (ilosc > 0),
    cena             REAL    NOT NULL CHECK (cena >= 0),    -- cena w chwili zamówienia
    rabat            REAL    NOT NULL DEFAULT 0
                             CHECK (rabat >= 0 AND rabat <= 1), -- 0.10 = 10%
    FOREIGN KEY (id_zamowienia) REFERENCES zamowienie (id_zamowienia)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_uslugi) REFERENCES usluga (id_uslugi)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE (id_zamowienia, id_uslugi)   -- ta sama usługa raz w danym zamówieniu
);

-- indeksy na kluczach obcych (Access zakłada je automatycznie dla relacji)
CREATE INDEX idx_zam_klient   ON zamowienie (id_klienta);
CREATE INDEX idx_szcz_zam     ON szczegoly_zamowienia (id_zamowienia);
CREATE INDEX idx_szcz_usluga  ON szczegoly_zamowienia (id_uslugi);
