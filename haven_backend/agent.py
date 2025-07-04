import requests
import os

LM_API_URL = os.getenv("LM_API_URL", "http://localhost:11434/v1")

class ClaudeRealtimeModel:
    def __init__(self, instructions, voice="shimmer", temperature=0.7, modalities=["audio", "text"]):
        self.instructions = instructions
        self.voice = voice
        self.temperature = temperature
        self.modalities = modalities
        self.sessions = [ClaudeSession(self)]

class ClaudeSession:
    def __init__(self, model):
        self.model = model
        self.conversation = ClaudeConversation()
        self.response = ClaudeResponse(self)

class ClaudeConversation:
    def __init__(self):
        self.messages = []

    def create(self, message):
        if isinstance(message, dict):
            print("[ClaudeConversation] Adding message:", message)
            self.messages.append(message)

    def history(self):
        return self.messages[-10:]

class ClaudeResponse:
    def __init__(self, session):
        self.session = session

    async def create(self):
        headers = {"Content-Type": "application/json"}
        body = {
            "model": "nous-hermes2:10.7b",
            "messages": self.session.conversation.history(),
            "temperature": self.session.model.temperature
        }
        try:
            response = requests.post(f"{LM_API_URL}/chat/completions", headers=headers, json=body)
            if response.status_code == 200:
                reply = response.json()['choices'][0]['message']['content']
                print("[Claude Response]", reply)
                self.session.conversation.create({"role": "assistant", "content": reply})
                return reply
            else:
                print("[Claude ERROR]", response.status_code, response.text)
                return "Sorry, I couldn't respond."
        except Exception as e:
            print("[Claude ERROR] Exception:", e)
            return "An error occurred while processing your request."


if __name__ == "__main__":
    print("🧠 Claude test mode")
    model = ClaudeRealtimeModel(
        instructions="You are Haven, a kind and empathetic therapist.",
        voice="shimmer"
    )
    session = model.sessions[0]
    user_input = input("You: ")
    session.conversation.create({"role": "user", "content": user_input})
    import asyncio
    reply = asyncio.run(session.response.create())
    print("Haven:", reply)
