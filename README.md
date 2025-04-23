# HttpCraft

**HttpCraft** is a minimal, extensible Python library for crafting, sending and debugging HTTP requests with JSON or form payloads. It offers precise control over headers, cookies, CSRF tokens, and logging of request/response history.

It is built on top of the excellent [requests](https://docs.python-requests.org/en/latest/) library, providing a structured and developer-friendly layer for advanced HTTP usage.

---


## 📦 Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/subnetMusk/httpcraft.git
```

Or, if you want the `httpcraft` CLI to be available **system-wide**, run:

```bash
sudo pip install git+https://github.com/subnetMusk/httpcraft.git
```

> ⚠️ Warning: Using `sudo pip` is generally discouraged, but valid for trusted tools like this.

---


## 🛠 Requirements

- Python 3.7+
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

For development:

```bash
pip install -r requirements-dev.txt
```

---


## 🧠 Core Data Types

### `HttpCraftRequest`
Metadata about the request sent:
```python
HttpCraftRequest(
    url: str,
    port: int,
    path: str,
    method: str,
    headers: dict,
    cookies: dict,
    payload: dict,
    payload_type: str  # either "json" or "form"
)
```

### `HttpCraftResponse`
Metadata about the HTTP response:
```python
HttpCraftResponse(
    status_code: int,
    elapsed_time: float,
    response_type: str,  # "json", "html", "text", "binary", "unknown"
    response_body: str | dict | bytes,
    raw_headers: dict
)
```

### `HttpCraftExchange`
Represents a complete request-response exchange:
```python
HttpCraftExchange(
    timestamp: str,
    request: HttpCraftRequest,
    response: HttpCraftResponse,
    csrf_token_updated: bool
)
```

---


## 🔧 API Overview

### 🎯 Target configuration
```python
set_target(url)
get_target()
set_port(port)
get_port()
reset_target()
```


### 🧾 Payload management
```python
set_payload(data, mode="json")
get_payload()
get_payload_mode()
set_payload_entry(key, value)
get_payload_entry(key)
remove_payload_entry(key)
append_payload(dict)
clear_payload()
```


### 🧠 Header handling
```python
set_headers(dict)
get_headers()
set_header_entry(key, value)
get_header_entry(key)
remove_header_entry(key)
append_headers(dict)
clear_headers()
```


### 🍪 Cookie handling
```python
set_cookies(dict)
get_cookies()
add_cookie(key, value)
get_cookie(key)
remove_cookie(key)
append_cookies(dict)
clear_cookies()
```


### 🔒 CSRF token management
```python
set_csrf(mode: str = "input", field: str = "csrf_token")
extract_csrf_token(html: str) -> str | None
```


### 📡 HTTP requests
```python
get(path="", params=None, port=None)
post(path="", json=None, data=None, port=None)
put(path="", json=None, data=None, port=None)
delete(path="", json=None, data=None, port=None)
patch(path="", json=None, data=None, port=None)
head(path="", port=None)
```
Each method returns a `HttpCraftExchange`.


### 🧾 File operations
```python
save_config_to_file(filepath)
load_config_from_file(filepath)
save_payload_to_file(filepath)
load_payload_from_file(filepath)
save_headers_to_file(filepath)
load_headers_from_file(filepath)
save_cookies_to_file(filepath)
load_cookies_from_file(filepath)
save_history_to_file(filepath)
save_response_to_file(exchange, filepath=None)
save_last_response_to_file(filepath=None)
save_response_from_history_to_file(index: int, filepath=None)
```


### 🐛 Debugging & History
```python
debug_exchange(exchange, limit_body=True)
print_history()
print_last_exchange()
print_exchange_from_history(index)
get_exchange(index)
reset_history()
```

---


## 🚀 CLI Usage

After installation, you can run from terminal:

```bash
httpcraft --run-tests
```

This automatically:
- Starts a local Flask server (`mock_server.py`)
- Runs all integration tests
- Cleans up afterward

To run in verbose mode:

```bash
httpcraft --run-tests --verbose
```

To display help:

```bash
httpcraft --help
```

---

## ✅ Test Behavior

Tests are divided into two categories:

### 🔹 Standard Integration Tests
These run automatically with the CLI using:

```bash
httpcraft --run-tests
```

They include tests for:
- GET, POST, PUT, DELETE, PATCH, HEAD methods
- JSON and form payloads
- Cookie and CSRF token handling
- History tracking and basic output

The CLI launches a mock Flask server (`mock_server.py`) and executes these tests in isolation.

---

### 🔸 Local Manual Tests
Optional test scripts are available in:

```
httpcraft/tests/locals/
```

These include:
- HTML content with embedded images and legal disclaimers
- Image and binary file downloads to verify MIME handling and file integrity
- Timestamp-based file naming to validate consistency
- Manual inspection flows for edge-case content types

To run the full manual test sequence in one step:

```bash
python httpcraft/tests/locals/run_all_manual_tests.py
```

This script will:
- Launch the mock server
- Run the manual saving tests
- Shut down the server automatically afterward

These tests are not part of the automated suite and are intended for manual development/debugging only.


## 📁 Project Structure

```
httpcraft/
├── httpcraft/
│   ├── __init__.py
│   ├── cli.py
│   ├── core.py
│   └── tests/
│       ├── __init__.py
│       ├── test_httpcraft.py
│       ├── runtests.py
│       ├── mock_server.py
│       └── locals/
│           ├── mock_saver_server.py
│           ├── test_saving_script.py
│           ├── run_all_manual_tests.py
│           ├── test_image.png
│           └── responses/
├── README.md
├── setup.py
├── setup.cfg
├── requirements.txt
├── requirements-dev.txt
```
---


## 📄 License

MIT License. Built with 💬@#$%! by subnetMusk.