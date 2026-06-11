# Symetryczny wzór z łuków – projekt Scratch

Rozwiązanie zadania: program po uruchomieniu pyta, ile figur narysować,
rysuje je rozłożone symetrycznie wokół środka sceny, a każda kolejna
figura jest odrobinę bardziej przezroczysta od poprzedniej.

Jedna figura to jeden ciągły ślad pisaka: duży łuk 180° („kopuła"),
zawrót o 180°, a pod spodem dwa mniejsze łuki 180°, które spotykają się
w ostrym dzióbku na środku.

## Jak uruchomić

1. Wejdź na https://scratch.mit.edu/projects/editor/
2. Plik → Wczytaj ze swojego komputera → wybierz `wirujace_spirale.sb3`
3. Kliknij zieloną flagę i podaj liczbę figur (np. 8).

Plik `.sb3` jest generowany skryptem `generuj_sb3.py`, a `podglad.py`
rysuje podgląd efektu (`podglad.png`) tym samym algorytmem.

## Skrypt (duszek „Rysownik", rozszerzenie Pisak)

```
kiedy kliknięto zieloną flagę
wyczyść wszystko
ukryj
podnieś pisak
ustaw rozmiar pisaka na 2
ustaw kolor pisaka na (#a03c3c)
ustaw [przezroczystość] pisaka na 0
zapytaj [Ile figur mam narysować?] i czekaj
ustaw [figury] na (odpowiedź)
ustaw [kierunek] na 0
powtórz (figury) razy
    idź do x: 0 y: 0
    ustaw kierunek na (kierunek)
    przyłóż pisak
    powtórz (36) razy            // duży łuk (kopuła)
        przesuń o (6) kroków
        obróć w prawo o (5) stopni
    obróć w prawo o (180) stopni // zawrót na końcu kopuły
    powtórz (36) razy            // pierwszy mały łuk (garb)
        przesuń o (3) kroków
        obróć w lewo o (5) stopni
    obróć w prawo o (180) stopni // zawrót w dzióbku na środku
    powtórz (36) razy            // drugi mały łuk (garb)
        przesuń o (3) kroków
        obróć w lewo o (5) stopni
    podnieś pisak
    zmień [kierunek] o (360 / figury)
    zmień [przezroczystość] pisaka o (75 / figury)
```

## Dlaczego to spełnia warunki zadania

- **Pytanie o liczbę figur** – blok „zapytaj … i czekaj", odpowiedź
  trafia do zmiennej `figury`.
- **Symetria** – każda figura zaczyna się na środku sceny, a przed
  kolejną duszek obraca się o `360 / figury` stopni, więc figury są
  rozłożone równomiernie niezależnie od podanej liczby.
- **Rosnąca przezroczystość** – po każdej figurze przezroczystość
  pisaka rośnie o `75 / figury`, czyli od 0% dla pierwszej do ok. 75%
  dla ostatniej.
- **Kształt figury** – łuk powstaje z powtarzania „przesuń + obróć o 5°";
  36 powtórzeń × 5° = 180°, czyli pół okręgu. Kopuła ma krok 6,
  garby krok 3, więc są o połowę mniejsze, a zawroty o 180° dają
  ostre dzióbki jak na rysunku.
