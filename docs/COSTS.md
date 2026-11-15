# Numervia — wstępny koszt AWS

Data sprawdzenia: 15 listopada 2026. Region wybrany przez użytkownika: **Europe (Ireland), eu-west-1**. CloudFront jest globalny; model przyjmuje odbiorców w Europie.

Status: szacunek lokalny na podstawie publicznych cenników. Nie tworzono zasobów, nie wykonywano bootstrap/deploy ani zmian uprawnień. Użytkownik korzysta z IAM i nie sprawdził Billing; plan konta, kredyty, wykorzystanie Free Tier i obecne opłaty pozostają nieznane. Nie potrzebujemy kosztów innych projektów do policzenia modelu Numervii, ale inne projekty mogą zużywać wspólne bezpłatne pule.

## Wynik i jego znaczenie

Dla przyjętego małego ruchu model daje **około 0,46 USD/miesiąc przed podatkami**, jeśli wszystkie opisane wolumeny rozliczymy po stawkach jednostkowych bez dostępnych bezpłatnych pul. To obliczenie na podstawie założeń, nie prognoza rachunku ani twardy limit. Dla planowania można zostawić bufor do kilku USD; jego wysokość nie zatrzymuje naliczania opłat.

Nie przeliczamy automatycznie USD na GBP: rzeczywista waluta rozliczeniowa, kurs i podatki konta nie są potwierdzone. Cel projektu £0–£5/miesiąc pozostaje celem. Przed wdrożeniem trzeba ponowić wycenę dla konkretnego planu CDK i sprawdzić Billing.

## Planowane składniki

- API: jedna standardowa Lambda on-demand x86, Function URL, bez provisioned concurrency i bez API Gateway.
- Frontend: prywatny S3 Standard, CloudFront z OAC, wariant pay-as-you-go. Model nie zakłada wyboru nowego planu CloudFront flat-rate.
- Cache: osobny prywatny bucket S3 ze stanami newsów i filmów, bez bazy danych.
- Odświeżanie: dwie Lambda i dwa harmonogramy EventBridge Scheduler, co 6 godzin.
- CloudWatch Logs z retencją 7 dni; bez logowania treści, kluczy i pełnych żądań.
- CDK bootstrap: bucket artefaktów, repozytorium ECR, role IAM i parametr wersji. Liczymy przechowywane artefakty; samo przygotowanie tego opisu nie uruchamia bootstrap.

Nie przewidujemy EC2, NAT Gateway, RDS, zakupu domeny, dedykowanego certyfikatu, płatnych zewnętrznych API, dodatkowych kluczy KMS ani płatnych rozszerzeń monitoringu. Domyślne szyfrowanie S3 zamiast własnego klucza KMS. Wersjonowanie i cykl życia artefaktów należy uwzględnić w projekcie CDK, by nie zakładać stałego 1 GB przy nieograniczonym gromadzeniu wersji.

## Założenia miesięczne — 31 dni

| Wielkość | Przyjęta wartość |
| --- | ---: |
| Wizyty | 1000 |
| Transfer frontendu na wizytę | 2 MiB; obejmuje obecne duże tło i skrypty, bez treści dostawców pobieranych bezpośrednio przez przeglądarkę |
| Żądania HTTPS CloudFront | 10 na wizytę = 10 000 |
| Wywołania API | Średnio 3 na wizytę = 3000, łącznie z uśrednieniem żądań pomocniczych; rzeczywisty miks GET/POST/preflight wymaga pomiaru |
| Lambda API | 512 MiB, średnio 1 s na wywołanie, razem 1500 GB-s |
| Wywołania odświeżające | 2 funkcje × 4 razy/dobę × 31 = 248 |
| Lambda odświeżające | 512 MiB, średnio 30 s na uruchomienie, razem 3720 GB-s |
| Zapytania do dostawców | 372 newsy + 372 wyszukiwania filmów; limity dostawców są osobne od kosztów AWS |
| S3: stan, frontend i artefakty bootstrap razem | 1 GB-miesiąc |
| S3 GET/HEAD | 15 000: model konserwatywnie uwzględnia odczyty cache, zadania i cache misses plików strony |
| S3 PUT/LIST itp. | 2000: około 1488 zapisów rezerwacji/wyników i zapas na publikację plików |
| Logi przyjęte do CloudWatch | 0,05 GB; przechowywanie przez 7/31 miesiąca |
| Transfer odpowiedzi API do internetu | Średnio 100 KiB × 3000, około 0,286 GB |
| Inwalidacje CloudFront | 20 ścieżek/miesiąc |

Są to założenia, nie zmierzone parametry Lambdy. Dłuższe cold starts, timeouty, duże harmonogramy kredytu, dodatkowe preflight i testy ręczne zwiększą wolumen. Pełne odświeżenie filmów to trzy wyszukiwania, nie jedno. Ruch widzów nie uruchamia odświeżania dostawców.

## Stawki i wyliczenie bez dostępnych bezpłatnych pul

Publiczny AWS Price List odczytano 15 listopada 2026. Użyto produktów eu-west-1; dla CloudFront produktów Europe. Stawki USD, pierwszy próg cenowy, bez rabatów.

| Składnik | Stawka | Koszt dla powyższych założeń |
| --- | --- | ---: |
| Lambda — czas x86 | 0,0000166667 USD/GB-s × 5220 GB-s | 0,0870 USD |
| Lambda — żądania | 0,20 USD/milion × 3248 | 0,0006 USD |
| CloudFront — transfer do widzów w Europie | 0,085 USD/GB × 1,953125 GB | 0,1660 USD |
| CloudFront — HTTPS | 0,012 USD/10 000 | 0,0120 USD |
| S3 Standard | 0,023 USD/GB-miesiąc | 0,0230 USD |
| S3 GET/HEAD | 0,0004 USD/1000 | 0,0060 USD |
| S3 PUT/LIST | 0,005 USD/1000 | 0,0100 USD |
| CloudWatch — logi i retencja | 0,57 USD/GB przyjęcia + 0,03 USD/GB-miesiąc przechowywania | 0,0288 USD |
| Transfer API do internetu | 0,09 USD/GB | 0,0257 USD |
| Scheduler | 1 USD/milion wywołań po bezpłatnej puli | 0,0002 USD |
| CloudFront — inwalidacje | 0,005 USD/ścieżkę po bezpłatnej puli | 0,1000 USD |
| **Suma z niezaokrąglonych wartości** | | **0,46 USD** |

Model celowo nalicza także Scheduler i inwalidacje po stawkach po wyczerpaniu bezpłatnych pul. Jeśli pule są dostępne, te pozycje wyniosą 0. Publiczne oferty obejmują m.in. 14 mln wywołań Scheduler/miesiąc, pierwsze 1000 ścieżek inwalidacji oraz bezpłatne wolumeny Lambda i CloudFront. Nie zakładamy, że wolumeny są dostępne na konkretnym koncie ani że kredyty pokryją pełny rachunek.

CloudFront pay-as-you-go obecnie opisuje bezpłatny transfer 1 TB i 10 mln żądań/miesiąc; nie mieszamy tych warunków z nowymi flat-rate plans. Transfer S3 do CloudFront nie jest ponownie naliczony w modelu. Przy bezpłatnych pulach i kredytach realna opłata może być niższa; dokładnej kwoty nie wyliczamy bez potwierdzenia konta. [CloudFront pay-as-you-go](https://aws.amazon.com/cloudfront/pricing/pay-as-you-go/), [Scheduler](https://aws.amazon.com/eventbridge/pricing/), [Lambda](https://aws.amazon.com/lambda/pricing/).

Dla bootstrap nie liczymy pustego ECR jako magazynu obrazów: plan zakłada paczki ZIP. Jeśli później pojawią się obrazy kontenerowe, trzeba doliczyć ECR, np. według opublikowanej stawki przechowywania 0,10 USD/GB-miesiąc. S3 z artefaktami już jest w 1 GB powyżej; nie naliczamy go podwójnie. [CDK bootstrap](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping-env.html), [ECR](https://aws.amazon.com/ecr/pricing/).

## Wpływ ruchu

Przy tym samym modelu na wizytę, stałych 248 odświeżeniach, 1 GB storage i 2000 zapisów S3:

| Wizyty/miesiąc | Transfer frontendu | Koszt nominalny bez dostępnych bezpłatnych pul |
| --- | ---: | ---: |
| 1000 | około 1,95 GB | 0,46 USD |
| 10 000 | około 19,53 GB | 2,78 USD |
| 100 000 | około 195,31 GB | 25,97 USD |

Wzory do powtórzenia obliczeń: API = 3 × wizyty; GB-s API = 1,5 × wizyty; GB-s odświeżania = 3720; GET S3 = 13 × wizyty + 2000; logi GB = 0,01 + 0,00004 × wizyty; frontend GB = 2 × wizyty / 1024; transfer API GB = 300 × wizyty / 1024². Koszt retencji logów = logi × 0,03 × 7/31. Mnożniki i czasy wymagają pomiaru po pierwszym wdrożeniu. GB w obliczeniach transferu oszacowano z MiB/KiB przy dzieleniu przez 1024; to model wolumenu, nie pomiar fakturowanych bajtów.

Tabela nie oznacza gwarantowanego kosztu przy dowolnym ruchu lub nadużyciach. Reserved concurrency, timeout i budżet dostawców nie są twardym limitem rachunku AWS.

## Co pozostaje przed wdrożeniem

- [x] Region: eu-west-1, wybrany przez użytkownika 15 listopada 2026.
- [x] Wstępny model kosztów całego wybranego zakresu oraz bootstrap, odświeżania, logów i transferu.
- [ ] Właściciel konta sprawdza plan, Free Tier, kredyty, dostępność usług i bieżące opłaty. Nie zmieniano uprawnień IAM użytkownika.
- [ ] Po osobnym poleceniu skonfigurować alerty budżetowe, np. progi odpowiadające £1/£3/£5 w walucie konta. Alerty mają opóźnienia i same nie odcinają wydatków.
- [ ] Przeliczyć po lokalnym cdk synth: dokładne zasoby, pamięć, timeouty, retencja, plan CloudFront, wersjonowanie i ewentualne dodatkowe usługi.
- [ ] Uzyskać wyraźne polecenie przed bootstrap/deploy oraz tworzeniem lub zmianą zasobów.

## Źródła stawek

Dokładne regionalne katalogi JSON są publiczne i nie wymagają konta ani płatnego API. Odczytane wersje: S3 2026-11-09, Lambda 2026-11-11, CloudFront 2026-10-19, CloudWatch 2026-11-04. Katalogi mogą zostać zaktualizowane, dlatego stawki należy ponownie sprawdzić przed wdrożeniem.

- [S3 — eu-west-1 Price List](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/eu-west-1/index.json), [cennik S3](https://aws.amazon.com/s3/pricing/).
- [Lambda — eu-west-1 Price List](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSLambda/current/eu-west-1/index.json).
- [CloudFront Price List](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudFront/current/index.json), produkty Europe.
- [CloudWatch — eu-west-1 Price List](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/eu-west-1/index.json), [cennik](https://aws.amazon.com/cloudwatch/pricing/).
- [Scheduler — AWSEvents eu-west-1 Price List](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSEvents/current/eu-west-1/index.json).
- [Transfer — eu-west-1 Price List](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSDataTransfer/current/eu-west-1/index.json), standardowy AWS Outbound do External.

Sprawdzenie: stawki wyodrębniono z odpowiednich produktów i pierwszych progów, a rachunek wykonano lokalnie z Decimal. Nie wykonano testów aplikacji, ponieważ zmieniono wyłącznie dokumentację. Nie odczytywano poświadczeń AWS ani danych Billing.
