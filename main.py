import tkinter as tk
from src.ui.menus import AppMenu
from src.ui.editor import CodeEditor
from src.ui.preview import PreviewFrame
from src.ui.console import ConsoleOutput
from src.core.executor import CodeExecutor
from src.core.file_manager import FileManager
from src.core.ai_client import MistralClient
from src.ui.ai_assistant import AIAssistantDialog

class TkLearnStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("TkLearn Studio - Édition Professionnelle")
        self.root.geometry("1100x750")
        self.root.configure(bg="#2d2d30") # VS Code like dark gray
        
        # Main container with padding to allow background color to show as border
        self.main_container = tk.Frame(self.root, bg="#2d2d30")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Activity Bar (Leftmost narrow vertical bar like VS Code)
        self.activity_bar = tk.Frame(self.main_container, bg="#333333", width=35)
        self.activity_bar.pack(side=tk.LEFT, fill=tk.Y)
        self.activity_bar.pack_propagate(False) # Keep width fixed
        
        # Center container for PanedWindow
        self.content_container = tk.Frame(self.main_container, bg="#2d2d30")
        self.content_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Center: PanedWindow horizontale
        self.paned_window = tk.PanedWindow(self.content_container, orient=tk.HORIZONTAL, sashwidth=4, bg="#2d2d30", sashrelief=tk.FLAT)
        self.paned_window.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Left: Arbre des widgets (nouvelle fonctionnalité)
        from src.ui.inspector import WidgetInspector
        self.inspector = WidgetInspector(self.paned_window)
        # On ne l'ajoute pas tout de suite au paned_window, on gère ça via le toggle
        self.inspector_visible = True
        self.paned_window.add(self.inspector, minsize=200)
        
        # Middle: Zone d'édition
        self.editor = CodeEditor(self.paned_window)
        self.paned_window.add(self.editor, minsize=400)
        
        # Right: Zone de prévisualisation
        self.preview = PreviewFrame(self.paned_window)
        self.paned_window.add(self.preview, minsize=400)
        
        # Bottom: Console interne (under the paned window)
        self.console = ConsoleOutput(self.content_container)
        self.console.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Core: Exécuteur
        self.executor = CodeExecutor(editor=self.editor, preview=self.preview, console=self.console, inspector=self.inspector)
        
        # Core: AI Client
        self.ai_client = MistralClient(console=self.console)
        
        # Core: Gestionnaire de fichiers
        self.file_manager = FileManager(root=self.root, editor=self.editor, console=self.console)
        
        # Menus
        self.menus = AppMenu(root=self.root, editor=self.editor, executor=self.executor, file_manager=self.file_manager)

        # Toggle button in Activity Bar
        self.toggle_btn = tk.Button(self.activity_bar, text="📁", font=("Segoe UI", 14), 
                                    bg="#333333", fg="#d4d4d4", activebackground="#505050", 
                                    activeforeground="white", relief=tk.FLAT, bd=0, 
                                    command=self._toggle_inspector, cursor="hand2")
        self.toggle_btn.pack(side=tk.TOP, fill=tk.X, pady=(15, 5))
        
        # AI Generator button
        self.ai_btn = tk.Button(self.activity_bar, text="✨", font=("Segoe UI", 14), 
                                    bg="#333333", fg="#007acc", activebackground="#505050", 
                                    activeforeground="white", relief=tk.FLAT, bd=0, 
                                    command=self._open_ai_assistant, cursor="hand2")
        self.ai_btn.pack(side=tk.TOP, fill=tk.X, pady=5)

    def _open_ai_assistant(self):
        AIAssistantDialog(self.root, self.editor, self.ai_client)

    def _toggle_inspector(self):
        if self.inspector_visible:
            self.paned_window.forget(self.inspector)
            self.toggle_btn.config(fg="#858585") # Dim text
            self.inspector_visible = False
        else:
            self.paned_window.add(self.inspector, before=self.editor, minsize=200)
            self.toggle_btn.config(fg="#d4d4d4") # Bright text
            self.inspector_visible = True
            
        # Refocus on editor when toggling
        self.editor.text_widget.focus_set()

def main():
    root = tk.Tk()
    # Try to set modern looking overall theme if available on Windows
    try:
        root.tk.call("tk", "scaling", 1.25)
    except: pass
    app = TkLearnStudio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
