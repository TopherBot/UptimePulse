#!/usr/bin/env python3
"""UptimePulse – tiny URL monitor with Telegram alerts.

Usage:
    python uptime_pulse.py \
        --url https://example.com \
        --interval 30 \
        --telegram-token <TOKEN> \
        --chat-id <CHAT_ID>

All arguments can also be supplied via environment variables:
    UPP_URL, UPP_INTERVAL, UPP_TELEGRAM_TOKEN, UPP_CHAT_ID, UPP_TIMEOUT
"""

import argparse
import os
import sys
import time
from typing import Optional

import requests

# -------------------- Configuration --------------------

def get_config() -> dict:
    parser = argparse.ArgumentParser(description="UptimePulse – tiny URL monitor with Telegram alerts")
    parser.add_argument("--url", help="Target URL to monitor", default=os.getenv("UPP_URL"))
    parser.add_argument("--interval", type=int, help="Check interval in seconds", default=os.getenv("UPP_INTERVAL", 60))
    parser.add_argument("--telegram-token", help="Telegram Bot token", default=os.getenv("UPP_TELEGRAM_TOKEN"))
    parser.add_argument("--chat-id", help="Telegram chat ID to receive alerts", default=os.getenv("UPP_CHAT_ID"))
    parser.add_argument("--timeout", type=int, help="HTTP request timeout seconds", default=os.getenv("UPP_TIMEOUT", 10))
    args = parser.parse_args()

    missing = []
    if not args.url:
        missing.append("--url / UPP_URL")
    if not args.telegram_token:
        missing.append("--telegram-token / UPP_TELEGRAM_TOKEN")
    if not args.chat_id:
        missing.append("--chat-id / UPP_CHAT_ID")
    if missing:
        sys.stderr.write(f"Error: missing required arguments: {', '.join(missing)}\n")
        sys.exit(1)

    return {
        "url": args.url,
        "interval": args.interval,
        "telegram_token": args.telegram_token,
        "chat_id": args.chat_id,
        "timeout": args.timeout,
    }

# -------------------- Telegram Helper --------------------

def telegram_send(token: str, chat_id: str, text: str) -> None:
    """Send a simple text message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        resp = requests.post(url, data=payload, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        sys.stderr.write(f"[Telegram] failed to send: {e}\n")

# -------------------- Monitoring Loop --------------------

def check_service(url: str, timeout: int) -> bool:
    """Return True if the service is up (HTTP <400), else False."""
    try:
        resp = requests.get(url, timeout=timeout)
        return resp.status_code < 400
    except Exception:
        return False


def main() -> None:
    cfg = get_config()
    last_status: Optional[bool] = None
    print(f"[UptimePulse] Monitoring {cfg['url']} every {cfg['interval']}s. Press Ctrl+C to stop.")
    try:
        while True:
            is_up = check_service(cfg["url"], cfg["timeout"])
            status_str = "UP" if is_up else "DOWN"
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if last_status is None:
                # initial state – just report
                print(f"[{timestamp}] Initial state: {status_str}")
                telegram_send(cfg["telegram_token"], cfg["chat_id"], f"🔔 *UptimePulse* – Initial state: *{status_str}* for `{cfg['url']}`")
            elif is_up != last_status:
                # state changed
                print(f"[{timestamp}] State change: {status_str}")
                emoji = "✅" if is_up else "❌"
                telegram_send(
                    cfg["telegram_token"],
                    cfg["chat_id"],
                    f"{emoji} *UptimePulse* – Service `{cfg['url']}` is now *{status_str}*",
                )
            else:
                # no change – keep silent (or debug print)
                pass
            last_status = is_up
            time.sleep(cfg["interval"])
    except KeyboardInterrupt:
        print("\n[UptimePulse] Stopped by user.")

if __name__ == "__main__":
    main()
