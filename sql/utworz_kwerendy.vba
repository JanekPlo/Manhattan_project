' =============================================================================
'  Makro VBA: tworzy 4 kwerendy w bazie ProServ.accdb
'
'  JAK URUCHOMIĆ (raz, ~30 sekund):
'   1. Otwórz ProServ.accdb w MS Access.
'   2. Naciśnij Alt + F11 (otworzy się edytor Visual Basic).
'   3. Menu: Insert -> Module.
'   4. Wklej CAŁĄ zawartość tego pliku do okna modułu.
'   5. Kliknij w środek procedury UtworzKwerendy i naciśnij F5 (Run).
'   6. Pojawi się komunikat "Utworzono 4 kwerendy." -> gotowe.
'   7. Zamknij edytor; kwerendy widać w panelu nawigacji po lewej.
'
'  Ponowne uruchomienie jest bezpieczne – stare kwerendy o tych nazwach
'  zostaną nadpisane.
' =============================================================================
Option Compare Database
Option Explicit

Public Sub UtworzKwerendy()
    Dim db As DAO.Database
    Set db = CurrentDb

    ' usuń ewentualne wcześniejsze wersje (bezpieczne ponowne uruchomienie)
    On Error Resume Next
    db.QueryDefs.Delete "Kw1_Klienci_Warszawa"
    db.QueryDefs.Delete "Kw2_Uslugi_powyzej_1000"
    db.QueryDefs.Delete "Kw3_Wartosc_zamowien"
    db.QueryDefs.Delete "Kw4_Ranking_uslug"
    On Error GoTo 0

    ' --- Kwerenda prosta nr 1: klienci z Warszawy ---
    db.CreateQueryDef "Kw1_Klienci_Warszawa", _
        "SELECT klient.id_klienta, klient.imie, klient.nazwisko, klient.nazwa_firmy, " & _
        "klient.telefon, klient.miasto " & _
        "FROM klient " & _
        "WHERE klient.miasto='Warszawa' " & _
        "ORDER BY klient.nazwisko, klient.imie;"

    ' --- Kwerenda prosta nr 2: usługi droższe niż 1000 zł ---
    db.CreateQueryDef "Kw2_Uslugi_powyzej_1000", _
        "SELECT usluga.nazwa_uslugi, usluga.kategoria, usluga.cena_jednostkowa, usluga.jednostka " & _
        "FROM usluga " & _
        "WHERE usluga.cena_jednostkowa>1000 " & _
        "ORDER BY usluga.cena_jednostkowa DESC;"

    ' --- Kwerenda złożona nr 1: wartość zamówień z danymi klienta ---
    db.CreateQueryDef "Kw3_Wartosc_zamowien", _
        "SELECT z.id_zamowienia AS nr_zamowienia, " & _
        "k.imie & ' ' & k.nazwisko AS klient, k.nazwa_firmy AS firma, " & _
        "z.data_zamowienia, z.status, " & _
        "Count(sz.id_szczegolu) AS liczba_pozycji, " & _
        "Round(Sum(sz.ilosc*sz.cena*(1-sz.rabat)),2) AS wartosc_zamowienia " & _
        "FROM (zamowienie AS z INNER JOIN klient AS k ON k.id_klienta=z.id_klienta) " & _
        "LEFT JOIN szczegoly_zamowienia AS sz ON sz.id_zamowienia=z.id_zamowienia " & _
        "GROUP BY z.id_zamowienia, k.imie, k.nazwisko, k.nazwa_firmy, z.data_zamowienia, z.status " & _
        "ORDER BY Round(Sum(sz.ilosc*sz.cena*(1-sz.rabat)),2) DESC;"

    ' --- Kwerenda złożona nr 2: ranking usług wg przychodu ---
    db.CreateQueryDef "Kw4_Ranking_uslug", _
        "SELECT u.nazwa_uslugi, u.kategoria, " & _
        "Count(*) AS liczba_zamowien, Sum(sz.ilosc) AS sztuk_sprzedanych, " & _
        "Round(Sum(sz.ilosc*sz.cena*(1-sz.rabat)),2) AS przychod " & _
        "FROM (usluga AS u INNER JOIN szczegoly_zamowienia AS sz ON sz.id_uslugi=u.id_uslugi) " & _
        "INNER JOIN zamowienie AS z ON z.id_zamowienia=sz.id_zamowienia " & _
        "WHERE z.status<>'Anulowane' " & _
        "GROUP BY u.id_uslugi, u.nazwa_uslugi, u.kategoria " & _
        "ORDER BY Round(Sum(sz.ilosc*sz.cena*(1-sz.rabat)),2) DESC;"

    db.QueryDefs.Refresh
    MsgBox "Utworzono 4 kwerendy:" & vbCrLf & _
           "  Kw1_Klienci_Warszawa" & vbCrLf & _
           "  Kw2_Uslugi_powyzej_1000" & vbCrLf & _
           "  Kw3_Wartosc_zamowien" & vbCrLf & _
           "  Kw4_Ranking_uslug", vbInformation, "Gotowe"

    Set db = Nothing
End Sub
