"""Full-stack Flask app serving a modern deployment status interface."""
import os
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

NAME = os.getenv("FULL_NAME", "User")
APP_VERSION = os.getenv("APP_VERSION", "dev")

@app.route("/")
def home():
    return render_template("index.html", name=NAME, version=APP_VERSION)

@app.route("/health")
def health():
    return jsonify(status="ok", version=APP_VERSION), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
