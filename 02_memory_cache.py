import random
import csv
import os
import sys
from datetime import date, timedelta

NGX_SYMBOLS = {
    "ZENITHBANK": "Banking", "UBA": "Banking", "GTCO": "Banking", 
    "ACCESSCORP": "Banking", "FBNH": "Banking", "FCMB": "Banking", 
    "FIDELITYBK": "Banking", "STERLINGNG": "Banking", "STANBIC": "Banking", 
    "WEMABANK": "Banking", "ETI": "Banking", "JAIZBANK": "Banking",
    "UNITYBNK": "Banking", "UCAP": "Financial Services", "NGXGROUP": "Financial Services",
    "CUSTODIAN": "Insurance", "AIICO": "Insurance", "SOVRENI": "Insurance",
    "NIDF": "Financial Services", "UHOMREI": "Real Estate",
    "DANGCEM": "Industrial Goods", "BUACEMENT": "Industrial Goods", "WAPCO": "Industrial Goods",
    "CAP": "Industrial Goods", "BETAGLA": "Industrial Goods", "MEYER": "Industrial Goods",
    "BERGER": "Industrial Goods", "CUTIX": "Industrial Goods",
    "MTNN": "Telecoms", "AIRTELAFRI": "Telecoms", "CHAMS": "Technology", 
    "CWG": "Technology", "COURTVILLE": "Technology", "NSLTECH": "Technology",
    "SEPLAT": "Oil & Gas", "OANDO": "Oil & Gas", "CONOIL": "Oil & Gas", 
    "TOTAL": "Oil & Gas", "ARADEL": "Oil & Gas", "ETERNA": "Oil & Gas", 
    "JAPAULGOLD": "Oil & Gas", "MRS": "Oil & Gas",
    "NESTLE": "Consumer Goods", "NB": "Consumer Goods", "GUINNES": "Consumer Goods", 
    "DANGSUG": "Consumer Goods", "FLOURMILL": "Consumer Goods", "UNILEVE": "Consumer Goods", 
    "NASCON": "Consumer Goods", "PZ": "Consumer Goods", "BUAFOODS": "Consumer Goods",
    "INTBREW": "Consumer Goods", "CADBURY": "Consumer Goods", "CHAMPION": "Consumer Goods",
    "VITAFOAM": "Consumer Goods", "NNFM": "Consumer Goods",
    "OKOMUOI": "Agriculture", "PRESCO": "Agriculture", "ELLAHLA": "Agriculture",
    "FTNCOCOA": "Agriculture", "LIVESTOCK": "Agriculture",
    "TRANSCO": "Conglomerates", "UACN": "Conglomerates", "NAHCO": "Services", 
    "TRANSCOHOT": "Services", "IKEJAHOTEL": "Services", "CILEASI": "Services",
    "ACADEMY": "Services", "GEREGU": "Power", "UPDC": "Real Estate",
    "FIDSON": "Healthcare", "NEIMETH": "Healthcare", "MAYBAKER": "Healthcare",
    "GLAXOSMITH": "Healthcare", "PHARMDEKO": "Healthcare"
}

BASE_PRICES = {
    "ZENITHBANK": 124.00, "UBA": 46.00, "GTCO": 128.00, "ACCESSCORP": 27.20, 
    "FBNH": 58.45, "FCMB": 11.75, "FIDELITYBK": 19.75, "STERLINGNG": 8.00, 
    "STANBIC": 182.55, "WEMABANK": 27.55, "ETI": 61.20, "JAIZBANK": 9.23,
    "UNITYBNK": 1.85, "UCAP": 16.15, "NGXGROUP": 167.00, "CUSTODIAN": 73.00, 
    "AIICO": 4.17, "SOVRENI": 2.10, "NIDF": 127.00, "UHOMREI": 72.50,
    "DANGCEM": 810.00, "BUACEMENT": 326.70, "WAPCO": 243.00, "CAP": 95.00, 
    "BETAGLA": 498.50, "MEYER": 3.40, "BERGER": 15.50, "CUTIX": 2.60,
    "MTNN": 755.00, "AIRTELAFRI": 2746.70, "CHAMS": 3.50, "CWG": 6.80, 
    "COURTVILLE": 0.65, "NSLTECH": 0.97, "SEPLAT": 10450.00, "OANDO": 46.50, 
    "CONOIL": 194.00, "TOTAL": 640.00, "ARADEL": 1547.50, "ETERNA": 15.90, 
    "JAPAULGOLD": 3.29, "MRS": 135.00, "NESTLE": 3249.90, "NB": 73.50, 
    "GUINNES": 499.00, "DANGSUG": 70.00, "FLOURMILL": 81.80, "UNILEVE": 103.30, 
    "NASCON": 156.00, "PZ": 76.30, "BUAFOODS": 798.00, "INTBREW": 14.50, 
    "CADBURY": 19.00, "CHAMPION": 3.40, "VITAFOAM": 20.00, "NNFM": 79.40,
    "OKOMUOI": 1765.00, "PRESCO": 1980.00, "ELLAHLA": 10.80, "FTNCOCOA": 1.60, 
    "LIVESTOCK": 1.75, "TRANSCO": 49.50, "UACN": 100.00, "NAHCO": 200.00, 
    "TRANSCOHOT": 203.00, "IKEJAHOTEL": 7.50, "CILEASI": 6.50, "ACADEMY": 7.65, 
    "GEREGU": 1132.50, "UPDC": 1.50, "FIDSON": 98.50, "NEIMETH": 9.50, 
    "MAYBAKER": 5.50, "GLAXOSMITH": 8.10, "PHARMDEKO": 1.90
}

def generate_trade_data(num_days=30):
    start_date = date.today() - timedelta(days=num_days)
    prices = dict(BASE_PRICES) 

    for day_offset in range(num_days):
        trade_date = start_date + timedelta(days=day_offset)
        
        # Skipping weekends
        if trade_date.weekday() >= 5:
            continue

        for symbol, sector in NGX_SYMBOLS.items():
            base = prices[symbol]

            # price movements (±3%)
            change_pct = random.uniform(-0.03, 0.03)
            close = round(base * (1 + change_pct), 2)
            open_  = round(base * (1 + random.uniform(-0.01, 0.01)), 2)
            high   = round(max(open_, close) * (1 + random.uniform(0, 0.015)), 2)
            low    = round(min(open_, close) * (1 - random.uniform(0, 0.015)), 2)
            volume = random.randint(100_000, 10_000_000)
            value  = round(close * volume, 2)
            deals  = random.randint(50, 2000)
            prices[symbol] = close  

            yield ({
                "trade_date":  trade_date.isoformat(),
                "symbol":      symbol,
                "sector":      sector,
                "open":        open_,
                "high":        high,
                "low":         low,
                "close":       close,
                "volume":      volume,
                "value":       value,
                "deals":       deals,
            })

def average_price(symbol, data, price_field="close"):
    symbol = symbol.upper()
    total = 0.0
    count = 0

    if isinstance(data, str):
        with open(data, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["symbol"] == symbol:
                    total += float(row[price_field])
                    count += 1
    else:
        for row in data:
            if row["symbol"] == symbol:
                total += float(row[price_field])
                count += 1

    if count == 0:
        print(f"Symbol '{symbol}' not found.")
        return None

    return total / count

if __name__ == "__main__":
    fieldnames = ["trade_date","symbol","sector","open","high","low","close","volume","value","deals"]
    buffer = []
    total_bytes = 0
    output_file = "ngx_trades.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    try:
        while True:
            trade_generator = generate_trade_data(num_days=60)
            for row in trade_generator:
               buffer.append(row)
               total_bytes += 1160  
               if len(buffer) >= 250000:
                with open(output_file, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writerows(buffer)
                buffer.clear()
                estimated_mb = total_bytes / 1024 ** 2
                print(f"written {estimated_mb:.2f} MB")
                if estimated_mb >= 10000:
                    print("10GB limit reached")
                    sys.exit()

    except KeyboardInterrupt:
        if buffer:
            with open(output_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerows(buffer)

