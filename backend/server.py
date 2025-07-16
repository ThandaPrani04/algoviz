from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import os

app = Flask(__name__)
CORS(app)  # ✅ enable CORS for all routes

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    url = data.get("url")
    print("Received URL:", url)
    if not url:
        return jsonify({"message": "No URL provided"}), 400

    def run_pipeline():
        os.system(f"python leetcode_visualizer.py {url}")

    threading.Thread(target=run_pipeline).start()

    return jsonify({"message": "🚀 Generation started! Video will be saved in the folder."})

if __name__ == "__main__":
    app.run(port=5000)
