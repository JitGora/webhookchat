from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Webhook URL from environment variable
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

@app.route('/')
def index():
    return render_template('index.html') ## new html template

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message', '')
    # Read cookies from request headers instead of body
    cf_authorization = request.cookies.get('CF_Authorization', '') 
    cf_appsession = request.cookies.get('CF_AppSession', '')
    
    # Forward the message to the webhook along with JWT and session ID
    try:
        response = requests.post(
            WEBHOOK_URL,
            json={
                "message": user_message,
                "CF_Authorization": cf_authorization,
                "cf_AppSession": cf_appsession
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
