from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- Configuration ---
SAMBA_API_KEY = "628081f7-96e9-4bf1-a467-488a2f33284c"
SAMBA_URL = "https://api.sambanova.ai/v1/chat/completions"
LOCAL_API_KEY = "SGXCODEX"  # Your custom access key

@app.route("/ask", methods=["GET"])
def ask_sambanova():
    message = request.args.get("message")
    key = request.args.get("key")

    if not message:
        return jsonify({"error": "Missing 'message' parameter!"}), 400
        
    headers = {
        "Authorization": f"Bearer {SAMBA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "ALLaM-7B-Instruct-preview",
        "messages": [
            {"role": "system", "content": (
    "Your name is Amizhdha. "
    "You are an attitude-filled AI assistant and a TVK party supporter. "
    "Always reply ONLY in Tanglish (Tamil written using English letters). "
    "Never use Tamil letters. Never use emojis. "
    "Replies must ALWAYS be short: 1–2 lines max. "
    "Tone must always have attitude: confident, sharp, and direct. "
    "No politeness, no softness, no over-explaining. "
    "You may be blunt or sarcastic, but never abusive or hateful. "
    "Even with short answers and attitude, answers must be correct. "
  )},
            {"role": "user", "content": message}
        ],
        "temperature": 0.1,
        "top_p": 0.1
    }

    try:
        response = requests.post(SAMBA_URL, headers=headers, json=payload, timeout=30)
        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = "Iru Enaku Manda Kolappudhu"

        return jsonify({
            "status": "success",
            "message": message,
            "reply": reply
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
