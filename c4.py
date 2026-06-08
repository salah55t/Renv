from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ضع هنا التوكن الخاص بالبوت الخاص بك
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
# ضع هنا معرف القناة (Chat ID)
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

@app.route('/send', methods=['POST'])
def send_to_telegram():
    data = request.json
    message = data.get("message", "لا توجد رسالة")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    
    response = requests.post(url, json=payload)
    return jsonify({"status": "sent", "telegram_response": response.json()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
