import tkinter as tk

class AppMenu:
    def __init__(self, root, editor, executor, file_manager):
        self.root = root
        self.editor = editor
        self.executor = executor
        self.file_manager = file_manager
        
        self.menubar = tk.Menu(self.root, bg="#2d2d30", fg="#cccccc", 
                               activebackground="#3e3e42", activeforeground="white",
                               relief=tk.FLAT, borderwidth=0)
        
        self._build_fichier_menu()
        self._build_lecons_menu()
        self._build_execution_menu()
        self._build_outils_menu()
        self._build_aide_menu()
        
        self.root.config(menu=self.menubar)
        
        self.root.bind("<F5>", lambda event: self.executor.run_code())
        self.root.bind("<Control-s>", lambda event: self.file_manager.save_file())
        self.root.bind("<Control-o>", lambda event: self.file_manager.open_file())

    def _styled_menu(self):
        return tk.Menu(self.menubar, tearoff=0, bg="#2d2d30", fg="#cccccc",
                       activebackground="#007acc", activeforeground="white",
                       relief=tk.FLAT, borderwidth=1)

    def _build_fichier_menu(self):
        menu = self._styled_menu()
        menu.add_command(label="Ouvrir                         Ctrl+O", command=self.file_manager.open_file)
        menu.add_command(label="Enregistrer                  Ctrl+S", command=self.file_manager.save_file)
        menu.add_command(label="Enregistrer sous...", command=self.file_manager.save_file_as)
        menu.add_separator()
        menu.add_command(label="Quitter", command=self.root.quit)
        self.menubar.add_cascade(label="Fichier", menu=menu)

    def _build_lecons_menu(self):
        menu = self._styled_menu()
        menu.add_command(label="1. Les Bases (Label, Entry, Bouton)", command=lambda: self._load_lesson("bases_widgets"))
        menu.add_command(label="2. Choix Multiples (Radio, Check, Combo)", command=lambda: self._load_lesson("choix_multiples"))
        menu.add_command(label="3. Mise en page (Grid)", command=lambda: self._load_lesson("geometrie_grid"))
        menu.add_command(label="4. Dessin (Canvas)", command=lambda: self._load_lesson("dessin_canvas"))
        menu.add_command(label="5. Evenements", command=lambda: self._load_lesson("evenements"))
        self.menubar.add_cascade(label="Lecons", menu=menu)

    def _build_execution_menu(self):
        menu = self._styled_menu()
        menu.add_command(label="Lancer                          F5", command=self.executor.run_code)
        self.menubar.add_cascade(label="Execution", menu=menu)

    def _build_outils_menu(self):
        menu = self._styled_menu()
        menu.add_command(label="Vider la console", command=self.executor.console.clear)
        self.menubar.add_cascade(label="Outils", menu=menu)

    def _build_aide_menu(self):
        menu = self._styled_menu()
        menu.add_command(label="A propos", command=lambda: self.executor.console.write(
            "TkLearn Studio\nOutil d'apprentissage Tkinter.", "info"
        ))
        self.menubar.add_cascade(label="Aide", menu=menu)

    def _load_lesson(self, lesson_name):
        from src.core.lesson_loader import LessonLoader
        code = LessonLoader.get_lesson(lesson_name)
        self.editor.set_code(code)
        self.editor.set_tab_name(f"{lesson_name}.py")
        self.executor.console.write(f"Lecon '{lesson_name}' chargee.", "system")
