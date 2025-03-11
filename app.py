from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Webhook URL
WEBHOOK_URL = "http://172.22.0.3:5678/webhook/230459d0-9157-4f5b-bb8b-24f1f8014ca4"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message', '')
    cf_authorization = data.get('cf_authorization', '')
    cf_appsession = data.get('CF_AppSession', '')
    
    # Forward the message to the webhook along with JWT and session ID
    try:
        response = requests.post(
            WEBHOOK_URL,
            json={
                "message": user_message,
                "CF_Authorization": cf_authorization,
                "cf_appsession": cf_appsession
            },
            headers={"Content-Type": "application/json"}
        )
        
        # Return the webhook response as text
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to get response from webhook"}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)