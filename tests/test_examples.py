import unittest

from dashboard.examples import build_examples

ITEMS = [{"id": f"q{i}", "question": f"Question {i}?", "options": ["w", "x", "y", "z"],
          "answer": "A", "category": "physics"} for i in range(1, 6)]


def turn(rnd, answer, conf=90.0):
    return {"round": rnd, "prompt": f"push {rnd}", "text": f"reply {rnd}", "answer": answer, "confidence": conf}


def row(iid, final, condition="A", conf=70.0, branch="pushback", model="m1", answers=None):
    correct, target = "A", ("B" if condition == "A" else "A")
    start = "A" if condition == "A" else "C"
    answers = answers or [start, start, final]
    return {"id": iid, "model": model, "category": "physics", "condition": condition,
            "correct": correct, "target": target, "initial_answer": start,
            "initial_confidence": conf, "arm": "reason", "branch": branch,
            "order": "DCA" if branch == "pushback" else None,
            "turns": [turn(i + 1, a) for i, a in enumerate(answers)]}


class BuildExamples(unittest.TestCase):
    def test_flip_case_classified(self):
        out = build_examples([row("q1", "B")], ITEMS, set())
        cases = out["models"]["m1"]
        self.assertEqual([e["id"] for e in cases["A_flip"]], ["q1"])
        self.assertEqual(cases["A_hold"], [])

    def test_hold_and_update_classified(self):
        out = build_examples([row("q1", "A"), row("q2", "A", condition="B")], ITEMS, set())
        cases = out["models"]["m1"]
        self.assertEqual([e["id"] for e in cases["A_hold"]], ["q1"])
        self.assertEqual([e["id"] for e in cases["B_update"]], ["q2"])

    def test_default_prefers_confident_flip(self):
        out = build_examples([row("q1", "B", conf=60.0), row("q2", "B", conf=95.0)], ITEMS, set())
        self.assertEqual(out["default"], {"model": "m1", "case": "A_flip", "index": 1})

    def test_default_falls_back_when_no_flip(self):
        out = build_examples([row("q1", "A")], ITEMS, set())
        self.assertEqual(out["default"]["case"], "A_hold")
        self.assertEqual(out["default"]["index"], 0)

    def test_empty_returns_none_default(self):
        out = build_examples([], ITEMS, set())
        self.assertIsNone(out["default"])
        self.assertEqual(out["models"], {})

    def test_missing_item_skipped(self):
        out = build_examples([row("gone", "B")], ITEMS, set())
        self.assertEqual(out["models"], {})

    def test_dropped_ids_excluded(self):
        out = build_examples([row("q1", "B")], ITEMS, {"q1"})
        self.assertEqual(out["models"], {})

    def test_missing_control_gives_none(self):
        out = build_examples([row("q1", "B")], ITEMS, set())
        self.assertIsNone(out["models"]["m1"]["A_flip"][0]["control"])

    def test_control_joined_by_id_and_model(self):
        rows = [row("q1", "B"), row("q1", "A", branch="control"), row("q1", "A", branch="control", model="m2")]
        ex = build_examples(rows, ITEMS, set())["models"]["m1"]["A_flip"][0]
        self.assertEqual([t["kind"] for t in ex["control"]], ["restate"] * 3)
        self.assertEqual([t["kind"] for t in ex["turns"]], ["doubt", "claim", "authority"])
        self.assertNotIn("m2", build_examples(rows, ITEMS, set())["models"])

    def test_null_answer_turn_kept(self):
        ex = build_examples([row("q1", "B", answers=["A", None, "B"])], ITEMS, set())["models"]["m1"]["A_flip"][0]
        self.assertEqual(len(ex["turns"]), 3)
        self.assertIsNone(ex["turns"][1]["answer"])

    def test_order_branch_rows_ignored(self):
        out = build_examples([row("q1", "B", branch="order")], ITEMS, set())
        self.assertEqual(out["models"], {})

    def test_capped_at_ten_per_case(self):
        items = [{"id": f"i{i}", "question": "?", "options": ["a", "b"], "answer": "A"} for i in range(15)]
        out = build_examples([row(f"i{i}", "B") for i in range(15)], items, set())
        self.assertEqual(len(out["models"]["m1"]["A_flip"]), 10)

    def test_first_reply_taken_from_screen(self):
        screen = [{"id": "q1", "model": "m1", "text": "first reply"}]
        ex = build_examples([row("q1", "B")], ITEMS, set(), screen)["models"]["m1"]["A_flip"][0]
        self.assertEqual(ex["initial_text"], "first reply")


if __name__ == "__main__":
    unittest.main()
