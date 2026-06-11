# Wirujące spirale – projekt Scratch

Rozwiązanie zadania: program po uruchomieniu pyta, ile figur narysować,
rysuje je rozłożone symetrycznie wokół środka, a każda kolejna figura
jest odrobinę bardziej przezroczysta od poprzedniej.

## Jak uruchomić

1. Wejdź na https://scratch.mit.edu/projects/editor/
2. Plik → Wczytaj ze swojego komputera → wybierz `wirujace_spirale.sb3`
3. Kliknij zieloną flagę i podaj liczbę figur (np. 12).

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
    ustaw [krok] na 1
    przyłóż pisak
    powtórz (45) razy
        przesuń o (krok) kroków
        obróć w prawo o (8) stopni
        zmień [krok] o 0.4
    podnieś pisak
    zmień [kierunek] o (360 / figury)
    zmień [przezroczystość] pisaka o (75 / figury)
```

## Dlaczego to spełnia warunki zadania

- **Pytanie o liczbę figur** – blok „zapytaj … i czekaj", odpowiedź
  trafia do zmiennej `figury`.
- **Symetria** – po każdej figurze duszek wraca na środek i obraca się
  o `360 / figury` stopni, więc ramiona są rozłożone równomiernie
  niezależnie od podanej liczby.
- **Rosnąca przezroczystość** – po każdej figurze przezroczystość
  pisaka rośnie o `75 / figury`, czyli od 0% dla pierwszej do ok. 75%
  dla ostatniej.
- **Kształt figury** – spirala: w pętli każdy krok jest dłuższy
  (`krok + 0.4`) przy stałym obrocie 8°, co daje rozkręcające się
  ramię jak na rysunku z zadania.
