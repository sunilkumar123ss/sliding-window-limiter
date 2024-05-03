"""An exact request-count limiter over the interval (now - window, now]."""
import argparse
from collections import deque
import json
import math


class SlidingWindowLimiter:
    def __init__(self, limit, window_seconds):
        if type(limit) is not int or limit <= 0:
            raise ValueError("limit must be a positive integer")
        if isinstance(window_seconds, bool) or not isinstance(window_seconds, (int, float)):
            raise ValueError("window_seconds must be a finite positive number")
        if not math.isfinite(window_seconds) or window_seconds <= 0:
            raise ValueError("window_seconds must be a finite positive number")
        self.limit = limit
        self.window_seconds = float(window_seconds)
        self._accepted = deque()
        self._last_now = None

    def _prune(self, now):
        if isinstance(now, bool) or not isinstance(now, (int, float)) or not math.isfinite(now):
            raise ValueError("now must be finite")
        if self._last_now is not None and now < self._last_now:
            raise ValueError("clock must not move backwards")
        self._last_now = now
        cutoff = now - self.window_seconds
        while self._accepted and self._accepted[0] <= cutoff:
            self._accepted.popleft()

    def allow(self, now):
        self._prune(now)
        if len(self._accepted) >= self.limit:
            return False
        self._accepted.append(now)
        return True

    def retry_after(self, now):
        self._prune(now)
        if len(self._accepted) < self.limit:
            return 0.0
        return max(0.0, self._accepted[0] + self.window_seconds - now)

    def count(self, now):
        self._prune(now)
        return len(self._accepted)


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    limiter = SlidingWindowLimiter(3, 10)
    events = []
    for timestamp in (0, 2, 3, 4, 9, 10, 11, 12):
        allowed = limiter.allow(timestamp)
        events.append({"at": timestamp, "allowed": allowed,
                       "in_window": limiter.count(timestamp),
                       "retry_after": limiter.retry_after(timestamp)})
    print(json.dumps(events, indent=2))


if __name__ == "__main__":
    main()
