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

    for attempt in range(1, max_retries + 1):
        try:
            r = requests.get(url, timeout=10)

            if r.status_code == 404:
                print(f"[ERROR] 404 Not Found for {url}")
                return {"error": "endpoint_not_available"}

            if r.status_code == 429:
                delay = 2 ** (attempt - 1)
                print(f"[429] Rate limit exceeded. Waiting {delay}s before retry {attempt}/{max_retries}...")
                time.sleep(delay)
                continue

            r.raise_for_status()

            _last_request_time = time.time()
            return r.json()

        except requests.exceptions.RequestException as e:
            print(f"[NETWORK ERROR] {e}")
            time.sleep(1)

    return {"error": "tatum_unavailable"}
