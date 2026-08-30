"""A Flask app using Docker and ECS"""
from flask import Flask, jsonify
from dotenv import load_dotenv
import os
 
app = Flask(__name__)
load_dotenv()

name = os.getenv("FULL_NAME")
 
@app.route("/")
def home():
    return jsonify(message=f"This is {name}'s Blue Green Deployment Lab")
 
@app.route("/health")
def health():
    return jsonify(status="ok"), 200
 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
