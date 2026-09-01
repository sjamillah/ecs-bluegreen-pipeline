"""Typing speed test, served from ECS Fargate behind an ALB."""
import os
import random

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from words import WORDS

load_dotenv()

app = Flask(__name__)

NAME = os.getenv("FULL_NAME", "User")
APP_VERSION = os.getenv("APP_VERSION", "dev")


@app.route("/")
def home():
    return render_template("index.html", name=NAME, version=APP_VERSION)


@app.route("/api/words")
def api_words():
    """Return a random run of words for one test.

    Sampled with replacement - real typing tests repeat common words, and it
    keeps the app stateless so any task can serve any request.
    """
    count = request.args.get("count", default=80, type=int)
    count = max(10, min(count, 300))
    return jsonify(words=random.choices(WORDS, k=count))


@app.route("/health")
def health():
    return jsonify(status="ok", version=APP_VERSION), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
