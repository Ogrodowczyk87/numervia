# Lokalny trwały stan newsów

Implementacja z 14 listopada 2026. Warstwa lokalna z NEWS_CACHE_DESIGN.md jest podłączona do endpointu i frontendu; bez S3, harmonogramu AWS i nowych zależności.

## Uruchomienie demo

## Zapisany podgląd prawdziwych nagłówków

`python -m app.news_preview --allow-live --confirm-quota-ready` przygotowuje jednorazowy lokalny podgląd. Pierwsze utworzenie licznika wymaga potwierdzenia wolnego budżetu kont dostawców; nie uruchamiać z flagą potwierdzenia bez tej wiedzy. Klucze są odczytywane wyłącznie przez jawnie wywołane CLI ze środowiska lub backend/.env, nigdy przez startup API i nigdy nie są wypisywane.

Stan i historia rezerwacji są w backend/.local/news-live.json. Nie tworzyć kolejnych liczników dla tych samych kluczy. CLI wykonuje najwyżej jedno żądanie na skonfigurowany zestaw (1 Marketaux + 2 Currents przy obu kluczach), bez paginacji i automatycznych ponowień. Rezerwacja jest zapisywana przed HTTP, zachowane są limity 80/200 w ostatnich 24 h, odstęp 6 h i blokady dostawców. Ręczne wywołanie może odbyć się poza pięciominutowym oknem harmonogramu; zwykłe refresh-live zachowuje dotychczasowy harmonogram.

Po udanym pobraniu marker backend/.local/news-preview.enabled włącza ten plik w lokalnym API, jeśli nie ustawiono NEWS_STATE_PATH. Frontend pokazuje „Saved preview · No automatic updates.”, źródła i linki. Odświeżenie przeglądarki nie pobiera danych dostawców. Nadal obowiązuje maksymalny wiek danych 24 h; starsze wiadomości nie są podawane. Nie jest to bezterminowe archiwum ani automatyczne odświeżanie. Nie usuwaj news-live.json w celu resetowania budżetów. Wyłączenie podglądu wymaga usunięcia tylko markera; licznik pozostaje.

Currents opisuje krótkotrwały cache operacyjny, a nie bezterminowe archiwum: https://currentsapi.services/en/faq. Lokalny podgląd nie potwierdza zakresu praw do publicznej republiki i zdjęć; pozostaje to osobnym warunkiem publikacji w roadmapie.

## Syntetyczne demo

Pełniejszy podgląd lokalnego interfejsu (6 kart finansowych i 4 przykłady mieszkaniowe w danych):

```sh
python -m app.news_cli preview-demo
```

Polecenie tworzy demo, jeśli brakuje pliku, albo aktualizuje jego syntetyczne snapshoty na kolejne 24 h. Odmawia zmiany stanu live, zachowuje istniejące liczniki i rezerwacje oraz nie wykonuje HTTP. Można je wywołać o dowolnej porze do podglądu UI; nie zmienia harmonogramu ani limitów odświeżania live. Karty demo mają lokalne ilustracje SVG, wyraźne oznaczenie i nie zawierają linków do fikcyjnych artykułów. Po wygaśnięciu danych uruchomić polecenie ponownie. To podgląd, nie prawdziwe wiadomości.

Z katalogu `backend`, z aktywnym `.venv`:

```sh
python -m app.news_cli init-demo
python -m app.news_cli read
python -m app.news_cli read --feed housing
python -m app.news_cli refresh-demo
```

Demo używa syntetycznych nagłówków i nie wykonuje połączeń sieciowych. Domyślny plik `backend/.local/news-demo.json` oraz plik blokady są ignorowane przez Git. Demo zostało utworzone i odczytane podczas sprawdzenia implementacji; ponowne `init-demo` odmówi nadpisania istniejącego stanu.

Odświeżanie dopuszcza bieżące okno 00:00, 06:00, 12:00 lub 18:00 UTC i najwyżej pięć minut opóźnienia. Poza tym oknem `skipped` jest poprawnym wynikiem. Każdy zestaw ma dodatkowo minimum sześć godzin przerwy od ostatniej próby. Nie nadrabiamy opuszczonych okien.

Osobna ścieżka pliku, gdy potrzebne jest nowe niezależne demo:

```sh
python -m app.news_cli --path .local/another-demo.json init-demo
python -m app.news_cli --path .local/another-demo.json read
```

## Co implementują moduły

- `news_state.py`: walidowany format wersji 1, trzy dozwolone zestawy, świadome strefy czasowe, metadane i osobne budżety dostawców.
- `news_store.py`: zapis JSON do pliku tymczasowego, fsync i atomowa zamiana. Osobny plik blokady flock chroni całą operację odczyt–zmiana–zapis między procesami lokalnymi. Maksymalny rozmiar stanu: 1 MiB.
- `news_refresh.py`: trwała rezerwacja przed HTTP, deduplikacja okien, osobne limity 80/200 w kroczącym oknie 24 h, ostrzeżenia 60/150, zachowanie rezerwacji po timeout/przerwaniu. Zapis wyniku scala aktualny stan i sprawdza identyfikator rezerwacji, więc starszy wynik nie nadpisuje nowszego.
- `news_cli.py`: jawne tworzenie stanu, odczyt i odświeżanie. Tryby demo/live mają oddzielny stan; nie można użyć magazynu demo jako live.

Uszkodzony, brakujący albo nieczytelny stan zatrzymuje odświeżanie. Nie tworzymy automatycznie nowego budżetu. Awaria zapisu rezerwacji oznacza zero wywołań dostawcy; awaria po skutecznej rezerwacji nie zwraca jednostki. Atomowość zamiany nie zastępuje blokady: potrzebne są obie rzeczy.

Odczyt `read_feed` nie wykonuje HTTP ani nie zmienia budżetów. Łączy dostępne źródła, usuwa powtórzone URL i wylicza aktualność z zegara. Pusta lista jest poprawnym wynikiem; brak zestawu i upływ 24 godzin to niedostępność. Dane po terminie dostępności są usuwane przy kolejnej zmianie stanu.

HTTP 402 blokuje dostawcę na 24 h. HTTP 429 respektuje Retry-After w sekundach lub formacie daty, z minimum sześciu godzin; nie rozpoznajemy jeszcze szczególnego kodu dziennego limitu Currents. HTTP 401/403 trwale blokuje dostawcę. Inne błędy zachowują ostatni poprawny zestaw; nie ma automatycznych ponowień HTTP ani przekierowań. Nowy proces zachowuje daty, liczniki i blokady z pliku.

## Tryb live — dostępny, nieuruchamiany w sprawdzeniach

Pierwszy stan live wymaga osobnej ścieżki i flagi `--confirm-quota-ready`. To potwierdzenie, że operator sprawdził odnowienie limitu konta lub odczekał pełne 24 h bez innych wywołań klucza. Sam program tego nie weryfikuje. Nie usuwać stanu live, aby zresetować budżet.

Odświeżenie live wymaga `--allow-live` oraz kluczy dostawców przekazanych przez środowisko. CLI celowo nie odczytuje kluczy z `.env`. Brak klucza pomija dostawcę, a brak obu kończy polecenie błędem. W stanie i logach nie zapisujemy tokenów ani odpowiedzi błędów dostawców. Po błędzie credentials, po poprawieniu konfiguracji operator musi świadomie zdjąć `provider_disabled`, zachowując rezerwacje i pozostały stan; nie ma automatycznego resetu ani polecenia czyszczącego budżet.

Żadnych prawdziwych wywołań dostawców nie wykonano w tym zadaniu. Aktualne limity kont, warunki przechowywania treści i limit minutowy wymagają potwierdzenia przed uruchomieniem live. Lista zestawów jest stała: Marketaux overview oraz Currents overview/housing; bez dowolnych filtrów i paginacji.

## Granica tego etapu

Endpoint `GET /api/v1/news?feed=overview|housing` odczytuje wyłącznie magazyn. Nie potrzebuje kluczy dostawców i nie ma awaryjnej ścieżki HTTP. Zwraca obiekt `articles`, `feed`, `fetched_at`, `fresh_until`, `serve_until`, `stale`, `demo`. Odpowiedź ma `Cache-Control: no-store`.

Brak poprawnego zestawu daje HTTP 503 z bezpiecznym kodem `news_unavailable`; brak pliku ma odrębny kod `news_not_configured`. Nagłówek Retry-After wskazuje następne planowane okno sześciogodzinne, bez obietnicy że konfiguracja, blokada dostawcy lub awaria magazynu będą do tego czasu naprawione. Nieznany feed daje 422, endpoint odświeżania nie istnieje. Liczniki i kody błędów dostawców nie trafiają do odpowiedzi API.

Domyślnie API odczytuje ten sam plik demo co CLI. Inną istniejącą ścieżkę można wskazać przez zmienną procesu `NEWS_STATE_PATH`, np. `NEWS_STATE_PATH=.local/another-demo.json python -m uvicorn app.main:app --reload` z katalogu backend. API nie odczytuje `.env` z kluczami newsów. Przy pierwszym uruchomieniu jawnie utworzyć demo przez CLI; brak pliku nie inicjalizuje go automatycznie.

Frontend obu zestawów pokazuje Demo news dla danych syntetycznych, czas pobrania w lokalnej strefie oraz Showing saved news dla starszych danych. Po terminie `serve_until` usuwa karty również z otwartej strony. Nie odpytuje dostawców ani nie wymusza odświeżania; kolejna wizyta odczytuje istniejący stan. Terminy w przeglądarce używają zegara urządzenia, a API niezależnie egzekwuje dostępność danych po stronie serwera.

Kryterium 1000 odczytów bez HTTP i bez zmian liczników sprawdzono teraz dla rzeczywistego endpointu. Sprawdzono także odtworzenie aplikacji nad tym samym plikiem, równoległych czytelników, brak/uszkodzenie/wygaszenie stanu i częściową dostępność dostawców. Testy obsługi dostawców przeniesiono na jawny mechanizm odświeżający zamiast utrzymywać wcześniejsze założenie, że GET uruchamia pobieranie.

Lokalny flock działa na macOS/Linux i wspólnym lokalnym systemie plików. Nie zapewnia synchronizacji osobnych instancji Lambda. Przyszły adapter S3 wymaga warunkowych zapisów i osobnych testów. Infrastruktura i filmy pozostają poza tym zadaniem.

## Sprawdzenia

Testy obejmują serializację i walidację dat, dwa osobne procesy, restart, duplikaty i opóźnione okna, limity obu dostawców, anulowanie/timeout, błędy HTTP, awarie zapisu rezerwacji i wyniku, konflikt wyniku, 1000 odczytów, stare i wygasłe dane, uszkodzony plik, nieobsługiwaną wersję i zakaz ponownej inicjalizacji.

```sh
python -m pytest -q
python -m ruff check .
```

Wynik końcowy: 183 testy backendu przeszły, Ruff bez błędów. Pozostaje znane ostrzeżenie Starlette/TestClient o httpx. Sprawdzono także CLI init-demo/read/refresh-demo i ignorowanie stanu przez Git.

Aktualizacja po integracji: 189 testów backendu i 67 testów frontendu przeszło; Ruff, TypeScript i build poprawne. Chrome: sprawdzono newsy demo przez lokalne API przy 320 i 1440 px, bez przewijania poziomego. Zewnętrzne widgety i endpoint filmów były blokowane podczas tego sprawdzenia; nie wykonywano live refresh.
