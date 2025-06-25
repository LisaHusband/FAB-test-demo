import asyncio
import httpx
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm
import threading

BASE_URL = "http://127.0.0.1:5000"
LOGIN_URL = f"{BASE_URL}/login/"
CATEGORIES = ['Test', 'Demo', 'Other', 'CategoryA', 'CategoryB']

REQUESTS_PER_CATEGORY = 100
PAGE_SIZE = 500

total_requests = 0
correct_requests = 0
lock = threading.Lock()

async def login() -> httpx.AsyncClient | None:
    client = httpx.AsyncClient(follow_redirects=True)
    try:
        resp = await client.get(LOGIN_URL)
        soup = BeautifulSoup(resp.text, "html.parser")
        csrf_input = soup.find("input", {"name": "csrf_token"})
        if not csrf_input:
            print("CSRF token not found")
            await client.aclose()
            return None
        csrf_token = csrf_input["value"]
        login_data = {
            "username": "admin",
            "password": "admin",
            "csrf_token": csrf_token,
            "next": "/"
        }
        resp = await client.post(LOGIN_URL, data=login_data)
        if str(resp.url).endswith("/"):
            print("Login successful")
            return client  # ✅ 返回未关闭的 client
        else:
            print("Login failed")
            await client.aclose()
            return None
    except Exception as e:
        print(f"Login exception: {e}")
        await client.aclose()
        return None

async def fetch_and_check(client: httpx.AsyncClient, category: str, pbar: tqdm):
    global total_requests, correct_requests
    for i in range(REQUESTS_PER_CATEGORY):
        q_param = f"(filters:!((col:category,opr:eq,value:'{category}')))"
        url = f"{BASE_URL}/api/v1/item/?q={q_param}&page_size={PAGE_SIZE}"
        try:
            resp = await client.get(url, timeout=10.0)
        except Exception as e:
            print(f"[{category}][{i+1}] Request exception: {e}")
            pbar.update(1)
            continue

        with lock:
            total_requests += 1

        if resp.status_code != 200:
            print(f"[{category}][{i+1}] Request failed with status {resp.status_code}")
            pbar.update(1)
            continue

        try:
            data = resp.json()
        except Exception as e:
            print(f"[{category}][{i+1}] JSON parse error: {e}")
            pbar.update(1)
            continue

        items = data.get('result', [])
        incorrect_items = [item for item in items if item.get('category') != category]
        if incorrect_items:
            print(f"[{category}][{i+1}] ERROR: Incorrect category: {incorrect_items}")
        else:
            with lock:
                correct_requests += 1
        pbar.update(1)

async def run_once(run_index=1):
    client = await login()
    if not client:
        return

    tasks = []
    pbars = []
    for idx, cat in enumerate(CATEGORIES):
        pbar = tqdm(total=REQUESTS_PER_CATEGORY, desc=f"[Run {run_index}] {cat}", position=idx)
        task = fetch_and_check(client, cat, pbar)
        tasks.append(task)
        pbars.append(pbar)

    await asyncio.gather(*tasks)
    for p in pbars:
        p.close()
    await client.aclose()

async def main():
    for i in tqdm(range(5), desc="Overall Progress"):
        await run_once(i + 1)

    accuracy = correct_requests / total_requests if total_requests > 0 else 0
    print(f"\nTotal requests: {total_requests}")
    print(f"Correct requests: {correct_requests}")
    print(f"Accuracy: {accuracy:.2%}")

if __name__ == "__main__":
    asyncio.run(main())
