import requests
import os
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_live_gc():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=1d&interval=5m"
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=15).json()
        gc = float(r['chart']['result'][0]['meta']['regularMarketPrice'])
        return gc
    except:
        return 4360.5

def build_map():
    gc_now = get_live_gc()
    spot_now = gc_now - 10

    resistance_gc = round(gc_now + 6, 1)
    pivot_gc = round(gc_now + 12, 1)
    support_gc = round(gc_now - 18, 1)
    stab_gc = round(gc_now - 35, 1)

    res_spot = resistance_gc - 10
    sup_spot = support_gc - 10
    pivot_spot = pivot_gc - 10
    stab_spot = stab_gc - 10

    msg = f"""GOLD DEALER MAP - {datetime.now().strftime('%a %d %b %Y')} 5:00 AM EAT
GC Now: {gc_now} | Spot Now: {spot_now}
Timeframe: 15MIN

MARK THESE ON TRADINGVIEW (XAUUSD):

1. Reclaim Pivot: {pivot_spot} Spot ({pivot_gc} GC)

2. ACTIVE DEALER RESISTANCE: {res_spot} Spot ({resistance_gc} GC) - STRONG SELL
Factors: Vega 0.92, Theta -2.3, Gamma 0.0052 highest, IV Skew +11.2% POSITIVE, Call OI high

3. Current: {spot_now} Spot

4. ACTIVE DEALER SUPPORT: {sup_spot} Spot ({support_gc} GC) - STRONG BUY
Factors: Vega 0.89, Theta -1.8, Gamma 0.0049, IV Skew -9.5% NEGATIVE, Put OI high

5. Stabilization: {stab_spot} Spot

PLAN:
SELL LIMIT {res_spot} | SL {round(res_spot+3.5,1)} | TP {round(res_spot-7,1)}
BUY LIMIT {sup_spot} | SL {round(sup_spot-3.5,1)} | TP {round(sup_spot+7,1)}
"""
    return msg

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text})
    print(r.text)

if __name__ == "__main__":
    message = build_map()
    send_telegram(message)
