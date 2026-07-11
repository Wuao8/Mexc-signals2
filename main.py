import os
import json
import requests

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

WATCHLIST = "watchlist.txt"
TRIGGERED = "triggered.json"

API = "https://api.mexc.com/api/v3/ticker/price"


def telegram(msg):
    r = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg},
        timeout=10,
    )
    print(r.status_code, r.text)


def load_watchlist():
    coins = []

    if not os.path.exists(WATCHLIST):
        return coins

    with open(WATCHLIST, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            try:
                symbol, target = line.split(",")
                symbol = symbol.strip().upper().replace("/", "")
                target = float(target.strip())
                coins.append((symbol, target))
            except:
                pass

    return coins


def load_triggered():
    if not os.path.exists(TRIGGERED):
        return {}

    with open(TRIGGERED, "r") as f:
        return json.load(f)


def save_triggered(data):
    with open(TRIGGERED, "w") as f:
        json.dump(data, f, indent=2)


def price(symbol):
    r = requests.get(API, params={"symbol": symbol}, timeout=10)

    if r.status_code != 200:
        return None

    return float(r.json()["price"])


def main():

    triggered = load_triggered()

    for symbol, target in load_watchlist():

        key = f"{symbol}_{target}"

        if key in triggered:
            continue

        p = price(symbol)
        print(symbol, "target:", target, "prezzo:", p)

        if p is None:
            continue

        if p >= target:

            telegram(
                f"🎯 TARGET RAGGIUNTO\n\n"
                f"{symbol}\n"
                f"Target: {target}\n"
                f"Prezzo: {p}"
            )

            triggered[key] = True

    save_triggered(triggered)


if __name__ == "__main__":
    main()
