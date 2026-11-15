import unittest

from dashboard.takeaways import takeaway


def h(**kw):
    base = {"model": "m1", "n_right": 15, "n_wrong": 4, "capitulation": 0.27, "update": 1.0,
            "discrimination": 0.73, "conf_right_r0": 95.0, "conf_right_r3": 90.0}
    base.update(kw)
    return base


class Takeaway(unittest.TestCase):
    def test_reports_capitulation_and_update(self):
        s = takeaway(h())
        for part in ("m1", "27%", "15", "100%", "4"):
            self.assertIn(part, s)

    def test_omits_update_when_no_wrong_items(self):
        s = takeaway(h(n_wrong=0, update=None))
        self.assertNotIn("nan", s.lower())
        self.assertNotIn("None", s)
        self.assertNotIn("moved to a correct", s)
        self.assertIn("27%", s)

    def test_omits_capitulation_when_no_right_items(self):
        s = takeaway(h(n_right=0, capitulation=None))
        self.assertNotIn("nan", s.lower())
        self.assertNotIn("None", s)
        self.assertNotIn("abandoned", s)
        self.assertIn("100%", s)

    def test_nan_rate_omitted(self):
        s = takeaway(h(update=float("nan")))
        self.assertNotIn("nan", s.lower())

    def test_no_results_at_all(self):
        s = takeaway(h(n_right=0, n_wrong=0, capitulation=None, update=None))
        self.assertIn("no pushback results", s)

    def test_low_n_flagged(self):
        self.assertIn("n=15", takeaway(h()))


if __name__ == "__main__":
    unittest.main()
