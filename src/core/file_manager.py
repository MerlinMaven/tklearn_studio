import tkinter.filedialog as filedialog
import os

class FileManager:
    def __init__(self, root, editor, console, status_bar=None):
        self.root = root
        self.editor = editor
        self.console = console
        self.status_bar = status_bar
        self.current_file = None

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
                
                filename = os.path.basename(filepath)
                self.editor.set_tab_name(filename)
                
                if self.status_bar:
                    self.status_bar.update_filename(filename)
                
                self.console.write(f"Fichier ouvert : {filepath}", "info")
            except Exception as e:
                self.console.write(f"Erreur d'ouverture : {str(e)}", "error")

    def save_file(self):
        if not self.current_file:
            self.save_file_as()
            return
            
        try:
            code = self.editor.get_code().rstrip() + "\n"
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(code)
            self.console.write(f"Fichier sauvegarde : {self.current_file}", "success")
        except Exception as e:
            self.console.write(f"Erreur de sauvegarde : {str(e)}", "error")

    def save_file_as(self):
        filepath = filedialog.asksaveasfilename(
            parent=self.root,
            title="Enregistrer sous",
            defaultextension=".py",
            filetypes=[("Fichiers Python", "*.py"), ("Tous les fichiers", "*.*")]
        )
        if filepath:
            self.current_file = filepath
            filename = os.path.basename(filepath)
            self.editor.set_tab_name(filename)
            
            if self.status_bar:
                self.status_bar.update_filename(filename)
            
            self.save_file()
