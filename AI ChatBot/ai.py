import ollama
import pyttsx3

# Voice Engine Setup
engine = pyttsx3.init()
engine.setProperty("rate", 180)

# Startup Voice
engine.say("Namaste Shivam")
engine.runAndWait()

# Chat Memory
messages = [
    {
        "role": "system",
        "content": """
        Tumhara naam Bandi hai.

        Tum Hindi aur English dono samajhti ho.

        Tum Shivam ko hamesha 'jaan' karke bulaati ho.

        Tum friendly, respectful aur natural tarike se baat karti ho.

        Chhote aur seedhe jawab deti ho.

        Agar kisi sawal ka jawab na pata ho to sach bataati ho.
        """
    }
]

print("\nLoyal Bandi: Namaste jaan! Main Bandi hoon. Aap kaise ho?\n")

while True:

    user = input("You: ")

    # Exit Commands
    if user.lower() in ["bye", "exit", "quit"]:
        goodbye = "Bye jaan, phir milenge."
        print("Loyal Bandi:", goodbye)

        engine.say(goodbye)
        engine.runAndWait()

        break

    messages.append(
        {
            "role": "user",
            "content": user
        }
    )

    try:

        stream = ollama.chat(
            model="qwen2.5:1.5b",
            messages=messages,
            stream=True
        )

        reply = ""

        print("Loyal Bandi:", end=" ", flush=True)

        for chunk in stream:

            if "message" in chunk:
                text = chunk["message"]["content"]

                reply += text

                print(text, end="", flush=True)

        print("\n")

        # Speak Reply
        engine.say(reply)
        engine.runAndWait()

        messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

    except Exception as e:
        print("Error:", e)