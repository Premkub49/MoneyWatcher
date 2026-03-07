# MoneyWatcher 💰

Personal automated expense tracker — captures Krungthai bank notifications via MacroDroid and records transactions through a webhook-based data pipeline.

**Built for personal use.** Not a general-purpose tool.

## How It Works

```
KTB Notification → MacroDroid → Webhook API → Bronze (raw) → Silver (cleaned) → Grafana
```

1. **MacroDroid** captures Krungthai bank notifications on Android
2. User selects a category from a dialog (fetched from API)
3. MacroDroid sends the data to the webhook
4. API stores the raw payload in the **Bronze layer** (`bronze.raw_data`)
5. ETL cleans the data and creates a **Silver layer** transaction (`public.transactions`)
6. **Grafana** reads from Silver tables for dashboards

## Tech Stack

- **Python 3.13** / FastAPI / Uvicorn
- **SQLAlchemy** (async) + asyncpg
- **Supabase** PostgreSQL (via pgbouncer)
- **Alembic** for migrations
- **MacroDroid** for Android notification capture
- **Grafana** for visualization
- **Zeabur** for deployment (auto-deploy on push)

## Project Structure

```
MoneyWatcher/
├── main.py                          # FastAPI entry point
├── alembic.ini
├── zbpack.json                      # Zeabur deploy config
├── requirements.txt
├── app/
│   ├── api/v1/
│   │   ├── webhook.py               # POST /krungthai, POST /process-raw
│   │   └── category.py              # GET / POST / DELETE categories
│   ├── database/
│   │   ├── core.py                  # Async engine & session
│   │   └── init_data.py             # Load category cache on startup
│   ├── models/
│   │   ├── base.py                  # RawData, Account, Category, Transaction
│   │   └── enums.py                 # CategoryType (INCOME, EXPENSE, OTHER)
│   ├── repositories/
│   │   ├── account.py
│   │   ├── category.py
│   │   ├── raw_data.py
│   │   └── transaction.py
│   ├── schemas/
│   │   └── webhook.py               # Pydantic models
│   └── services/
│       ├── account.py
│       ├── category.py
│       ├── category_cache.py        # In-memory cache (O(1) lookup)
│       ├── raw_data.py
│       └── transaction.py           # ETL: raw → cleaned transaction
└── migrations/
    └── versions/                    # Alembic migrations + seed data
```

## Database Schema

### Bronze Layer (`bronze` schema)

| Table | Columns |
|-------|---------|
| **raw_data** | id (UUID), source, raw_payload, is_processed, created_at |

### Silver Layer (`public` schema)

| Table | Columns |
|-------|---------|
| **categories** | name, display_name (with emoji), type (INCOME/EXPENSE/OTHER) |
| **accounts** | name, account_number, provider, balance, created_at |
| **transactions** | account_id, category_id, amount, bank_timestamp, note, created_at |

### Default Categories

| Name | Display | Type |
|------|---------|------|
| food | 🍕 food | EXPENSE |
| travel | 🚗 travel | EXPENSE |
| shopping | 🛒 shopping | EXPENSE |
| bill | 💡 bill | EXPENSE |
| transfer_in | 📥 transfer_in | INCOME |
| transfer_out | 📤 transfer_out | EXPENSE |
| other | 📝 other | OTHER |

## MacroDroid Setup

### Macro 1 — Notification Capture

- **Trigger**: Krungthai app notification
- **Action**: Create a persistent notification with amount info

### Macro 2 — Category Selection & Webhook

- **Trigger**: Click the persistent notification
- **Actions**:
  1. Fetch categories from `GET /api/v1/category`
  2. Show selection dialog (Food, Travel, Shopping, Bill, Transfer IN/OUT, Other)
  3. Send choice + notification data to `POST /api/v1/webhook/krungthai`

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/webhook/krungthai` | Receive MacroDroid webhook |
| `POST` | `/api/v1/webhook/process-raw` | Trigger ETL on raw data |
| `GET` | `/api/v1/category` | List all categories (for MacroDroid selector) |
| `POST` | `/api/v1/category` | Add a category |
| `DELETE` | `/api/v1/category/{name}` | Remove a category |

## Setup

```bash
pip install -r requirements.txt

# create .env with DATABASE_URL
export DATABASE_URL=postgresql+asyncpg://user:pass@host:port/dbname

alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Deploy (Zeabur)

Auto-deploys on push to `main` via [Zeabur](https://zeabur.com).

1. Connect GitHub repo to Zeabur
2. Set `DATABASE_URL` in Zeabur dashboard
3. Zeabur reads `zbpack.json` and handles the rest

No Docker required.
