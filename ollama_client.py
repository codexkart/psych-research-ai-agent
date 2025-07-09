import requests

def query_ollama(prompt, model="mistral:7b-instruct-q3_K_S"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )

        data = response.json()
        print("🟡 Full Ollama JSON response:")
        print(data)

        if "response" in data:
            return data["response"]
        else:
            raise ValueError(f"❌ 'response' key not found in Ollama output.\nReturned: {data}")

    except Exception as e:
        print("🔥 Error while querying Ollama:", str(e))
        raise e
