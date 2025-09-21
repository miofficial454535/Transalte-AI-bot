import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from deep_translator import GoogleTranslator

# -----------------------------
# Flask App Initialization
# -----------------------------
app = Flask(__name__)

# -----------------------------
# WhatsApp Webhook Route
# -----------------------------
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """
    This function will be called every time a message is 
    sent to your Twilio WhatsApp sandbox number.
    """
    # Get incoming user message
    incoming_msg = request.values.get("Body", "").strip()

    # Create a Twilio Messaging Response object
    resp = MessagingResponse()

    if incoming_msg:
        try:
            # STEP 1: Translate incoming message to English
            translated_en = GoogleTranslator(
                source="auto", target="en"
            ).translate(incoming_msg)

            # STEP 2: Translate English into Arabic
            translated_ar = GoogleTranslator(
                source="en", target="ar"
            ).translate(translated_en)

            # Final text reply
            reply_text = (
                "🌐 Translation Service\n\n"
                f"English: {translated_en}\n"
                f"Arabic: {translated_ar}"
            )

        except Exception as e:
            # If translation fails (e.g. Google API issue)
            reply_text = f"⚠️ Translation failed: {str(e)}"

    else:
        # If user sends empty message
        reply_text = "⚠️ Please type something to translate."

    # Attach reply into Twilio XML response
    resp.message(reply_text)

    # Return response back to Twilio (must be string)
    return str(resp)


# -----------------------------
# Run Flask App (for Render/Local)
# -----------------------------
if __name__ == "__main__":
    # Render sets its own PORT env variable
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
