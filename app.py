from flask import Flask, request, jsonify
from googletrans import Translator

# Twilio example import
from twilio.rest import Client

app = Flask(__name__)
translator = Translator()

# SID and Auth Token from your details
TWILIO_SID = "AC606533d9e625f2daa604327665b20189"
TWILIO_TOKEN = "d40a6e63406449e46955cedbb35a568c"

# Twilio client setup
twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

def translate_message(text):
    detected = translator.detect(text)
    if detected.lang == 'ar':
        result = translator.translate(text, src='ar', dest='en')
    elif detected.lang == 'en':
        result = translator.translate(text, src='en', dest='ar')
    else:
        result = translator.translate(text, dest='ar')
    return result.text

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    text = data.get('text', '')
    translated = translate_message(text)
    return jsonify({'translated': translated})

@app.route('/reply', methods=['POST'])
def reply():
    data = request.get_json()
    text = data.get('text', '')
    translated = translate_message(text)
    return jsonify({'translated': translated})

# Example function to send SMS using Twilio
@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    to_number = data.get('to', '')
    message = data.get('message', '')
    # Translate message if needed
    translated_message = translate_message(message)
    # Send SMS (replace 'from_' with your Twilio phone number)
    sms = twilio_client.messages.create(
        body=translated_message,
        from_='+YOUR_TWILIO_PHONE_NUMBER',  # Replace with your Twilio number
        to=to_number
    )
    return jsonify({'sid': sms.sid, 'translated_message': translated_message})

if __name__ == '__main__':
    app.run(debug=True)
