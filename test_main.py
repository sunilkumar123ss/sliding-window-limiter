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







if __name__ == '__main__':
    unittest.main()
