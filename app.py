from flask import Flask, request, render_template_string
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Positive Chatbot</title>
</head>
<body>
    <h1>Positive Chatbot</h1>

    <form method="POST">
        <input name="message" placeholder="Type here..." required>
        <button type="submit">Send</button>
    </form>

    {% if user %}
        <p><b>You:</b> {{ user }}</p>
        <p><b>Bot:</b> {{ bot }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    user = ""
    bot = ""

    if request.method == "POST":
        user = request.form["message"]

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user
        )

        bot = response.text

    return render_template_string(HTML, user=user, bot=bot)

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
