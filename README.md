# Numervia

Numervia to rozwijana aplikacja webowa do porównywania scenariuszy finansowych i lepszego rozumienia wpływu decyzji na własne finanse.

Pierwsza wersja będzie umożliwiać porównanie spłaty kredytu hipotecznego z regularnymi nadpłatami i bez nich — z harmonogramem, kosztami odsetek i wykresem salda.

Planowane technologie: Python, FastAPI, React i TypeScript.

Projekt jest w rozwoju. Dostępny jest kalkulator kredytu hipotecznego oraz sekcje wiadomości i filmów.

## Uruchomienie frontendu

Wymagany Node.js 24 i npm. Z głównego folderu projektu:

```sh
cd frontend
npm ci
npm run dev
```

Otwórz adres podany przez Vite w terminalu (zwykle http://localhost:5173).
Zatrzymaj serwer skrótem Ctrl+C.

Sprawdzenie typów i przygotowanie wersji produkcyjnej:

```sh
npm run build
```

Narzędzie ma charakter edukacyjny i nie stanowi porady finansowej.

## Backend i lokalne newsy demo

W osobnym terminalu, z zainstalowanymi zależnościami backendu i Pythonem 3.14+:

```sh
cd backend
source .venv/bin/activate
python -m app.news_cli init-demo
python -m uvicorn app.main:app --reload
```

`init-demo` wykonaj tylko przy pierwszym utworzeniu pliku; jeśli stan już istnieje, pomiń to polecenie. API: http://localhost:8000/docs. Frontend uruchom według instrukcji powyżej, równolegle z backendem.

Newsy są odczytywane z lokalnego zapisanego stanu. Demo nie wymaga kluczy dostawców. Wejście na stronę nie uruchamia pobierania newsów z zewnętrznych API. Szczegóły odświeżania i formatu odpowiedzi: [lokalny cache newsów](docs/NEWS_LOCAL_CACHE.md). Filmy również korzystają z trwałego stanu. Demo utworzysz jednorazowo w katalogu backend przez `python -m app.video_cli init-demo`. Wejścia na stronę nie uruchamiają wyszukiwania na YouTube. Instrukcja: [lokalny cache filmów](docs/VIDEO_LOCAL_CACHE.md).

## Konfiguracja przed AWS

Adapter Lambda: `app.handler.handler`. Frontend obsługuje publiczną zmienną `VITE_API_BASE_URL`, a backend listę originów `ALLOWED_ORIGINS`. Zmiana adresu API po publikacji wymaga nowego buildu frontendu. Instrukcja uruchomienia z osobnym API, konfiguracja CORS i otwarte warunki danych live: [przygotowanie aplikacji do AWS](docs/AWS_APP_PREPARATION.md). Zasoby AWS nie są jeszcze utworzone.
