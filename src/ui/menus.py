import tkinter as tk

class AppMenu:
    def __init__(self, root, editor, executor, file_manager):
        self.root = root
        self.editor = editor
        self.executor = executor
        self.file_manager = file_manager
        
        self.menubar = tk.Menu(self.root)
        
        self._build_fichier_menu()
        self._build_lecons_menu()
        self._build_execution_menu()
        self._build_outils_menu()
        self._build_aide_menu()
        
        # On attache le menu à la racine APRÈS l'avoir construit
        self.root.config(menu=self.menubar)
        
        # Raccourci F5 pour lancer le code
        self.root.bind("<F5>", lambda event: self.executor.run_code())
        self.root.bind("<Control-s>", lambda event: self.file_manager.save_file())

    def _build_fichier_menu(self):
        menu = tk.Menu(self.menubar, tearoff=0)
        menu.add_command(label="Ouvrir...", command=self.file_manager.open_file)
        menu.add_command(label="Enregistrer (Ctrl+S)", command=self.file_manager.save_file)
        menu.add_command(label="Enregistrer sous...", command=self.file_manager.save_file_as)
        menu.add_separator()
        menu.add_command(label="Quitter", command=self.root.quit)
        self.menubar.add_cascade(label="Fichier", menu=menu)

    def _build_lecons_menu(self):
        menu = tk.Menu(self.menubar, tearoff=0)
        menu.add_command(label="1. Les Bases (Label, Entry, Bouton)", command=lambda: self._load_lesson("bases_widgets"))
        menu.add_command(label="2. Choix Multiples (Radio, Check, Combo)", command=lambda: self._load_lesson("choix_multiples"))
        menu.add_command(label="3. Mise en page (Geométrie Grid)", command=lambda: self._load_lesson("geometrie_grid"))
        menu.add_command(label="4. Dessin Artistique (Canvas)", command=lambda: self._load_lesson("dessin_canvas"))
        menu.add_command(label="5. Interactions (Événements)", command=lambda: self._load_lesson("evenements"))
        self.menubar.add_cascade(label="Leçons", menu=menu)

    def _build_execution_menu(self):
        menu = tk.Menu(self.menubar, tearoff=0)
        menu.add_command(label="Lancer (F5)", command=self.executor.run_code)
        self.menubar.add_cascade(label="Exécution", menu=menu)

    def _build_outils_menu(self):
        menu = tk.Menu(self.menubar, tearoff=0)
        menu.add_command(label="Nettoyer Console", command=self.executor.console.clear)
        self.menubar.add_cascade(label="Outils", menu=menu)

    def _build_aide_menu(self):
        menu = tk.Menu(self.menubar, tearoff=0)
        menu.add_command(label="À propos", command=lambda: self.executor.console.write("TkLearn Studio - Outil d'apprentissage Tkinter\nDéveloppé pour l'apprentissage guidé."))
        self.menubar.add_cascade(label="Aide", menu=menu)

    def _load_lesson(self, lesson_name):
        from src.core.lesson_loader import LessonLoader
        
        # Récupérer le code via le loader externe
        code = LessonLoader.get_lesson(lesson_name)
        
        # Injecter le code dans l'éditeur
        self.editor.set_code(code)
        self.executor.console.write(f"--- Leçon '{lesson_name}' chargée ---")
