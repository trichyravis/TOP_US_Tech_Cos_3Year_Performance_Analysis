# Data Backup - CSV Format

This directory contains CSV backup files for stock price data.

## File Structure

```
backup/
├── README_BACKUP.md                 (this file)
├── .gitkeep                         (git placeholder)
├── NVDA_3y_backup.csv               (auto-created)
├── MSFT_3y_backup.csv               (auto-created)
├── AAPL_3y_backup.csv               (auto-created)
├── GOOGL_3y_backup.csv              (auto-created)
└── AMZN_3y_backup.csv               (auto-created)
```

## CSV File Format

**File Name:** `{TICKER}_3y_backup.csv`

**Columns:**
```
Date,Open,High,Low,Close,Adj Close,Volume
2025-01-10,234.56,236.78,233.45,235.67,235.67,45678900
2025-01-09,232.34,234.56,231.23,233.45,233.45,42567800
2025-01-08,230.12,234.56,229.90,232.34,232.34,41234500
```

**Example Row Breakdown:**
- **Date:** 2025-01-10 (ISO format YYYY-MM-DD)
- **Open:** 234.56 (Opening price in USD)
- **High:** 236.78 (Highest price during day)
- **Low:** 233.45 (Lowest price during day)
- **Close:** 235.67 (Closing price in USD)
- **Adj Close:** 235.67 (Adjusted for splits/dividends)
- **Volume:** 45678900 (Number of shares traded)

## Files for Each Ticker

### NVDA_3y_backup.csv
- **Company:** NVIDIA Corporation
- **Rows:** ~750 (3 years × 252 trading days)
- **Size:** ~70 KB
- **Format:** Same as above

### MSFT_3y_backup.csv
- **Company:** Microsoft Corporation
- **Rows:** ~750
- **Size:** ~70 KB

### AAPL_3y_backup.csv
- **Company:** Apple Inc.
- **Rows:** ~750
- **Size:** ~70 KB

### GOOGL_3y_backup.csv
- **Company:** Alphabet Inc. (Google)
- **Rows:** ~750
- **Size:** ~70 KB

### AMZN_3y_backup.csv
- **Company:** Amazon.com Inc.
- **Rows:** ~750
- **Size:** ~70 KB

## When These Files Are Created

1. **First App Run:**
   - SQLite database is created
   - Data fetched from Yahoo Finance
   - CSV files can be optionally created

2. **Manual Creation:**
   - User can export data from app
   - Or run backup script manually

3. **Automatic Refresh:**
   - Every 4 hours when data updates
   - Backups can be refreshed alongside database

## How They're Used

### Primary Usage (Fallback)

If SQLite database fails or is corrupted:
```
API Error
    ↓
SQLite Database (fails)
    ↓
CSV Backup ← Used as fallback
    ↓
Data displayed to user
```

### Manual Import

To manually load from CSV:
```python
import pandas as pd

# Load NVDA data from CSV
df = pd.read_csv('data/backup/NVDA_3y_backup.csv', 
                  index_col='Date', 
                  parse_dates=True)
print(df.head())
```

### Data Validation

Check CSV file integrity:
```python
import pandas as pd

# Load and validate
df = pd.read_csv('data/backup/NVDA_3y_backup.csv')

# Check shape
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")

# Check for missing values
print(df.isnull().sum())

# Check data types
print(df.dtypes)
```

## Creating CSV Backups Manually

### Option 1: From App Data

```python
from data_handler import get_stock_data
from config import TICKERS, BACKUP_DIR

for ticker in TICKERS.keys():
    data = get_stock_data(ticker)
    if data is not None:
        csv_path = f'{BACKUP_DIR}/{ticker}_3y_backup.csv'
        data.to_csv(csv_path)
        print(f"Saved {ticker} to {csv_path}")
```

### Option 2: Direct Download from Yahoo Finance

```python
import yfinance as yf
from config import BACKUP_DIR

ticker = 'NVDA'
data = yf.download(ticker, period='3y', interval='1d')
csv_path = f'{BACKUP_DIR}/{ticker}_3y_backup.csv'
data.to_csv(csv_path)
print(f"Saved to {csv_path}")
```

### Option 3: Using Pandas

```python
import pandas as pd
from config import BACKUP_DIR

# Load from any source and save
df = pd.read_csv('some_data.csv')
df.to_csv(f'{BACKUP_DIR}/NVDA_3y_backup.csv')
```

## CSV Data Quality Checks

### Check for Gaps

```python
import pandas as pd

df = pd.read_csv('data/backup/NVDA_3y_backup.csv', 
                  index_col='Date', 
                  parse_dates=True)

# Check for date gaps > 2 days
date_diffs = df.index.to_series().diff()
gaps = date_diffs[date_diffs > pd.Timedelta(days=2)]
print(f"Found {len(gaps)} gaps in data")
```

### Validate OHLC Relationships

```python
# High should be >= Low
assert (df['High'] >= df['Low']).all(), "Invalid High/Low"

# Close should be between High and Low
assert ((df['Close'] >= df['Low']) & (df['Close'] <= df['High'])).all()

# Volume should be positive
assert (df['Volume'] > 0).all(), "Invalid volume"

print("✓ All validations passed!")
```

## Backup Strategy

### Recommended Backup Frequency

- **Automated:** Every 4 hours with data refresh
- **Manual:** After major app changes
- **Archive:** Monthly backups to cloud storage

### Backup to Cloud

```bash
# Example: Upload to GitHub
git add data/backup/
git commit -m "Backup stock data"
git push origin main

# Example: Upload to AWS S3
aws s3 cp data/backup/ s3://my-bucket/stock-data-backup/
```

## Restoring from Backup

### If Database is Corrupted

1. Delete database: `rm data/price_cache.db`
2. App will detect missing database
3. Will load from CSV backups
4. Will recreate database from CSV data
5. No data loss!

### Manual Restore

```python
import pandas as pd
from data_handler import save_to_sqlite

# Load from CSV
data = pd.read_csv('data/backup/NVDA_3y_backup.csv',
                    index_col='Date',
                    parse_dates=True)

# Save back to database
save_to_sqlite('NVDA', data)
print("✓ Restored from backup")
```

## File Encoding

All CSV files are:
- **Encoding:** UTF-8
- **Line Ending:** LF (Unix style)
- **Delimiter:** Comma (,)
- **Quote Char:** " (double quote)

## Git Configuration

### Commit vs. Don't Commit

```
✓ CAN commit:           ✗ DON'T commit:
- CSV files             - price_cache.db
- Backup files          - Temporary files
- README files          - __pycache__/
                        - .pyc files
```

In `.gitignore`:
```
data/price_cache.db     # Don't commit database
# data/backup/*.csv    # Comment out to commit CSVs
```

## Performance Notes

- **Size:** ~350 KB for all 5 backups
- **Load time:** <1 second per file
- **Memory:** ~50 MB when loaded all 5 files
- **Recommended:** Keep only 1-2 months of backups

## Troubleshooting

### "CSV file not found"
- Check file name matches ticker exactly
- Verify file is in `data/backup/` directory
- Run app to auto-create backups

### "Cannot read CSV"
- Check file encoding is UTF-8
- Verify columns are named correctly
- Check for corrupted rows

### "Data mismatches"
- Compare with app data
- Check CSV timestamp is recent
- Regenerate if older than 1 month

### "Import errors"
```python
# If pandas can't read:
df = pd.read_csv('data/backup/NVDA_3y_backup.csv',
                  on_bad_lines='skip',  # Skip bad rows
                  dtype={'Volume': 'int64'})  # Force types
```

## Best Practices

✓ Create backups after data updates  
✓ Test restore procedures monthly  
✓ Store backups in version control  
✓ Archive old backups to cloud storage  
✓ Validate data after each backup  
✓ Document backup schedule  
✓ Monitor backup file sizes  

## Automation Example

Create a daily backup script:

```python
# backup_data.py
#!/usr/bin/env python

from data_handler import get_stock_data
from config import TICKERS, BACKUP_DIR
from datetime import datetime

print(f"Starting backup at {datetime.now()}")

for ticker in TICKERS.keys():
    try:
        data = get_stock_data(ticker)
        if data is not None:
            csv_path = f'{BACKUP_DIR}/{ticker}_3y_backup.csv'
            data.to_csv(csv_path)
            print(f"✓ Backed up {ticker}")
    except Exception as e:
        print(f"✗ Failed to backup {ticker}: {e}")

print(f"Backup complete at {datetime.now()}")
```

Run daily with cron:
```bash
0 0 * * * python /path/to/backup_data.py
```

---

**Note:** .gitkeep is a placeholder. Once CSV files are created, you can delete it.
