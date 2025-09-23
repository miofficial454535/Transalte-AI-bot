# Define your two users
user_a = "whatsapp:+91XXXXXXXXXX"  # Person A (Arabic sender)
user_b = "whatsapp:+91YYYYYYYYYY"  # Person B (English sender)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From")

    if incoming_msg:
        if from_number == user_a:  # Arabic → English → send to B
            translated = GoogleTranslator(source="ar", target="en").translate(incoming_msg)
            client.messages.create(from_=twilio_whatsapp, body=f"A (AR→EN): {translated}", to=user_b)

        elif from_number == user_b:  # English → Arabic → send to A
            translated = GoogleTranslator(source="en", target="ar").translate(incoming_msg)
            client.messages.create(from_=twilio_whatsapp, body=f"B (EN→AR): {translated}", to=user_a)

    return "OK"
