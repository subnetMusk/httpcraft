# subnet_musk

import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dataclasses import dataclass
import time
import os
from datetime import datetime
import mimetypes
import re

@dataclass
class HttpCraftRequest:
    url: str
    port: int
    path: str
    method: str
    headers: dict
    cookies: dict
    payload: dict
    payload_type: str

    def to_dict(self):
        return {
            "url": self.url,
            "port": self.port,
            "path": self.path,
            "method": self.method,
            "headers": self.headers,
            "cookies": self.cookies,
            "payload": self.payload,
            "payload_type": self.payload_type
        }
    
    def was_json(self):
        return self.payload_type == "json"

    def was_form(self):
        return self.payload_type == "form"

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
    csrf_token_updated: bool = False  # default to False

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "request": self.request.to_dict(),
            "response": self.response.to_dict(),
            "csrf_token_updated": self.csrf_token_updated
        }

class HttpCraft:
    def __init__(self, base_url: str):
        parsed = urlparse(base_url)
        if not parsed.scheme:
            raise ValueError("URL must include a scheme (http:// or https://)")

        self.scheme = parsed.scheme
        self.host = parsed.hostname
        self.port = parsed.port
        self.base_url = f"{self.scheme}://{self.host}"

        self.headers = {}
        self.payload = {}
        self.payload_mode = "json"  # default mode
        self.cookies = {}
        self.history = []
        self.session = requests.Session()

        self.csrf_mode = "none"
        self.csrf_field = "csrf_token"

    # Print the current configuration
    def print_config(self):
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
        print("Payload Mode:", self.payload_mode)
        print("Payload:")
        print(json.dumps(self.payload, indent=2))

    # Reset all configuration and state
    def reset(self):
        self.scheme = "http"
        self.host = ""
        self.port = None
        self.base_url = ""

        self.headers = {}
        self.payload = {}
        self.payload_mode = "json"  # default mode
        self.cookies = {}
        self.history = []
        self.session = requests.Session()

        self.csrf_mode = "none"
        self.csrf_field = "csrf_token"

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
        parsed = urlparse(base_url)
        if not parsed.scheme:
            raise ValueError("URL must include a scheme (http:// or https://)")
        self.scheme = parsed.scheme
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
    # Set the entire payload and its mode ("json" or "form")
    def set_payload(self, payload: dict, mode: str = "json"):
        assert mode in ["json", "form"], "Payload mode must be either 'json' or 'form'"
        self.payload = payload
        self.payload_mode = mode

    # Get the entire payload
    def get_payload(self):
        return self.payload

    # Get the current payload mode ("json" or "form")
    def get_payload_mode(self):
        return self.payload_mode

    # Set or update a single payload entry
    def set_payload_entry(self, key, value):
        self.payload[key] = value

    # Get a specific payload entry
    def get_payload_entry(self, key):
        return self.payload.get(key, "no entry for this key")

    # Remove a specific entry from the payload
    def remove_payload_entry(self, key):
        if key in self.payload:
            del self.payload[key]

    # Append or update multiple entries in the payload
    def append_payload(self, new_data: dict):
        self.payload.update(new_data)

    # Clear the payload completely (but keep current mode)
    def clear_payload(self):
        self.payload = {}
        self.payload_mode = "json"  # reset to default mode
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
                "payload": self.payload,
                "payload_mode": self.payload_mode
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"[+] Configuration saved to '{filepath}'")
        except Exception as e:
            print(f"[!] Error saving configuration: {e}")

    # Load a configuration from a JSON file
    def load_config_from_file(self, filepath):
        if not os.path.isfile(filepath):
            print(f"[!] File '{filepath}' does not exist.")
            return
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.base_url = config.get("base_url", "")
                self.host = config.get("host", "")
                self.port = config.get("port")
                self.csrf_mode = config.get("csrf_mode", "none")
                self.csrf_field = config.get("csrf_field", "csrf_token")
                self.headers = config.get("headers", {}) if isinstance(config.get("headers"), dict) else {}
                self.cookies = config.get("cookies", {}) if isinstance(config.get("cookies"), dict) else {}
                self.payload = config.get("payload", {}) if isinstance(config.get("payload"), dict) else {}
                self.payload_mode = config.get("payload_mode", "json")  # fallback to json if missing
            print(f"[+] Configuration loaded from '{filepath}'")
        except Exception as e:
            print(f"[!] Error loading configuration: {e}")

    # Load payload from file (JSON only)
    def load_payload_from_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.payload = json.load(f)

    # Save payload to file
    def save_payload_to_file(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.payload, f, indent=4, ensure_ascii=False)

    # Load headers from file
    def load_headers_from_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.headers = json.load(f)

    # Save headers to file
    def save_headers_to_file(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.headers, f, indent=4, ensure_ascii=False)

    # Load cookies from file
    def load_cookies_from_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.cookies = json.load(f)

    # Save cookies to file
    def save_cookies_to_file(self, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.cookies, f, indent=4, ensure_ascii=False)

    # Save the full request history to a JSON file
    def save_history_to_file(self, filepath):
        try:
            history_list = [exchange.to_dict() for exchange in self.history]
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(history_list, f, indent=2, ensure_ascii=False)
            print(f"[+] Request history successfully saved to '{filepath}'")
        except Exception as e:
            print(f"[!] Error saving request history: {e}")
 
    # Guess the file extension based on the first few bytes of the response body
    def guess_extension_from_bytes(body: bytes):
        signatures = [
            (b"\x89PNG\r\n\x1a\n", ".png"),
            (b"\xff\xd8\xff", ".jpg"),
            (b"GIF87a", ".gif"),
            (b"GIF89a", ".gif"),
            (b"%PDF", ".pdf"),
            (b"PK\x03\x04", ".zip"),
            (b"Rar!\x1A\x07\x00", ".rar"),
            (b"\x1F\x8B", ".gz"),
            (b"OggS", ".ogg"),
            (b"\x00\x00\x01\xba", ".mpg"),
            (b"\x00\x00\x00\x18ftyp3gp", ".3gp"),
            (b"ID3", ".mp3"),
            (b"\x52\x49\x46\x46", ".wav"),  # RIFF header
        ]
        for sig, ext in signatures:
            if body.startswith(sig):
                return ext
        return ".bin"

    # Save a response to a file based on its content type
    def save_response_to_file(self, exchange, filepath: str = None):
        res = exchange.response
        content_type = res.raw_headers.get("Content-Type", "").split(";")[0].strip().lower()

        # Estensione da MIME (mimetypes + mapping manuale)
        extension = mimetypes.guess_extension(content_type)

        ext_map = {
            "text/plain": ".txt",
            "text/html": ".html",
            "text/css": ".css",
            "text/javascript": ".js",
            "application/javascript": ".js",
            "application/json": ".json",
            "application/xml": ".xml",
            "text/xml": ".xml",
            "application/x-www-form-urlencoded": ".txt",
            "text/csv": ".csv",
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "image/svg+xml": ".svg",
            "image/bmp": ".bmp",
            "image/x-icon": ".ico",
            "image/tiff": ".tiff",
            "font/woff": ".woff",
            "font/woff2": ".woff2",
            "application/font-woff": ".woff",
            "application/font-woff2": ".woff2",
            "application/pdf": ".pdf",
            "application/msword": ".doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/vnd.ms-excel": ".xls",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
            "application/vnd.ms-powerpoint": ".ppt",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
            "application/zip": ".zip",
            "application/x-tar": ".tar",
            "application/x-gzip": ".gz",
            "application/x-7z-compressed": ".7z",
            "application/x-rar-compressed": ".rar",
            "audio/mpeg": ".mp3",
            "audio/wav": ".wav",
            "audio/ogg": ".ogg",
            "video/mp4": ".mp4",
            "video/webm": ".webm",
            "video/ogg": ".ogv",
            "unknown": ".bin"
        }

        if not extension:
            extension = ext_map.get(content_type)

        # fallback su response_type
        if not extension:
            fallback_types = {
                "json": ".json",
                "html": ".html",
                "text": ".txt",
                "unknown": ".bin"
            }
            extension = fallback_types.get(res.response_type, None)

        # fallback finale: sniffa i primi byte
        if not extension:
            body_preview = res.response_body
            if isinstance(body_preview, str):
                body_preview = body_preview.encode("utf-8", errors="ignore")
            extension = guess_extension_from_bytes(body_preview[:32])

        # Filename automatico se non fornito
        if filepath is None:
            sanitized_path = re.sub(r'[^\w\-]+', '_', exchange.request.path.strip("/"))
            filename = f"{exchange.timestamp.replace(':', '').replace(' ', '_')}_{sanitized_path or 'index'}{extension}"
            filepath = os.path.join("responses", filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

        try:
            # Testuale o JSON
            if res.response_type in ["json", "html", "text"] or "text" in content_type or "json" in content_type:
                with open(filepath, "w", encoding="utf-8") as f:
                    if isinstance(res.response_body, (dict, list)):
                        json.dump(res.response_body, f, indent=2, ensure_ascii=False)
                    else:
                        f.write(str(res.response_body))
            else:
                with open(filepath, "wb") as f:
                    body = res.response_body
                    if isinstance(body, str):
                        body = body.encode("utf-8", errors="ignore")
                    f.write(body)
            print(f"[+] Response salvata in '{filepath}'")
        except Exception as e:
            print(f"[!] Errore durante il salvataggio della risposta: {e}")

    # Save the last response to a file
    def save_last_response_to_file(self, filepath: str = None):
        if not self.history:
            print("[!] No request history available.")
            return

        last_exchange = self.history[-1]
        self.save_response_to_file(last_exchange, filepath)

    # Save a specific response from history to a file
    def save_response_from_history_to_file(self, index: int, filepath: str = None):
        if index < 0 or index >= len(self.history):
            print("[!] Invalid index.")
            return

        exchange = self.get_exchange(index)
        if not exchange:
            print("[!] No exchange found at this index.")
            return
        self.save_response_to_file(exchange, filepath)
    ''' -------------------------- '''


    ''' -------- REQUESTS -------- '''
    # Send a GET request to the specified path
    def get(self, path="", params=None, port=None):
        return self._send_request("GET", path, json=None, data=params, port=port)

    # Send a POST request to the specified path
    def post(self, path="", json=None, data=None, port=None):
        return self._send_request("POST", path, json=json, data=data, port=port)

    # Send a PUT request to the specified path
    def put(self, path="", json=None, data=None, port=None):
        return self._send_request("PUT", path, json=json, data=data, port=port)

    # Send a DELETE request to the specified path
    def delete(self, path="", json=None, data=None, port=None):
        return self._send_request("DELETE", path, json=json, data=data, port=port)

    # Send a PATCH request to the specified path
    def patch(self, path="", json=None, data=None, port=None):
        return self._send_request("PATCH", path, json=json, data=data, port=port)

    # Send a HEAD request to the specified path
    def head(self, path="", port=None):
        return self._send_request("HEAD", path, json=None, data=None, port=port)

    # Core method used by all HTTP verb wrappers
    def _send_request(self, method, path, json=None, data=None, port=None):
        url = self._build_url(path, override_port=port)
        start = time.time()

        request_func = getattr(self.session, method.lower())
        kwargs = {
            "headers": self.headers,
            "cookies": self.cookies
        }

        if method in ["GET", "HEAD"]:
            kwargs["params"] = data or self.payload
            payload_used = data or self.payload
            payload_type = "form"
        else:
            if json is not None:
                kwargs["json"] = json
                payload_used = json
                payload_type = "json"
            elif data is not None:
                kwargs["data"] = data
                payload_used = data
                payload_type = "form"
            else:
                if self.payload_mode == "json":
                    kwargs["json"] = self.payload
                    payload_used = self.payload
                    payload_type = "json"
                else:
                    kwargs["data"] = self.payload
                    payload_used = self.payload
                    payload_type = "form"

        response = request_func(url, **kwargs)
        elapsed = time.time() - start

        # Detect response type and body format (updated to handle binary content)
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
        elif "image" in content_type or "application/octet-stream" in content_type:
            response_type = "binary"
            response_body = response.content
        else:
            response_type = "unknown"
            response_body = response.content

        # CSRF token update
        csrf_token_updated = False
        if self.csrf_mode != "none":
            token = self.extract_csrf_token(response.text)
            if token:
                self.add_cookie(self.csrf_field, token)
                csrf_token_updated = True

        sent = response.request
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        http_request = HttpCraftRequest(
            url=self.base_url,
            port=port or self.port,
            path=path,
            method=sent.method,
            headers=dict(sent.headers),
            cookies=self.cookies.copy(),
            payload=payload_used,
            payload_type=payload_type
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
            response=http_response,
            csrf_token_updated=csrf_token_updated
        )

        self.history.append(http_exchange)

        return http_exchange

    # Print detailed information about a single HttpCraftExchange
    def print_exchange(self, exchange, limit_body: bool = True):
        req = exchange.request
        res = exchange.response

        print(f"------------------------------")
        print(f"Timestamp:     {exchange.timestamp}")
        print(f"Base URL:      {req.url}")
        print(f"Port:          {req.port}")
        print(f"Path:          {req.path}")
        print(f"Method:        {req.method}")
        print(f"Status Code:   {res.status_code}")
        print(f"Response Type: {res.response_type}")
        print(f"Payload Mode:  {req.payload_type}")
        print(f"CSRF Updated:  {exchange.csrf_token_updated}")
        print("Headers:")
        print(json.dumps(req.headers, indent=2))
        print("Cookies:")
        print(json.dumps(req.cookies, indent=2))
        print("Payload:")
        print(json.dumps(req.payload, indent=2))
        print(f"Elapsed Time:  {round(res.elapsed_time * 1000, 2)} ms")

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

        index = 0
        for exchange in self.history:
            print(f"[{index}]")
            self.print_exchange(exchange, True)
            index += 1
    
    # Print a summary of the last exchange in the history
    def print_last_exchange(self):
        if not self.history:
            print("[!] No request history available.")
            return

        last_exchange = self.history[-1]
        self.print_exchange(last_exchange, True)
    
    # Print a specific request from the history
    def print_exchange_from_history(self, index):
        if index < 0 or index >= len(self.history):
            print("[!] Invalid index.")
            return

        exchange = self.get_exchange(index)
        if not exchange:
            print("[!] No exchange found at this index.")
            return
        print_exchange(exchange, True)

    # Return a specific request from the history
    def get_exchange(self, index):
        if index < 0 or index >= len(self.history):
            print("[!] Invalid index.")
            return

        return self.history[index]

    # Clear the request history
    def reset_history(self):
        self.history = []
        print("[+] Request history cleared.")

    ''' -------------------------- '''

