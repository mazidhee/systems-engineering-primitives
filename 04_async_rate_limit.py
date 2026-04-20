import asyncio
import aiohttp
import time

class AsyncScraper:
    def __init__(self, rate_limit: int, workers: int = 100):
        self.rate_limit = rate_limit
        self.workers = workers
        self.tokens = rate_limit
        self.last_refill = time.monotonic()
        self.lock = asyncio.Lock()

    async def _wait_for_token(self):
        while True:
            async with self.lock:
                now = time.monotonic()
                elapsed = now - self.last_refill
                self.tokens = min(self.rate_limit, self.tokens + elapsed * self.rate_limit)
                self.last_refill = now
                if self.tokens >= 1:
                    self.tokens -= 1
                    return
            await asyncio.sleep(1 / self.rate_limit)

    async def fetch_one(self, session, url, idx):
        await self._wait_for_token()
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                status = response.status
                await response.read()
                if idx % 500 == 0:
                    print(f"Task {idx} fetched (Status {status})")
                return status
        except Exception as e:
            print(f"Task {idx} failed: {e}")
            return None

    async def worker(self, session, queue, results):
        while True:
            item = await queue.get()
            if item is None:  #pill 
                queue.task_done()
                break
            idx, url = item
            result = await self.fetch_one(session, url, idx)
            results[idx] = result
            queue.task_done()

    async def run(self, urls):
        queue = asyncio.Queue(maxsize=200)
        results = [None] * len(urls)

        connector = aiohttp.TCPConnector(limit=self.workers)
        async with aiohttp.ClientSession(connector=connector) as session:
            worker_tasks = [
                asyncio.create_task(self.worker(session, queue, results))
                for _ in range(self.workers)
            ]
            for idx, url in enumerate(urls):
                await queue.put((idx, url)) 
            for _ in range(self.workers):
                await queue.put(None)

            await asyncio.gather(*worker_tasks)

        return results


async def main():
    urls = ["https://httpbin.org/get"] * 10000
    scraper = AsyncScraper(rate_limit=50, workers=100)

    print(f"Starting to fetch {len(urls)} URLs at {scraper.rate_limit} RPS")
    start = time.time()
    results = await scraper.run(urls)
    elapsed = time.time() - start

    successes = sum(1 for r in results if r is not None)
    print(f"Done: {successes}/{len(urls)} succeeded")
    print(f"time: {elapsed:.2f}s")
    print(f"RPS: {len(urls) / elapsed:.2f}")

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())