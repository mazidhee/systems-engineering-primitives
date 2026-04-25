# Sandbox

A collection of atomic primitives I wrote to master python internals, distributed systems, and high-performance data architecture.

## Primitives

01 - Circuit Breaker (Retry & Backoff): a stateful decorator to manage service resilience. It wraps unstable functions to provide exponential backoff with jitter. If the retry limit (3) is hit, the circuit "opens" and enters a 60-second lockout period. During this time, the function rejects all calls immediately to prevent cascading failures.

02 - Memory safe generator: a two-part primitive for generating and querying large files under a fixed RAM budget. The generator simulates 60 days of NGX stock market trade data across 75 symbols, producing realistic OHLCV rows with ±3% daily price movement. It buffers 250,000 rows in memory, flushes to disk, then clears, repeating until 10GB is written. The streamer queries the resulting file one row at a time using a running total and count, computing the average close price of any symbol without ever loading more than a single row into RAM.

03 - Thread safe message queue: simulating an exchange floor using threading.Lock and collections.deque. It manages 5 producer threads generating trade orders and 3 consumer threads validating them against a stateful, fluctuating market price dictionary. The system prevents race conditions and data duplication during simultaneous queue access and implements a "poison pill" shutdown pattern to ensure every message is processed before the threads join and the process terminates.

04 - Rate-Limited Token Bucket: fetches 10,000 URLs using asyncio and aiohttp under a strict 50 requests-per-second ceiling. A token bucket refills continuously at the rate limit and is consumed before each request. A fixed pool of 100 workers pulls from a bounded queue (maxsize=200), creating natural backpressure so the event loop is never flooded with thousands of live coroutines simultaneously. Rate control and concurrency control are kept separate, so the bucket governs RPS, the worker pool governs parallelism.

05 - Write-Ahead Log (WAL): a tiny database implementation focused on core database internals and ACID durability. Before updating the in-memory dictionary, it appends the command (e.g SET AAPL 60000) to a raw text file on disk. If the process is killed mid-run and restarted, the system uses custom logic to parse the text file and rebuild the exact previous state.

06 - LRU Cache with TTL: a from-scratch cache implementation built on a doubly linked list and a hash map, achieving O(1) lookups and evictions without any external dependencies like Redis. The list maintains access order on every get or set, the accessed node is promoted to the head. When capacity is exceeded, the tail node (least recently used) is evicted in constant time. Each entry is stamped with an insertion time and a 5-second TTL; expired keys are invalidated lazily on access rather than via a background sweep.