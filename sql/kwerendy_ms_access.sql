-- =============================================================================
--  Kwerendy w dialekcie MS Access (Access SQL / JET SQL)
--  Każdą kwerendę wklej osobno w: Tworzenie -> Projekt kwerendy ->
--  zamknij okno "Pokazywanie tabeli" -> Widok SQL -> wklej -> Uruchom (!).
--  Następnie zapisz kwerendę pod podaną nazwą.
--
--  Różnice względem wersji z pliku 03_kwerendy.sql:
--   * łączenie tekstu operatorem  &  (a nie ||),
--   * funkcja Round(...) zamiast ROUND(...),
--   * wielokrotne złączenia ujęte w nawiasy (wymóg składni Access),
--   * Access nie obsługuje COUNT(DISTINCT ...) – patrz kwerenda 4.
-- =============================================================================


-- ============ KWERENDA 1 (prosta): "Klienci z Warszawy" ============
SELECT klient.id_klienta, klient.imie, klient.nazwisko,
       klient.nazwa_firmy, klient.telefon, klient.miasto
FROM   klient
WHERE  klient.miasto = 'Warszawa'
ORDER BY klient.nazwisko, klient.imie;


-- ============ KWERENDA 2 (prosta): "Uslugi powyzej 1000 zl" ============
SELECT usluga.nazwa_uslugi, usluga.kategoria,
       usluga.cena_jednostkowa, usluga.jednostka
FROM   usluga
WHERE  usluga.cena_jednostkowa > 1000
ORDER BY usluga.cena_jednostkowa DESC;


-- ============ KWERENDA 3 (zlozona): "Wartosc zamowien" ============
-- Złączenie 3 tabel + obliczenie wartości z rabatem + grupowanie.
-- LEFT JOIN sprawia, że zamówienie anulowane bez pozycji też się pokaże.
SELECT z.id_zamowienia AS nr_zamowienia,
       k.imie & ' ' & k.nazwisko AS klient,
       k.nazwa_firmy AS firma,
       z.data_zamowienia,
       z.status,
       Count(sz.id_szczegolu) AS liczba_pozycji,
       Round(Sum(sz.ilosc * sz.cena * (1 - sz.rabat)), 2) AS wartosc_zamowienia
FROM   (zamowienie AS z
        INNER JOIN klient AS k ON k.id_klienta = z.id_klienta)
        LEFT JOIN szczegoly_zamowienia AS sz ON sz.id_zamowienia = z.id_zamowienia
GROUP BY z.id_zamowienia, k.imie, k.nazwisko, k.nazwa_firmy,
         z.data_zamowienia, z.status
ORDER BY Round(Sum(sz.ilosc * sz.cena * (1 - sz.rabat)), 2) DESC;


-- ============ KWERENDA 4 (zlozona): "Ranking uslug wg przychodu" ============
-- Access nie obsługuje COUNT(DISTINCT id_zamowienia). Używamy Count(*),
-- co jest poprawne, bo indeks unikalny (id_zamowienia, id_uslugi) gwarantuje,
-- że dana usługa występuje w jednym zamówieniu najwyżej raz.
SELECT u.nazwa_uslugi,
       u.kategoria,
       Count(*) AS liczba_zamowien,
       Sum(sz.ilosc) AS sztuk_sprzedanych,
       Round(Sum(sz.ilosc * sz.cena * (1 - sz.rabat)), 2) AS przychod
FROM   (usluga AS u
        INNER JOIN szczegoly_zamowienia AS sz ON sz.id_uslugi = u.id_uslugi)
        INNER JOIN zamowienie AS z ON z.id_zamowienia = sz.id_zamowienia
WHERE  z.status <> 'Anulowane'
GROUP BY u.id_uslugi, u.nazwa_uslugi, u.kategoria
ORDER BY Round(Sum(sz.ilosc * sz.cena * (1 - sz.rabat)), 2) DESC;
