import tkinter.filedialog as filedialog

class FileManager:
    def __init__(self, root, editor, console):
        self.root = root
        self.editor = editor
        self.console = console

    def open_file(self):
        filepath = filedialog.askopenfilename(
            parent=self.root,
            title="Ouvrir un fichier",
            filetypes=[("Fichiers Python", "*.py"), ("Tous les fichiers", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    code = f.read()
                self.editor.set_code(code)
                self.current_file = filepath
                self.console.write(f"--- Fichier ouvert : {filepath} ---")
            except Exception as e:
                self.console.write(f"Erreur lors de l'ouverture du fichier : {str(e)}")

    def save_file(self):
        if not hasattr(self, 'current_file') or not self.current_file:
            self.save_file_as()
            return
            
        try:
            code = self.editor.get_code().rstrip() + "\n"
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(code)
            self.console.write(f"--- Fichier sauvegardé : {self.current_file} ---")
        except Exception as e:
            self.console.write(f"Erreur lors de la sauvegarde : {str(e)}")

    def save_file_as(self):
        filepath = filedialog.asksaveasfilename(
            parent=self.root,
            title="Enregistrer sous",
            defaultextension=".py",
            filetypes=[("Fichiers Python", "*.py"), ("Tous les fichiers", "*.*")]
        )
        if filepath:
            self.current_file = filepath
            self.save_file()
