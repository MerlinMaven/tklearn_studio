import tkinter as tk
from src.ui.theme import (
    BG_MEDIUM, FG_SECONDARY, FG_DIM, FG_BRIGHT, ACCENT_BLUE, FONT_UI_BOLD
)


class PreviewFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_MEDIUM)
        
        # Header
        self.header_frame = tk.Frame(self, bg=BG_MEDIUM)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.accent = tk.Frame(self.header_frame, bg=ACCENT_BLUE, width=3)
        self.accent.pack(side=tk.LEFT, fill=tk.Y)
        
        self.header = tk.Label(
            self.header_frame, text="  APERCU", 
            bg=BG_MEDIUM, fg=FG_DIM, font=FONT_UI_BOLD, 
            anchor="w", padx=10, pady=5
        )
        self.header.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Shortcut badge
        self.badge = tk.Label(
            self.header_frame, text="F5", bg="#3e3e42", fg=FG_DIM,
            font=("Segoe UI", 7), padx=4, pady=1
        )
        self.badge.pack(side=tk.RIGHT, padx=(0, 8), pady=4)
        
        # Preview area (click to capture keyboard focus)
        self.inner_frame = tk.Frame(self, bg="#f0f0f0", takefocus=1)
        self.inner_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=(0, 1))
        self.inner_frame.bind("<Button-1>", lambda e: self.inner_frame.focus_set())
        
    def clear(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
