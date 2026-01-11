# Data Directory

This directory stores all application data, including cached stock price data and backups.

## Directory Structure

```
data/
├── price_cache.db          (auto-created - SQLite database)
├── backup/                 (CSV backup files)
│   ├── NVDA_3y_backup.csv
│   ├── MSFT_3y_backup.csv
│   ├── AAPL_3y_backup.csv
│   ├── GOOGL_3y_backup.csv
│   ├── AMZN_3y_backup.csv
│   └── .gitkeep
├── README_DATA.md          (this file)
└── .gitkeep
```

## Files Description

### price_cache.db (SQLite Database)

**Purpose:** Primary cache for stock price data  
**Created:** Automatically on first app run  
**Contains:**
- Daily OHLCV data (Open, High, Low, Close, Volume)
- Adjusted Close prices
- Metadata about last update times

**Tables:**
1. `price_cache` - Historical price data for all tickers
2. `metadata` - Update timestamps and quality scores

**Size:** ~5-10 MB (for 3 years of daily data × 5 tickers)

**NOT committed to GitHub** (in .gitignore) because:
- Database is environment-specific
- Rebuilt automatically on first run
- Contains time-based data

### NVDA_3y_backup.csv (CSV Backup Files)

**Purpose:** Fallback data source if database or API fails  
**Format:** CSV with columns: Date, Open, High, Low, Close, Adj Close, Volume  
**Contains:** 3 years of daily stock data (~750 rows)

**Files Created:**
- `NVDA_3y_backup.csv` - NVIDIA data
- `MSFT_3y_backup.csv` - Microsoft data
- `AAPL_3y_backup.csv` - Apple data
- `GOOGL_3y_backup.csv` - Alphabet data
- `AMZN_3y_backup.csv` - Amazon data

**Size per file:** ~50-70 KB

**Can be committed to GitHub:** Yes (optional)

## Data Flow & Caching

### 3-Layer Fallback System

```
┌─────────────────────────┐
│   1. Try Streamlit      │
│      Cache (Memory)     │
│    4-hour TTL           │
└────────────┬────────────┘
             │ (if miss)
             ▼
┌─────────────────────────┐
│   2. Try SQLite         │
│      Database           │
│    (price_cache.db)     │
└────────────┬────────────┘
             │ (if empty)
             ▼
┌─────────────────────────┐
│   3. Try CSV            │
│      Backup             │
│    (data/backup/*.csv)  │
└─────────────────────────┘
```

### What Happens on Each Run

**First Run:**
1. Database is created: `price_cache.db`
2. Data fetched from Yahoo Finance
3. Data saved to database
4. Data cached in memory
5. CSV backups optionally created

**Subsequent Runs (within 4 hours):**
1. Load from Streamlit memory cache (instant)
2. No API calls needed
3. Fast response times

**After 4 Hours:**
1. Cache expires
2. New data fetched from Yahoo Finance
3. Database updated
4. New memory cache created

**If API Fails:**
1. Load from SQLite database
2. If database empty, load from CSV
3. Show data freshness warning to user

## Data Storage Details

### SQLite Database Schema

**Table: price_cache**
```sql
CREATE TABLE price_cache (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    date DATE NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL NOT NULL,
    adj_close REAL,
    volume INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ticker, date)
)
```

**Table: metadata**
```sql
CREATE TABLE metadata (
    ticker TEXT PRIMARY KEY,
    last_update TIMESTAMP,
    records_count INTEGER,
    data_quality_score REAL
)
```

### CSV Backup Format

```
Date,Open,High,Low,Close,Adj Close,Volume
2025-01-10,234.56,236.78,233.45,235.67,235.67,45678900
2025-01-09,232.34,234.56,231.23,233.45,233.45,42567800
...
```

## Data Lifecycle

1. **Creation:** First app run fetches from Yahoo Finance
2. **Storage:** Saved to SQLite database
3. **Caching:** Cached in memory for 4 hours
4. **Refresh:** After 4 hours, new data fetched
5. **Backup:** Optionally exported to CSV
6. **Access:** Used for all calculations and visualizations

## Cleaning Up Data

### Clear Database (Force Fresh Fetch)

```bash
# On Linux/macOS
rm data/price_cache.db

# On Windows
del data\price_cache.db

# App will recreate on next run
```

### Clear CSV Backups

```bash
# On Linux/macOS
rm data/backup/*.csv

# On Windows
del data\backup\*.csv

# These are optional; app will recreate if needed
```

### Keep Only Latest Data

```bash
# Keep database only (smaller footprint)
rm data/backup/*.csv

# Or keep CSV only (no database)
rm data/price_cache.db
```

## Backup & Recovery

### Creating Backups

The app automatically creates backups on first run. To manually create backups:

```python
# In Python script
import pandas as pd
from data_handler import get_stock_data
from config import TICKERS, BACKUP_DIR

for ticker in TICKERS.keys():
    data = get_stock_data(ticker)
    if data is not None:
        csv_path = f'{BACKUP_DIR}/{ticker}_3y_backup.csv'
        data.to_csv(csv_path)
        print(f"Backed up {ticker} to {csv_path}")
```

### Recovering from Backup

If database is corrupted:
1. Delete `data/price_cache.db`
2. CSV backups will be used as fallback
3. App will recreate database from backups
4. Or manually import CSV data

## .gitignore Configuration

```gitignore
data/price_cache.db         # Don't commit database
logs/*.log                  # Don't commit logs
data/backup/*.csv           # Don't commit large CSV files (optional)
```

**Reasoning:**
- Database is rebuilt on first run
- Data is environment and time-specific
- Reduces repository size
- Each environment has own data

**To commit backups (optional):**
Remove from `.gitignore`:
```bash
# Comment out or remove this line:
# data/backup/*.csv
```

## Disk Space Usage

| File | Size | Growth |
|------|------|--------|
| price_cache.db | ~10 MB | Minimal after initial setup |
| NVDA_backup.csv | ~70 KB | Minimal |
| MSFT_backup.csv | ~70 KB | Minimal |
| AAPL_backup.csv | ~70 KB | Minimal |
| GOOGL_backup.csv | ~70 KB | Minimal |
| AMZN_backup.csv | ~70 KB | Minimal |
| **Total** | **~11 MB** | Very efficient |

## Data Update Schedule

| Event | Frequency | Source |
|-------|-----------|--------|
| Memory Cache | Every 4 hours | Streamlit @st.cache_data |
| Database Update | Every 4 hours | Yahoo Finance API |
| CSV Backup | Optional | Manual or on demand |
| Full Refresh | On demand | "Refresh Data" button |

## Best Practices

✓ Keep both database and CSV for redundancy  
✓ Don't delete `data/` folder  
✓ Don't commit database files to GitHub  
✓ Monitor disk space for long-term use  
✓ Backup data before major updates  
✓ Clear cache if data seems stale  

## Troubleshooting

### "No data displayed"
→ Delete `data/price_cache.db` and restart app

### "Stale data"
→ Click "Refresh Data" button in sidebar

### "Database locked"
→ Ensure only one Streamlit instance running

### "CSV file not found"
→ Check file name matches ticker exactly (e.g., `NVDA_3y_backup.csv`)

### "Out of disk space"
→ Delete old backups: `rm data/backup/*.csv`

## Future Enhancements

Potential improvements:
- Automatic daily backups to cloud storage
- Data compression for large datasets
- Archive old data (>5 years)
- Real-time database replication
- Automated data validation checks

**Note:** .gitkeep files are placeholders. Once real files are created, you can delete them.
