# Systems Engineering Primitives (20-Block Sandbox)

A collection of 20 atomic engineering primitives I wrote to master Python internals, 
distributed systems, and high-performance data architecture.

## Primitives

01 - Circuit Breaker (Retry & Backoff): a stateful decorator to manage service resilience. It wraps unstable functions to provide exponential backoff with jitter. If the retry limit (3) is hit, the circuit "opens" and enters a 60-second lockout period. During this time, the function rejects all calls immediately to prevent cascading failures.

02 - Memory safe generator: a two-part primitive for generating and querying large files under a fixed RAM budget. The generator simulates 60 days of NGX stock market trade data across 75 symbols, producing realistic OHLCV rows with ±3% daily price movement. It buffers 250,000 rows in memory, flushes to disk, then clears, repeating until 10GB is written. The streamer queries the resulting file one row at a time using a running total and count, computing the average close price of any symbol without ever loading more than a single row into RAM.