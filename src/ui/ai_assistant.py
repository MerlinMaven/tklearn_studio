import tkinter as tk

class AIAssistantDialog:
    def __init__(self, parent_root, editor, ai_client):
        self.root = parent_root
        self.editor = editor
        self.ai_client = ai_client
        
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title("✨ Assistant de Code IA (Mistral)")
        self.dialog.geometry("550x250")
        self.dialog.configure(bg="#2d2d30")
        self.dialog.attributes("-topmost", True)
        self.dialog.resizable(False, False)
        
        # Center the dialog on the root window
        self.dialog.transient(self.root)
        
        lbl = tk.Label(self.dialog, text="Que souhaitez-vous créer ou apprendre avec Tkinter aujourd'hui ?", bg="#2d2d30", fg="white", font=("Segoe UI", 11))
        lbl.pack(pady=(15, 5))
        
        # User input text area
        self.prompt_text = tk.Text(self.dialog, height=5, font=("Consolas", 11), bg="#1e1e1e", fg="white", insertbackground="white", relief=tk.FLAT, padx=10, pady=10)
        self.prompt_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Bottom frame for buttons
        self.btn_frame = tk.Frame(self.dialog, bg="#2d2d30")
        self.btn_frame.pack(fill=tk.X, pady=(5, 15), padx=15)
        
        self.btn_generate = tk.Button(self.btn_frame, text="✨ Générer le code", bg="#007acc", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, command=self.on_generate, cursor="hand2")
        self.btn_generate.pack(side=tk.RIGHT)
        
        self.btn_cancel = tk.Button(self.btn_frame, text="Annuler", bg="#4d4d4d", fg="white", font=("Segoe UI", 10), relief=tk.FLAT, command=self.dialog.destroy, cursor="hand2")
        self.btn_cancel.pack(side=tk.RIGHT, padx=10)
        
        # Insert example placeholder
        self.prompt_text.insert("1.0", "Exemple : Fais-moi une calculatrice complète avec une grille de boutons.")
        self.prompt_text.bind("<FocusIn>", self._clear_placeholder)
        
    def _clear_placeholder(self, event):
        if "Exemple :" in self.prompt_text.get("1.0", tk.END):
            self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.unbind("<FocusIn>")
        
    def on_generate(self):
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        if not prompt or prompt.startswith("Exemple :"): 
            return
        
        # Disable inputs while loading
        self.btn_generate.config(text="Génération en cours...", state=tk.DISABLED, bg="#333333")
        self.btn_cancel.config(state=tk.DISABLED)
        self.prompt_text.config(state=tk.DISABLED)
        
        # Lancer la génération Asynchrone
        self.ai_client.generate_code_async(prompt, self._on_result)
        
    def _on_result(self, success, result_data):
        # We must use tk's .after() to safely modify the GUI from the callback (which is in a worker thread)
        self.root.after(0, self._handle_result, success, result_data)
        
    def _handle_result(self, success, result_data):
        if success:
            # Inject directly into the editor
            self.editor.set_code(result_data)
            self.dialog.destroy()
        else:
            # Re-enable inputs if failed
            self.btn_generate.config(text="Réessayer", state=tk.NORMAL, bg="#007acc")
            self.btn_cancel.config(state=tk.NORMAL)
            self.prompt_text.config(state=tk.NORMAL)
