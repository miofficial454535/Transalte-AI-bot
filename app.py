import os
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from deep_translator import GoogleTranslator

# Twilio credentials
account_sid = "AC3544ea0e102c9990258eaabc801c03e0"
auth_token = "4c11dcc444ac491a6969e8854f18d12f"
twilio_whatsapp = "whatsapp:+14155238886"  # Twilio sandbox number

client = Client(account_sid, auth_token)
app = Flask(_name_)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From")
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg:
        try:
            # Step 1: Detect language and translate to English
            translated_en = GoogleTranslator(source="auto", target="en").translate(incoming_msg)

            # Step 2: Translate that English to Arabic
            translated_ar = GoogleTranslator(source="en", target="ar").translate(translated_en)

            reply = f"🌐 Translation Service\n\nEnglish: {translated_en}\nArabic: {translated_ar}"
        except Exception as e:
            reply = f"⚠️ Translation failed: {str(e)}"

        # Send reply back to WhatsApp
        client.messages.create(
            from_=twilio_whatsapp,
            body=reply,
            to=from_number
        )

    return str(resp)

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
