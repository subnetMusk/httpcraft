# subnet_musk

import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dataclasses import dataclass
import time
import os
from datetime import datetime

@dataclass
class HttpCraftRequest:
    url: str
    port: int
    path: str
    method: str
    headers: dict
    cookies: dict
    payload: dict

    def to_dict(self):
        return {
            "url": self.url,
            "port": self.port,
            "path": self.path,
            "method": self.method,
            "headers": self.headers,
            "cookies": self.cookies,
            "payload": self.payload
        }

@dataclass
class HttpCraftResponse:
    status_code: int
    elapsed_time: float
    response_type: str
    response_body: any
    raw_headers: dict

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "elapsed_time": self.elapsed_time,
            "response_type": self.response_type,
            "response_body": self.response_body,
            "raw_headers": self.raw_headers
        }

@dataclass
class HttpCraftExchange:
    timestamp: str
    request: HttpCraftRequest
    response: HttpCraftResponse

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "request": self.request.to_dict(),
            "response": self.response.to_dict()
        }


class HttpCraft:
    # Initialize HttpCraft with base URL and default configuration
    def __init__(self, base_url: str):
        parsed = urlparse(base_url)
        self.scheme = parsed.scheme or "http"
        self.host = parsed.hostname
        self.port = parsed.port
        self.base_url = f"{self.scheme}://{self.host}"

        self.headers = {}
        self.payload = {}
        self.cookies = {}
        self.history = {}
        self.session = requests.Session()

        self.csrf_mode = "none"
        self.csrf_field = "csrf_token"

    # Print the current configuration
    def debug_config(self):
        print("--- HttpCraft Configuration ---")
        print("Target URL:", self.base_url)
        print("Host:", self.host)
        print("Port:", self.port if self.port else "default")
        print("CSRF Mode:", self.csrf_mode)
        print("CSRF Field:", self.csrf_field)
        print("Headers:")
        print(json.dumps(self.headers, indent=2))
        print("Cookies:")
        print(json.dumps(self.cookies, indent=2))
        print("Payload:")
        print(json.dumps(self.payload, indent=2))

    # Reset all configuration and state
    def reset(self):
        self.base_url = ""
        self.headers = {}
        self.payload = {}
        self.cookies = {}

    ''' --------- TARGET --------- '''
    # Build full URL using base, host, and optional override port
    def _build_url(self, path: str, override_port: int = None):
        port = override_port if override_port is not None else self.port
        base = f"{self.scheme}://{self.host}"
        if port:
            base += f":{port}"
        return f"{base}/{path.lstrip('/')}"

    # Set a new target URL
    def set_target(self, url):
        parsed = urlparse(url)
        self.scheme = parsed.scheme or "http"
        self.host = parsed.hostname
        self.port = parsed.port
        self.base_url = f"{self.scheme}://{self.host}"

    # Get the current target URL
    def get_target(self):
        return self.base_url

    # Set port manually
    def set_port(self, port: int):
        self.port = port

    # Get the current port
    def get_port(self):
        return self.port

    # Reset only the target and port
    def reset_target(self):
        self.base_url = ""
        self.port = None
    ''' -------------------------- '''

    ''' ---------- CSRF ---------- '''
    # Configure CSRF handling and token field name
    def set_csrf(self, mode="input", field="csrf_token"):
        assert mode in ["none", "input", "meta"]
        self.csrf_mode = mode
        self.csrf_field = field

    # Extract CSRF token from HTML based on mode
    def extract_csrf_token(self, html):
        soup = BeautifulSoup(html, "html.parser")
        if self.csrf_mode == "input":
            tag = soup.find("input", {"type": "hidden", "name": self.csrf_field})
            return tag["value"] if tag and tag.has_attr("value") else None
        elif self.csrf_mode == "meta":
            tag = soup.find("meta", {"name": self.csrf_field})
            return tag["content"] if tag and tag.has_attr("content") else None
        return None
    ''' -------------------------- '''

    ''' -------- HEADERS --------- '''
    # Set full headers dictionary
    def set_headers(self, headers):
        self.headers = headers

    # Get all headers
    def get_headers(self):
        return self.headers

    # Set or update a single header
    def set_header_entry(self, key, value):
        self.headers[key] = value

    # Get a specific header
    def get_header_entry(self, key):
        return self.headers.get(key, "no entry for this key")

    # Remove a specific header
    def remove_header_entry(self, key):
        if key in self.headers:
            del self.headers[key]

    # Append or update multiple headers
    def append_headers(self, new_data: dict):
        self.headers.update(new_data)

    # Clear all headers
    def clear_headers(self):
        self.headers = {}
    ''' -------------------------- '''

    ''' -------- PAYLOAD --------- '''
    # Set the entire payload dictionary
    def set_payload(self, payload):
        self.payload = payload

    # Get the entire payload
    def get_payload(self):
        return self.payload

    # Set or update a single payload entry
    def set_payload_entry(self, key, value):
        self.payload[key] = value

    # Get a specific payload entry
    def get_payload_entry(self, key):
        return self.payload.get(key, "no entry for this key")

    # Remove a specific entry from payload
    def remove_payload_entry(self, key):
        if key in self.payload:
            del self.payload[key]

    # Append or update multiple payload entries
    def append_payload(self, new_data: dict):
        self.payload.update(new_data)

    # Clear the payload
    def clear_payload(self):
        self.payload = {}
    ''' -------------------------- '''

    ''' -------- COOKIES --------- '''
    # Set all cookies
    def set_cookies(self, cookies):
        self.cookies = cookies

    # Get all cookies
    def get_cookies(self):
        return self.cookies

    # Add or update a single cookie
    def add_cookie(self, key, value):
        self.cookies[key] = value

    # Get a specific cookie
    def get_cookie(self, key):
        return self.cookies.get(key, "no entry for this key")

    # Remove a specific cookie
    def remove_cookie(self, key):
        if key in self.cookies:
            del self.cookies[key]

    # Append or update multiple cookies
    def append_cookies(self, new_data: dict):
        self.cookies.update(new_data)

    # Clear all cookies
    def clear_cookies(self):
        self.cookies = {}
    ''' -------------------------- '''

    ''' -------- FILE IMPORT/EXPORT -------- '''
    # Save the current configuration to a JSON file
    def save_config_to_file(self, filepath):
        try:
            config = {
                "base_url": self.base_url,
                "host": self.host,
                "port": self.port,
                "csrf_mode": self.csrf_mode,
                "csrf_field": self.csrf_field,
                "headers": self.headers,
                "cookies": self.cookies,
                "payload": self.payload
            }
            with open(filepath, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"[+] Configuration saved to '{filepath}'")
        except Exception as e:
            print(f"[!] Error saving configuration: {e}")

    # Load a configuration from a JSON file
    def load_config_from_file(self, filepath):
        if not os.path.isfile(filepath):
            print(f"[!] File '{filepath}' does not exist.")
            return
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
                self.base_url = config.get("base_url", "")
                self.host = config.get("host", "")
                self.port = config.get("port")
                self.csrf_mode = config.get("csrf_mode", "none")
                self.csrf_field = config.get("csrf_field", "csrf_token")
                self.headers = config.get("headers", {}) if isinstance(config.get("headers"), dict) else {}
                self.cookies = config.get("cookies", {}) if isinstance(config.get("cookies"), dict) else {}
                self.payload = config.get("payload", {}) if isinstance(config.get("payload"), dict) else {}
            print(f"[+] Configuration loaded from '{filepath}'")
        except Exception as e:
            print(f"[!] Error loading configuration: {e}")

    # Load payload from file
    def load_payload_from_file(self, filepath):
        with open(filepath, 'r') as f:
            self.payload = json.load(f)

    # Save payload to file
    def save_payload_to_file(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.payload, f, indent=4)

    # Load headers from file
    def load_headers_from_file(self, filepath):
        with open(filepath, 'r') as f:
            self.headers = json.load(f)

    # Save headers to file
    def save_headers_to_file(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.headers, f, indent=4)

    # Load cookies from file
    def load_cookies_from_file(self, filepath):
        with open(filepath, 'r') as f:
            self.cookies = json.load(f)

    # Save cookies to file
    def save_cookies_to_file(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.cookies, f, indent=4)
    
    # Save the full request history to a JSON file
    def save_history_to_file(self, filepath):
        try:
            history_dict = {
                ts: exchange.to_dict()
                for ts, exchange in self.history.items()
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(history_dict, f, indent=2, ensure_ascii=False)

            print(f"[+] Request history successfully saved to '{filepath}'")
        except Exception as e:
            print(f"[!] Error saving request history: {e}")
    ''' -------------------------- '''


    ''' -------- REQUESTS -------- '''
    # Send a GET request to the specified path
    def get(self, path="", params=None, port=None):
        return self._send_request("GET", path, data=params, port=port)

    # Send a POST request to the specified path
    def post(self, path="", json=None, port=None):
        return self._send_request("POST", path, data=json, port=port)

    # Send a PUT request to the specified path
    def put(self, path="", json=None, port=None):
        return self._send_request("PUT", path, data=json, port=port)

    # Send a DELETE request to the specified path
    def delete(self, path="", json=None, port=None):
        return self._send_request("DELETE", path, data=json, port=port)

    # Send a PATCH request to the specified path
    def patch(self, path="", json=None, port=None):
        return self._send_request("PATCH", path, data=json, port=port)

    # Send a HEAD request to the specified path
    def head(self, path="", port=None):
        return self._send_request("HEAD", path, data=None, port=port)

    # Core method used by all HTTP verb wrappers above
    from datetime import datetime

    # Core method used by all HTTP verb wrappers above
    def _send_request(self, method, path, data=None, port=None):
        url = self._build_url(path, override_port=port)
        start = time.time()

        request_func = getattr(self.session, method.lower())
        kwargs = {
            "headers": self.headers,
            "cookies": self.cookies
        }

        if method in ["GET", "HEAD"]:
            kwargs["params"] = data or self.payload
        else:
            kwargs["json"] = data or self.payload

        response = request_func(url, **kwargs)
        elapsed = time.time() - start

        # Detect response type and body format
        content_type = response.headers.get("Content-Type", "").lower()

        if "application/json" in content_type:
            response_type = "json"
            try:
                response_body = response.json()
            except Exception:
                response_body = response.text
        elif "text/html" in content_type:
            response_type = "html"
            response_body = response.text
        elif "text" in content_type:
            response_type = "text"
            response_body = response.text
        else:
            response_type = "unknown"
            response_body = response.text

        # CSRF token update
        if self.csrf_mode != "none":
            token = self.extract_csrf_token(response.text)
            if token:
                self.add_cookie(self.csrf_field, token)
                print(f"[+] CSRF token '{self.csrf_field}' updated in cookies.")

        sent = response.request
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        http_request = HttpCraftRequest(
            url=self.base_url,
            port=port or self.port,
            path=path,
            method=sent.method,
            headers=dict(sent.headers),
            cookies=self.cookies.copy(),
            payload=data or self.payload
        )

        http_response = HttpCraftResponse(
            status_code=response.status_code,
            elapsed_time=elapsed,
            response_type=response_type,
            response_body=response_body,
            raw_headers=dict(response.headers)
        )

        http_exchange = HttpCraftExchange(
            timestamp=timestamp,
            request=http_request,
            response=http_response
        )

        self.history[timestamp] = http_exchange

        return http_exchange

    # Print detailed information about a single HttpCraftExchange
    def debug_response(self, exchange, limit_body: bool = True):
        req = exchange.request
        res = exchange.response

        print(f"--- {exchange.timestamp} ---")
        print(f"Base URL:     {req.url}")
        print(f"Port:         {req.port}")
        print(f"Path:         {req.path}")
        print(f"Method:       {req.method}")
        print(f"Status Code:  {res.status_code}")
        print(f"Response Type:{res.response_type}")
        print("Headers:")
        print(json.dumps(req.headers, indent=2))
        print("Cookies:")
        print(json.dumps(req.cookies, indent=2))
        print("Payload:")
        print(json.dumps(req.payload, indent=2))
        print(f"Elapsed Time: {round(res.elapsed_time * 1000, 2)} ms")

        print("Response Body:")
        body = res.response_body
        if isinstance(body, dict):
            print(json.dumps(body, indent=2))
        else:
            body_str = str(body)
            print(body_str[:500] + ("..." if limit_body and len(body_str) > 500 else ""))

        print("------------------------------\n")


    # Print a readable summary of the request history
    def print_history(self):
        if not self.history:
            print("[!] No request history available.")
            return

        for timestamp, exchange in sorted(self.history.items()):
            req = exchange.request
            res = exchange.response

            print(f"--- {timestamp} ---")
            print(f"Base URL:     {req.url}")
            print(f"Port:         {req.port}")
            print(f"Path:         {req.path}")
            print(f"Method:       {req.method}")
            print(f"Status Code:  {res.status_code}")
            print(f"Response Type:{res.response_type}")
            print("Headers:")
            print(json.dumps(req.headers, indent=2))
            print("Cookies:")
            print(json.dumps(req.cookies, indent=2))
            print("Payload:")
            print(json.dumps(req.payload, indent=2))
            print(f"Elapsed Time: {round(res.elapsed_time * 1000, 2)} ms")
            print("Response Body:")
            body = res.response_body
            if isinstance(body, dict):
                print(json.dumps(body, indent=2))
            else:
                print(body[:500] + ("..." if isinstance(body, str) and len(body) > 500 else ""))
            print("------------------------------\n")


    ''' -------------------------- '''

