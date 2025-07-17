import time
from btc_sniper_engine import run_btc_sniper
from bybit_sniper_scanner import run_bybit_sniper_scan

def run_sniper_loop():
    print("🔁 Starting sniper loop: KuCoin + Bybit")
    while True:
        run_btc_sniper()
        run_bybit_sniper_scan()
        print("🕒 Sleeping 60s...\n")
        time.sleep(60)

if __name__ == "__main__":
    run_sniper_loop()
