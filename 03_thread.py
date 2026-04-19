import threading
from collections import deque
import time
import random

class Pool:
    def __init__(self, producers=5, consumers=3):
        self.trade_queue = deque()
        self.order_lock = threading.Lock()
        self.market_lock = threading.Lock()
        self.num_producers = producers
        self.num_consumers = consumers
        self.all_workers = []
        self.ticker = [
            "NVDA", "AAPL", "BTC", "ETH", "TSLA",
            "PLTR", "COIN", "RIVN", "AMD", "SHOP",
            "SQ", "PYPL", "ABNB", "HOOD", "SNOW"
        ]
        self.market_prices = {t: 150.00 for t in self.ticker}

    def update_market(self):
        with self.market_lock:
            for t in self.market_prices:
                change = random.uniform(-1.0, 1.0)
                self.market_prices[t] += change

    def producer_sh(self, wid):
        for i in range(3):
            time.sleep(random.uniform(0.1, 0.3))
            trade_data = {
                "trade_id": f"TXN-{random.randint(1000, 9999)}",
                "timestamp": time.time(),
                "type": random.choice(['BUY', 'SELL']),
                "ticker": random.choice(self.ticker),
                "shares": random.randint(1, 100),
                "price_limit": round(random.uniform(100, 500), 2)
            }
            with self.order_lock:
                self.trade_queue.append(trade_data)
            print(f"producer {wid} generated {trade_data['type']} for {trade_data['ticker']}")

    def consumer_sh(self, wid):
        while True:
            time.sleep(random.uniform(0.1, 0.2))
            
            trade = None
            with self.order_lock:
                if len(self.trade_queue) > 0:
                    trade = self.trade_queue.popleft()
            
            if trade is not None:
                if trade == "SHUTDOWN":
                    print(f"Consumer {wid} shutting down")
                    break
                
                self.update_market()
                ticker = trade['ticker']
                limit = trade['price_limit']
                
                with self.market_lock:
                    current_price = self.market_prices[ticker]
                
                print(f" consumer {wid} processing {trade['trade_id']} ({ticker})")

                if trade['type'] == 'BUY':
                    if current_price <= limit:
                        print(f" cons {wid} bought {ticker} at {current_price:.2f} (limit {limit})")
                    else:
                        print(f" cons {wid} {ticker} {current_price:.2f} too expensive for {limit}")
                elif trade['type'] == 'SELL':
                    if current_price >= limit:
                        print(f" cons {wid} sold {ticker} at {current_price:.2f} (limit {limit})")
                    else:
                        print(f" cons {wid} {ticker} {current_price:.2f} too low for {limit}")
            else:
                print(f" cons {wid}: queue empty, waiting")

    def open_trading_day(self):
        producers = []
        for i in range(self.num_producers):
            p = threading.Thread(target=self.producer_sh, args=(i,))
            producers.append(p)
            p.start()

        consumers = []
        for i in range(self.num_consumers):
            c = threading.Thread(target=self.consumer_sh, args=(i,))
            consumers.append(c)
            c.start()

        for p in producers:
            p.join()

        with self.order_lock:
            for _ in range(self.num_consumers):
                self.trade_queue.append("SHUTDOWN")

        for c in consumers:
            c.join()

if __name__ == "__main__":
    testing = Pool(producers=5, consumers=3)
    testing.open_trading_day()