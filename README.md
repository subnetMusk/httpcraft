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
    response_type: str,  # "json", "html", "text", "unknown"
    response_body: str | dict,
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
```


### 🐛 Debugging & History
```python
debug_exchange(exchange, limit_body=True)
print_history()
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

Tests run automatically in CLI mode with `--run-tests` and do **not require any manual setup**. A local test server is launched automatically.

---


## 📁 Project Structure

```
httpcraft/
├── httpcraft/
│   ├── __init__.py
│   ├── cli.py
│   └── httpcraft.py
├── tests/
│   ├── __init__.py
│   ├── mock_server.py
│   ├── runtests.py
│   └── test_httpcraft.py
├── README.md
├── setup.py
├── setup.cfg
├── requirements.txt
├── requirements-dev.txt
```
---


## 📄 License

MIT License. Built with ❤️ by subnetMusk.