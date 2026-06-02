# Sztuczna inteligencja w optymalizacji łańcucha dostaw — studium przypadku systemu UPS ORION

> **Temat:** 01. AI Transformation — transformacja branży logistycznej (KEP / last mile) z wykorzystaniem sztucznej inteligencji
> **Typ pracy:** Case study (praca indywidualna)
>
> **⚠️ Instrukcja dla autora (usuń przed oddaniem):** To jest **baza do redakcji**, a nie gotowiec. Miejsca oznaczone `[TWÓJ WNIOSEK]` musisz uzupełnić własnymi przemyśleniami — to one decydują o ocenie ("poziom samodzielnego myślenia", "własne wnioski i rekomendacje"). Przejrzyj każdy akapit, przeredaguj własnymi słowami i dorzuć własną krytyczną ocenę. Wszystkie liczby pochodzą z realnych, podanych w bibliografii źródeł — jeśli którąś zmienisz, zaktualizuj źródło.

---

## Wprowadzenie

Logistyka kuriersko-ekspresowo-paczkowa (KEP) jest jedną z branż, w których przewaga
konkurencyjna mierzona jest w pojedynczych minutach i kilometrach. Wraz z eksplozją
handlu elektronicznego operatorzy logistyczni doręczają dziś dziesiątki milionów
przesyłek dziennie, a zdecydowana większość kosztów oraz emisji powstaje na etapie
tzw. ostatniej mili — finalnego odcinka dostawy do odbiorcy. W tym kontekście
sztuczna inteligencja (AI), a ściślej algorytmy optymalizacji i uczenia maszynowego,
przestała być technologiczną ciekawostką, a stała się narzędziem bezpośrednio
wpływającym na rentowność i ślad środowiskowy przedsiębiorstwa.

Niniejsze studium przypadku analizuje wdrożenie systemu **ORION** (On-Road
Integrated Optimization and Navigation) w firmie **UPS** — jednego z najlepiej
udokumentowanych przykładów zastosowania AI w logistyce na dużą skalę. Na tym
realnym przykładzie pokazuję, jak transformacja oparta na danych przekłada się na
konkretne efekty biznesowe, jakie wyzwania architektoniczne, regulacyjne i etyczne
za sobą pociąga, oraz jakie wnioski strategiczne płyną z niej dla branży logistycznej
w Europie.

`[TWÓJ WNIOSEK: dodaj 2–3 zdania o tym, dlaczego ten temat jest dla Ciebie ciekawy / dlaczego wybrałeś akurat logistykę. Recenzenci cenią osobiste, świadome uzasadnienie wyboru.]`

---

## 1. Problem biznesowy

**Definicja problemu.** Centralnym problemem operacyjnym firmy kurierskiej jest
zaplanowanie tras doręczeń dla tysięcy kierowców tak, aby zminimalizować przejechany
dystans i czas, przy jednoczesnym dotrzymaniu okien czasowych dostaw. Jest to wariant
klasycznego problemu komiwojażera (TSP) i problemu marszrutyzacji pojazdów (VRP) —
zadań NP-trudnych, w których liczba możliwych kombinacji tras dla jednego kierowcy z
~120–150 przystankami przekracza możliwości intuicyjnego planowania człowieka.

**Skala i kontekst.** UPS obsługuje w samych Stanach Zjednoczonych ok. **55 000 tras**
dziennie (INFORMS). Przy takiej skali nawet niewielka oszczędność dystansu na jednej
trasie przekłada się na ogromne efekty zagregowane: redukcja o zaledwie jedną milę
dziennie na kierowcę oznacza dla UPS oszczędności rzędu **50 mln USD rocznie**
(INFORMS). To pokazuje, dlaczego problem, który na poziomie pojedynczego kuriera
wydaje się błahy, na poziomie organizacji jest problemem strategicznym.

**Interesariusze:**
- **Przedsiębiorstwo** — dąży do redukcji kosztów paliwa, taboru i nadgodzin oraz
  do realizacji celów ESG (redukcja emisji CO₂).
- **Kierowcy** — bezpośredni użytkownicy systemu; ich akceptacja decyduje o sukcesie
  wdrożenia (wątek rozwinięty w sekcji 6).
- **Klienci / odbiorcy** — oczekują szybkich, przewidywalnych i tanich dostaw.
- **Środowisko i regulator** — emisje transportu drogowego są przedmiotem coraz
  ostrzejszych regulacji.

**Dlaczego temat jest istotny.** Wzrost wolumenów e-commerce strukturalnie zwiększa
presję na ostatnią milę, a jednocześnie rośnie wrażliwość cenowa klientów (oczekiwanie
darmowej dostawy) i presja środowiskowa. Optymalizacja tras oparta na AI jest jedną z
nielicznych dźwigni, która **jednocześnie** obniża koszty i emisje — stąd jej
strategiczne znaczenie.

`[TWÓJ WNIOSEK: odnieś problem do rynku polskiego / europejskiego — np. InPost, DPD, DHL Parcel. Jak presja last mile wygląda w Polsce? To wzmocni sekcję.]`

---

## 2. Kontekst technologiczny

**Ewolucja podejścia.** Przed wdrożeniem ORION planowanie tras w UPS opierało się na
doświadczeniu kierowców i prostych regułach (np. stałe sekwencje przystanków).
Nawigacja GPS wskazywała najkrótszą drogę między dwoma punktami, ale nie rozwiązywała
problemu **kolejności** odwiedzania wielu punktów przy ograniczeniach (okna czasowe,
priorytety przesyłek, charakterystyka pojazdu).

**Istota rozwiązania AI.** ORION to silnik optymalizacyjny łączący zaawansowane
algorytmy badań operacyjnych (optymalizacja kombinatoryczna, heurystyki i metaheurystyki
przeszukiwania ogromnej przestrzeni rozwiązań) z danymi mapowymi i historycznymi danymi
o dostawach. INFORMS określa ORION jako "prawdopodobnie największy projekt badań
operacyjnych na świecie", a jego rozwój zajął ponad dekadę.

**Dojrzałość rynku i trend.** Optymalizacja tras to dziś dojrzała, komercyjnie dostępna
klasa rozwiązań, ale liderzy (jak UPS) budują przewagę dzięki **skali własnych danych**
i ciągłemu doskonaleniu modeli. Szerszy trend potwierdza McKinsey: wbudowanie AI w
operacje dystrybucyjne pozwala obniżyć koszty logistyki o **5–20%**, koszty zakupów o
**5–15%**, a poziom zapasów o **20–30%** (McKinsey).

**Porównanie podejść.** Pierwotny ORION wykonywał optymalizację statyczną — trasa była
wyznaczana raz, przed wyjazdem. W 2024 r. UPS wdrożył **dynamiczny ORION** (dynamic
ORION), który przelicza trasy w ciągu dnia, reagując na zmiany (nowe odbiory, korki).
Ta iteracja przyniosła dodatkową redukcję o 2–4 mile na kierowcę ponad wcześniejsze
efekty (INFORMS).

| Cecha | Planowanie tradycyjne | ORION (statyczny) | Dynamic ORION (2024) |
|---|---|---|---|
| Podstawa decyzji | Doświadczenie kierowcy | Optymalizacja przed wyjazdem | Optymalizacja w czasie rzeczywistym |
| Reakcja na zmiany w trakcie dnia | Brak / ręczna | Ograniczona | Tak, automatyczna |
| Wykorzystanie danych | Minimalne | Dane mapowe + historyczne | + dane bieżące (odbiory, ruch) |

`[TWÓJ WNIOSEK: porównaj krótko z konkurencją — np. FedEx, Amazon (Amazon stosuje własne systemy routingu). Czy przewaga UPS jest trwała, czy łatwa do skopiowania?]`

---

## 3. Architektura rozwiązania

Rozwiązanie klasy ORION można opisać jako wielowarstwowy system przepływu danych:

1. **Warstwa danych (wejście)** — cyfrowe mapy drogowe, dane historyczne o dostawach,
   informacje o przesyłkach (adresy, okna czasowe, priorytet), dane telematyczne z
   pojazdów oraz dane bieżące (nowe zlecenia odbioru, warunki ruchu).
2. **Warstwa optymalizacji (silnik AI)** — rdzeń systemu: algorytmy optymalizacji
   kombinatorycznej wyznaczające sekwencję przystanków minimalizującą koszt (dystans/
   czas) przy spełnieniu ograniczeń.
3. **Warstwa integracji / interfejsu** — przekazanie zoptymalizowanej trasy do
   urządzenia kierowcy (DIAD — Delivery Information Acquisition Device) wraz z
   nawigacją krok po kroku.
4. **Pętla sprzężenia zwrotnego (feedback loop)** — rzeczywisty przebieg trasy wraca
   do systemu jako dane uczące, co pozwala doskonalić kolejne optymalizacje (kluczowy
   mechanizm w wersji dynamicznej).

**Proponowany diagram blokowy** (do wstawienia jako rysunek autorski):

```
   ┌─────────────────────────────────────────────────────────┐
   │                    WARSTWA DANYCH                         │
   │  Mapy │ Dane historyczne │ Przesyłki │ Telematyka │ Ruch  │
   └───────────────────────────┬─────────────────────────────-┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────┐
   │           SILNIK OPTYMALIZACJI (AI / OR)                  │
   │   Optymalizacja kombinatoryczna tras (VRP/TSP)            │
   └───────────────────────────┬─────────────────────────────-┘
                               │  zoptymalizowana trasa
                               ▼
   ┌─────────────────────────────────────────────────────────┐
   │       INTEGRACJA: urządzenie kierowcy (DIAD) + nawigacja  │
   └───────────────────────────┬─────────────────────────────-┘
                               │  rzeczywisty przebieg
                               ▼
   ┌─────────────────────────────────────────────────────────┐
   │     PĘTLA SPRZĘŻENIA ZWROTNEGO → doskonalenie modelu      │
   └──────────────────────────────────────────────────────────┘
            ▲                                          │
            └──────────────────────────────────────────┘
```

`[TWÓJ WNIOSEK: możesz przerysować ten diagram w narzędziu graficznym (np. draw.io) — punktowane są "diagramy, modele lub autorskie frameworki analizy". Dodaj 1–2 zdania interpretacji, np. który element jest najtrudniejszy do skopiowania przez konkurencję.]`

---

## 4. Model przychodowy / ekonomika rozwiązania

W przypadku ORION nie mówimy o sprzedaży produktu na zewnątrz, lecz o **wewnętrznym
uzasadnieniu kosztowym (business case)** — system jest źródłem oszczędności, nie
przychodu. Logika wartości wygląda następująco:

**Źródła wartości (oszczędności):**
- **Paliwo** — ORION oszczędza ok. **10 mln galonów paliwa rocznie** (INFORMS).
- **Dystans** — ok. **100 mln mil mniej rocznie** (INFORMS).
- **Koszty operacyjne** — przy pełnym wdrożeniu oszczędności szacowane na
  **300–400 mln USD rocznie** (INFORMS).
- **Emisje** — redukcja ok. **100 tys. ton CO₂ rocznie** (INFORMS) — wartość zarówno
  środowiskowa, jak i regulacyjna/wizerunkowa.

**Struktura kosztów:**
- **CAPEX/OPEX** — wieloletni rozwój algorytmów (>10 lat prac B+R), infrastruktura
  danych, integracja z flotą i urządzeniami, szkolenia kierowców.
- Koszt jednostkowy maleje wraz ze skalą — to samo rozwiązanie obsługuje dziesiątki
  tysięcy tras.

**Model wartości i skalowalność.** Rozwiązanie cechuje silny **efekt skali i efekt
sieciowy danych**: im więcej tras przejeżdża system, tym lepsze dane uczące i tym
dokładniejsza optymalizacja. To tworzy barierę wejścia trudną do pokonania dla
mniejszych graczy. W szerszym ujęciu McKinsey wskazuje, że AI w operacjach
dystrybucyjnych obniża koszty logistyki o 5–20% (McKinsey) — co dla branży o niskich
marżach jest różnicą między zyskiem a stratą.

**Uproszczony rachunek ROI.** Skoro redukcja o jedną milę dziennie na kierowcę to
~50 mln USD/rok (INFORMS), a osiągnięta redukcja jest wielokrotnie większa, zwrot z
inwestycji — mimo wysokich kosztów rozwoju — jest jednoznacznie dodatni.

`[TWÓJ WNIOSEK: oceń, czy taki model (oszczędność, nie przychód) da się "sprzedać" jako produkt SaaS mniejszym firmom. Czy to potencjalne nowe źródło przychodu dla UPS? To dobra okazja na własną rekomendację.]`

---

## 5. Wpływ regulacji

Wdrożenie AI w logistyce w Unii Europejskiej podlega rosnącemu otoczeniu regulacyjnemu.

**EU AI Act (Rozporządzenie (UE) 2024/1689).** Pierwszy na świecie kompleksowy akt
prawny regulujący AI; wszedł w życie **1 sierpnia 2024 r.**, a pełne stosowanie
przypada na **2 sierpnia 2026 r.** Wprowadza podejście oparte na ryzyku. System
optymalizacji tras sam w sobie prawdopodobnie nie jest "wysokiego ryzyka", ale jeśli
AI jest wykorzystywana do **oceny i monitorowania pracowników** (a dane z routingu i
telematyki łatwo do tego prowadzą), może wejść w zakres obowiązków dotyczących takich
zastosowań — w tym wymogów dokumentacji, przejrzystości i **nadzoru człowieka**
(art. 9–15 dla systemów wysokiego ryzyka).

**RODO (Rozporządzenie (UE) 2016/679).** System przetwarza dane osobowe: adresy
odbiorców oraz dane kierowców (lokalizacja, wydajność, czas pracy). Kluczowe są zasady
minimalizacji danych, ograniczenia celu oraz przepisy o **profilowaniu i
zautomatyzowanym podejmowaniu decyzji** (art. 22), zwłaszcza gdy ocena trasy przekłada
się na ocenę pracownika.

**Prawo pracy i dialog społeczny.** Monitorowanie kierowców w czasie rzeczywistym
dotyka prawa pracy i wymaga dialogu ze związkami zawodowymi (w przypadku UPS bardzo
silnymi w USA) — to nie tylko kwestia prawna, ale i akceptacji społecznej wdrożenia.

`[TWÓJ WNIOSEK: która z tych regulacji jest dla polskiej/europejskiej firmy logistycznej najtrudniejsza do spełnienia i dlaczego? Zajmij stanowisko.]`

---

## 6. Ryzyka technologiczne i etyczne

- **"Czarna skrzynka" i akceptacja kierowców.** ORION bywał odbierany nieufnie —
  trasy AI bywały kontrintuicyjne (np. unikanie skrętów w lewo), a kierowcy z
  wieloletnim doświadczeniem niechętnie ufali maszynie. Ryzyko oporu wdrożeniowego
  jest realne i potrafi zniweczyć korzyści techniczne.
- **Presja wydajnościowa i etyka pracy.** Optymalizacja "co do minuty" może zwiększać
  presję na pracowników i prowadzić do nadmiernego monitorowania — to ryzyko etyczne i
  reputacyjne.
- **Uzależnienie od danych i dostawcy (vendor/data lock-in).** Jakość optymalizacji
  zależy od jakości danych mapowych i ciągłości systemu; błędne dane mapowe = błędne
  trasy.
- **Cyberbezpieczeństwo.** System sterujący ruchem całej floty jest krytyczny — jego
  awaria lub atak paraliżuje operacje.
- **Ryzyko nadmiernej optymalizacji.** Skupienie wyłącznie na minimalizacji dystansu
  może pomijać czynniki jakościowe (bezpieczeństwo, satysfakcja klienta).

`[TWÓJ WNIOSEK: wskaż, które ryzyko uważasz za najpoważniejsze i zaproponuj sposób jego ograniczenia. Punktowana jest "identyfikacja ryzyk i kompromisów" — pokaż trade-off, np. efektywność vs dobrostan pracownika.]`

---

## 7. Wnioski strategiczne

**Synteza.** Przypadek ORION pokazuje, że transformacja AI w logistyce nie jest
projektem IT, lecz **programem strategicznym** o wieloletnim horyzoncie, w którym
sukces zależy w równym stopniu od technologii, danych i zarządzania zmianą (akceptacja
kierowców).

**Rekomendacje (do rozwinięcia własnymi słowami):**
1. Traktować wdrożenie AI jako program biznesowy z zaangażowaniem zarządu, nie jako
   projekt techniczny.
2. Inwestować w jakość danych i zarządzanie zmianą (szkolenia, komunikacja z
   pracownikami) na równi z algorytmami.
3. Wbudować zgodność regulacyjną (AI Act, RODO) oraz nadzór człowieka od początku
   projektowania ("compliance by design").

**Kluczowe czynniki sukcesu:** skala danych, akceptacja użytkowników, ciągłe
doskonalenie modelu, jasny business case.

**Scenariusze rozwoju (3–5 lat):** przejście od optymalizacji statycznej do w pełni
dynamicznej w czasie rzeczywistym, integracja z flotą elektryczną (planowanie
ładowania), łączenie z prognozowaniem popytu oraz potencjalnie z dostawami dronami /
pojazdami autonomicznymi.

`[TWÓJ WNIOSEK — NAJWAŻNIEJSZA SEKCJA: napisz własną ocenę potencjału rozwiązania w perspektywie 3–5 lat oraz własną rekomendację dla zarządu hipotetycznej polskiej firmy KEP. Tu egzaminator szuka samodzielnego myślenia.]`

---

## Bibliografia

1. INFORMS (Institute for Operations Research and the Management Sciences). *O.R. & Analytics Success Stories: UPS — On-Road Integrated Optimization and Navigation (ORION).* https://www.informs.org/Impact/O.R.-Analytics-Success-Stories/UPS *(źródło eksperckie / badania operacyjne)*
2. McKinsey & Company. *Harnessing the power of AI in distribution operations.* https://www.mckinsey.com/industries/industrials/our-insights/distribution-blog/harnessing-the-power-of-ai-in-distribution-operations *(źródło branżowe / raport doradczy)*
3. Parlament Europejski i Rada UE. *Rozporządzenie (UE) 2024/1689 (AI Act).* Dziennik Urzędowy UE. https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689 — streszczenie: https://artificialintelligenceact.eu/high-level-summary/ *(źródło dotyczące regulacji/prawa)*
4. Parlament Europejski i Rada UE. *Rozporządzenie (UE) 2016/679 (RODO).* Dziennik Urzędowy UE. *(źródło uzupełniające — regulacja)*

> **Weryfikacja źródeł:** wszystkie powyższe linki są realne i otwierane (stan na czerwiec 2026). Przed oddaniem pracy ponownie otwórz każdy z nich i upewnij się, że cytowane liczby się zgadzają.

---

## Załącznik: checklista zgodności z wymaganiami

- [ ] Wszystkie 7 wymaganych sekcji obecnych (1–7) ✔ (szkielet gotowy)
- [ ] Objętość 5–8 stron (bez strony tytułowej i bibliografii) — sprawdź po redakcji
- [ ] Min. 3 wiarygodne źródła, w tym: branżowe/raport (McKinsey), naukowe/eksperckie (INFORMS), regulacje/prawo (AI Act, RODO) ✔
- [ ] Wikipedia nie jest głównym źródłem ✔
- [ ] Formatowanie: Arial/Times New Roman, 11/12, interlinia 1.5, justowanie, marginesy 2.5 cm, numeracja stron → realizuje `build_docx.py`
- [ ] Uzupełnione wszystkie sekcje `[TWÓJ WNIOSEK]` — **własna analiza i rekomendacje**
- [ ] Diagram architektury przerysowany / podpisany
- [ ] Plik wyeksportowany do PDF lub DOCX
