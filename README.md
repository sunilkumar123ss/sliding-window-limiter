# Sliding Window Limiter

Enforce exact request counts over a moving time window.

All bundled examples use synthetic data.

## Run

Requires Python 3.9 or later; no third-party packages or network access are needed.

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

Run these commands from this repository's directory. The demo can also be launched from any directory by passing the absolute path to `main.py`.

## How it works

The limiter stores accepted timestamps in a deque. Before each decision it removes entries at or before `now - window_seconds`, giving the interval `(now - window_seconds, now]`. Accepted requests enter the deque; denied requests do not extend the window. `retry_after()` returns the delay until the oldest accepted request expires.

Memory is O(limit). Each accepted timestamp is added and removed once, giving amortized O(1) pruning work per accepted request.

## Reuse

```python
from main import SlidingWindowLimiter

limiter = SlidingWindowLimiter(limit=2, window_seconds=10)
assert limiter.allow(0)
assert limiter.allow(1)
assert not limiter.allow(2)
assert limiter.retry_after(2) == 8
assert limiter.allow(10)
```

## Demo behavior

The default timeline includes requests immediately before and at an expiry boundary. Repeated timestamps count as separate requests.

## Boundaries

This is an exact log in one process, with no persistence or synchronization. The caller must provide nondecreasing finite timestamps; denied requests and inspections also advance that clock. For very large limits, an approximate bucketed window may use less memory but would have different boundary behavior.

## Verification

`test_main.py` exercises boundary conditions, invalid inputs, and meaningful behavior specific to this implementation. The default demo is deterministic and completes without external services. See the collection's verification report for the recorded run; run the commands above to verify this repository independently.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
