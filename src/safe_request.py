import time
import requests

_last_request_time = 0


def safe_get(url, max_retries=6, min_interval=3.0):
    global _last_request_time

    now = time.time()
    elapsed = now - _last_request_time
    if elapsed < min_interval:
        wait = min_interval - elapsed
        print(f"[THROTTLE] Waiting {wait:.2f}s before next request...")
        time.sleep(wait)

    delay = 1

    for attempt in range(1, max_retries + 1):
        r = requests.get(url)
        _last_request_time = time.time()

        if r.status_code == 429:
            print(f"[429] Rate limit exceeded. Waiting {delay}s before retry {attempt}/{max_retries}...")
            time.sleep(delay)
            delay *= 2
            continue

        if r.status_code >= 400:
            print(f"[ERROR] HTTP {r.status_code} for {url}")
            r.raise_for_status()

        return r

    raise Exception("Too many retries. Tatum gateway still returning 429.")
