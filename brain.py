import requests

def ask_rooney(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:latest",
                "prompt": f"Answer clearly and briefly in 5 sentences: {prompt}",
                "stream": False,
                "options": {
                    "num_predict": 150,
                    "temperature": 0.7
                }
            },
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            return data["response"]
        else:
            return "I received an unexpected response."

    except Exception as e:
        print("Ollama error:", e)
        return "I am having trouble connecting to my brain."