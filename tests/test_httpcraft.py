import unittest
import os
import sys
from http_craft import HttpCraft

# Parse verbosity flag
VERBOSE = "--verbose" in sys.argv or os.getenv("HTTPCRAFT_VERBOSE", "false").lower() == "true"
if "--verbose" in sys.argv:
    sys.argv.remove("--verbose")  # Remove custom flag so unittest doesn't complain

def log(msg):
    if VERBOSE:
        print(msg)

class TestHttpCraftFull(unittest.TestCase):
    def setUp(self):
        self.client = HttpCraft("http://127.0.0.1:5000")

    def test_get_echo(self):
        log("TEST: GET /echo")
        self.client.set_payload({"hello": "world"}, mode="form")
        exchange = self.client.get("/echo")
        self.assertEqual(exchange.response.status_code, 200)
        log("  - Status code OK")
        self.assertEqual(exchange.response.response_body.get("args", {}).get("hello"), "world")
        log("  - Payload echoed correctly")

    def test_post_json(self):
        log("TEST: POST /echo with JSON")
        self.client.set_payload({"user": "admin"}, mode="json")
        exchange = self.client.post("/echo")
        self.assertEqual(exchange.response.status_code, 200)
        log("  - Status code OK")
        self.assertEqual(exchange.response.response_body.get("json", {}).get("user"), "admin")
        log("  - JSON payload echoed correctly")

    def test_post_form(self):
        log("TEST: POST /echo with form data")
        self.client.set_payload({"user": "formmode"}, mode="form")
        exchange = self.client.post("/echo")
        self.assertEqual(exchange.response.status_code, 200)
        log("  - Status code OK")
        self.assertEqual(exchange.response.response_body.get("form", {}).get("user"), "formmode")
        log("  - Form payload echoed correctly")

    def test_put_echo(self):
        log("TEST: PUT /echo")
        self.client.set_payload({"put": "yes"}, mode="json")
        exchange = self.client.put("/echo")
        self.assertEqual(exchange.response.status_code, 200)
        log("  - Status code OK")
        self.assertEqual(exchange.response.response_body.get("json", {}).get("put"), "yes")
        log("  - PUT payload echoed correctly")

    def test_patch_echo(self):
        log("TEST: PATCH /echo")
        self.client.set_payload({"patch": "done"}, mode="json")
        exchange = self.client.patch("/echo")
        self.assertEqual(exchange.response.status_code, 200)
        log("  - Status code OK")
        self.assertEqual(exchange.response.response_body.get("json", {}).get("patch"), "done")
        log("  - PATCH payload echoed correctly")

    def test_delete_echo(self):
        log("TEST: DELETE /echo")
        self.client.set_payload({"delete": True}, mode="json")
        exchange = self.client.delete("/echo")
        self.assertEqual(exchange.response.status_code, 200)
        log("  - Status code OK")
        self.assertTrue(exchange.response.response_body.get("json", {}).get("delete"))
        log("  - DELETE payload echoed correctly")

    def test_head_echo(self):
        log("TEST: HEAD /echo (basic)")
        exchange = self.client.head("/echo")
        self.assertEqual(exchange.response.status_code, 200)
        log("  - Status code OK")
        self.assertIn(exchange.response.response_type, ["json", "text", "unknown"])
        log("  - Response type classified")

    def test_head_echo_detailed(self):
        log("TEST: HEAD /echo (detailed checks)")
        exchange = self.client.head("/echo")
        self.assertEqual(exchange.response.status_code, 200)
        log("  - Status code OK")
        self.assertIsInstance(exchange.response.raw_headers, dict)
        self.assertIn("Content-Type", exchange.response.raw_headers)
        log("  - Content-Type header found")
        self.assertIsInstance(exchange.response.response_body, str)
        self.assertLessEqual(len(exchange.response.response_body.strip()), 1)
        log("  - Body is empty or near empty")
        self.assertIn(exchange.response.response_type, ["json", "text", "html", "unknown"])
        log("  - Response type classified")
        self.assertLess(exchange.response.elapsed_time, 0.5)
        log("  - Request completed under 500ms")

    def test_csrf_form_submission(self):
        log("TEST: CSRF token auto-extraction + form POST")
        self.client.set_csrf("input", field="csrf_token")
        self.client.get("/form")
        token = self.client.get_cookie("csrf_token")
        self.assertEqual(token, "secure123")
        log("  - CSRF token extracted successfully")
        self.client.set_payload({"username": "admin", "csrf_token": token}, mode="form")
        exchange = self.client.post("/submit")
        self.assertTrue(exchange.response.response_body.get("token_valid"))
        log("  - CSRF token accepted in form POST")

    def test_cookie_handling(self):
        log("TEST: Cookie setting and sending")
        self.client.get("/set_cookie")
        self.client.add_cookie("sessionid", "abc123")
        session = self.client.get_cookie("sessionid")
        self.assertEqual(session, "abc123")
        log("  - Cookie manually stored in client")
        exchange = self.client.get("/echo")
        self.assertIn("sessionid", exchange.response.response_body.get("cookies", {}))
        log("  - Cookie sent back and received by server")

    def test_history_tracking(self):
        log("TEST: History tracking and payload recording")
        self.client.set_payload({"track": "yes"}, mode="json")
        exchange = self.client.post("/echo")
        self.assertIn(exchange.timestamp, self.client.history)
        log("  - Exchange recorded in history")
        self.assertEqual(exchange.request.payload.get("track"), "yes")
        self.assertEqual(exchange.request.payload_type, "json")
        log("  - Payload and type tracked correctly")

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=0 if not VERBOSE else 2)
    suite = unittest.defaultTestLoader.discover("tests")
    result = runner.run(suite)

    if not VERBOSE and result.wasSuccessful():
        print("Running tests with verbose=False... All tests passed successfully.")