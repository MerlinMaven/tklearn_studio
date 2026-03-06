import json
import urllib.request
import urllib.error
import threading
import re
import os

API_URL = "https://api.mistral.ai/v1/chat/completions"

AVAILABLE_MODELS = [
    "mistral-small-latest",
    "mistral-medium-latest",
    "mistral-large-latest",
]

def _get_api_key():
    return os.environ.get("MISTRAL_API_KEY", "nhwnKYKWlfpS4KwuZV6feol7iOyCPYfl")

class MistralClient:
    def __init__(self, console=None):
        self.console = console
        self.model = AVAILABLE_MODELS[0]

    def set_model(self, model_name):
        self.model = model_name

    def generate_code_async(self, prompt, callback):
        def worker():
            try:
                api_key = _get_api_key()
                
                system_prompt = (
                    "Tu es un expert développeur Python spécialisé en Tkinter. "
                    "Ta mission est de générer du code Tkinter complet et fonctionnel. "
                    "RÈGLES STRICTES : "
                    "1. Ne donne AUCUNE explication textuelle (ni bonjour ni politesse), génère UNIQUEMENT le bloc de code. "
                    "2. Tu dois inclure 'import tkinter as tk'. "
                    "3. Crée la fenêtre avec 'root = tk.Tk()' et finis par 'root.mainloop()'."
                )
                
                data = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2
                }
                
                req = urllib.request.Request(API_URL, data=json.dumps(data).encode('utf-8'))
                req.add_header('Content-Type', 'application/json')
                req.add_header('Authorization', f'Bearer {api_key}')
                
                if self.console:
                    self.console.write(f"[{self.model}] Generation en cours...", "info")
                
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    
                content = result['choices'][0]['message']['content']
                
                code_match = re.search(r'```(?:python)?\s*(.*?)\s*```', content, re.DOTALL)
                if code_match:
                    clean_code = code_match.group(1).strip()
                else:
                    clean_code = content.strip()
                
                if self.console:
                    self.console.write(f"[{self.model}] Code genere.", "success")
                    
                callback(True, clean_code)
                
            except Exception as e:
                error_msg = str(e)
                if self.console:
                    self.console.write(f"[{self.model}] Erreur : {error_msg}", "error")
                callback(False, error_msg)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
