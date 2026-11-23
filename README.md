# Numervia

Numervia is a personal finance web application for exploring financial decisions through transparent calculations and visual comparisons.

Its first working module, **Mortgage Lab**, compares mortgage repayments with and without regular monthly overpayments. The project is also a hands-on learning journey through Python, React, TypeScript, Docker, and AWS infrastructure as code.

**Status:** the application runs locally. AWS infrastructure is defined and validated with CDK, but has not been deployed. Shared S3 content storage and scheduled refreshes are still in progress.

## Features

- Mortgage calculations performed by the Python backend using `Decimal` and explicit rounding rules.
- Comparison of monthly payments, total interest, interest savings, and repayment duration.
- Outstanding-balance charts and a paginated repayment schedule.
- Input validation, loading states, and API error handling.
- Responsive layouts, keyboard navigation, and light and dark themes.
- Saved financial and property news with timestamps, publisher links, and image fallbacks.
- Video sections backed by saved metadata, with freshness and expiry handling.
- Clearly labelled synthetic demos for development without provider API keys.

News and video endpoints only read saved data. Visiting or refreshing the site does not trigger news-provider requests or YouTube searches. Third-party widgets, publisher images, and video embeds may make their own browser requests.

The calculator is educational and does not provide financial advice. It assumes a fixed interest rate, monthly repayments, no fees, and no early repayment charges. Monthly overpayments shorten the term rather than reduce the regular payment.

## Technology

| Area | Tools |
| --- | --- |
| Backend | Python 3.14, FastAPI, Pydantic, Decimal, Mangum, Boto3 |
| Frontend | React, TypeScript, Vite, Tailwind CSS, Recharts |
| Backend checks | pytest, Ruff |
| Frontend checks | Vitest, React Testing Library, TypeScript, Vite build |
| Infrastructure | AWS CDK v2 in TypeScript |
| Planned AWS runtime | Lambda with a Function URL, private S3, CloudFront with OAC |
| Packaging | Docker using the AWS Lambda Python image |

## Run locally

### Requirements

- Python 3.14.
- Node.js 24 and npm.
- Two terminals: one for the backend and one for the frontend.

The commands below target macOS and Linux. Docker, an AWS account, and provider API keys are not required to run the calculator locally. Run each command on its own line.

### Backend

From the repository root, create a virtual environment and install the pinned development dependencies:

```sh
cd backend
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.lock.txt
```

If `.venv` already exists, activate it and install dependencies only when needed. Start the API from the `backend` directory:

```sh
python -m uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

Activate `.venv` again when opening a new backend terminal. Stop the server with `Ctrl+C`.

### Frontend

In a second terminal, starting from the repository root:

```sh
cd frontend
npm ci
npm run dev
```

Open the URL printed by Vite, usually http://localhost:5173. The development server proxies `/api` requests to the backend at `http://127.0.0.1:8000`.

The mortgage calculator is available at `/mortgage-calculator`. The `/market-data` and `/tech` pages are placeholders for future work. Keep both servers running; stop either one with `Ctrl+C` in its terminal.

## Local news and video previews

Content files are stored under `backend/.local/` and are ignored by Git. A fresh checkout does not include saved news or videos. Missing or expired content shows an unavailable state; it does not prevent mortgage calculations.

### Synthetic news demo

From `backend`, with `.venv` active:

```sh
python -m app.news_cli preview-demo
```

This creates or updates synthetic news snapshots without network requests. Demo cards are labelled and do not link to fictional publisher articles. Snapshots expire after 24 hours; run the command again when needed.

To explicitly use the demo when an existing saved-news preview is enabled, start the backend with:

```sh
NEWS_STATE_PATH=.local/news-demo.json python -m uvicorn app.main:app --reload
```

### Saved real-news preview

An explicitly invoked local command can fetch headlines once using configured free-tier provider accounts. It saves each request reservation before making the request and preserves provider budgets, cooldowns, and blocks.

The UI labels this mode **Saved preview · No automatic updates** and displays the retrieval time. Page visits read the saved file without fetching new headlines. Saved content is served for no more than 24 hours; expiry does not trigger an automatic refresh.

This is a local preview, not a permanent archive or a deployed refresh service. Before initializing a live request ledger, verify the available provider quota and other use of the same keys. Never delete a live ledger to reset its counters.

See [news storage and preview instructions](docs/NEWS_LOCAL_CACHE.md) for configuration and commands. Credentials are read only by the explicitly invoked preview command, not by API startup.

### Synthetic video demo

For the first initialization, from `backend` with `.venv` active:

```sh
python -m app.video_cli init-demo
```

This refuses to overwrite an existing state file. Demo videos are synthetic previews without an active player. Video snapshots also expire after 24 hours. Refresh commands follow a controlled schedule and may return `skipped` outside their refresh window.

Real YouTube fetching requires separate quota configuration and explicit initialization; it is not enabled by starting the app. See [video storage instructions](docs/VIDEO_LOCAL_CACHE.md).

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | API health response |
| `POST` | `/api/v1/mortgage/simulate` | Compare mortgage repayment scenarios |
| `GET` | `/api/v1/news?feed=overview` | Read saved financial headlines |
| `GET` | `/api/v1/news?feed=housing` | Read saved property and mortgage headlines |
| `GET` | `/api/v1/videos` | Read saved video metadata |

Use `/docs` for the request and response schemas. Financial amounts are serialized as strings to preserve decimal values.

## Configuration

| Setting | Used by | Purpose |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Frontend | Public API origin; omit locally to use the Vite proxy |
| `ALLOWED_ORIGINS` | Backend | Comma-separated exact origins allowed by CORS |
| `NEWS_STATE_PATH` | Backend | Override the local news-state file |
| `VIDEOS_STATE_PATH` | Backend | Override the local video-state file |

`VITE_API_BASE_URL` is embedded in the frontend build and must never contain credentials. Changing it for production requires rebuilding the frontend. CORS is handled by FastAPI without wildcard origins or credentials. CORS does not authenticate callers or prevent non-browser access.

The `.env.example` files document available settings. The API does not automatically load provider credentials from `.env`. The explicit saved-news preview command can read `backend/.env`; other live refresh commands use their documented process environment.

Keep API keys, AWS credentials, local state, and generated deployment packages out of Git and the frontend bundle. No paid external API is required for local development.

## Checks

Backend, from `backend` with `.venv` active:

```sh
python -m pytest
python -m ruff check .
python -m pip check
```

Frontend, from `frontend`:

```sh
npm test
npm run build
```

`npm run build` includes TypeScript checking. Frontend ESLint configuration is still pending. Backend tests cover mortgage calculations, API validation, cache expiry, request budgets, storage failures, and S3 read adapters without contacting AWS.

## AWS preparation

The CDK project targets **Europe (Ireland), `eu-west-1`**. Its local template defines:

- A private frontend S3 bucket and CloudFront distribution with Origin Access Control, HTTPS redirects, and compression.
- React page routing through a CloudFront Function and a separate cache policy.
- A Python 3.14 Lambda using `app.handler.handler`, with a public Function URL.
- 512 MB Lambda memory, a 10-second timeout, concurrency limited to two, and seven-day log retention.
- A separate private content-state bucket. The API role is limited to reading `news/state.json` and `videos/state.json`.

The endpoints currently read local files. News and video S3 read adapters have been implemented and tested locally, but endpoint integration, conditional writes, and scheduled refresh functions are unfinished.

Install infrastructure dependencies and compile from the repository root:

```sh
cd infra
npm ci
npx --no-install tsc
```

Local synthesis also requires a prepared `backend/build/lambda/` package containing application code and Linux x86-64 dependencies. This generated directory is ignored by Git and is not included in a fresh checkout. Packaging currently uses Docker and is not yet automated; the package must be rebuilt after backend changes.

Once that package exists, run from `infra`:

```sh
npx --no-install cdk synth --no-lookups
```

Synthesis generates local CloudFormation templates and stages assets. It does not deploy resources. No AWS resources have been created for this project yet. Cost assumptions, permissions, provider usage terms, and budget-alert coverage must be reviewed before bootstrap or deployment. S3 object cache headers also remain part of the publishing work.

## Repository layout

```text
backend/
  app/finance/       Mortgage calculation engine
  app/               FastAPI, content stores, refresh logic, and Lambda handler
  tests/             Backend tests
frontend/
  src/               React pages, components, and feature modules
  tests/             Frontend tests
infra/
  bin/               CDK application entry point
  lib/               Infrastructure modules
  functions/         CloudFront routing function
docs/               Roadmap, implementation notes, and cost assumptions
```

## Next milestones

1. Complete S3 read adapters and select local or S3 storage through configuration.
2. Implement conditional state updates and scheduled refreshes with durable request budgets.
3. Automate Lambda packaging and finish deployment configuration and checks.
4. Review costs, permissions, and content-provider conditions, then deploy and verify the first public release.

Future financial modules remain planned work. The current priority is completing and deploying Mortgage Lab with the agreed news and video sections.

## Further documentation

- [AWS roadmap](docs/AWS_ROADMAP.md)
- [Application preparation for AWS](docs/AWS_APP_PREPARATION.md)
- [News storage and local previews](docs/NEWS_LOCAL_CACHE.md)
- [Video storage and quota handling](docs/VIDEO_LOCAL_CACHE.md)
- [First-release scope](docs/RELEASE_SCOPE.md)
- [Cost assumptions](docs/COSTS.md)
- [UI quality checks](docs/UI_QA.md)

These implementation notes are currently maintained in Polish.
