import com.healthmarketscience.jackcess.*;
import java.io.File;
import java.math.BigDecimal;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Buduje natywny plik MS Access ProServ.accdb (format V2016) z czterema
 * tabelami, kluczami podstawowymi (autonumerowanie), relacjami z wymuszonymi
 * więzami integralności oraz danymi przykładowymi.
 */
public class BuildAccdb {

    static SimpleDateFormat F = new SimpleDateFormat("yyyy-MM-dd");
    static Date d(String s) throws Exception { return F.parse(s); }

    static ColumnBuilder txt(String name)  { return new ColumnBuilder(name, DataType.TEXT).setLengthInUnits(255); }
    static ColumnBuilder memo(String name) { return new ColumnBuilder(name, DataType.MEMO); }
    static ColumnBuilder num(String name)  { return new ColumnBuilder(name, DataType.LONG); }
    static ColumnBuilder money(String name){ return new ColumnBuilder(name, DataType.MONEY); }
    static ColumnBuilder dbl(String name)  { return new ColumnBuilder(name, DataType.DOUBLE); }
    static ColumnBuilder date(String name) { return new ColumnBuilder(name, DataType.SHORT_DATE_TIME); }
    static ColumnBuilder pk(String name)   { return new ColumnBuilder(name, DataType.LONG).setAutoNumber(true); }

    public static void main(String[] args) throws Exception {
        File f = new File(args.length > 0 ? args[0] : "ProServ.accdb");
        if (f.exists()) f.delete();

        Database db = new DatabaseBuilder(f)
                .setFileFormat(Database.FileFormat.V2016)
                .create();

        // ---------------- TABELA klient ----------------
        Table klient = new TableBuilder("klient")
                .addColumn(pk("id_klienta"))
                .addColumn(txt("imie"))
                .addColumn(txt("nazwisko"))
                .addColumn(txt("nazwa_firmy"))
                .addColumn(txt("email"))
                .addColumn(txt("telefon"))
                .addColumn(txt("adres"))
                .addColumn(txt("miasto"))
                .addColumn(txt("kod_pocztowy"))
                .addColumn(date("data_rejestracji"))
                .addIndex(new IndexBuilder(IndexBuilder.PRIMARY_KEY_NAME).addColumns("id_klienta").setPrimaryKey())
                .toTable(db);

        // ---------------- TABELA usluga ----------------
        Table usluga = new TableBuilder("usluga")
                .addColumn(pk("id_uslugi"))
                .addColumn(txt("nazwa_uslugi"))
                .addColumn(txt("kategoria"))
                .addColumn(memo("opis"))
                .addColumn(money("cena_jednostkowa"))
                .addColumn(txt("jednostka"))
                .addColumn(num("czas_realizacji"))
                .addIndex(new IndexBuilder(IndexBuilder.PRIMARY_KEY_NAME).addColumns("id_uslugi").setPrimaryKey())
                .toTable(db);

        // ---------------- TABELA zamowienie ----------------
        Table zamowienie = new TableBuilder("zamowienie")
                .addColumn(pk("id_zamowienia"))
                .addColumn(num("id_klienta"))
                .addColumn(date("data_zamowienia"))
                .addColumn(txt("status"))
                .addColumn(txt("metoda_platnosci"))
                .addColumn(memo("uwagi"))
                .addIndex(new IndexBuilder(IndexBuilder.PRIMARY_KEY_NAME).addColumns("id_zamowienia").setPrimaryKey())
                .toTable(db);

        // ---------------- TABELA szczegoly_zamowienia ----------------
        Table szczegoly = new TableBuilder("szczegoly_zamowienia")
                .addColumn(pk("id_szczegolu"))
                .addColumn(num("id_zamowienia"))
                .addColumn(num("id_uslugi"))
                .addColumn(num("ilosc"))
                .addColumn(money("cena"))
                .addColumn(dbl("rabat"))
                .addIndex(new IndexBuilder(IndexBuilder.PRIMARY_KEY_NAME).addColumns("id_szczegolu").setPrimaryKey())
                .toTable(db);

        // ---------------- RELACJE (więzy integralności) ----------------
        new RelationshipBuilder("klient", "zamowienie")
                .addColumns("id_klienta", "id_klienta")
                .setReferentialIntegrity().setCascadeUpdates()
                .toRelationship(db);
        new RelationshipBuilder("zamowienie", "szczegoly_zamowienia")
                .addColumns("id_zamowienia", "id_zamowienia")
                .setReferentialIntegrity().setCascadeDeletes().setCascadeUpdates()
                .toRelationship(db);
        new RelationshipBuilder("usluga", "szczegoly_zamowienia")
                .addColumns("id_uslugi", "id_uslugi")
                .setReferentialIntegrity().setCascadeUpdates()
                .toRelationship(db);

        // ---------------- DANE: klient (autonumer -> null) ----------------
        Object[][] klienci = {
            {null,"Anna","Kowalska",null,"anna.kowalska@gmail.com","601234567","ul. Lipowa 12/4","Warszawa","00-123",d("2024-01-15")},
            {null,"Piotr","Nowak","Nowak Consulting","biuro@nowakconsulting.pl","512987654","ul. Kwiatowa 8","Kraków","30-001",d("2024-02-03")},
            {null,"Magdalena","Wiśniewska",null,"m.wisniewska@op.pl","698112233","os. Słoneczne 5/12","Poznań","60-200",d("2024-02-20")},
            {null,"Tomasz","Zieliński","TechBud sp. z o.o.","kontakt@techbud.com.pl","224556677","al. Jerozolimskie 99","Warszawa","02-222",d("2024-03-10")},
            {null,"Katarzyna","Lewandowska",null,"kasia.lewandowska@wp.pl","605998877","ul. Polna 3","Gdańsk","80-100",d("2024-04-05")},
            {null,"Marek","Wójcik","Wójcik Transport","m.wojcik@wojciktrans.pl","601456789","ul. Przemysłowa 14","Kraków","31-200",d("2024-05-12")},
            {null,"Agnieszka","Kamińska",null,"a.kaminska@gmail.com","503221144","ul. Ogrodowa 7/2","Wrocław","50-300",d("2024-06-01")},
        };
        for (Object[] r : klienci) klient.addRow(r);

        // ---------------- DANE: usluga ----------------
        Object[][] uslugi = {
            {null,"Projekt strony WWW","Web","Projekt graficzny i wdrożenie strony wizytówki",new BigDecimal("3500.00"),"szt.",21},
            {null,"Pozycjonowanie SEO","Marketing","Miesięczny pakiet działań SEO",new BigDecimal("1200.00"),"m-c",30},
            {null,"Logo i identyfikacja","Grafika","Projekt logo oraz podstawowej identyfikacji wizualnej",new BigDecimal("1800.00"),"szt.",14},
            {null,"Audyt informatyczny","IT","Audyt bezpieczeństwa i wydajności infrastruktury IT",new BigDecimal("2500.00"),"szt.",7},
            {null,"Wsparcie techniczne","IT","Pakiet godzinowego wsparcia technicznego",new BigDecimal("150.00"),"godz.",1},
            {null,"Kampania Google Ads","Marketing","Konfiguracja i prowadzenie kampanii reklamowej",new BigDecimal("900.00"),"m-c",30},
            {null,"Sklep internetowy","Web","Wdrożenie sklepu e-commerce na platformie",new BigDecimal("7900.00"),"szt.",45},
            {null,"Szkolenie z obsługi CMS","Szkolenia","Szkolenie online z obsługi systemu zarządzania treścią",new BigDecimal("600.00"),"szt.",2},
        };
        for (Object[] r : uslugi) usluga.addRow(r);

        // ---------------- DANE: zamowienie ----------------
        Object[][] zamowienia = {
            {null,1,d("2024-03-01"),"Zrealizowane","Przelew","Strona dla gabinetu kosmetycznego"},
            {null,2,d("2024-03-15"),"Zrealizowane","Przelew","Pakiet startowy dla firmy"},
            {null,4,d("2024-04-02"),"W realizacji","Przelew","Duże wdrożenie e-commerce"},
            {null,3,d("2024-04-20"),"Zrealizowane","BLIK",null},
            {null,5,d("2024-05-08"),"Nowe","Karta","Klient prosi o kontakt telefoniczny"},
            {null,6,d("2024-05-25"),"W realizacji","Przelew","Stała obsługa marketingowa"},
            {null,1,d("2024-06-10"),"Nowe","BLIK","Druga współpraca z klientem"},
            {null,2,d("2024-06-18"),"Anulowane","Przelew","Klient zrezygnował"},
        };
        for (Object[] r : zamowienia) zamowienie.addRow(r);

        // ---------------- DANE: szczegoly_zamowienia ----------------
        Object[][] poz = {
            {null,1,1,1,new BigDecimal("3500.00"),0.00},
            {null,1,3,1,new BigDecimal("1800.00"),0.10},
            {null,2,3,1,new BigDecimal("1800.00"),0.00},
            {null,2,2,3,new BigDecimal("1200.00"),0.05},
            {null,2,8,1,new BigDecimal("600.00"),0.00},
            {null,3,7,1,new BigDecimal("7900.00"),0.10},
            {null,3,4,1,new BigDecimal("2500.00"),0.00},
            {null,3,5,10,new BigDecimal("150.00"),0.00},
            {null,4,1,1,new BigDecimal("3500.00"),0.00},
            {null,5,6,2,new BigDecimal("900.00"),0.00},
            {null,6,2,6,new BigDecimal("1200.00"),0.15},
            {null,6,6,6,new BigDecimal("900.00"),0.15},
            {null,7,5,5,new BigDecimal("150.00"),0.00},
        };
        for (Object[] r : poz) szczegoly.addRow(r);

        db.close();
        System.out.println("Utworzono: " + f.getAbsolutePath()
                + "  (" + f.length() + " B)");
        System.out.println("Tabele: klient=" + klienci.length
                + ", usluga=" + uslugi.length
                + ", zamowienie=" + zamowienia.length
                + ", szczegoly_zamowienia=" + poz.length);
    }
}
