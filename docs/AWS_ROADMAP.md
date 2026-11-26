# Numervia — plan pierwszego wdrożenia na AWS

- Cel: opublikować kalkulator, newsy i filmy, a następnie aktualizować aplikację pod tym samym adresem.
- Prowadzić wyłącznie listę punktów i ich statusów, bez dziennika realizacji.
- Odhaczać zadania po sprawdzeniu wyniku; zachowywać przy punktach istotne ograniczenia i wyniki weryfikacji.
- Przed pracą przeczytać `AGENTS.md`, `PROJECT_PLAN.md` i sprawdzić stan repozytorium.
- Realizować tylko uzgodnione zadanie. Kod aplikacji użytkownik edytuje sam z pomocą asystenta, chyba że wyraźnie zleci zmianę.
- Tworzenie zasobów AWS, wdrożenie, zmiany uprawnień, usuwanie zasobów, commit i push wymagają wyraźnego polecenia.
- Chronić sekrety; nie korzystać z płatnych zewnętrznych API.
- Obecnie nie wykonano bootstrap ani deploy; zasoby AWS są opisane lokalnie.

### 1. Sprawdzenie obecnej aplikacji — GOTOWE (14 listopada 2026)

- [x] Uruchomić istniejące testy backendu i kontrolę Ruff.

- [x] Uruchomić istniejące testy frontendu, sprawdzanie TypeScript i build; sprawdzić dostępność konfiguracji ESLint.

- [x] Zapisać wyniki i listę problemów wymagających poprawy przed publikacją.

- [ ] Skonfigurować i uruchomić ESLint frontendu.

- [ ] Sprawdzić zgodność zależności testowych Starlette/httpx przed usunięciem ostrzeżenia TestClient.

### 2. Sprawdzenie wyglądu i obsługi — GOTOWE LOKALNIE (14 listopada 2026)

- [x] Sprawdzić układ przy szerokościach telefonu i komputera: 320, 375, 768 i 1440 px w Chrome.

- [x] Sprawdzić formularz, wyniki, wykres, tabelę, menu, stany ładowania i błędy.

- [x] Sprawdzić obsługę klawiaturą, widoczny fokus i przewijanie tabeli.

- [ ] Wykonać końcowe QA na fizycznym telefonie oraz z załadowanymi treściami i widgetami zewnętrznymi; sprawdzić również ostrzeżenie ResizeObserver.

- [ ] Ocenić wpływ rozmiaru tła i logo na czas ładowania strony.

- [x] Ocenić ostrzeżenie o rozmiarze paczki z Recharts (LL-047) i zapisać decyzję.

- [x] Poprawić wykryte problemy i zapisać wyniki QA dla LL-048 w [UI_QA.md](UI_QA.md).

### 3. Ustalenie zakresu pierwszej publikacji — GOTOWE (14 listopada 2026)

- [x] Potwierdzić kalkulator hipoteczny jako podstawę pierwszej wersji.

- [x] Sprawdzić gotowość newsów i filmów, w tym limity zapisane w kodzie, cache i zachowanie przy błędach. Wyniki w [RELEASE_SCOPE.md](RELEASE_SCOPE.md); rzeczywiste plany dostawców wymagają weryfikacji przed publikacją dodatków.

- [x] Uzgodnić, czy newsy i filmy publikujemy teraz, czy odkładamy do następnej aktualizacji. Użytkownik wybrał publikację obu dodatków po przygotowaniu wspólnego cache i limitów.

### 4. Przygotowanie aplikacji do AWS — KOD GOTOWY, WARUNKI LIVE OTWARTE

- [x] Przygotować osobny lokalny podgląd z jednorazowo pobranych prawdziwych nagłówków, źródeł i linków; zachować datę pobrania i oznaczenie archiwalnego podglądu. Pobieranie wyłącznie przez trwały licznik prób i po sprawdzeniu dostępnego budżetu. Nie pobierać pełnych artykułów. Czas przechowywania treści i obrazów uzgodnić z warunkami dostawców; nie zakładać bezterminowego cache.

- [ ] Przed publikacją wyłączyć lokalny podgląd archiwalny i zastąpić syntetyczne karty w domyślnym widoku rzeczywistym, kontrolowanie odświeżanym cache. Demo pozostawić wyłącznie jako jawnie wybraną opcję developerską/testową; brak danych live ma pokazywać uczciwy stan niedostępności. Nie wyłączać produkcyjnego limitu wieku 24 h.

- [x] Zaimplementować lokalnie trwały stan newsów, metadane aktualności, budżety prób i kontrolowane odświeżanie według NEWS_CACHE_DESIGN.md, z testami restartów i awarii. Wyniki: [NEWS_LOCAL_CACHE.md](NEWS_LOCAL_CACHE.md).

- [x] Podłączyć endpoint i frontend newsów do trwałego magazynu; pokazać daty, oznaczenie demo i starszych danych oraz usuwać wygasłe karty. Odczyt API nie wywołuje dostawców.

- [x] Przygotować lokalną logikę wspólnego cache i limitów filmów: trwałe rezerwacje każdego wyszukiwania, maksymalny wiek 24 h, odświeżanie oraz testy restartów, współbieżności i awarii. Wyniki: [VIDEO_LOCAL_CACHE.md](VIDEO_LOCAL_CACHE.md).

- [x] Podłączyć endpoint i frontend filmów do trwałego magazynu; pokazać datę i demo, usuwać wygasłe karty oraz odtwarzacz. Odczyt API nie wywołuje YouTube.

- [x] Sprawdzić lokalne zmiany w newsach i filmach: 239 testów backendu, 73 frontendu, Ruff, TypeScript i build poprawne; demo w Chrome przy 320/1440 px sprawdzone.

- [x] Potwierdzić rzeczywisty limit projektu YouTube i koszt search.list: zrzut użytkownika z 14 listopada 2026 pokazuje Search Queries per day = 100, wykorzystanie 9; koszt 1 w koszyku Search Queries zgodnie z dokumentacją. Wybrano budżet Numervii 80 wyszukiwań w ostatnich 24 h przy planie 12/dobę.

- [ ] Zainicjalizować osobny trwały stan live filmów z daily_quota=100, cost_per_search=1 i request_budget=80 po potwierdzeniu odnowienia limitu lub 24 h bez innych wywołań. Nie zerować istniejących rezerwacji; samo potwierdzenie limitu nie potwierdza pustego licznika.

- [x] Potwierdzić plany kont: użytkownik potwierdził Free dla Marketaux i Currents; YouTube potwierdzony zrzutem. Przejrzano aktualne cenniki i warunki publiczne, dodano link atrybucji Currents. Ustalenia: [AWS_APP_PREPARATION.md](AWS_APP_PREPARATION.md).

- [x] Sprawdzić interfejs z danymi demo oraz rzeczywiście załadowanymi widgetami TradingView w Chrome przy 320/375/768/1440 px; brak przewijania poziomego strony.

- [ ] Wyjaśnić zakres publicznego użycia nagłówków, obrazów i cache 24 h w planach newsów przed uruchomieniem danych live. Przegląd publicznych źródeł nie potwierdza dodatkowych praw wydawców ani nieudostępnionych warunków kont.

- [x] Przygotować adapter Mangum uruchamiający FastAPI w Lambda: app.handler.handler, testy payload v2 dla health, walidacji i obliczeń, zgodność z Pythonem 3.14.

- [x] Dodać VITE_API_BASE_URL dla wszystkich klientów API. Proxy Vite pozostaje opcją lokalną; produkcyjny build korzysta ze skonfigurowanego originu backendu.

- [x] Przygotować CORS: ALLOWED_ORIGINS, dokładne originy, bez wildcard i credentials; testy preflight oraz odrzuconych originów. Prawdziwy origin CloudFront zostanie ustawiony po utworzeniu infrastruktury.

- [x] Opisać konfigurację środowiska w .env.example, README i AWS_APP_PREPARATION.md; nie dodano sekretów ani kluczy do frontendu.

- [x] Sprawdzić działanie aplikacji po zmianach: 249 testów backendu, 81 frontendu, Ruff, TypeScript i build poprawne; rzeczywisty przepływ przeglądarka → osobny backend sprawdzony lokalnie.

### 5. Konto AWS i koszty — W TOKU (15 listopada 2026)

- [ ] Sprawdzić plan konta, Free Tier, kredyty i bieżące opłaty. Użytkownik korzysta z IAM bez potwierdzonego dostępu do Billing; sprawdzenie pozostaje dla właściciela konta przed wdrożeniem. Nie zmieniano uprawnień.

- [x] Wybrać region i wstępnie oszacować koszty w `docs/COSTS.md`: Europe (Ireland), eu-west-1. Model 1000 wizyt i 3000 wywołań API/miesiąc: około 0,46 USD przed podatkami, bez dostępnych bezpłatnych pul; założenia wymagają pomiarów.

- [x] Uwzględnić Lambda, S3, CloudFront, logi, transfer oraz zasoby CDK bootstrap w modelu; ponowić wycenę po cdk synth.

- [x] Uwzględnić cache newsów i filmów, dwie funkcje odświeżające i dwa harmonogramy; model obejmuje pełny wybrany zakres.

- [ ] Sprawdzić zakres istniejącego alarmu budżetowego zgłoszonego przez użytkownika: czy obejmuje Numervię, jest aktywny i ma właściwego odbiorcę. Jeśli tak, wykorzystać go; nowy alert tworzyć tylko w razie potrzeby i po wyraźnym poleceniu. Samo istnienie alarmu nie potwierdza jego filtrów ani nie zatrzymuje wydatków.

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

- [x] Dodać content/s3_reader.py: odczyt bajtów, limit 1 MiB, zamknięcie strumienia i wspólny wyjątek błędu. Pierwszy test sprawdza treść, argumenty i zamknięcie strumienia bez AWS.

- [x] Sprawdzić czytnik S3: 7 przypadków obejmuje poprawny odczyt, brak pliku, odmowę dostępu, granicę 1 MiB, deklarowane i faktyczne przekroczenie limitu oraz przerwany odczyt; zamknięcie strumienia i przyczyny błędów sprawdzone bez AWS.

- [x] Zaimplementować adaptery S3NewsStore i S3VideoStore z walidacją modeli oraz 10 przypadkami testowymi: 4 dla newsów i 6 dla filmów. Commit 2a3d132 wysłany na GitHub.

- [x] Dodać osobny plik content/readers.py z protokołami NewsReader i VideoReader; import i Ruff poprawne.

- [x] Uporządkować backend w pakiety content, news i videos; poprawić importy, komendy CLI i ścieżki do dotychczasowego backend/.local. Po zmianie 283 testy backendu i Ruff poprawne.

- [x] Zastosować NewsReader/VideoReader w funkcjach odczytu read_feed/read_videos. Ruff poprawny; użytkownik potwierdził 277 testów backendu bez błędów (jedno ostrzeżenie Starlette/httpx).

- [x] Przygotować konfigurację wyboru magazynu w content/config.py: local albo s3 oraz wymagane ustawienia bucketa i kluczy. Sprawdzono 6 przypadków wyboru trybu i 8 przypadków ustawień S3. Pełna weryfikacja backendu przed pushem: 291 testów i Ruff poprawne; pozostaje znane ostrzeżenie Starlette/httpx.

- [ ] Przygotować klienta S3 tworzonego dopiero przy wyborze S3, z ograniczonym czasem oczekiwania; bez stałych kluczy AWS w kodzie.

- [ ] Podłączyć wybór magazynu do endpointów newsów i filmów, zachowując lokalny podgląd; błędy S3 mają zwracać kontrolowane 503 bez zastępowania danych demo.

- [ ] Sprawdzić integrację wyboru magazynu z endpointami i odpowiedzi 503 przy błędach konfiguracji testami bez połączeń AWS. Testy samych funkcji konfiguracji są już gotowe.

- [ ] Przekazać bucket, klucze i wybór magazynu S3 do API z CDK. Obecne API nadal czyta lokalne pliki.

- [ ] Przygotować warunkowy zapis S3 (ETag), trwałe rezerwacje prób i obsługę konfliktów bez resetowania budżetów; testy współbieżności i awarii.

- [ ] Dodać osobne funkcje odświeżające i harmonogramy oraz ich ograniczone uprawnienia i bezpieczną konfigurację kluczy dostawców; odczyt publicznego API pozostaje bez wywołań dostawców.

- [ ] Zapisać powtarzalne budowanie paczki Lambda i przebudować ją po dodaniu Boto3 oraz adapterów; ponowić testy w kontenerze AWS. Dotychczasowa paczka build nie zawiera nowych zmian.

- [x] Ustawić parametry Lambda API: 512 MB, timeout 10 s, reserved concurrency 2 i retencja logów 7 dni, RemovalPolicy.RETAIN. Sprawdzono w lokalnym synth. Parametry przyszłych funkcji odświeżających pozostają do ustalenia.

- [x] Obsłużyć bezpośrednie wejścia na /mortgage-calculator, /market-data i /tech, także z końcowym ukośnikiem, przez osobny plik CloudFront Function. Sprawdzono 12 przypadków tras i zachowanie query string.

- [x] Przygotować politykę cache CloudFront w osobnym infra/lib/frontend-cache.ts i podłączyć ją do dystrybucji: MinTTL=0, DefaultTTL=0, MaxTTL=31536000; Gzip i Brotli włączone. Kompilacja, synth i sprawdzenie powiązania w szablonie przeszły 21 listopada 2026.

- [x] Wykonać kompilację TypeScript i lokalne cdk synth --no-lookups dla aktualnego zakresu frontendu. Wynik zawiera AWS::S3::Bucket, AWS::S3::BucketPolicy, AWS::CloudFront::OriginAccessControl oraz AWS::CloudFront::Distribution. Sprawdzono blokadę publicznego dostępu, Deny bez HTTPS i uprawnienie GetObject tylko dla wskazanej dystrybucji.

- [ ] Po dodaniu pozostałych zasobów ponownie wykonać synth, przejrzeć cały szablon, uprawnienia i uaktualnić wycenę. Ocenić dwa zgłoszenia moderate dotyczące zależności CDK; nie używać audit fix --force bez przeglądu zmian.

### 7. Zatwierdzenie wdrożenia

- [ ] Pokazać użytkownikowi zasoby, uprawnienia, szacunek kosztów i dokładne komendy.

- [ ] Uwzględnić dodatkowe zasoby CDK bootstrap.

- [ ] Uzyskać wyraźne polecenie wykonania wdrożenia.

### 8. Pierwsze wdrożenie

- [ ] Przy publikacji ustawić metadane Cache-Control obiektów S3: index.html = no-cache, pliki assets z nazwami zawierającymi hash = public, max-age=31536000, immutable. Sprawdzić nagłówki odpowiedzi po wdrożeniu; polityka CloudFront sama ich nie ustawia.

- [ ] Wykonać zatwierdzony bootstrap i deploy.

- [ ] Opublikować backend i zbudować frontend z produkcyjną konfiguracją API.

- [ ] Wgrać frontend i sprawdzić ustawienia CORS.

- [ ] Zapisać publiczny adres aplikacji w dokumentacji.

### 9. Sprawdzenie publicznej wersji

- [ ] Sprawdzić health endpoint oraz pełne obliczenie kredytu.

- [ ] Sprawdzić telefon, wykres, tabelę, odświeżanie strony i błędy API.

- [ ] Sprawdzić HTTPS, CORS i funkcje dodatkowe dopuszczone do publikacji.

- [ ] Sprawdzić logi oraz dostępne dane o naliczanych kosztach; uwzględnić opóźnienie raportów billingowych.

### 10. Proces kolejnych aktualizacji

- [ ] Uzupełnić README i `docs/DEPLOYMENT.md` o działające instrukcje.

- [ ] Opisać proces: zmiana lokalna → sprawdzenie → publikacja → kontrola strony.

- [ ] Opisać aktualizowanie pamięci podręcznej CloudFront oraz powrót do poprzedniej wersji.

- [ ] Automatyzację publikacji pozostawić jako osobno uzgadniane zadanie.
