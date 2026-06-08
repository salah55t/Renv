from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ضع بيانات البوت الخاصة بك هنا أو استخدم متغيرات البيئة (Environment Variables)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8945425967:AAEveKpqSEib2iZ5aT4mOAX5og5j2-uc_MU")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "6624995237")

# مسار للحفاظ على السيرفر مستيقظاً (يتم استدعاؤه بواسطة Cron-job)
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "alive", "message": "السيرفر مستيقظ!"}), 200

# مسار استقبال البيانات من n8n وإرسالها لتلغرام
@app.route('/send', methods=['POST'])
def send_to_telegram():
    try:
        data = request.json
        if not data or "message" not in data:
            return jsonify({"status": "error", "message": "البيانات غير صحيحة"}), 400
        
        message = data.get("message")
        
        # رابط API تلغرام
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return jsonify({"status": "sent", "telegram_response": response.json()}), 200
        else:
            return jsonify({"status": "error", "message": "فشل الإرسال لتلغرام"}), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # تشغيل السيرفر
    app.run(host='0.0.0.0', port=5000)
