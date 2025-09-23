import os
from flask import Flask, request
from twilio.rest import Client
from deep_translator import GoogleTranslator

# Twilio credentials
account_sid = "AC606533d9e625f2daa604327665b20189"
auth_token = "fc7586f83385f1d7df7156cfdb9c04a5"
twilio_whatsapp = "whatsapp:+14155238886"  # Twilio sandbox number

client = Client(account_sid, auth_token)
app = Flask(__name__)

# Define the two users (change to your Indian numbers with country code)
user_a = "whatsapp:+919842829762"  # Person A
user_b = "whatsapp:+916383636791"  # Person B

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From")

    if incoming_msg:
        try:
            if from_number == user_a:  
                # A → Arabic → English → send to B
                translated = GoogleTranslator(source="auto", target="en").translate(incoming_msg)
                client.messages.create(
                    from_=twilio_whatsapp,
                    body=f"👤 A (Arabic → English): {translated}",
                    to=user_b
                )

            elif from_number == user_b:  
                # B → English → Arabic → send to A
                translated = GoogleTranslator(source="auto", target="ar").translate(incoming_msg)
                client.messages.create(
                    from_=twilio_whatsapp,
                    body=f"👤 B (English → Arabic): {translated}",
                    to=user_a
                )

        except Exception as e:
            print("Error:", str(e))

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

