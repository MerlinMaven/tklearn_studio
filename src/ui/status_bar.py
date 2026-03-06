import tkinter as tk
from src.ui.theme import (STATUS_BG, STATUS_FG, FONT_UI)


class StatusBar(tk.Frame):
    """Barre de statut minimaliste."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=STATUS_BG, height=22)
        self.pack_propagate(False)
        
        # Left: status + file
        self.left_frame = tk.Frame(self, bg=STATUS_BG)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))
        
        self.status_label = tk.Label(
            self.left_frame, text="Pret", 
            bg=STATUS_BG, fg=STATUS_FG, font=FONT_UI, anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 15))
        
        self.file_label = tk.Label(
            self.left_frame, text="sans_titre.py", 
            bg=STATUS_BG, fg=STATUS_FG, font=FONT_UI, anchor="w"
        )
        self.file_label.pack(side=tk.LEFT)
        
        # Right: cursor + encoding
        self.right_frame = tk.Frame(self, bg=STATUS_BG)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
        
        self.encoding_label = tk.Label(
            self.right_frame, text="UTF-8",
            bg=STATUS_BG, fg=STATUS_FG, font=FONT_UI, anchor="e"
        )
        self.encoding_label.pack(side=tk.RIGHT, padx=(12, 0))
        
        self.lang_label = tk.Label(
            self.right_frame, text="Python",
            bg=STATUS_BG, fg=STATUS_FG, font=FONT_UI, anchor="e"
        )
        self.lang_label.pack(side=tk.RIGHT, padx=(12, 0))
        
        self.cursor_label = tk.Label(
            self.right_frame, text="Ln 1, Col 1", 
            bg=STATUS_BG, fg=STATUS_FG, font=FONT_UI, anchor="e"
        )
        self.cursor_label.pack(side=tk.RIGHT)
    
    def update_cursor(self, line, col):
        self.cursor_label.config(text=f"Ln {line}, Col {col}")
    
    def update_filename(self, name):
        self.file_label.config(text=name if name else "sans_titre.py")
    
    def set_status(self, text, running=False):
        self.status_label.config(text=text)
