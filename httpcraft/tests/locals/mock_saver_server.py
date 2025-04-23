
from flask import Flask, send_file, jsonify, make_response

app = Flask(__name__)

@app.route("/test/json")
def test_json():
    return jsonify({"status": "ok", "type": "json"})

@app.route("/test/html")
def test_html():
    html = """
    <html>
        <body>
            <div class="content">
                <p>This page is used to verify that the client correctly interprets and saves HTML content.</p>
                <img src="http://localhost:5050/test/image" alt="Sample image" style="max-width: 300px; display: block; margin-top: 1em;" />
                <p class="notice">
                    The image shown via this test was downloaded from the internet and is assumed to be in the public domain.
                    It is used here solely for illustrative purposes. No copyright ownership is claimed.
                </p>
            </div>
        </body>
    </html>
    """
    response = make_response(html)
    response.headers["Content-Type"] = "text/html"
    return response

@app.route("/test/image")
def test_image():
    # This image was downloaded from the internet and is assumed to be public domain.
    # It is used here for illustrative purposes only. No copyright ownership is claimed.
    return send_file("test_image.png", mimetype="image/png")

@app.route("/test/binary")
def test_binary():
    binary_data = bytes([0xDE, 0xAD, 0xBE, 0xEF])
    response = make_response(binary_data)
    response.headers["Content-Type"] = "application/octet-stream"
    return response

if __name__ == "__main__":
    app.run(port=5050)
