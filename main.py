import os
import requests

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

WATCHLIST = "watchlist.txt"
MEXC_API = "https://api.mexc.com/api/v3/ticker/price"


def send_telegram(text):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=10,
    )


def load_watchlist():
    data = []

    if not os.path.exists(WATCHLIST):
        return data

    with open(WATCHLIST, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            try:
                symbol, target = line.split(",")
                symbol = symbol.strip().upper().replace("/", "")
                target = float(target.strip())
                data.append((symbol, target))
            except:
                pass

    return data


def get_price(symbol):
    r = requests.get(
        MEXC_API,
        params={"symbol": symbol},
        timeout=10
    )

    if r.status_code != 200:
        return None

    return float(r.json()["price"])


def main():
    watchlist = load_watchlist()

    for symbol, target in watchlist:

        price = get_price(symbol)

        if price is None:
            continue

        if price >= target:
            send_telegram(
                f"🚨 {symbol}\n\n"
                f"Prezzo raggiunto!\n"
                f"Target: {target}\n"
                f"Prezzo attuale: {price}"
            )


if __name__ == "__main__":
    main()
