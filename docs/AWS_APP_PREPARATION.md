# Przygotowanie aplikacji do AWS — punkt 4

Data: 14 listopada 2026. Prace programistyczne zakończone lokalnie. Brak zasobów, bootstrap, deploymentu i prawdziwych wywołań dostawców. Stan live filmów nadal nieutworzony: użytkownik nie potwierdził resetu limitu ani 24 godzin bez wywołań.

## Adapter Lambda

Entry point: `app.handler.handler`, z katalogiem `backend` jako katalogiem głównym paczki. Mangum przekłada HTTP payload v2 z Function URL na żądanie FastAPI. Lokalnie sprawdzono health, walidację HTTP 422 i rzeczywiste obliczenie kredytu. Instancja adaptera tworzona przy wywołaniu zapewnia odtworzenie pętli zdarzeń w Pythonie 3.14; aplikacja FastAPI pozostaje wspólna. Lifespan wyłączono, ponieważ aplikacja nie rejestruje obecnie zasobów startup/shutdown.

Mangum już był zależnością projektu, niczego nie instalowano. [Dokumentacja adaptera](https://mangum.fastapiexpert.com/adapter/). AWS wymienia Python 3.14 jako obsługiwany runtime; paczki z bibliotekami natywnymi trzeba później przygotować dla Linux i wybranej architektury Lambdy, zamiast kopiować macOS `.venv`. [Runtime Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html).

## Adres API i CORS

Wszystkie trzy klienty frontendu korzystają ze wspólnego `frontend/src/config/api.ts`.

| Zmienna | Gdzie ustawić | Znaczenie |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Frontend, przed startem Vite lub buildem | Puste: względne /api przez lokalne proxy. Produkcja: sam origin HTTPS backendu, bez /api, tokenów i końcowej ścieżki. Wartość jest publiczna, wbudowana w JS. |
| `ALLOWED_ORIGINS` | Środowisko procesu backendu | Lista originów oddzielonych przecinkami. Domyślnie localhost:5173 i 127.0.0.1:5173. Produkcja: dokładny origin CloudFront. Bez wildcard, ścieżki i końcowego ukośnika. Pusty ciąg wyłącza dostęp przez CORS. |
| `NEWS_STATE_PATH` | Backend | Istniejący plik stanu newsów; domyślnie lokalne demo. |
| `VIDEOS_STATE_PATH` | Backend | Istniejący plik stanu filmów; domyślnie lokalne demo. |
| Klucze dostawców | Wyłącznie osobne polecenia odświeżające | Nie są potrzebne publicznemu API i nie trafiają do frontendu. |

Po zmianie konfiguracji zrestartować odpowiedni proces. Po zmianie adresu produkcyjnego API ponowić build frontendu. Backend czyta zmienne procesu; przykłady w `.env.example` nie są automatycznie wczytywane. Vite obsługuje własne pliki `.env.local` i zmienne przekazane przed poleceniem. Nie nadpisywać istniejących lokalnych plików `.env`.

Sprawdzenie lokalne z dwoma originami, w dwóch terminalach:

```sh
# Terminal 1, katalog backend, aktywne .venv:
python -m uvicorn app.main:app --reload
```

```sh
# Terminal 2, katalog frontend:
VITE_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

W przeglądarce otworzyć adres Vite. Domyślne CORS pozwala lokalnemu frontendowi połączyć się z portem 8000. Proxy Vite pozostaje wygodnym wariantem lokalnym, ale build produkcyjny już od niego nie zależy.

Przykład późniejszego buildu: `VITE_API_BASE_URL=https://API-ORIGIN npm run build` — zastąpić symbol prawdziwym originem Function URL, gdy powstanie w etapie infrastruktury. Nie utworzono takiego adresu w tym zadaniu.

CORS obsługuje FastAPI: GET, POST i preflight z Content-Type, bez cookies/credentials. Obce originy nie otrzymują nagłówka ze zgodą. W przyszłej konfiguracji Function URL nie dodawać drugiej, konkurencyjnej warstwy CORS. CORS ogranicza zachowanie przeglądarki, nie zabezpiecza publicznego API przed klientami HTTP.

## Gotowość magazynów

Newsy i filmy są odczytywane z trwałego stanu, bez pobierania przy wizycie. Brak pliku daje bezpieczne 503, bez inicjalizacji budżetu. Instrukcje: [newsy](NEWS_LOCAL_CACHE.md), [filmy](VIDEO_LOCAL_CACHE.md).

Lokalny plik nie jest wspólnym magazynem dla wielu instancji Lambda. Adapter S3 z warunkowymi zapisami, osobne funkcje odświeżające i harmonogramy pozostają w punkcie 6. Pliki `.local` nie są paczką produkcyjnego cache. Sam adapter Lambda nie oznacza gotowości pełnego wdrożenia dodatków.

## Przegląd planów i warunków dostawców

Użytkownik potwierdził 14 listopada 2026, że konta Marketaux i Currents mają Free. Limit Search Queries YouTube 100/dzień potwierdzono zrzutem panelu; wybrany budżet aplikacji 80/24 h. Nie zwiększano żadnego limitu ani nie aktywowano płatnego planu.

| Dostawca | Ustalenia z publicznych źródeł | Pozostałe warunki uruchomienia |
| --- | --- | --- |
| Marketaux | Free: 100 żądań/dzień i 3 artykuły na żądanie. Ogólne ToS zawierają ograniczenia osobistego, niekomercyjnego użycia; nie dają jednoznacznego potwierdzenia całego planowanego publicznego cache. | Wyjaśnić zakres publicznego pokazywania nagłówków/obrazów i przechowywania 24 h dla tego konta; do tego czasu demo. |
| Currents | Free: 250 żądań/dzień, 20 wyników, reset 00:00 UTC. FAQ przewiduje preview, attribution, link-out i krótkotrwały cache operacyjny; nie obejmuje pełnej republiki artykułów. Dodano widoczny link Powered by Currents News API obok treści, także w kompaktowych kartach. | Przed live potwierdzić zakres użycia zdjęć i pól wydawców w planowanym publicznym widoku; nie kopiować pełnych artykułów. |
| YouTube | Zapisujemy ograniczone metadane i odnośniki, nie pliki filmów. Polityki przewidują limit czasowego przechowywania oraz aktualizację danych; nasze 24 h jest ostrzejszym limitem produktu. Zachowujemy oryginalny odtwarzacz i oznaczenia. | Pierwsza inicjalizacja live nadal oczekuje na potwierdzenie stanu zużycia; testy odtwarzacza wykonano na mockach, nie przez pobranie realnej listy live. |
| TradingView | Oficjalne komponenty webowe, zachowane ich oznaczenia i linki. W przeglądarce rzeczywiście załadowały się ticker i mapa. | Zachować branding i nie traktować danych widgetu jako własnego API ani usuwać atrybucji. |

Źródła do tabeli: [Marketaux pricing](https://www.marketaux.com/pricing), [Marketaux ToS](https://www.marketaux.com/tos), [Currents pricing](https://currentsapi.services/en/product/price), [Currents FAQ](https://currentsapi.services/en/faq), [Currents attribution](https://currentsapi.services/terms), [YouTube policies](https://developers.google.com/youtube/terms/developer-policies), [TradingView attribution](https://www.tradingview.com/widget-docs/faq/general/). To zapis sprawdzonych warunków i ograniczeń, nie stwierdzenie dodatkowych praw z nieudostępnionych umów kont.

## Sprawdzenie interfejsu

Chrome, szerokości 320, 375, 768 i 1440 px. Frontend 127.0.0.1:5173, API bezpośrednio 127.0.0.1:8000: formularz oblicza przez CORS i pokazuje wykres; obie sekcje danych demo dostępne, widgety TradingView załadowane, brak poziomego przewijania całej strony. Oceniono zrzuty. Nie wykonywano płatnych ani prawdziwych wywołań newsów i YouTube API. Odtwarzanie i błędy live pozostają sprawdzone przez testy zastępujące odpowiedzi.

Fizyczny telefon i końcowa kontrola z dopuszczonymi danymi live nadal należą do QA przed publikacją. Brak konfiguracji ESLint i znane ostrzeżenie zależności Starlette pozostają wcześniej zapisanymi uwagami; nie ukrywano ich przez wyłączenie sprawdzeń.

Wynik końcowy: 249 testów backendu, 81 testów frontendu, Ruff, TypeScript i build poprawne. Pozostaje znane ostrzeżenie Starlette/TestClient o httpx. Poprawiono także testową fabrykę dat filmów: wszystkie terminy korzystają z jednego odczytu zegara, zamiast sporadycznie przekraczać limit 24 h o milisekundę.

Uwaga z końcowego QA: przy ładowaniu zewnętrznych widgetów wystąpiło ostrzeżenie ResizeObserver loop completed with undelivered notifications. Porównanie tego samego widoku: skrypty TradingView zablokowane — 0 ostrzeżeń; włączone — 9. Instrumentacja pokazała obserwatory zewnętrznych skryptów, bez zapętlania obserwatora HousingNews. Wskazuje to na zachowanie widgetów podczas układania strony; nie stwierdzono przewijania całej strony ani zablokowania kalkulatora. Nie wyciszano błędu globalnie i nie modyfikowano kodu dostawcy. Obserwować ponownie podczas końcowego QA przed publikacją.
