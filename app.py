from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

def translate_message(text):
    # Auto detect language
    detected = translator.detect(text)
    # If Arabic, translate to English
    if detected.lang == 'ar':
        result = translator.translate(text, src='ar', dest='en')
    # If English, translate to Arabic
    elif detected.lang == 'en':
        result = translator.translate(text, src='en', dest='ar')
    else:
        # For other languages, just return the original
        result = translator.translate(text, dest='ar')
    return result.text

@app.route('/send', methods=['POST'])
def send():
    """
    Sender's message. Send Arabic, get English.
    Send English, get Arabic.
    """
    data = request.get_json()
    text = data.get('text', '')
    translated = translate_message(text)
    return jsonify({'translated': translated})

# Example usage for reply (can use /send endpoint itself)
@app.route('/reply', methods=['POST'])
def reply():
    """
    Receiver's reply. Send English, get Arabic.
    Send Arabic, get English.
    """
    data = request.get_json()
    text = data.get('text', '')
    translated = translate_message(text)
    return jsonify({'translated': translated})

if __name__ == '__main__':
    app.run(debug=True)
