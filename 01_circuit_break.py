import urllib.request
import urllib.parse
import json
import time
from functools import wraps
import datetime
import random

def circuit(condition, times=3, delay=1):
    
    def decorator(func):
        last_failure_time = None 
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_failure_time
            if last_failure_time:
                elapsed = (datetime.datetime.now() - last_failure_time).total_seconds()
                if elapsed < 60:
                    print(f"{60 - int(elapsed)}s remaining")
                    return "Error"
            for attempt in range(1, times + 1):
                result = func(*args, **kwargs)
                if condition(result):
                    last_failure_time = None 
                    return result
                # (delay * 2^attempt) random 0-1 seconds
                wait_time = (delay * (2 ** attempt)) + random.random()
                print(f"Attempt {attempt} failed. Retrying")
                time.sleep(wait_time)
            print("Attempts exhausted. Circuit break 60s ")
            last_failure_time = datetime.datetime.now()
            return 'Error'     
        return wrapper
    return decorator


@circuit(condition=lambda t: t != None, times=3, delay=1)
def call_api(url, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read()
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        # Server responds but with an error status
        print(f"HTTP Error - {e.code} - {e.reason}")

    except urllib.error.URLError as e:
        # I did not get a response at all
        print(f"URL Error - {e.reason}")

    except json.JSONDecodeError:
        # Got a response but it wasn't JSON
        print("Response was not valid JSON")

    return None   
   
