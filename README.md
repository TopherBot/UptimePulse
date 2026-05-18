# UptimePulse

**UptimePulse** is a minimalistic command‑line utility written in Python that:

- Pings a target HTTP/HTTPS URL at a configurable interval.
- Detects status changes (up → down, down → up).
- Sends a Telegram message to a bot when a change is detected.

## Features (tiny version)
- Single‑file implementation (`uptime_pulse.py`).
- No external dependencies except `requests` (included in the standard Python ecosystem). 
- Configurable via command‑line arguments or environment variables.
- Works on any platform with Python 3.8+.

## Quick Start
```bash
# Clone (or just copy the files)
git clone https://github.com/yourname/UptimePulse.git
cd UptimePulse

# Install the only required package
pip install requests

# Run the monitor (replace placeholders)
python uptime_pulse.py \
  --url https://example.com \
  --interval 30 \
  --telegram-token <YOUR_BOT_TOKEN> \
  --chat-id <YOUR_CHAT_ID>
```

The script will now check `https://example.com` every 30 seconds and notify you via Telegram whenever the site goes down or comes back up.

## Command‑Line Options
| Option | Env Var | Description |
|--------|---------|-------------|
| `--url` | `UPP_URL` | URL to monitor (required). |
| `--interval` | `UPP_INTERVAL` | Check interval in seconds (default: `60`). |
| `--telegram-token` | `UPP_TELEGRAM_TOKEN` | Telegram Bot API token (required for alerts). |
| `--chat-id` | `UPP_CHAT_ID` | Telegram chat ID to receive alerts (required). |
| `--timeout` | `UPP_TIMEOUT` | HTTP request timeout in seconds (default: `10`). |

## How It Works
1. The script performs a `GET` request to the target URL.
2. If the request succeeds (status code < 400), the service is considered **up**; otherwise **down**.
3. On a state transition, a formatted message is sent to the configured Telegram chat.
4. The current state is kept in memory; the script is intended for short‑term runs or can be daemonized with tools like `systemd` or `pm2`.

## License
This project is released into the public domain (see the `UNLICENSE` file on the repo). Feel free to copy, modify, and distribute.

---
*Happy monitoring! 🚀*