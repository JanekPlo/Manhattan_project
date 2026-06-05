-- =============================================================================
--  Plik: 02_dane.sql  —  przykładowe dane testowe
--  Dane są realistyczne i pokrywają typowe przypadki użycia systemu:
--  klienci indywidualni i firmowi, usługi z różnych kategorii, zamówienia
--  o różnych statusach oraz wielopozycyjne szczegóły zamówień (w tym rabaty).
-- =============================================================================

-- -------------------------- KLIENCI -----------------------------------------
INSERT INTO klient (imie, nazwisko, nazwa_firmy, email, telefon, adres, miasto, kod_pocztowy, data_rejestracji) VALUES
 ('Anna',     'Kowalska',   NULL,                  'anna.kowalska@gmail.com',   '601234567', 'ul. Lipowa 12/4',     'Warszawa', '00-123', '2024-01-15'),
 ('Piotr',    'Nowak',      'Nowak Consulting',    'biuro@nowakconsulting.pl',  '512987654', 'ul. Kwiatowa 8',      'Kraków',   '30-001', '2024-02-03'),
 ('Magdalena','Wiśniewska', NULL,                  'm.wisniewska@op.pl',        '698112233', 'os. Słoneczne 5/12',  'Poznań',   '60-200', '2024-02-20'),
 ('Tomasz',   'Zieliński',  'TechBud sp. z o.o.',  'kontakt@techbud.com.pl',    '224556677', 'al. Jerozolimskie 99','Warszawa', '02-222', '2024-03-10'),
 ('Katarzyna','Lewandowska',NULL,                  'kasia.lewandowska@wp.pl',   '605998877', 'ul. Polna 3',         'Gdańsk',   '80-100', '2024-04-05'),
 ('Marek',    'Wójcik',     'Wójcik Transport',    'm.wojcik@wojciktrans.pl',   '601456789', 'ul. Przemysłowa 14',  'Kraków',   '31-200', '2024-05-12'),
 ('Agnieszka','Kamińska',   NULL,                  'a.kaminska@gmail.com',      '503221144', 'ul. Ogrodowa 7/2',    'Wrocław',  '50-300', '2024-06-01');

-- -------------------------- USŁUGI ------------------------------------------
INSERT INTO usluga (nazwa_uslugi, kategoria, opis, cena_jednostkowa, jednostka, czas_realizacji) VALUES
 ('Projekt strony WWW',        'Web',        'Projekt graficzny i wdrożenie strony wizytówki',          3500.00, 'szt.',  21),
 ('Pozycjonowanie SEO',        'Marketing',  'Miesięczny pakiet działań SEO',                            1200.00, 'm-c',   30),
 ('Logo i identyfikacja',      'Grafika',    'Projekt logo oraz podstawowej identyfikacji wizualnej',    1800.00, 'szt.',  14),
 ('Audyt informatyczny',       'IT',         'Audyt bezpieczeństwa i wydajności infrastruktury IT',      2500.00, 'szt.',   7),
 ('Wsparcie techniczne',       'IT',         'Pakiet godzinowego wsparcia technicznego',                  150.00, 'godz.',  1),
 ('Kampania Google Ads',       'Marketing',  'Konfiguracja i prowadzenie kampanii reklamowej',            900.00, 'm-c',   30),
 ('Sklep internetowy',         'Web',        'Wdrożenie sklepu e-commerce na platformie',                7900.00, 'szt.',  45),
 ('Szkolenie z obsługi CMS',   'Szkolenia',  'Szkolenie online z obsługi systemu zarządzania treścią',    600.00, 'szt.',   2);

-- -------------------------- ZAMÓWIENIA --------------------------------------
INSERT INTO zamowienie (id_klienta, data_zamowienia, status, metoda_platnosci, uwagi) VALUES
 (1, '2024-03-01', 'Zrealizowane', 'Przelew', 'Strona dla gabinetu kosmetycznego'),
 (2, '2024-03-15', 'Zrealizowane', 'Przelew', 'Pakiet startowy dla firmy'),
 (4, '2024-04-02', 'W realizacji', 'Przelew', 'Duże wdrożenie e-commerce'),
 (3, '2024-04-20', 'Zrealizowane', 'BLIK',    NULL),
 (5, '2024-05-08', 'Nowe',         'Karta',   'Klient prosi o kontakt telefoniczny'),
 (6, '2024-05-25', 'W realizacji', 'Przelew', 'Stała obsługa marketingowa'),
 (1, '2024-06-10', 'Nowe',         'BLIK',    'Druga współpraca z klientem'),
 (2, '2024-06-18', 'Anulowane',    'Przelew', 'Klient zrezygnował');

-- -------------------------- SZCZEGÓŁY ZAMÓWIEŃ ------------------------------
-- Zamówienie 1 (Anna Kowalska): strona WWW + logo
INSERT INTO szczegoly_zamowienia (id_zamowienia, id_uslugi, ilosc, cena, rabat) VALUES
 (1, 1, 1, 3500.00, 0.00),
 (1, 3, 1, 1800.00, 0.10);
-- Zamówienie 2 (Nowak Consulting): logo + SEO 3 m-ce + szkolenie
INSERT INTO szczegoly_zamowienia (id_zamowienia, id_uslugi, ilosc, cena, rabat) VALUES
 (2, 3, 1, 1800.00, 0.00),
 (2, 2, 3, 1200.00, 0.05),
 (2, 8, 1,  600.00, 0.00);
-- Zamówienie 3 (TechBud): sklep + audyt + wsparcie 10h
INSERT INTO szczegoly_zamowienia (id_zamowienia, id_uslugi, ilosc, cena, rabat) VALUES
 (3, 7, 1, 7900.00, 0.10),
 (3, 4, 1, 2500.00, 0.00),
 (3, 5, 10, 150.00, 0.00);
-- Zamówienie 4 (Magdalena Wiśniewska): strona WWW
INSERT INTO szczegoly_zamowienia (id_zamowienia, id_uslugi, ilosc, cena, rabat) VALUES
 (4, 1, 1, 3500.00, 0.00);
-- Zamówienie 5 (Katarzyna Lewandowska): Google Ads 2 m-ce
INSERT INTO szczegoly_zamowienia (id_zamowienia, id_uslugi, ilosc, cena, rabat) VALUES
 (5, 6, 2, 900.00, 0.00);
-- Zamówienie 6 (Wójcik Transport): SEO 6 m-cy + Google Ads 6 m-cy
INSERT INTO szczegoly_zamowienia (id_zamowienia, id_uslugi, ilosc, cena, rabat) VALUES
 (6, 2, 6, 1200.00, 0.15),
 (6, 6, 6,  900.00, 0.15);
-- Zamówienie 7 (Anna Kowalska): wsparcie 5h
INSERT INTO szczegoly_zamowienia (id_zamowienia, id_uslugi, ilosc, cena, rabat) VALUES
 (7, 5, 5, 150.00, 0.00);
-- Zamówienie 8 (anulowane) celowo bez pozycji
