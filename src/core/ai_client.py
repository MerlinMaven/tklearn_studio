import json
import urllib.request
import urllib.error
import threading
import re

API_KEY = "nhwnKYKWlfpS4KwuZV6feol7iOyCPYfl"
API_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL = "mistral-small-latest"

class MistralClient:
    def __init__(self, console=None):
        self.console = console

    def generate_code_async(self, prompt, callback):
        def worker():
            try:
                # Prompt système robuste qui s'intègre parfaitement avec notre mocking tk
                system_prompt = (
                    "Tu es un expert développeur Python spécialisé en Tkinter. "
                    "Ta mission est de générer du code Tkinter complet et fonctionnel. "
                    "RÈGLES STRICTES : "
                    "1. Ne donne AUCUNE explication textuelle (ni bonjour ni politesse), génère UNIQUEMENT le bloc de code. "
                    "2. Tu dois inclure 'import tkinter as tk'. "
                    "3. Crée la fenêtre avec 'root = tk.Tk()' et finis par 'root.mainloop()'."
                )
                
                data = {
                    "model": MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2
                }
                
                req = urllib.request.Request(API_URL, data=json.dumps(data).encode('utf-8'))
                req.add_header('Content-Type', 'application/json')
                req.add_header('Authorization', f'Bearer {API_KEY}')
                
                if self.console:
                    self.console.write("🤖 [Mistral AI] Réflexion en cours...")
                
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    
                content = result['choices'][0]['message']['content']
                
                # Extraire uniquement le code (on retire les balises markdown)
                code_match = re.search(r'```(?:python)?\s*(.*?)\s*```', content, re.DOTALL)
                if code_match:
                    clean_code = code_match.group(1).strip()
                else:
                    clean_code = content.strip()
                
                if self.console:
                    self.console.write("✨ [Mistral AI] Code magique généré avec succès !")
                    
                # The callback updates the UI safely across thread boundary
                callback(True, clean_code)
                
            except Exception as e:
                error_msg = str(e)
                if self.console:
                    self.console.write(f"❌ [Mistral AI Erreur] API injoignable ou erreur : {error_msg}")
                callback(False, error_msg)

        # Lancer le worker dans un thread externe pour ne pas geler Tkinter
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
