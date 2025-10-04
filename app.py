from flask import Flask, request, jsonify
from ocr_service import extract_text
from entity_service import extract_entities
from normalize_service import normalize_entities
import json

app = Flask(__name__)

# ------------------ Global store for last request ------------------
last_request_json = {}

# ------------------ Process text input (real pipeline) ------------------
def process_input_real(input_text):
    if not input_text:
        return {"status": "needs_clarification", "message": "No input text"}

    # 1️⃣ Extract entities
    entity_result = extract_entities(input_text)
    if entity_result.get("status"):
        return entity_result  # Ambiguous department/date/time

    entities = entity_result.get("entities", {})

    # 2️⃣ Normalize entities
    normalized_result = normalize_entities(entities)
    if normalized_result.get("status"):
        return normalized_result  # Could not normalize date/time

    # 3️⃣ Build final JSON
    return {
        "appointment": {
            "department": entities.get("department"),
            "date": normalized_result["normalized"]["date"],
            "time": normalized_result["normalized"]["time"],
            "tz": normalized_result["normalized"]["tz"]
        },
        "status": "ok"
    }

# ------------------ POST Text (multiple texts supported) ------------------
@app.route("/schedule_text", methods=["POST"])
def schedule_text():
    global last_request_json
    data = request.get_json(force=True)

    if not data or "text" not in data:
        return jsonify({"status": "error", "message": "Missing 'text' field"}), 400

    texts = data["text"]
    if isinstance(texts, str):
        texts = [texts]

    results = [process_input_real(t) for t in texts]

    last_request_json = {"appointments": results, "status": "ok"}
    return jsonify(last_request_json)

# ------------------ POST Image ------------------
@app.route("/schedule_image", methods=["POST"])
def schedule_image():
    global last_request_json
    if "image" not in request.files:
        return jsonify({"status": "error", "message": "No image uploaded"}), 400

    file = request.files["image"]

    # 1️⃣ OCR extraction
    ocr_result = extract_text(file, is_image=True)
    raw_texts = ocr_result.get("raw_texts", [])

    # 2️⃣ Process each extracted line through entity + normalization pipeline
    results = [process_input_real(t) for t in raw_texts]

    last_request_json = {"appointments": results, "status": "ok"}
    return jsonify(last_request_json)

# ------------------ Browser Live JSON View ------------------
@app.route("/live_last_request", methods=["GET"])
def live_last_request():
    if not last_request_json:
        return jsonify({"status": "idle", "message": "No requests processed yet"})
    return jsonify(last_request_json)

# ------------------ Root page shows live JSON with auto-refresh ------------------
@app.route("/", methods=["GET"])
def home():
    if not last_request_json:
        return "<h2>API running — no requests processed yet</h2>"

    pretty_json = json.dumps(last_request_json, indent=4)
    
    html_content = f"""
    <html>
    <head>
        <title>Live API Dashboard</title>
        <meta http-equiv="refresh" content="5"> <!-- refresh every 5 seconds -->
        <style>
            body {{ font-family: monospace; background-color: #f5f5f5; padding: 20px; }}
            pre {{ background-color: #eaeaea; padding: 15px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h2>API running — Last Processed Request:</h2>
        <pre>{pretty_json}</pre>
    </body>
    </html>
    """
    return html_content

# ------------------ Run the app ------------------
if __name__ == "__main__":
    app.run(debug=True)
