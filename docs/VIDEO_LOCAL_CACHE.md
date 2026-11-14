# Trwały cache filmów — lokalna implementacja

Data: 14 listopada 2026. Kod lokalny gotowy. Limit konkretnego konta YouTube potwierdzono zrzutem panelu użytkownika: Search Queries per day = 100, wykorzystanie 9 (9%). Wybrany budżet Numervii: 80 wyszukiwań/24 h. Stan live nie został jeszcze utworzony. Nie uruchamiano prawdziwych zapytań do YouTube ani zasobów AWS.

## Jak to działa

Odwiedzający odczytują zapisaną listę, zamiast uruchamiać wyszukiwanie na YouTube. Osobne polecenie odświeża trzy obecne kategorie: Finance, Economy i Technology. Każda kategoria to jedno wyszukiwanie, najwyżej dwa zapisane wyniki, bez pobierania następnych stron. Powtórzone identyfikatory filmów pojawiają się na stronie tylko raz.

Nową próbę można wykonać w oknie 00:00, 06:00, 12:00 lub 18:00 UTC, z tolerancją pięciu minut i minimum sześciu godzin od poprzedniej próby danej kategorii. Opóźnione zdarzenia nie nadrabiają pominiętych wyszukiwań. Zwykły plan to 3 kategorie × 4 odświeżenia = 12 wyszukiwań na dobę. Nie jest to liczba zapytań na użytkownika.

Lista jest świeża przez 6 godzin i 5 minut tolerancji. Może być pokazana jako zapisana/starsza maksymalnie przez 24 godziny od pobrania. Przy braku części kategorii nadal wyświetlamy dostępne dane z informacją o niepełnej lub starszej liście. Po terminie dostępności API nie zwraca wygasłych danych, a frontend usuwa karty i odtwarzacz również z otwartej strony. Daty w pliku mają strefę czasową; na stronie są prezentowane w lokalnym czasie urządzenia.

Nie pobieramy plików wideo. Zapisujemy tylko identyfikatory, tytuły, kanały, daty i adresy miniaturek. Dane demo są syntetyczne: mają jawne oznaczenie, bez aktywnego odtwarzacza, odnośników do fikcyjnych nagrań i pobierania ich miniaturek.

## Uruchomienie demo

W katalogu `backend`, z aktywnym `.venv`:

```sh
python -m app.video_cli init-demo
python -m app.video_cli read
python -m app.video_cli refresh-demo
python -m uvicorn app.main:app --reload
```

Demo zostało już utworzone podczas sprawdzania tego zadania. `init-demo` służy wyłącznie pierwszemu utworzeniu pliku i odmawia nadpisania istniejącego stanu. `refresh-demo` poza oknem harmonogramu zwraca `skipped`; to oczekiwane zachowanie. Dane demo i blokada w `backend/.local/` są ignorowane przez Git.

Frontend uruchamia się jak dotychczas przez `npm run dev`. Bez klucza API newsy i filmy demo działają z istniejących plików. Start aplikacji ani wejście na stronę nie tworzy stanu automatycznie.

Inny niezależny plik demo można utworzyć przez `python -m app.video_cli --path .local/another-video-demo.json init-demo`. Aby API go odczytywało, przekaż zmienną procesu: `VIDEOS_STATE_PATH=.local/another-video-demo.json python -m uvicorn app.main:app --reload`. API nie odczytuje kluczy z `.env`.

## Limit darmowego API i konfiguracja live

Darmowy dostęp ma limit. Publiczna dokumentacja aktualnie opisuje domyślnie 100 wywołań search.list dziennie i koszt 1 jednostki w osobnym koszyku Search Queries. Zrzut użytkownika potwierdził dla projektu dzienny limit Search Queries równy 100; widoczne Queries per day = 10 000 to osobna pula, której nie dodajemy do limitu wyszukiwań. [YouTube Search: list](https://developers.google.com/youtube/data/reference/rest/v3/search/list), [YouTube Data API overview](https://developers.google.com/youtube/data/getting-started).

Przed live trzeba otworzyć Google Cloud Console, wybrać projekt używany przez klucz, następnie APIs & Services → YouTube Data API v3 → Quotas / System Limits. Sprawdzić limit dzienny wyszukiwań i jego jednostkę oraz bieżące wykorzystanie. Samo określenie „darmowe API” nie wystarcza do ustalenia tej wartości. Nie przekazywać klucza API do dokumentacji, czatu ani repozytorium.

Stan live wymaga osobnego pliku i jawnych parametrów przy `init-live`:

| Parametr | Znaczenie |
| --- | --- |
| `--daily-quota` | Potwierdzona dzienna pula w jednostkach pokazanych dla projektu. |
| `--cost-per-search` | Ile tych jednostek zużywa jedno wyszukiwanie. Przy limicie wyrażonym bezpośrednio w wywołaniach: 1. |
| `--request-budget` | Wewnętrzna maksymalna liczba wyszukiwań w ostatnich 24 godzinach. |
| `--confirm-quota-ready` | Jawne potwierdzenie, że operator sprawdził konfigurację i odnowienie limitu albo odczekał 24 h bez innych wywołań klucza. |

Zależność sprawdzana przez kod: budżet × koszt wyszukiwania nie przekracza 80% zadeklarowanej puli. Budżet musi wystarczać na obecny plan 12 wyszukiwań dziennie. Jeśli potwierdzone konto nie wystarcza na taki plan, kod odmawia konfiguracji; wymaga to osobnego uzgodnienia mniejszej liczby kategorii lub rzadszego odświeżania.

Dla potwierdzonego projektu wybrano daily_quota=100, cost_per_search=1 i request_budget=80. Te wartości przechodzą walidację; zapisanie ich w osobnym stanie live pozostaje do wykonania. Kod obsługuje też pule wyrażone inną liczbą jednostek i kosztem; nie zakłada historycznego kosztu wyszukiwania.

`refresh-live` wymaga `--allow-live`, istniejącego stanu live z budżetem i datą jego potwierdzenia oraz `YOUTUBE_API_KEY` w środowisku procesu. Nie czyta klucza z `.env`. Sam endpoint API nigdy nie uruchamia tej ścieżki. `python -m app.video_cli init-live --help` pokazuje składnię bez tworzenia stanu i bez HTTP.

Potwierdzono limit konta, lecz nie utworzono jego stanu live. Zrzut pokazuje 9 już wykonanych wyszukiwań; nie potwierdza pustego licznika ani pełnej historii ostatnich 24 h. Zgodnie z przyjętą procedurą pierwszą inicjalizację wykonać dopiero po potwierdzeniu odnowienia limitu lub po 24 h bez innych wywołań klucza. W tym kroku zweryfikowano model VideoBudget dla wartości 100/1/80 bez tworzenia stanu i bez HTTP. Inna aplikacja używająca tego samego projektu może zużywać wspólną pulę; wewnętrzny licznik obejmuje wyłącznie wywołania wykonane przez ten mechanizm.

## Zapis i zachowanie przy błędach

Status pierwszego uruchomienia na 14 listopada 2026: użytkownik nie potwierdził resetu limitu ani pełnych 24 godzin bez wywołań. Nie utworzono pliku live i nie uruchomiono pobierania. Powrót do inicjalizacji wymaga potwierdzenia tego warunku; nie liczymy 24 godzin od tej rozmowy, jeśli w międzyczasie wystąpią kolejne wywołania projektu.

- `video_state.py`: wersjonowany format danych, terminy, rezerwacje i jawny budżet.
- `video_store.py`: atomowa zamiana pliku po fsync, osobny flock synchronizujący lokalne procesy; maksymalnie 1 MiB. Brak/uszkodzenie pliku nie tworzy nowego licznika. Ponowna inicjalizacja istniejącego stanu jest zabroniona.
- `video_refresh.py`: zapisuje jedną rezerwację przed każdym wyszukiwaniem. Błąd zapisu oznacza zero HTTP; timeout, anulowanie i błąd dostawcy nie zwracają próby. Zapis wyniku scala aktualny stan i sprawdza rezerwację, więc stary wynik nie nadpisuje nowszego. Brak automatycznych ponowień i przekierowań.
- `video_cli.py`: jawne tworzenie, odczyt i odświeżanie demo/live.
- `videos.py`: wyłącznie odczyt; odpowiedź ma videos, updated_at, fresh_until, serve_until, stale i demo. Nie ujawnia liczników ani błędów dostawcy. Cache-Control: no-store; brak danych daje 503 i Retry-After do kolejnego planowanego okna, bez gwarancji powodzenia wtedy.

Wyczerpanie lokalnego budżetu blokuje następne wyszukiwanie do wyjścia odpowiednich prób z kroczącego okna 24 h. Ostrzeżenie pojawia się przy 80% budżetu. Konfiguracja i licznik przeżywają restart; nie usuwać pliku live ani rezerwacji, żeby obchodzić blokadę.

HTTP 403 quotaExceeded/dailyLimitExceeded blokuje dostawcę na 24 h. HTTP 429 oraz rozpoznane chwilowe limity 403 respektują Retry-After z minimum 6 h. Błędy uprawnień i nieprawidłowy klucz trwale zatrzymują live do świadomej korekty konfiguracji; odblokowanie nie może usuwać licznika. Pozostałe błędy zachowują ostatni poprawny zestaw. Nie zapisujemy tokenów ani treści odpowiedzi błędów.

Blokada plikowa działa dla procesów macOS/Linux korzystających z tego samego pliku. Osobne instancje Lambda będą wymagały przyszłego wspólnego magazynu i zapisów warunkowych. Adapter S3, automatyczny harmonogram oraz weryfikacja produkcyjnego osadzenia YouTube pozostają poza tą implementacją. Reguła 24 godzin jest naszym limitem produktu, nie deklaracją pełnej zgodności ze wszystkimi warunkami YouTube; przed publikacją należy uwzględnić [polityki API](https://developers.google.com/youtube/terms/developer-policies).

## Sprawdzenia

Testy obejmują restart, dwa procesy odświeżające to samo okno, 1000 odczytów API bez wywołań dostawcy i zmiany licznika, limity jednostek/wywołań, wyjście prób z okna 24 h, duplikaty i opóźnione okna, awarie zapisu rezerwacji i wyniku, anulowanie/timeout, błędy YouTube, niepoprawne dane, starsze i wygasłe listy, brak konfiguracji live oraz demo i usuwanie odtwarzacza po wygaśnięciu w przeglądarce. Testy nie wywołują YouTube.

Wynik końcowy: 239 testów backendu, 73 testy frontendu, Ruff, TypeScript i build poprawne. Pozostaje znane ostrzeżenie Starlette/TestClient o httpx. CLI init-demo/read/refresh-demo sprawdzone; plik i blokada ignorowane przez Git. Chrome przy 320 i 1440 px: trzy jawne karty demo, data pobrania, brak fikcyjnego odtwarzacza i przewijania całej strony. Zewnętrzne żądania były blokowane.
