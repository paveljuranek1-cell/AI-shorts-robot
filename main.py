import os

key = os.getenv("GEMINI_API_KEY")

if key:
    print("API klíč nalezen ✅")
else:
    print("API klíč chybí ❌")
