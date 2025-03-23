import requests
import json

def extract_text(messages,text):
    api_key = "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"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com"  # Replace with your site URL
    }

    messages.append({"role": "user", "content": text})
    # Create your request payload
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": messages, 
        "temperature": 0.7,
        "max_tokens": 150
    }

    # Make the API request
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(payload)
    )

    # Parse the response
    result = response.json()

    # Extract just the model's response text (nothing else)
    if "choices" in result and len(result["choices"]) > 0:
        assistant_response = result["choices"][0]["message"]["content"]
        print(assistant_response)
        return assistant_response
    else:
        print("Error or unexpected response format:")
        print(json.dumps(result, indent=2))
        return "Sorry, I encountered an error."