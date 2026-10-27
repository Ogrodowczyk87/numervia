# Numervia

Numervia to rozwijana aplikacja webowa do porównywania scenariuszy finansowych i lepszego rozumienia wpływu decyzji na własne finanse.

Pierwsza wersja będzie umożliwiać porównanie spłaty kredytu hipotecznego z regularnymi nadpłatami i bez nich — z harmonogramem, kosztami odsetek i wykresem salda.

Planowane technologie: Python, FastAPI, React i TypeScript.

Projekt jest na wczesnym etapie rozwoju. Obecny frontend wyświetla nazwę Numervia.

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
