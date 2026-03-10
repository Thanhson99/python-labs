from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Cấu hình API của Composio
COMPOSIO_API_URL = "https://api.composio.ai/v1/run"  # Thay thế bằng URL thật
API_KEY = os.getenv("COMPOSIO_API_KEY", "your_composio_api_key")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_composio():
    user_input = request.json.get("input")

    # Gửi yêu cầu đến Composio
    payload = {
        "prompt": user_input,
        "model": "gpt-4-turbo"  # Chọn mô hình phù hợp
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(COMPOSIO_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "API request failed"}), 500

if __name__ == "__main__":
    app.run(debug=True)
