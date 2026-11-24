# Numervia — zakres pierwszej publikacji

Data przeglądu: 14 listopada 2026.
Status: zakres uzgodniony z użytkownikiem — wariant B, kalkulator, newsy i filmy w pierwszej publikacji.

Ten dokument dotyczy punktu 3 z `AWS_ROADMAP.md`. Nie jest zgodą na wdrożenie, tworzenie zasobów ani wyłączanie istniejących funkcji.

## Podstawa pierwszej wersji

Zgodnie z `PROJECT_PLAN.md` podstawą MVP jest kalkulator hipoteczny: formularz, walidacja, obliczenia Python Decimal, porównanie scenariuszy, podsumowanie, wykres i harmonogram. Dochodzą obecna nawigacja, motywy i informacje o uproszczeniach obliczeń.

Pozostałe planowane kalkulatory i Finance Operations nie wchodzą do pierwszego wdrożenia.

## Gotowość dodatków

| Funkcja | Obecny stan w kodzie | Co pozostaje przed publicznym uruchomieniem |
| --- | --- | --- |
| Newsy ogólne i mieszkaniowe | Cache 6 h w pamięci procesu; lokalne liczniki prób; obsługa limitów i częściowej awarii dostawców. | Trwały wspólny cache i budżety, kontrolowane odświeżanie niezależne od odwiedzin, testy restartów i wielu instancji. |
| Filmy YouTube | Cache 6 h w pamięci; do trzech żądań wyszukiwania na pełne odświeżenie; starsze dane przy awarii i przerwa 5 min po błędzie. | Wspólny cache, trwała kontrola zużycia limitu, uzgodnione odświeżanie i maksymalny wiek starszych danych. |
| Widgety TradingView | Skrypty zewnętrzne w index.html; ticker globalnie i podsumowanie rynków na stronie głównej; bez wywołań backendu do tych widgetów. | Sprawdzenie z prawdziwie załadowanymi widgetami, na telefonie i przy zablokowanym skrypcie; potwierdzenie warunków publicznego osadzenia. |

### Dlaczego lokalny cache nie wystarcza na Lambda

`NewsCache` i `VideoCache` to globalne obiekty w pamięci Pythona. Każdy nowy proces otrzymuje własny stan. Dla standardowej Lambda ponowne użycie środowiska jest optymalizacją; nie zapewnia trwałego stanu aplikacji. Restart lub kolejna instancja oznacza pusty cache i nowe lokalne liczniki. Wniosek z kodu: obecne limity nie są wspólne dla całej aplikacji. [Cykl życia środowiska Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html)

Liczby 80 i 200 w `news/routes.py` są limitami zapisanymi w aplikacji; nie potwierdzają limitów ani praw do publikacji z kont dostawców. Przed publikacją trzeba sprawdzić rzeczywiste plany i warunki używania nagłówków, zdjęć i przechowywania danych.

W repozytorium istnieje [NEWS_CACHE_DESIGN.md](NEWS_CACHE_DESIGN.md): projekt prywatnego S3, osobnego zadania odświeżającego i harmonogramu. To propozycja, nie działająca infrastruktura. Dla filmów potrzebny jest osobny zakres przygotowania. Aktualny limit YouTube trzeba sprawdzić na koncie projektu przed uruchomieniem; nie zakładamy go z historycznych opisów jednostek API. [Dokumentacja limitów YouTube](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits)

## Warianty do wyboru

### A. Kalkulator jako pierwsza publikacja — wariant niewybrany

- Opublikować kalkulator i stronę wprowadzającą z wyraźnym przejściem do niego.
- Zachować kod newsów i filmów do kolejnej aktualizacji; przed publikacją przygotować ich wyłączenie w produkcji, zarówno w UI, jak i endpointach.
- Samo ukrycie kart nie wyłącza publicznych endpointów; samo pominięcie kluczy zostawia użytkownikom komunikaty o niedostępnej konfiguracji. Potrzebne jest świadome zachowanie produkcyjnej wersji.
- Widgety TradingView dopuścić wyłącznie po sprawdzeniu; nie są niezbędne dla działania kalkulatora.

Ten wariant wymaga mniej przygotowań do pierwszego publicznego linku i odpowiada obecnemu zakresowi MVP.

### B. Kalkulator, newsy i filmy w pierwszej publikacji — WYBRANY

- Przed wdrożeniem wykonać osobno uzgodnione prace nad wspólnym cache i limitami.
- Zapewnić, że wejście użytkownika na stronę nie wymusza odpytywania dostawców.
- Sprawdzić aktualne darmowe plany, warunki publikacji i zachowanie po ich wyczerpaniu.
- Sprawdzić pełny interfejs z danymi, stan starszych danych i awarie na telefonie.
- Uzupełnić późniejszą listę zasobów AWS i kosztów o cache oraz zadania odświeżania.

Ten wariant zachowuje więcej obecnych funkcji w dniu premiery, lecz zwiększa zakres przygotowań przed pierwszym wdrożeniem.

## Decyzja

14 listopada 2026 użytkownik wybrał: „Publikujemy także newsy i filmy; najpierw przygotowujemy ich cache i limity”. Punkt 3 zakończony. Funkcje i endpointy zachowujemy; ich przygotowanie do AWS to następna praca, a nie część wykonanego przeglądu.

Przed uznaniem dodatków za gotowe do publikacji:

1. Zaimplementować i przetestować lokalnie wspólny stan newsów według NEWS_CACHE_DESIGN.md: format danych, metadane aktualności, trwałe rezerwacje prób i kontrolowane odświeżanie.
2. Przygotować analogiczny zakres dla filmów: stan, limit prób wyszukiwania, odświeżanie i maksymalny wiek danych przy awarii. Nie przenosić limitów newsów na YouTube.
3. Sprawdzić rzeczywiste darmowe plany i warunki dostawców oraz przetestować restart, równoległość, awarie zapisu i wyczerpanie limitu.
4. W osobnym etapie przygotować adapter przechowywania w AWS i harmonogram; publiczne endpointy mają czytać zapisane dane, bez wywoływania dostawców przy odwiedzinach.
5. Sprawdzić pełny interfejs z newsami, filmami i widgetami. Widgety TradingView pozostają elementem do weryfikacji, nie potwierdzoną gotowością.

Tworzenie zasobów nadal wymaga późniejszego zatwierdzenia konfiguracji i kosztów.

## Wykonane sprawdzenia

Przegląd news/routes.py, news/providers.py, videos/routes.py, klientów API frontendu i NEWS_CACHE_DESIGN.md. Uruchomiono osiem istniejących plików testów obejmujących cache, lokalne budżety, częściową awarię newsów, brak kluczy, starsze filmy przy błędzie oraz błędy dostawcy filmów: 24 testy przeszły. Pozostaje znane ostrzeżenie Starlette/TestClient dotyczące httpx.

Testy zastępują odpowiedzi dostawców; nie weryfikują limitów kont ani gotowości wielu instancji Lambda. Powtórzenie: w katalogu backend uruchomić `.venv/bin/python -m pytest -q tests/test_news_cache.py tests/test_news_provider_budget.py tests/test_news_partial_failure.py tests/test_news_missing_token.py tests/test_videos_cache.py tests/test_videos_fallback.py tests/test_videos_missing_key.py tests/test_videos_provider_errors.py`.
