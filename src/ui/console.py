import tkinter as tk
from tkinter import ttk
from src.ui.theme import (
    BG_MEDIUM, BG_DARK, FG_SECONDARY, FG_DIM, FG_BRIGHT, FONT_UI_BOLD, FONT_CODE,
    CONSOLE_BG, CONSOLE_FG, CONSOLE_ERROR, CONSOLE_SUCCESS, 
    CONSOLE_INFO, CONSOLE_SYSTEM, ACCENT_BLUE, BG_HOVER
)


class ConsoleOutput(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_MEDIUM)
        
        # Header
        self.header_frame = tk.Frame(self, bg=BG_MEDIUM)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.accent = tk.Frame(self.header_frame, bg=ACCENT_BLUE, width=3)
        self.accent.pack(side=tk.LEFT, fill=tk.Y)
        
        self.header = tk.Label(
            self.header_frame, text="  CONSOLE", 
            bg=BG_MEDIUM, fg=FG_DIM, font=FONT_UI_BOLD, 
            anchor="w", padx=10, pady=5
        )
        self.header.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Clear button
        self.clear_btn = tk.Label(
            self.header_frame, text="\u2715", bg=BG_MEDIUM, fg=FG_DIM,
            font=("Segoe UI", 9), cursor="hand2", padx=8
        )
        self.clear_btn.pack(side=tk.RIGHT, padx=(0, 4))
        self.clear_btn.bind("<Button-1>", lambda e: self.clear())
        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(fg=FG_BRIGHT))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(fg=FG_DIM))
        
        # Text output
        self.text_frame = tk.Frame(self, bg=CONSOLE_BG)
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=(0, 1))
        
        self.scrollbar = ttk.Scrollbar(self.text_frame, style="Dark.Vertical.TScrollbar")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_widget = tk.Text(
            self.text_frame, height=8, state='disabled', 
            bg=CONSOLE_BG, fg=CONSOLE_FG, font=FONT_CODE,
            relief=tk.FLAT, padx=10, pady=8, borderwidth=0,
            yscrollcommand=self.scrollbar.set
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.text_widget.yview)
        
        # Tags
        self.text_widget.tag_configure("error", foreground=CONSOLE_ERROR)
        self.text_widget.tag_configure("success", foreground=CONSOLE_SUCCESS)
        self.text_widget.tag_configure("info", foreground=CONSOLE_INFO)
        self.text_widget.tag_configure("system", foreground=CONSOLE_SYSTEM)
        self.text_widget.tag_configure("default", foreground=CONSOLE_FG)
        
    def write(self, message, tag="default"):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, message + "\n", tag)
        self.text_widget.configure(state='disabled')
        self.text_widget.see(tk.END)
        
    def clear(self):
        self.text_widget.configure(state='normal')
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.configure(state='disabled')
