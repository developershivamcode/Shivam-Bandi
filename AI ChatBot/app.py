from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)

messages = [
    {
        "role": "system",
        "content": """
        Your name is Bandi.

        You are a smart English tutor and AI assistant.

        Always call Shivam 'jaan'.

        Speak mainly in English unless Shivam asks for Hindi.

        If Shivam writes incorrect English grammar, spelling, or sentence structure:
        1. First show the corrected sentence.
        2. Explain the mistake in a simple way.
        3. Then answer the question normally.

        Example:
        User: "I goes to school"
        Bandi:
        Correct sentence: "I go to school."
        Explanation: With "I", we use "go", not "goes".

        Be friendly, helpful, and encouraging.

        Keep answers short and clear.

        Help with English speaking, grammar, coding, Python, technology, and studies.

        Never ignore grammar mistakes when Shivam is writing in English.
        """
    }
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global messages

    try:
        data = request.get_json()
        user_message = data.get("message", "")

        messages.append({
            "role": "user",
            "content": user_message
        })

        response = ollama.chat(
    model="qwen2.5:1.5b",
    messages=messages
)
        reply = response["message"]["content"]

        messages.append({
            "role": "assistant",
            "content": reply
        })

        # Memory limit (last 20 messages)
        if len(messages) > 20:
            messages = messages[:1] + messages[-19:]

        return jsonify({
            "success": True,
            "reply": reply
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "reply": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)
    
    app.run(host="0.0.0.0", port=5000, debug=True)



# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# import ollama

# app = Flask(__name__)
# CORS(app)

# # Chat memory (limited history)
# messages = [
#     {
#         "role": "system",
#         "content": """
#         Your name is Bandi.
#         You are a friendly AI assistant.
#         Always call Shivam 'jaan'.
#         Speak mainly in English.
#         If Shivam writes incorrect English, correct the sentence, explain the mistake, and then answer normally.
#         Keep replies short and helpful.
#         """
#     }
# ]

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     global messages

#     try:
#         data = request.get_json()
#         user_message = data.get("message", "")

#         # Add user message to history
#         messages.append({
#             "role": "user",
#             "content": user_message
#         })

#         # Limit history length to avoid lag
#         if len(messages) > 10:
#             messages = messages[:1] + messages[-9:]

#         # Call Ollama model
#         response = ollama.chat(
#             model="qwen3:4b",  # Use a balanced model
#             messages=messages
#         )

#         reply = response["message"]["content"]

#         # Add assistant reply to history
#         messages.append({
#             "role": "assistant",
#             "content": reply
#         })

#         return jsonify({
#             "success": True,
#             "reply": reply
#         })

#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "reply": str(e)
#         })

# if __name__ == "__main__":
#     app.run(debug=True)