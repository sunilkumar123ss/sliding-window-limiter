import unittest
from main import SlidingWindowLimiter


class SlidingWindowTests(unittest.TestCase):
    def test_same_timestamp_counts_separate_requests(self):
        limiter = SlidingWindowLimiter(2, 10)
        self.assertTrue(limiter.allow(0))
        self.assertTrue(limiter.allow(0))
        self.assertFalse(limiter.allow(0))

    def test_exact_boundary_expires(self):
        limiter = SlidingWindowLimiter(1, 10)
        self.assertTrue(limiter.allow(0))
        self.assertFalse(limiter.allow(9.999))
        self.assertTrue(limiter.allow(10))

    def test_denials_do_not_extend_window(self):
        limiter = SlidingWindowLimiter(1, 10)
        limiter.allow(0)
        self.assertFalse(limiter.allow(9))
        self.assertEqual(limiter.retry_after(9), 1)
        self.assertTrue(limiter.allow(10))

    def test_staggered_expiry(self):
        limiter = SlidingWindowLimiter(3, 10)
        for timestamp in (0, 2, 4):
            limiter.allow(timestamp)
        self.assertEqual(limiter.count(10), 2)
        self.assertEqual(limiter.count(12), 1)
        self.assertEqual(limiter.count(14), 0)

    def test_empty_has_no_delay(self):
        self.assertEqual(SlidingWindowLimiter(1, 10).retry_after(100), 0)

    def test_rejected_requests_advance_clock(self):
        limiter = SlidingWindowLimiter(1, 10)
        limiter.allow(0)
        limiter.allow(5)
        with self.assertRaises(ValueError):
            limiter.allow(4)



if __name__ == '__main__':
    unittest.main()
