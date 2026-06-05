import com.healthmarketscience.jackcess.*;
import java.io.File;
import java.util.*;

public class VerifyAccdb {
    public static void main(String[] args) throws Exception {
        Database db = DatabaseBuilder.open(new File(args[0]));
        System.out.println("Format pliku: " + db.getFileFormat());
        System.out.println("Tabele: " + db.getTableNames());
        for (String t : new String[]{"klient","usluga","zamowienie","szczegoly_zamowienia"}) {
            Table tab = db.getTable(t);
            System.out.println("  " + t + " -> wierszy: " + tab.getRowCount()
                    + ", kolumny: " + tab.getColumns().size());
        }
        System.out.println("\nRelacje:");
        for (Relationship r : db.getRelationships()) {
            System.out.println("  " + r.getFromTable().getName() + " -> " + r.getToTable().getName()
                    + "  RI=" + r.hasReferentialIntegrity()
                    + " cascDel=" + r.cascadeDeletes() + " cascUpd=" + r.cascadeUpdates());
        }
        System.out.println("\nPierwszy klient:");
        System.out.println("  " + db.getTable("klient").getNextRow());
        System.out.println("Pierwsza usluga:");
        System.out.println("  " + db.getTable("usluga").getNextRow());
        db.close();
    }
}
