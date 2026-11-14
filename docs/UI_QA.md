# Numervia — sprawdzenie wyglądu i obsługi

Data: 14 listopada 2026. Zakres: punkt 2 z `AWS_ROADMAP.md`.

## Sposób sprawdzenia

Lokalny Vite i FastAPI, Chrome headless, rzeczywisty silnik kalkulatora. Sprawdzono szerokości 320, 375, 768 i 1440 px; nawigację także przy 1536 px. Oceniono zrzuty ekranu oraz zachowania przez sterowanie przeglądarką. Bez fizycznego telefonu, Safari i czytnika ekranu.

Zablokowano żądania zewnętrzne oraz endpointy newsów i filmów, żeby nie zużywać limitów dostawców. Stronę główną sprawdzono w stanie błędu pobierania danych. Pełny widok z załadowanymi widgetami wymaga osobnego sprawdzenia, jeśli wejdą do pierwszej publikacji.

## Wyniki

| Obszar | Wynik |
| --- | --- |
| Układ 320, 375, 768, 1440 px | Po poprawkach brak przewijania poziomego całej strony głównej i kalkulatora; porównano scrollWidth z clientWidth. |
| Nawigacja | Menu rozwijane poniżej 1536 px; od 1536 px linki i przyciski mieszczą się w jednym wierszu. Escape zamyka menu i zwraca fokus do przycisku. |
| Klawiatura | Tab przechodzi z menu do formularza; pole ma widoczną ramkę i cień fokusu. Obszar tabeli można skupić i przewijać. |
| Walidacja | Ujemna kwota kredytu nie przechodzi natywnej walidacji. |
| Obliczenie | £180 000, 4,5%, 25 lat, nadpłata £200: wynik, wykres i harmonogram z backendu; okresy 300 i 221 miesięcy. |
| Ładowanie i błąd | Opóźniona odpowiedź pokazuje Calculating… i blokuje wysłanie. Zerwanie połączenia pokazuje komunikat z role=alert. |
| Wykres | Dwie linie, czytelna legenda i oś kwot po poprawce. Oceniono zrzuty w motywie jasnym i ciemnym. |
| Tabela | Przewijanie wewnątrz własnego obszaru, bez rozszerzania strony. |
| Paginacja | Ostatnia strona 25/25, miesiące 289–300, Next zablokowany. Zmiana scenariusza przywraca stronę 1/19. Istniejące testy obejmują również Previous. |
| Krótki harmonogram | £100, 0%, 1 rok, nadpłata £200: wariant z nadpłatą ma jeden wiersz i zablokowane Previous/Next. |

## Poprawki

- `frontend/src/styles/global.css`: zniesiono minimum szerokości body. Przy oknie 320 px pionowy pasek przewijania zmniejsza dostępne miejsce; wcześniejsze minimum powodowało poziome przewijanie.
- `frontend/src/components/Navbar.tsx`: pełna nawigacja od progu 2xl (1536 px); przełącznik motywu nie spada do drugiego wiersza przy 1440 px.
- `frontend/src/features/mortgage/MortgageChart.tsx`: krótsze kwoty na osi, np. £180k; pełne kwoty pozostają w podpowiedziach i tabeli. Bez zmian w obliczeniach.

## Rozmiar aplikacji i LL-047

Build po zmianach: główna paczka JS 245,03 kB (gzip 76,26 kB); strona kalkulatora z wykresem 375,47 kB (gzip 108,86 kB). Brak ostrzeżenia o JS przekraczającym 500 kB.

Decyzja: zachować obecny podział na strony przez lazy i Suspense w App.tsx oraz komunikat Loading page… . Nie dodawać teraz osobnego importu samego wykresu. Sprawdzono jego działanie po Calculate. Nie podnoszono limitu ostrzeżeń Vite.

Tło PNG: 1 448,87 kB, logo: 262,33 kB. Nie mierzono ładowania przez sieć komórkową. Kompresja lub konwersja obrazów pozostaje propozycją poprawy wydajności; w tym zadaniu grafik nie zmieniano.

## Weryfikacja i ograniczenia

- `npm test`: 32 pliki, 60 testów — wszystkie przeszły.
- `npm run build`: TypeScript i build Vite przeszły.
- Backend bez zmian; wykorzystano go do rzeczywistego obliczenia w przeglądarce.

Lokalne QA zakończone. Przed publikacją pozostaje fizyczny telefon i załadowane usługi zewnętrzne, jeśli będą publikowane. To sprawdzenie nie zastępuje pełnego audytu dostępności. Komunikat błędu kalkulatora wspomina o backendzie; warto uprościć go dla publicznej wersji w punkcie 4.
