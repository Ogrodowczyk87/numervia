# Zmiany do commita — 14 listopada 2026

Proponowany tytuł:

```text
feat: add durable content caches and prepare Numervia for AWS
```

## Opis

Newsy i filmy korzystają z trwałego lokalnego magazynu. Wejścia na stronę odczytują zapisany stan, a pobieranie danych odbywa się przez osobne polecenia odświeżające z licznikami prób. Aplikacja otrzymała adapter Lambda oraz konfigurowalne połączenie frontend–API.

## Lista zmian

- Dodano modele, magazyny JSON z atomowym zapisem i blokadą między procesami, metadane świeżości oraz trwałe rezerwacje prób dla newsów i filmów.
- Dodano CLI demo/live; rozdzielono odczyt API od odświeżania. Błędy i restart nie zerują liczników; przechowywanie danych ma limit 24 godzin.
- Zmieniono kontrakty API i frontend: oznaczenie danych demo, daty aktualizacji, informacja o starszych danych i usuwanie wygasłych kart oraz odtwarzacza.
- Domyślny widok korzysta obecnie z danych demo. Pobierania prawdziwych newsów i filmów nie uruchomiono; jest to widoczna zmiana względem wcześniejszego pobierania przy żądaniu.
- Dodano adapter Mangum `app.handler.handler`, konfigurowalny CORS `ALLOWED_ORIGINS` oraz wspólny `VITE_API_BASE_URL` dla klientów kalkulatora, newsów i filmów.
- Poprawiono układ nawigacji, przewijanie strony przy 320 px i czytelność kwot na osi wykresu. Uproszczono komunikaty błędów kalkulatora i dodano odnośnik atrybucji Currents.
- Rozbudowano testy restartów, współbieżności, limitów, awarii magazynu, odczytu bez HTTP, wygasania danych, konfiguracji adresu API, CORS i zdarzeń Lambda.
- Uzupełniono README, przykłady konfiguracji i dokumentację planu wdrożenia. Wykluczono lokalne magazyny i blokady z Git.

## Najważniejsze pliki

- Backend: `backend/app/news/state.py`, `news/store.py`, `news/refresh.py`, `news/cli.py` oraz odpowiedniki w `videos/`; endpointy `news/routes.py`, `videos/routes.py`, konfiguracja `main.py` i adapter `handler.py`.
- Frontend: `frontend/src/config/api.ts`, komponenty i klienty w `features/news`, `features/videos`, poprawki w nawigacji, kalkulatorze i stylach.
- Dokumentacja: `AWS_ROADMAP.md`, `AWS_APP_PREPARATION.md`, `NEWS_LOCAL_CACHE.md`, `VIDEO_LOCAL_CACHE.md`, `UI_QA.md` i `RELEASE_SCOPE.md`.

## Weryfikacja wykonana przed przygotowaniem tego opisu

- Backend: 249 testów przeszło; Ruff bez błędów.
- Frontend: 81 testów przeszło; TypeScript i build poprawne.
- Chrome: 320, 375, 768 i 1440 px; osobny origin API, dane demo i załadowane widgety TradingView.
- Znane uwagi: ostrzeżenie Starlette/TestClient, brak konfiguracji ESLint, ostrzeżenia ResizeObserver powiązane z ładowaniem widgetów TradingView. Ograniczenia opisano w AWS_APP_PREPARATION.md.

## Granice tego commita

Podczas przygotowania opisu wykonano podstawową kontrolę 210 plików tekstowych śledzonych i nowych: znane wzorce kluczy oraz dokładne wartości sekretów z lokalnej konfiguracji sprawdzano bez wypisywania tych wartości. Nie wykryto dopasowań ani śledzonych plików poświadczeń/lokalnego stanu. Indeks Git nie zawierał przygotowanych zmian; `git diff --check` przeszedł. To kontrola bieżących plików, nie pełny audyt historii Git ani gwarancja wykrycia każdego rodzaju sekretu.

- Bez zasobów AWS, deploymentu i bootstrap. Na późniejsze polecenie użytkownika commit zostaje przygotowany lokalnie; push wykonuje użytkownik.
- Stan live filmów nieutworzony; oczekuje na potwierdzenie resetu limitu lub 24 h bez wywołań. Zakres publicznego użycia treści newsowych nadal wymaga wyjaśnienia.
- Nie dodawać `.env`, poświadczeń, `.venv`, `node_modules`, `dist` ani `backend/.local` do commita. Przykłady `.env.example` zawierają jedynie puste wartości i publiczne ustawienia.
- Do lokalnego `AGENTS.md` dodano krytyczne zasady ochrony sekretów i kontroli przed commitem. `AGENTS.md` i `PROJECT_PLAN.md` są ignorowane przez Git; ta lokalna instrukcja nie wejdzie do commita przy obecnych regułach.

## Uruchomienie

Backend: w `backend`, z aktywnym `.venv`, uruchomić `python -m uvicorn app.main:app --reload`. Frontend: w drugim terminalu, w `frontend`, `npm run dev`. Pierwsze utworzenie danych demo opisano w dokumentach lokalnych cache; istniejącego stanu nie nadpisywać.
