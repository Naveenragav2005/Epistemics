import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from dashboard import server


class Routes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        cls.base = f"http://127.0.0.1:{cls.srv.server_address[1]}"
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def get(self, path):
        with urllib.request.urlopen(self.base + path, timeout=120) as r:
            return r.status, r.read().decode()

    def test_root_serves_explainer(self):
        status, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("<!-- page:explainer -->", body)

    def test_live_serves_dashboard(self):
        status, body = self.get("/live")
        self.assertEqual(status, 200)
        self.assertIn("<!-- page:live -->", body)

    def test_nav_css_served(self):
        status, body = self.get("/nav.css")
        self.assertEqual(status, 200)
        self.assertIn(".nav", body)

    def test_examples_endpoint_json(self):
        status, body = self.get("/api/examples")
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertIn("models", data)
        self.assertIn("default", data)

    def test_examples_respect_key_exclusions(self):
        bad = server.excluded_ids()
        data = json.loads(self.get("/api/examples?exclude_bad_keys=1")[1])
        ids = {e["id"] for cases in data["models"].values() for exs in cases.values() for e in exs}
        self.assertFalse(ids & bad)

    def test_data_has_takeaways(self):
        data = json.loads(self.get("/api/data")[1])
        self.assertIsInstance(data["takeaways"], dict)
        self.assertEqual(set(data["takeaways"]), {h["model"] for h in data["headline"]})

    def test_unknown_404(self):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self.get("/nope")
        self.assertEqual(cm.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
