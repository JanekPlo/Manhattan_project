-- =============================================================================
--  Plik: 03_kwerendy.sql  —  cztery przykładowe kwerendy (zapytania)
--  Wymaganie: dwie kwerendy proste oraz dwie kwerendy złożone.
--
--  Uwaga dot. MS Access: składnia poniżej jest standardowym SQL i działa
--  zarówno w SQLite, jak i w MS Access. Drobne różnice opisano w komentarzach.
-- =============================================================================


-- =====================  KWERENDA PROSTA 1  ==================================
-- Cel: wyświetlić klientów z jednego miasta (filtrowanie wg kryterium).
-- Demonstruje: SELECT z jednej tabeli + warunek WHERE + sortowanie.
-- W Access: kreator kwerend wybierający, kryterium "Warszawa" w polu miasto.
-- ----------------------------------------------------------------------------
SELECT  id_klienta,
        imie,
        nazwisko,
        nazwa_firmy,
        telefon,
        miasto
FROM    klient
WHERE   miasto = 'Warszawa'
ORDER BY nazwisko, imie;


-- =====================  KWERENDA PROSTA 2  ==================================
-- Cel: katalog usług droższych niż 1000 zł, posortowany od najdroższej.
-- Demonstruje: SELECT z jednej tabeli + filtr liczbowy + ORDER BY DESC.
-- ----------------------------------------------------------------------------
SELECT  nazwa_uslugi,
        kategoria,
        cena_jednostkowa,
        jednostka
FROM    usluga
WHERE   cena_jednostkowa > 1000
ORDER BY cena_jednostkowa DESC;


-- =====================  KWERENDA ZŁOŻONA 1  =================================
-- Cel: wartość każdego zamówienia wraz z danymi klienta.
-- Demonstruje: złączenie 3 tabel (klient, zamowienie, szczegoly_zamowienia),
--              agregację SUM oraz GROUP BY z obliczeniem rabatu.
--   wartość pozycji = ilosc * cena * (1 - rabat)
-- W Access: w kwerendzie złożonej dodaje się kolumnę obliczeniową
--   Wartosc: [ilosc]*[cena]*(1-[rabat]) oraz włącza "Podsumowania" (Suma).
-- ----------------------------------------------------------------------------
SELECT  z.id_zamowienia                                   AS nr_zamowienia,
        k.imie || ' ' || k.nazwisko                       AS klient,
        k.nazwa_firmy                                     AS firma,
        z.data_zamowienia,
        z.status,
        COUNT(sz.id_szczegolu)                            AS liczba_pozycji,
        ROUND(SUM(sz.ilosc * sz.cena * (1 - sz.rabat)),2) AS wartosc_zamowienia
FROM        zamowienie z
JOIN        klient     k  ON k.id_klienta    = z.id_klienta
LEFT JOIN   szczegoly_zamowienia sz ON sz.id_zamowienia = z.id_zamowienia
GROUP BY    z.id_zamowienia, k.imie, k.nazwisko, k.nazwa_firmy,
            z.data_zamowienia, z.status
ORDER BY    wartosc_zamowienia DESC;


-- =====================  KWERENDA ZŁOŻONA 2  =================================
-- Cel: ranking usług wg przychodu i popularności (analiza sprzedaży).
-- Demonstruje: złączenie usluga + szczegoly_zamowienia + zamowienie,
--              grupowanie wg usługi, kilka funkcji agregujących oraz
--              wykluczenie zamówień anulowanych (warunek WHERE na złączeniu).
-- ----------------------------------------------------------------------------
SELECT  u.nazwa_uslugi,
        u.kategoria,
        COUNT(DISTINCT sz.id_zamowienia)                  AS liczba_zamowien,
        SUM(sz.ilosc)                                     AS sztuk_sprzedanych,
        ROUND(SUM(sz.ilosc * sz.cena * (1 - sz.rabat)),2) AS przychod
FROM        usluga u
JOIN        szczegoly_zamowienia sz ON sz.id_uslugi    = u.id_uslugi
JOIN        zamowienie          z  ON z.id_zamowienia = sz.id_zamowienia
WHERE       z.status <> 'Anulowane'
GROUP BY    u.id_uslugi, u.nazwa_uslugi, u.kategoria
ORDER BY    przychod DESC;
