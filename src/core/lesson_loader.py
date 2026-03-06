class LessonLoader:
    """Catalogue de leçons embarquées et getter de contenus."""
    
    _LESSONS = {
        "bases_widgets": '''import tkinter as tk

# 1. Label (Afficher du texte)
label = tk.Label(preview_frame, text="Les Bases : Label, Entry, Button", font=("Arial", 12, "bold"))
label.pack(pady=10)

# 2. Entry (Saisie de texte)
tk.Label(preview_frame, text="Entrez votre prénom :").pack()
entry = tk.Entry(preview_frame, font=("Arial", 11), justify="center")
entry.pack(pady=5)

# 3. Button (Action interactive)
def_reponse = tk.Label(preview_frame, text="", fg="blue", font=("Arial", 11, "italic"))

def saluer():
    nom = entry.get()
    if nom:
        def_reponse.config(text=f"👋 Bonjour, {nom} !")
    else:
        def_reponse.config(text="Veuillez entrer un nom.", fg="red")

btn = tk.Button(preview_frame, text="Valider", command=saluer, bg="#4CAF50", fg="white", cursor="hand2")
btn.pack(pady=10)

def_reponse.pack(pady=5)
''',

        "choix_multiples": '''import tkinter as tk
from tkinter import ttk

tk.Label(preview_frame, text="Choisir des Options", font=("Arial", 12, "bold")).pack(pady=10)

# 1. Checkbutton (Cases à cocher)
var_check = tk.IntVar()
chk = tk.Checkbutton(preview_frame, text="Activer le mode sombre", variable=var_check)
chk.pack(anchor="w", padx=30, pady=5)

# 2. Radiobutton (Choix unique)
var_radio = tk.IntVar()
var_radio.set(1) # Valeur par défaut
tk.Label(preview_frame, text="Niveau :").pack(anchor="w", padx=20, pady=(10, 0))
tk.Radiobutton(preview_frame, text="Débutant", variable=var_radio, value=1).pack(anchor="w", padx=30)
tk.Radiobutton(preview_frame, text="Expert", variable=var_radio, value=2).pack(anchor="w", padx=30)

# 3. Combobox (Menu déroulant - ttk)
tk.Label(preview_frame, text="Langage préféré :").pack(anchor="w", padx=20, pady=(10, 0))
combo = ttk.Combobox(preview_frame, values=["Python", "JavaScript", "C++"], state="readonly")
combo.set("Python")
combo.pack(anchor="w", padx=30, pady=5)
''',

        "geometrie_grid": '''import tkinter as tk

# Titre centré sur 2 colonnes
tk.Label(preview_frame, text="Formulaire avec Grid()", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

# Ligne 1
tk.Label(preview_frame, text="Prénom :").grid(row=1, column=0, sticky="e", padx=10, pady=5)
tk.Entry(preview_frame).grid(row=1, column=1, padx=10, pady=5)

# Ligne 2
tk.Label(preview_frame, text="Nom :").grid(row=2, column=0, sticky="e", padx=10, pady=5)
tk.Entry(preview_frame).grid(row=2, column=1, padx=10, pady=5)

# Ligne 3: Bouton qui s'étend ("sticky=ew")
btn = tk.Button(preview_frame, text="Envoyer", bg="#008CBA", fg="white")
btn.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=20)
''',

        "dessin_canvas": '''import tkinter as tk

tk.Label(preview_frame, text="Dessin & Formes (Canvas)", font=("Arial", 12, "bold")).pack(pady=10)

# Création de la zone de dessin
canvas = tk.Canvas(preview_frame, width=300, height=200, bg="white", highlightthickness=1, highlightbackground="gray")
canvas.pack(pady=10)

# 1. Ligne
canvas.create_line(20, 20, 280, 50, fill="red", width=3)

# 2. Rectangle
canvas.create_rectangle(50, 70, 150, 150, fill="lightblue", outline="blue", width=2)

# 3. Ovale / Cercle
canvas.create_oval(170, 70, 250, 150, fill="yellow", outline="orange", width=2)

# 4. Texte dans le canvas
canvas.create_text(150, 180, text="Tkinter Canvas", fill="green", font=("Arial", 10, "italic"))
''',

        "evenements": '''import tkinter as tk

tk.Label(preview_frame, text="Gestion des Événements", font=("Arial", 12, "bold")).pack(pady=10)
info = tk.Label(preview_frame, text="Passez la souris sur le bouton", fg="gray")
info.pack(pady=10)

def on_enter(e):
    btn.config(bg="gold", text="🔥 Magique !")
    info.config(text="Événement : <Enter>", fg="orange")

def on_leave(e):
    btn.config(bg="SystemButtonFace", text="Survolez-moi")
    info.config(text="Événement : <Leave>", fg="gray")

def on_click(e):
    info.config(text=f"Clic aux coordonnées X:{e.x} Y:{e.y}", fg="green")

btn = tk.Button(preview_frame, text="Survolez-moi", font=("Arial", 12), width=20, height=2)
btn.pack(pady=20)

# Attachement des "Bindings"
btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)
btn.bind("<Button-1>", on_click)
'''
    }

    @staticmethod
    def get_lesson(lesson_name):
        """Retourne le code source de la leçon demandée."""
        return LessonLoader._LESSONS.get(lesson_name, "# Leçon introuvable.")
