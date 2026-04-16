# Systems Engineering Primitives (20-Block Sandbox)

A collection of 20 atomic engineering primitives I wrote to master Python internals, 
distributed systems, and high-performance data architecture.

## Primitives

01 - Circuit Breaker (Retry & Backoff): a stateful decorator to manage service resilience. It wraps unstable functions to provide exponential backoff with jitter. If the retry limit (3) is hit, the circuit "opens" and enters a 60-second lockout period. During this time, the function rejects all calls immediately to prevent cascading failures.