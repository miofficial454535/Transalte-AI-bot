import os
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from deep_translator import GoogleTranslator

app = Flask(__name__)

# -------------------------------
# Twilio Credentials
# -------------------------------
account_sid = "AC606533d9e625f2daa604327665b20189"
auth_token = "7041b6cebf4372018097e687cbcef4d3"
twilio_whatsapp = "whatsapp:+14155238886"  # Twilio Sandbox Number
client = Client(account_sid, auth_token)

# -------------------------------
# Chat Pair (Sender <-> Receiver)
# -------------------------------
chat_pairs = {
    "whatsapp:+919842829762": "whatsapp:+916383636791",   # Sender -> Receiver
    "whatsapp:+916383636791": "whatsapp:+919842829762"    # Receiver -> Sender
}

# -------------------------------
# Webhook Route
# -------------------------------
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """Handle incoming WhatsApp messages from Twilio"""
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From")
    partner_number = chat_pairs.get(from_number)

    # Twilio requires some response
    resp = MessagingResponse()

    if not partner_number:
        resp.message("⚠️ You are not paired for translation bridge.")
        return str(resp)

    try:
        if incoming_msg.isascii():
            # English -> Arabic
            translated_msg = GoogleTranslator(source="en", target="ar").translate(incoming_msg)
        else:
            # Assume Arabic (or non-English) -> English
            translated_msg = GoogleTranslator(source="auto", target="en").translate(incoming_msg)

        # Forward translated msg to partner
        client.messages.create(
            from_=twilio_whatsapp,
            body=translated_msg,
            to=partner_number
        )

    except Exception as e:
        client.messages.create(
            from_=twilio_whatsapp,
            body=f"⚠️ Translation failed: {str(e)}",
            to=from_number
        )

    # Always return a valid response
    return str(resp)

# -------------------------------
# Run for Render
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
