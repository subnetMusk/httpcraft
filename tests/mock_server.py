from flask import Flask, request, jsonify, render_template_string, make_response

app = Flask(__name__)
CSRF_TOKEN = "secure123"

@app.route("/echo", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def echo():
    return jsonify({
        "method": request.method,
        "headers": dict(request.headers),
        "args": request.args,
        "form": request.form,
        "json": request.get_json(silent=True),
        "cookies": request.cookies
    })

@app.route("/form")
def form():
    html = f'''
    <html>
        <body>
            <form action="/submit" method="POST">
                <input type="hidden" name="csrf_token" value="{CSRF_TOKEN}">
                <input type="text" name="username" value="admin">
                <input type="submit" value="Send">
            </form>
        </body>
    </html>
    '''
    return render_template_string(html)

@app.route("/submit", methods=["POST"])
def submit():
    token = request.form.get("csrf_token")
    return jsonify({
        "message": "Form submitted",
        "token_valid": token == CSRF_TOKEN,
        "form": request.form
    })

@app.route("/set_cookie")
def set_cookie():
    resp = make_response("Cookie set")
    resp.set_cookie("sessionid", "abc123")
    return resp

if __name__ == "__main__":
    app.run(port=5000)