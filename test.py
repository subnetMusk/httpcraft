from http_craft import HttpCraft

# Initialize tool
client = HttpCraft("http://127.0.0.1:5000")

# --- BASIC GET TEST ---
print("Testing GET /echo")
client.set_payload({"test": "value"})
exchange = client.get("/echo")
client.debug_response(exchange)

# --- POST TEST ---
print("Testing POST /echo")
client.set_payload({"user": "admin", "pass": "123"})
exchange = client.post("/echo")
client.debug_response(exchange)

# --- CSRF FORM FETCH AND SUBMIT ---
print("Testing CSRF auto-detection from /form and submission to /submit")
client.set_csrf("input", field="csrf_token")
client.get("/form")  # Extracts CSRF token
client.set_payload({
    "username": "admin",
    "csrf_token": client.get_cookie("csrf_token")
})
exchange = client.post("/submit")
client.debug_response(exchange)

# --- PUT TEST ---
print("Testing PUT /echo")
exchange = client.put("/echo", json={"data": "put test"})
client.debug_response(exchange)

# --- DELETE TEST ---
print("Testing DELETE /echo")
exchange = client.delete("/echo", json={"confirm": True})
client.debug_response(exchange)

# --- PATCH TEST ---
print("Testing PATCH /echo")
exchange = client.patch("/echo", json={"update": "field"})
client.debug_response(exchange)

# --- HEAD TEST ---
print("Testing HEAD /echo")
exchange = client.head("/echo")
client.debug_response(exchange)

# --- History print ---
print("\n=== REQUEST HISTORY ===")
client.print_history()

# --- Save to file ---
client.save_history_to_file("request_history.json")
client.save_config_to_file("session_config.json")
