# HttpCraft

HttpCraft is a minimal Python tool for crafting and inspecting HTTP requests with headers, cookies, CSRF handling, and history tracking.

## Usage

```python
from http_craft import HttpCraft

client = HttpCraft("http://127.0.0.1:5000")
exchange = client.get("/echo")
client.debug_response(exchange)
