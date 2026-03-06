"""
Module de thème centralisé pour TkLearn Studio.
Toutes les couleurs, polices et spacings en un seul endroit.
"""
from tkinter import ttk

# ─── Couleurs Principales ───────────────────────────────────────
BG_DARK = "#1e1e1e"         # Fond d'éditeur / zones profondes
BG_MEDIUM = "#252526"       # Fond de panneaux
BG_SURFACE = "#2d2d30"      # Fond principal de la fenêtre
BG_ACTIVITY = "#333333"     # Activity bar
BG_HOVER = "#3e3e42"        # Survol
BG_ACTIVE = "#505050"       # Actif/pressé

# ─── Couleurs d'Accent ─────────────────────────────────────────
ACCENT_BLUE = "#007acc"     # Bleu VS Code
ACCENT_GREEN = "#4ec9b0"    # Vert succès / builtins
ACCENT_RED = "#f44747"      # Erreur
ACCENT_ORANGE = "#ce9178"   # Avertissement / strings
ACCENT_YELLOW = "#dcdcaa"   # Fonctions
ACCENT_PURPLE = "#c586c0"   # Mots-clés importés

# ─── Couleurs de Texte ─────────────────────────────────────────
FG_PRIMARY = "#d4d4d4"      # Texte principal
FG_SECONDARY = "#cccccc"    # Texte secondaire
FG_DIM = "#858585"          # Texte atténué
FG_BRIGHT = "#ffffff"       # Texte blanc pur

# ─── Console ───────────────────────────────────────────────────
CONSOLE_BG = "#181818"      # Fond console (gris fonce neutre)
CONSOLE_FG = "#cccccc"      # Texte console standard
CONSOLE_ERROR = "#f44747"   # Texte erreur
CONSOLE_SUCCESS = "#4ec9b0" # Texte succès
CONSOLE_INFO = "#569cd6"    # Texte info
CONSOLE_SYSTEM = "#858585"  # Texte système

# ─── Status Bar ─────────────────────────────────────────────────
STATUS_BG = "#007acc"       # Fond barre de statut
STATUS_FG = "#ffffff"       # Texte barre de statut

# ─── Polices ────────────────────────────────────────────────────
FONT_CODE = ("Consolas", 12)
FONT_CODE_BOLD = ("Consolas", 12, "bold")
FONT_CODE_ITALIC = ("Consolas", 12, "italic")
FONT_UI = ("Segoe UI", 9)
FONT_UI_BOLD = ("Segoe UI", 9, "bold")
FONT_UI_MEDIUM = ("Segoe UI", 10)
FONT_UI_LARGE = ("Segoe UI", 11)
FONT_ICON = ("Segoe UI", 14)
FONT_ICON_SMALL = ("Segoe UI", 12)

# ─── Espacements ────────────────────────────────────────────────
PAD_HEADER = 8
PAD_PANEL = 2
ACTIVITY_BAR_WIDTH = 45
SASH_WIDTH = 4

# ─── Syntax Highlighting (VS Code Dark+) ───────────────────────
SYNTAX_KEYWORD = "#569cd6"
SYNTAX_BUILTIN = "#4ec9b0"
SYNTAX_STRING = "#ce9178"
SYNTAX_COMMENT = "#6a9955"
SYNTAX_NUMBER = "#b5cea8"
SYNTAX_SELF = "#569cd6"
SYNTAX_DECORATOR = "#dcdcaa"


def configure_dark_scrollbar(root):
    """Configure un style de scrollbar sombre pour ttk."""
    style = ttk.Style(root)
    
    # S'assurer d'utiliser le thème 'clam' qui supporte bien la personnalisation
    if "clam" in style.theme_names():
        style.theme_use("clam")
    
    style.configure("Dark.Vertical.TScrollbar",
                     background=BG_HOVER,
                     troughcolor=BG_DARK,
                     bordercolor=BG_DARK,
                     arrowcolor=FG_DIM,
                     relief="flat",
                     borderwidth=0)
    style.map("Dark.Vertical.TScrollbar",
              background=[("active", BG_ACTIVE), ("pressed", FG_DIM)])

    style.configure("Dark.Horizontal.TScrollbar",
                     background=BG_HOVER,
                     troughcolor=BG_DARK,
                     bordercolor=BG_DARK,
                     arrowcolor=FG_DIM,
                     relief="flat",
                     borderwidth=0)
    style.map("Dark.Horizontal.TScrollbar",
              background=[("active", BG_ACTIVE), ("pressed", FG_DIM)])
              
    return style
