import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


# Variables
app = Flask(__name__)

if str(os.environ.get("FLASK_REVERSE_PROXY", "false")).lower() == "true":
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
    )


# Functions
@app.route("/api") # I did not use / since we pass the /api directly to the Flask application
def index():
    environment = os.environ.get("FLASK_ENV", "development")
    if environment == "production":
        return "Hello from production api!"
    elif environment == "development":
        return "Hello from development api!"
    else:
        return f"Hello from {environment} api!"

@app.route("/api/health")
def api_health():
    return {"status": "ok"}


# Start and bind the Flask application to all IPs of the container
port = int(os.environ.get("FLASK_PORT", "5000"))
debug = int(os.environ.get("FLASK_DEBUG", "0")) == 1
app.run(host="0.0.0.0", port=port, debug=debug)
