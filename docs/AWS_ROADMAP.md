# Numervia — plan pierwszego wdrożenia na AWS

Data utworzenia: 14 listopada 2026.

Cel: opublikować pierwszą działającą wersję Numervii, a następnie regularnie ją aktualizować pod tym samym adresem.

## Jak korzystać z planu

- Przed pracą przeczytać `AGENTS.md`, `PROJECT_PLAN.md` i ten dokument oraz sprawdzić stan repozytorium.
- Realizować wyłącznie zadanie uzgodnione z użytkownikiem. Ten plan nie upoważnia do automatycznego przechodzenia do kolejnych punktów.
- Odhaczać krok dopiero po sprawdzeniu wyniku; zapisywać datę, wykonane sprawdzenia i pozostałe problemy.
- Tworzenie zasobów AWS, wdrożenie, zmiana uprawnień, usuwanie zasobów, commit i push wymagają wyraźnego polecenia użytkownika.
- Nie zapisywać sekretów ani danych konta w dokumentacji. Nie korzystać z płatnych zewnętrznych API.

## Bieżący stan

Stan sprawdzony ponownie 14 listopada 2026 przez porównanie roadmapy z kodem i raportami wykonanych sprawdzeń.

- **Punkty 1 i 3 — gotowe.** Pierwsza publikacja obejmuje kalkulator, newsy i filmy; szczegóły w [RELEASE_SCOPE.md](RELEASE_SCOPE.md).
- **Punkt 2 — gotowy lokalnie w Chrome.** Fizyczny telefon oraz pełny interfejs z prawdziwymi widgetami i treściami zewnętrznymi pozostają do sprawdzenia przed publikacją. Wyniki w [UI_QA.md](UI_QA.md).
- **Punkt 4 — kod gotowy lokalnie, warunki live otwarte.** Trwały stan, limity, kontrolowane odświeżanie oraz integracja API i frontendu dla newsów i filmów są gotowe lokalnie. Instrukcje: [NEWS_LOCAL_CACHE.md](NEWS_LOCAL_CACHE.md) i [VIDEO_LOCAL_CACHE.md](VIDEO_LOCAL_CACHE.md). Limit konta YouTube potwierdzono na zrzucie: Search Queries per day = 100, wykorzystanie 9. Wybrany budżet: 80 wyszukiwań/24 h, koszt 1 w tym koszyku; inicjalizacja stanu live pozostaje do wykonania.
- **Punkty 5–10 — niewykonane.** Brak wdrożenia AWS; adapter Lambda jest zaimplementowany, ale infra nadal zawiera pliki zastępcze i nie wykonywano wdrożenia.

Ostatnie wykonane sprawdzenia: **249 testów backendu i 81 testów frontendu przeszły; Ruff, TypeScript i build poprawne.** Newsy i filmy demo sprawdzono także w Chrome przy 320 i 1440 px. Po przygotowaniu konfiguracji wykonano pełne testy i build. Chrome sprawdzono przy 320/375/768/1440 px z osobnym originem API i załadowanymi widgetami TradingView. Szczegóły w [AWS_APP_PREPARATION.md](AWS_APP_PREPARATION.md).

Następne proponowane niezależne zadanie: punkt 5, sprawdzenie konta AWS i oszacowanie kosztów, bez tworzenia zasobów. Warunki danych live wskazane w punkcie 4 nadal pozostają do zamknięcia przed ich publikacją. Otwarte pozostają również brak konfiguracji ESLint, znane ostrzeżenie Starlette/TestClient i końcowe QA przed publikacją.

## Kolejność prac

### 1. Sprawdzenie obecnej aplikacji — GOTOWE (14 listopada 2026)

- [x] Uruchomić istniejące testy backendu i kontrolę Ruff.
- [x] Uruchomić istniejące testy frontendu, sprawdzanie TypeScript i build; sprawdzić dostępność konfiguracji ESLint.
- [x] Zapisać wyniki i listę problemów wymagających poprawy przed publikacją.

Wyniki z 14 listopada 2026 (komendy uruchomił użytkownik i przekazał ich wyniki):

- Backend: `python -m pytest` — 143 testy przeszły; `python -m ruff check .` — All checks passed.
- Frontend: `npm test` — 60 testów w 32 plikach przeszło; `npm run build` — TypeScript i build Vite przeszły.
- W przekazanym wyniku buildu brak ostrzeżenia o paczce JS przekraczającej 500 kB. Główna paczka: 245,02 kB; paczka strony kalkulatora: 375,36 kB (przed gzip). Nie zamyka to ręcznej weryfikacji wykresu z LL-047.
- Kontrola repozytorium: ESLint i pluginy są w zależnościach, ale brak pliku konfiguracji ESLint oraz skryptu `lint` w `frontend/package.json`. Lint frontendu nie został wykonany; przygotowanie konfiguracji pozostaje osobnym zadaniem przed publikacją.

Uwagi do dalszej pracy:

- Ostrzeżenie Starlette o wycofywaniu `httpx` w TestClient — sprawdzić zgodność zależności testowych przed ich zmianą.
- Vitest wyświetla sugestię optymalizacji środowiska jsdom; nie jest to błąd testów. Bez zmiany izolacji testów na tym etapie.
- Grafika tła ma 1 448,87 kB, logo 262,33 kB. Ocenić wpływ na ładowanie strony podczas punktu 2; rozważyć optymalizację obrazów.
- Przejście testów i buildu nie potwierdza jeszcze wyglądu na telefonie ani gotowości konfiguracji AWS.

Wynik: wiemy, co działa, a co wymaga naprawy. Sam audyt nie oznacza zgody na wszystkie wykryte poprawki.

### 2. Sprawdzenie wyglądu i obsługi — GOTOWE LOKALNIE (14 listopada 2026)

- [x] Sprawdzić układ przy szerokościach telefonu i komputera: 320, 375, 768 i 1440 px w Chrome.
- [x] Sprawdzić formularz, wyniki, wykres, tabelę, menu, stany ładowania i błędy.
- [x] Sprawdzić obsługę klawiaturą, widoczny fokus i przewijanie tabeli.
- [x] Ocenić ostrzeżenie o rozmiarze paczki z Recharts (LL-047) i zapisać decyzję.
- [x] Poprawić wykryte problemy i zapisać wyniki QA dla LL-048 w [UI_QA.md](UI_QA.md).

Poprawiono przewijanie całej strony przy 320 px, układ nawigacji przy 1440 px i przycięte kwoty na osi wykresu. 60 testów frontendu, TypeScript i build przeszły. Przed publikacją sprawdzić fizyczny telefon i pełną stronę z zewnętrznymi treściami; zewnętrzne żądania podczas QA były blokowane.

Wynik: pierwsza wersja jest czytelna i nadaje się do pokazania na telefonie oraz komputerze.

### 3. Ustalenie zakresu pierwszej publikacji — GOTOWE (14 listopada 2026)

- [x] Potwierdzić kalkulator hipoteczny jako podstawę pierwszej wersji.
- [x] Sprawdzić gotowość newsów i filmów, w tym limity zapisane w kodzie, cache i zachowanie przy błędach. Wyniki w [RELEASE_SCOPE.md](RELEASE_SCOPE.md); rzeczywiste plany dostawców wymagają weryfikacji przed publikacją dodatków.
- [x] Uzgodnić, czy newsy i filmy publikujemy teraz, czy odkładamy do następnej aktualizacji. Użytkownik wybrał publikację obu dodatków po przygotowaniu wspólnego cache i limitów.

Wynik: jawna lista funkcji pierwszej publikacji. Bez rozpoczynania nowych modułów.

### 4. Przygotowanie aplikacji do AWS — KOD GOTOWY, WARUNKI LIVE OTWARTE

- [x] Zaimplementować lokalnie trwały stan newsów, metadane aktualności, budżety prób i kontrolowane odświeżanie według NEWS_CACHE_DESIGN.md, z testami restartów i awarii. Wyniki: [NEWS_LOCAL_CACHE.md](NEWS_LOCAL_CACHE.md).
- [x] Podłączyć endpoint i frontend newsów do trwałego magazynu; pokazać daty, oznaczenie demo i starszych danych oraz usuwać wygasłe karty. Odczyt API nie wywołuje dostawców.
- [x] Przygotować lokalną logikę wspólnego cache i limitów filmów: trwałe rezerwacje każdego wyszukiwania, maksymalny wiek 24 h, odświeżanie oraz testy restartów, współbieżności i awarii. Wyniki: [VIDEO_LOCAL_CACHE.md](VIDEO_LOCAL_CACHE.md).
- [x] Podłączyć endpoint i frontend filmów do trwałego magazynu; pokazać datę i demo, usuwać wygasłe karty oraz odtwarzacz. Odczyt API nie wywołuje YouTube.
- [x] Sprawdzić lokalne zmiany w newsach i filmach: 239 testów backendu, 73 frontendu, Ruff, TypeScript i build poprawne; demo w Chrome przy 320/1440 px sprawdzone.
- [x] Potwierdzić rzeczywisty limit projektu YouTube i koszt search.list: zrzut użytkownika z 14 listopada 2026 pokazuje Search Queries per day = 100, wykorzystanie 9; koszt 1 w koszyku Search Queries zgodnie z dokumentacją. Wybrano budżet Numervii 80 wyszukiwań w ostatnich 24 h przy planie 12/dobę.
- [ ] Zainicjalizować osobny trwały stan live filmów z daily_quota=100, cost_per_search=1 i request_budget=80 po potwierdzeniu odnowienia limitu lub 24 h bez innych wywołań. Nie zerować istniejących rezerwacji; samo potwierdzenie limitu nie potwierdza pustego licznika.

  Status na 14 listopada 2026: użytkownik odpowiedział „Nie lub nie wiem” na pytanie o reset/24 h bez wywołań. Inicjalizacja odłożona; plik live nie został utworzony, pobieranie live pozostaje wyłączone. Można niezależnie przygotować adapter Lambda po uzgodnieniu tego osobnego zadania.
- [x] Potwierdzić plany kont: użytkownik potwierdził Free dla Marketaux i Currents; YouTube potwierdzony zrzutem. Przejrzano aktualne cenniki i warunki publiczne, dodano link atrybucji Currents. Ustalenia: [AWS_APP_PREPARATION.md](AWS_APP_PREPARATION.md).
- [x] Sprawdzić interfejs z danymi demo oraz rzeczywiście załadowanymi widgetami TradingView w Chrome przy 320/375/768/1440 px; brak przewijania poziomego strony.
- [ ] Wyjaśnić zakres publicznego użycia nagłówków, obrazów i cache 24 h w planach newsów przed uruchomieniem danych live. Przegląd publicznych źródeł nie potwierdza dodatkowych praw wydawców ani nieudostępnionych warunków kont.
- [x] Przygotować adapter Mangum uruchamiający FastAPI w Lambda: app.handler.handler, testy payload v2 dla health, walidacji i obliczeń, zgodność z Pythonem 3.14.
- [x] Dodać VITE_API_BASE_URL dla wszystkich klientów API. Proxy Vite pozostaje opcją lokalną; produkcyjny build korzysta ze skonfigurowanego originu backendu.
- [x] Przygotować CORS: ALLOWED_ORIGINS, dokładne originy, bez wildcard i credentials; testy preflight oraz odrzuconych originów. Prawdziwy origin CloudFront zostanie ustawiony po utworzeniu infrastruktury.
- [x] Opisać konfigurację środowiska w .env.example, README i AWS_APP_PREPARATION.md; nie dodano sekretów ani kluczy do frontendu.
- [x] Sprawdzić działanie aplikacji po zmianach: 249 testów backendu, 81 frontendu, Ruff, TypeScript i build poprawne; rzeczywisty przepływ przeglądarka → osobny backend sprawdzony lokalnie.

Docelowy wynik: kod przygotowany do wdrożenia. Kod punktu 4 ukończono lokalnie. Pozostały dwa warunki danych live: pierwsza inicjalizacja licznika filmów oraz wyjaśnienie zakresu publikacji newsów. Demo działa; całości nie oznaczono jako gotowej do publikacji live. Zasoby AWS jeszcze nie powstają.

### 5. Konto AWS i koszty

- [ ] Sprawdzić plan konta, aktualne warunki Free Tier i bieżące opłaty.
- [ ] Wybrać region i oszacować koszty w `docs/COSTS.md`.
- [ ] Uwzględnić Lambda, S3, CloudFront, logi, transfer oraz zasoby tworzone przez CDK bootstrap.
- [ ] Uwzględnić także trwały cache newsów i filmów oraz zadania ich odświeżania; ponownie oszacować koszt pełnej wybranej wersji.
- [ ] Po wyraźnym poleceniu skonfigurować alerty budżetowe przed upublicznieniem API.

Wynik: znane założenia kosztowe. Cel £0–£5 miesięcznie nie jest gwarancją ani twardym limitem; alerty same nie zatrzymują wydatków.

### 6. Przygotowanie infrastruktury w kodzie

- [ ] Przygotować AWS CDK v2 w katalogu `infra/`.
- [ ] Opisać Lambda z Function URL, prywatny S3 oraz CloudFront z OAC i HTTPS.
- [ ] Przygotować uzgodnione przechowywanie wspólnego stanu oraz harmonogramy odświeżania dodatków; oddzielić odczyt publicznego API od pobierania danych dostawców.
- [ ] Ustawić timeout, pamięć, limit współbieżności i retencję logów.
- [ ] Uwzględnić obsługę adresów aplikacji i pamięci podręcznej frontendu.
- [ ] Wykonać lokalne `cdk synth` i przejrzeć wygenerowaną konfigurację.

Wynik: konkretna lista zasobów gotowa do przeglądu; bez wykonywania bootstrap ani deploy.

### 7. Zatwierdzenie wdrożenia

- [ ] Pokazać użytkownikowi zasoby, uprawnienia, szacunek kosztów i dokładne komendy.
- [ ] Uwzględnić dodatkowe zasoby CDK bootstrap.
- [ ] Uzyskać wyraźne polecenie wykonania wdrożenia.

Wynik: zgoda dotycząca konkretnej konfiguracji, zgodnie z `AGENTS.md`.

### 8. Pierwsze wdrożenie

- [ ] Wykonać zatwierdzony bootstrap i deploy.
- [ ] Opublikować backend i zbudować frontend z produkcyjną konfiguracją API.
- [ ] Wgrać frontend i sprawdzić ustawienia CORS.
- [ ] Zapisać publiczny adres aplikacji w dokumentacji.

Wynik: Numervia dostępna pod publicznym adresem HTTPS.

### 9. Sprawdzenie publicznej wersji

- [ ] Sprawdzić health endpoint oraz pełne obliczenie kredytu.
- [ ] Sprawdzić telefon, wykres, tabelę, odświeżanie strony i błędy API.
- [ ] Sprawdzić HTTPS, CORS i funkcje dodatkowe dopuszczone do publikacji.
- [ ] Sprawdzić logi oraz dostępne dane o naliczanych kosztach; uwzględnić opóźnienie raportów billingowych.

Wynik: sprawdzona pierwsza wersja i zapisana lista ewentualnych usterek.

### 10. Proces kolejnych aktualizacji

- [ ] Uzupełnić README i `docs/DEPLOYMENT.md` o działające instrukcje.
- [ ] Opisać proces: zmiana lokalna → sprawdzenie → publikacja → kontrola strony.
- [ ] Opisać aktualizowanie pamięci podręcznej CloudFront oraz powrót do poprzedniej wersji.
- [ ] Automatyzację publikacji pozostawić jako osobno uzgadniane zadanie.

Wynik: powtarzalny sposób publikowania zmian pod tym samym adresem.

## Dziennik realizacji

| Data | Krok | Wynik i sprawdzenia | Pozostałe problemy |
| --- | --- | --- | --- |
| 2026-11-14 | Utworzenie planu | Zapisano kolejność prac; bez wdrożenia i zmian w aplikacji. | Punkty 1–10 oczekują realizacji. |
| 2026-11-14 | 1. Sprawdzenie aplikacji | Według wyników użytkownika: 143 testy backendu i 60 testów frontendu przeszły; Ruff, TypeScript i build poprawne. Sprawdzono dostępność ESLint w repozytorium. | Brak konfiguracji lint frontendu; ostrzeżenie zależności testowej; ocena rozmiaru obrazów i ręczne QA pozostają do wykonania. |
| 2026-11-14 | 2. Wygląd i obsługa | Lokalne QA w Chrome, trzy poprawki; 60 testów, TypeScript i build poprawne. Szczegóły w UI_QA.md. | Fizyczny telefon, załadowane widgety i ewentualna optymalizacja obrazów pozostają do sprawdzenia przed publikacją. |
| 2026-11-14 | 3. Zakres publikacji | Użytkownik wybrał kalkulator, newsy i filmy. Przegląd kodu i 24 testy dodatków poprawne; RELEASE_SCOPE.md zawiera warunki publikacji. | Wspólny trwały cache, limity i odświeżanie dodatków do przygotowania w punkcie 4; dodatkowe zasoby i koszty do uwzględnienia w punktach 5–6. |
| 2026-11-14 | 4. Newsy i filmy lokalnie | Trwałe magazyny i rezerwacje, osobne CLI odświeżające, API wyłącznie odczytujące, metadane i wygaszanie we frontendzie. Ostatnie sprawdzenia: 239 testów backendu, 73 frontendu, Ruff, TypeScript i build poprawne; demo w Chrome 320/1440 px sprawdzone. | Rzeczywiste limity i warunki kont, pełne QA z treściami zewnętrznymi oraz przygotowanie AWS pozostają otwarte. |
| 2026-11-14 | Ponowny przegląd roadmapy | Porównano kod i raporty z checklistą; odhaczono ukończone części punktu 4 i poprawiono nieaktualny opis bieżącego stanu. Bez zmian w kodzie aplikacji i bez ponawiania testów. | Punkty 5–10 niewykonane. Historyczne wpisy powyżej opisują stan w chwili wykonania danego kroku. |

| 2026-11-14 | Limit YouTube potwierdzony | Zrzut panelu: Search Queries per day 100, wykorzystanie 9 (9%). Wybrany budżet Numervii 80/24 h; planowane 12 wyszukiwań/dobę. | Stan live jeszcze nieutworzony; przed pierwszą inicjalizacją potwierdzić odnowienie limitu lub 24 h bez innych wywołań. Bez zapytań live. |

| 2026-11-14 | 4. Pozostałe przygotowanie kodu | Mangum, produkcyjny adres API i CORS, konfiguracja środowiska, prostsze błędy kalkulatora, atrybucja Currents. 249 testów backendu, 81 frontendu, Ruff, TypeScript i build poprawne; Chrome z osobnym API i prawdziwymi widgetami TradingView sprawdzony. | Live filmów czeka na potwierdzenie resetu/24 h bez wywołań; zakres publikacji newsów do wyjaśnienia. Bez AWS i live refresh. |

Uwaga QA punktu 4: z widgetami TradingView występuje ostrzeżenie ResizeObserver (w porównaniu 9 z widgetami, 0 bez). Układ i kalkulator działają; szczegóły oraz ograniczenia w AWS_APP_PREPARATION.md. Nie wyciszano ostrzeżenia.
