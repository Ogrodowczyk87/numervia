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

Stan zaktualizowany 21 listopada 2026 przez porównanie roadmapy z kodem i raportami wykonanych sprawdzeń.

- **Punkty 1 i 3 — gotowe.** Pierwsza publikacja obejmuje kalkulator, newsy i filmy; szczegóły w [RELEASE_SCOPE.md](RELEASE_SCOPE.md).
- **Punkt 2 — gotowy lokalnie w Chrome.** Fizyczny telefon oraz pełny interfejs z prawdziwymi widgetami i treściami zewnętrznymi pozostają do sprawdzenia przed publikacją. Wyniki w [UI_QA.md](UI_QA.md).
- **Punkt 4 — kod gotowy lokalnie, warunki live otwarte.** Trwały stan, limity, kontrolowane odświeżanie oraz integracja API i frontendu dla newsów i filmów są gotowe lokalnie. Instrukcje: [NEWS_LOCAL_CACHE.md](NEWS_LOCAL_CACHE.md) i [VIDEO_LOCAL_CACHE.md](VIDEO_LOCAL_CACHE.md). Limit konta YouTube potwierdzono na zrzucie: Search Queries per day = 100, wykorzystanie 9. Wybrany budżet: 80 wyszukiwań/24 h, koszt 1 w tym koszyku; inicjalizacja stanu live pozostaje do wykonania.
- **Punkt 5 — w toku:** region eu-west-1 wybrany, wstępny szacunek w COSTS.md. Użytkownik potwierdził istniejący alarm budżetowy z wcześniejszych projektów; jego zakres i Billing pozostają niesprawdzone. Nie trzeba tworzyć duplikatu, jeśli alarm obejmuje Numervię.
- **Punkt 6 — w toku:** projekt CDK w infra, prywatny S3 frontendu oraz CloudFront z OAC, HTTPS i wyjściem FrontendUrl opisane i sprawdzone lokalnym synth. Obsługa podstron jest wydzielona do functions/frontend-routes.js i podłączona jako viewer-request. Lambda API jest opisana w osobnym backend-api.ts i podłączona do stacka, z originem CloudFront w ALLOWED_ORIGINS. Function URL jest opisany w backend-url.ts, a BackendUrl dodany do wyjść stacka. Prywatny ContentStateBucket i odczyt dwóch kluczy dla roli API są opisane w CDK. Czytnik S3 ma pierwszy test; podłączenie modeli i endpointów, zapis warunkowy i harmonogramy pozostają otwarte.
- **Punkty 7–10 — niewykonane.** Nie wykonywano bootstrap ani deploy; zasoby są tylko opisem w lokalnym szablonie.

Ostatnie sprawdzenia 21 listopada 2026: **250 testów backendu, Ruff, pip check, kompilacja infrastruktury TypeScript i lokalny synth przeszły.** Ostatni wynik frontendu: 81 testów, TypeScript i build poprawne; nie ponawiano ich przy tej zmianie backendu. Newsy i filmy demo sprawdzono także w Chrome przy 320 i 1440 px. Po przygotowaniu konfiguracji wykonano pełne testy i build. Chrome sprawdzono przy 320/375/768/1440 px z osobnym originem API i załadowanymi widgetami TradingView. Szczegóły w [AWS_APP_PREPARATION.md](AWS_APP_PREPARATION.md).

Następne proponowane zadanie: testy błędów i limitu 1 MiB czytnika S3, następnie walidacja modeli i podłączenie endpointów przez konfigurację. Warunki danych live wskazane w punkcie 4 nadal pozostają do zamknięcia przed ich publikacją. Otwarte pozostają również brak konfiguracji ESLint, znane ostrzeżenie Starlette/TestClient, dwa zgłoszenia moderate w zależnościach CDK oraz końcowe QA przed publikacją.

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

### 5. Konto AWS i koszty — W TOKU (15 listopada 2026)

- [ ] Sprawdzić plan konta, Free Tier, kredyty i bieżące opłaty. Użytkownik korzysta z IAM bez potwierdzonego dostępu do Billing; sprawdzenie pozostaje dla właściciela konta przed wdrożeniem. Nie zmieniano uprawnień.
- [x] Wybrać region i wstępnie oszacować koszty w `docs/COSTS.md`: Europe (Ireland), eu-west-1. Model 1000 wizyt i 3000 wywołań API/miesiąc: około 0,46 USD przed podatkami, bez dostępnych bezpłatnych pul; założenia wymagają pomiarów.
- [x] Uwzględnić Lambda, S3, CloudFront, logi, transfer oraz zasoby CDK bootstrap w modelu; ponowić wycenę po cdk synth.
- [x] Uwzględnić cache newsów i filmów, dwie funkcje odświeżające i dwa harmonogramy; model obejmuje pełny wybrany zakres.
- [ ] Sprawdzić zakres istniejącego alarmu budżetowego zgłoszonego przez użytkownika: czy obejmuje Numervię, jest aktywny i ma właściwego odbiorcę. Jeśli tak, wykorzystać go; nowy alert tworzyć tylko w razie potrzeby i po wyraźnym poleceniu. Samo istnienie alarmu nie potwierdza jego filtrów ani nie zatrzymuje wydatków.

Wynik: znane założenia kosztowe. Cel £0–£5 miesięcznie nie jest gwarancją ani twardym limitem; alerty same nie zatrzymują wydatków.

### 6. Przygotowanie infrastruktury w kodzie — W TOKU (15 listopada 2026)

- [x] Przygotować AWS CDK v2 w infra: package.json i lockfile, tsconfig.json, cdk.json, bin/numervia.ts oraz lib/numervia-stack.ts. Zależności są w infra; usunięto duplikat pakage.json. CDK CLI 2.1148.1 działa.
- [x] Opisać prywatny S3 frontendu: blokada dostępu publicznego, BucketOwnerEnforced, szyfrowanie S3-managed, wymuszenie HTTPS i RemovalPolicy.RETAIN.
- [x] Opisać CloudFront z OAC i podpisywaniem SigV4, odczytem S3 ograniczonym do tej dystrybucji, przekierowaniem na HTTPS, kompresją, PriceClass_100 i index.html jako domyślnym dokumentem.
- [x] Dodać CfnOutput FrontendUrl. Adres zostanie wyliczony przy przyszłym wdrożeniu; nie jest jeszcze działającą stroną.
- [x] Przygotować requirements-lambda.lock.txt i lokalną paczkę backend/build/lambda w kontenerze AWS Python 3.14 dla Linux x86_64. Użytkownik potwierdził import handlera i symulację health payload v2: HTTP 200, {"status":"ok"}. Paczka build jest ignorowana przez Git.
- [x] Opisać Lambda API w osobnym infra/lib/backend-api.ts i podłączyć do stacka: Python 3.14, x86_64, app.handler.handler, paczka z fromAsset i dokładny origin CloudFront dla CORS w FastAPI.
- [x] Dodać Function URL w osobnym backend-url.ts oraz output BackendUrl. Sprawdzono AuthType NONE, uprawnienia InvokeFunctionUrl z FunctionUrlAuthType NONE i InvokeFunction z InvokedViaFunctionUrl=true, output oraz brak drugiej konfiguracji CORS. Nie wdrożono publicznego API.
- [x] Opisać prywatny ContentStateBucket w osobnym content-state.ts i podłączyć do stacka: blokada dostępu publicznego, szyfrowanie S3-managed, HTTPS, RETAIN.
- [x] Opisać w content-state-access.ts odczyt API: tylko s3:GetObject dla news/state.json i videos/state.json, bez zapisu, usuwania i listowania; sprawdzono lokalny szablon IAM.
- [x] Dodać Boto3 do pyproject.toml i obu plików lock; wersje zgodne z lokalnym środowiskiem, pip check bez konfliktów.
- [x] Dodać s3_reader.py: odczyt bajtów, limit 1 MiB, zamknięcie strumienia i wspólny wyjątek błędu. Pierwszy test sprawdza treść, argumenty i zamknięcie strumienia bez AWS.
- [ ] Dodać testy awarii S3, braku pliku, błędu strumienia i przekroczenia limitu; zweryfikować czytnik przed integracją.
- [ ] Dodać adaptery modeli NewsState/VideoState z pełną walidacją oraz wybór magazynu lokalnego/S3 w endpointach; przekazać bucket i klucze z CDK. Obecne API nadal czyta lokalne pliki.
- [ ] Przygotować warunkowy zapis S3 (ETag), trwałe rezerwacje prób i obsługę konfliktów bez resetowania budżetów; testy współbieżności i awarii.
- [ ] Dodać osobne funkcje odświeżające i harmonogramy oraz ich ograniczone uprawnienia i bezpieczną konfigurację kluczy dostawców; odczyt publicznego API pozostaje bez wywołań dostawców.
- [ ] Zapisać powtarzalne budowanie paczki Lambda i przebudować ją po dodaniu Boto3 oraz adapterów; ponowić testy w kontenerze AWS. Dotychczasowa paczka build nie zawiera nowych zmian.
- [x] Ustawić parametry Lambda API: 512 MB, timeout 10 s, reserved concurrency 2 i retencja logów 7 dni, RemovalPolicy.RETAIN. Sprawdzono w lokalnym synth. Parametry przyszłych funkcji odświeżających pozostają do ustalenia.
- [x] Obsłużyć bezpośrednie wejścia na /mortgage-calculator, /market-data i /tech, także z końcowym ukośnikiem, przez osobny plik CloudFront Function. Sprawdzono 12 przypadków tras i zachowanie query string.
- [x] Przygotować politykę cache CloudFront w osobnym infra/lib/frontend-cache.ts i podłączyć ją do dystrybucji: MinTTL=0, DefaultTTL=0, MaxTTL=31536000; Gzip i Brotli włączone. Kompilacja, synth i sprawdzenie powiązania w szablonie przeszły 21 listopada 2026.
- [ ] Przy publikacji ustawić metadane Cache-Control obiektów S3: index.html = no-cache, pliki assets z nazwami zawierającymi hash = public, max-age=31536000, immutable. Sprawdzić nagłówki odpowiedzi po wdrożeniu; polityka CloudFront sama ich nie ustawia.
- [x] Wykonać kompilację TypeScript i lokalne cdk synth --no-lookups dla aktualnego zakresu frontendu. Wynik zawiera AWS::S3::Bucket, AWS::S3::BucketPolicy, AWS::CloudFront::OriginAccessControl oraz AWS::CloudFront::Distribution. Sprawdzono blokadę publicznego dostępu, Deny bez HTTPS i uprawnienie GetObject tylko dla wskazanej dystrybucji.
- [ ] Po dodaniu pozostałych zasobów ponownie wykonać synth, przejrzeć cały szablon, uprawnienia i uaktualnić wycenę. Ocenić dwa zgłoszenia moderate dotyczące zależności CDK; nie używać audit fix --force bez przeglądu zmian.

Docelowy wynik: kompletna lista zasobów gotowa do przeglądu. Aktualnie przygotowano frontend i Lambda API z Function URL; bez bootstrap ani deploy. RemovalPolicy.RETAIN oznacza, że po przyszłym usunięciu stacka bucket pozostanie i może nadal generować koszty przechowywania.

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

| 2026-11-15 | 5. Region i model kosztów | Wybrano eu-west-1; publiczne regionalne stawki AWS i model 1000/10 000/100 000 wizyt zapisano w COSTS.md. Bez zasobów, zmian IAM i dostępu do Billing. | Plan konta, Free Tier/kredyty i alerty budżetowe wymagają potwierdzenia przed wdrożeniem. |

## Aktualizacja infrastruktury — 15 listopada 2026

Użytkownik przygotował kod S3 i CloudFront oraz uruchomił tsc/synth. Pokazany wynik i lokalny szablon potwierdzają cztery typy zasobów frontendowych oraz FrontendUrl. Odhaczono tylko wykonany zakres; podstrony React, backend i stan dodatków w CDK, harmonogramy oraz końcowy przegląd pozostają otwarte. Nie uruchamiano dodatkowego synth przy tej aktualizacji dokumentacji. Użytkownik zgłosił istniejący alarm budżetowy; zakres alarmu pozostaje do sprawdzenia. Bez zasobów AWS, zmian uprawnień, commita i pushu.

Obsługa podstron: dodano osobny plik infra/functions/frontend-routes.js i powiązanie viewer-request. Kompilacja TypeScript, lokalny synth i 12 przypadków tras przeszły; sprawdzono także powiązanie w szablonie. Szablon zawiera dodatkowo AWS::CloudFront::Function. Nie wdrażano zasobów AWS.

## Cache frontendu — 21 listopada 2026

Dodano osobny moduł frontend-cache.ts i podłączono politykę do dystrybucji. Ponownie wykonano tsc i cdk synth --no-lookups; sprawdzono wartości TTL oraz referencję CachePolicyId. Nagłówki Cache-Control plików S3 pozostają do ustawienia przy publikacji. Punkt 6 nadal w toku; Lambda, stan dodatków i harmonogramy nie są jeszcze opisane. Bez bootstrap i deploy.

## Paczka backendu i Lambda w CDK — 21 listopada 2026

W ramach nauki Dockera przygotowano paczkę Linux x86_64 z przypiętymi bibliotekami i kodem app, bez lokalnego .env i stanu .local. Użytkownik potwierdził import handlera oraz lokalny health check payload v2 (200). Dodano backend-api.ts i połączenie ze stackiem. Kompilacja TypeScript, synth i kontrole runtime, handlera, pamięci, timeoutu, współbieżności, originu CloudFront oraz retencji logów przeszły. Brak Function URL i brak wdrożenia AWS. Przygotowanie paczki jest na razie ręczne; przed powtarzalnymi wdrożeniami należy zapisać proces budowania.

## Function URL — 21 listopada 2026

Dodano osobny moduł backend-url.ts, połączenie w stacku i output BackendUrl. TypeScript, lokalny synth i kontrola obu uprawnień oraz ich warunków przeszły; CORS pozostaje w FastAPI. Adres będzie publiczny dopiero po przyszłym zatwierdzonym wdrożeniu. Wspólny stan dodatków, harmonogramy i pozostałe warunki publikacji nadal otwarte. Bez bootstrap i deploy.

## Początek integracji stanu S3 — 21 listopada 2026

Dodano bucket stanu, ograniczony odczyt roli API, Boto3 z przypiętymi zależnościami, czytnik bajtów S3 i pierwszy test bez AWS. Weryfikacja: 250 testów backendu, Ruff, pip check, kompilacja TypeScript i lokalny synth poprawne. Znane ostrzeżenie Starlette pozostaje. Nie oznacza to gotowego cache S3: modele, wybór magazynu, zapis warunkowy i harmonogramy nadal do wykonania. Nie wykonywano bootstrap/deploy ani zapytań do dostawców.
