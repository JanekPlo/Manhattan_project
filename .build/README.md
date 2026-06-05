# Generowanie pliku ProServ.accdb

Plik `ProServ.accdb` (natywny format MS Access 2016) został wygenerowany
programowo biblioteką **Jackcess** (czysta Java, tworzy pliki .accdb bez
instalacji MS Access). Tu znajduje się kod źródłowy generatora — wystarcza do
odtworzenia bazy od zera.

## Jak zbudować ponownie

```bash
cd .build
mkdir -p lib && cd lib
BASE=https://repo1.maven.org/maven2
curl -fsSL -o jackcess.jar        $BASE/com/healthmarketscience/jackcess/jackcess/4.0.5/jackcess-4.0.5.jar
curl -fsSL -o commons-lang3.jar   $BASE/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar
curl -fsSL -o commons-logging.jar $BASE/commons-logging/commons-logging/1.2/commons-logging-1.2.jar
cd ..

CP="lib/jackcess.jar:lib/commons-lang3.jar:lib/commons-logging.jar"
javac -encoding UTF-8 -cp "$CP" BuildAccdb.java
java  -Dfile.encoding=UTF-8 -cp "$CP:." BuildAccdb ../ProServ.accdb

# (opcjonalnie) weryfikacja zawartości:
javac -encoding UTF-8 -cp "$CP" VerifyAccdb.java
java  -Dfile.encoding=UTF-8 -cp "$CP:." VerifyAccdb ../ProServ.accdb
```

Katalog `lib/` (pobierane biblioteki) jest celowo pominięty w repozytorium
(`.gitignore`).
