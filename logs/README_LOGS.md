# Logs Directory

This directory stores application logs for debugging and monitoring.

## Purpose

The logs directory contains:
- `data_handler.log` - Data fetching and caching operations
- Error messages and debugging information
- Performance metrics and timing data

## Files Created Automatically

When the app runs, the following file will be created:

```
logs/
├── data_handler.log         (auto-created by the app)
└── .gitkeep                 (ensures folder is tracked)
```

## Log Format

Each log entry includes:
- Timestamp (YYYY-MM-DD HH:MM:SS)
- Log Level (INFO, WARNING, ERROR)
- Message (details of the operation)

Example:
```
2025-01-11 10:30:45,123 - INFO - Database initialized successfully
2025-01-11 10:30:46,456 - INFO - Risk-free rate fetched from FRED: 0.0425
2025-01-11 10:30:47,789 - INFO - Successfully fetched 1095 records for NVDA
```

## Viewing Logs

To see what's happening in the app:

```bash
# Watch logs in real-time
tail -f logs/data_handler.log

# View last 50 lines
tail -50 logs/data_handler.log

# View specific error
grep ERROR logs/data_handler.log
```

## Log Levels

| Level | Meaning | When Used |
|-------|---------|-----------|
| INFO | Informational messages | Successful operations, data loaded |
| WARNING | Warning messages | API fallback used, data stale |
| ERROR | Error messages | Operation failed, exception caught |

## .gitignore Configuration

The `.gitignore` file prevents log files from being committed to GitHub:
```
logs/*.log    # Don't commit log files
```

This is because:
- Logs are environment-specific
- Logs contain timestamps and runtime data
- Logs can grow large
- Each deployment has its own logs

## Troubleshooting with Logs

1. **Check if data is updating:**
   ```bash
   tail logs/data_handler.log
   ```

2. **Find specific errors:**
   ```bash
   grep "NVDA" logs/data_handler.log
   ```

3. **Monitor performance:**
   ```bash
   grep "fetched" logs/data_handler.log
   ```

## Clearing Old Logs

To clear old log files:

```bash
# Clear all logs
rm logs/*.log

# Or just the data_handler log
rm logs/data_handler.log
```

The app will create new logs on next run.

## Integration with App

In `data_handler.py`, logging is set up as:

```python
import logging

logging.basicConfig(
    filename=f'{LOG_DIR}/data_handler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

## Best Practices

✓ Check logs when troubleshooting  
✓ Don't commit log files to GitHub  
✓ Clear old logs periodically  
✓ Use log rotation in production  
✓ Monitor for ERROR messages  

**Note:** .gitkeep is a placeholder. It will be replaced by actual log files when the app runs.
