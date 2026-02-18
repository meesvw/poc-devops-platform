import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


# Variables
app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1,
)


# Functions
@app.route("/api")
def api_health():
    return {"status": "ok"}


# Start and bind the Flask application to all IPs of the container
port = int(os.environ.get("PORT", "5000"))
app.run(host="0.0.0.0", port=port)
