import unittest
from utils import stitch_logos


class FetchLogos:
    def __init__(self, names):
        self.Names = names
        self.Counter = 0

    def get(self):
        name = self.Names[self.Counter]
        self.Counter += 1
        return name


class LogoServiceTests(unittest.TestCase):
    def test_get_logos(self):
        event_name = 'Liverpool vs Arsenal'
        fetcher = FetchLogos(['Liverpool', 'Arsenal'])
        logos = stitch_logos(event_name, lambda s: fetcher.get())
        self.assertEqual('Liverpool|Arsenal', logos)

    def test_get_logos_first_empty(self):
        event_name = 'Liverpool vs Arsenal'
        fetcher = FetchLogos(['', 'Arsenal'])
        logos = stitch_logos(event_name, lambda s: fetcher.get())
        self.assertEqual('|Arsenal', logos)

    def test_get_logos_second_empty(self):
        event_name = 'Liverpool vs Arsenal'
        fetcher = FetchLogos(['Liverpool', ''])
        logos = stitch_logos(event_name, lambda s: fetcher.get())
        self.assertEqual('Liverpool|', logos)

    def test_get_logos_both_empty(self):
        event_name = 'Liverpool vs Arsenal'
        fetcher = FetchLogos(['', ''])
        logos = stitch_logos(event_name, lambda s: fetcher.get())
        self.assertEqual(None, logos)
