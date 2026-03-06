import tkinter as tk
from tkinter import ttk
from src.ui.theme import (
    BG_MEDIUM, BG_DARK, FG_SECONDARY, FG_PRIMARY, FG_DIM, FG_BRIGHT,
    ACCENT_BLUE, FONT_UI_BOLD, FONT_UI_MEDIUM, BG_HOVER
)


class WidgetInspector(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_MEDIUM)
        
        # Header
        self.header_frame = tk.Frame(self, bg=BG_MEDIUM)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.accent = tk.Frame(self.header_frame, bg=ACCENT_BLUE, width=3)
        self.accent.pack(side=tk.LEFT, fill=tk.Y)
        
        self.header = tk.Label(
            self.header_frame, text="  EXPLORATEUR", 
            bg=BG_MEDIUM, fg=FG_DIM, font=FONT_UI_BOLD, 
            anchor="w", padx=10, pady=5
        )
        self.header.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Container
        self.tree_frame = tk.Frame(self, bg=BG_DARK)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=1, pady=(0, 1))
        
        # Treeview styling (theme already set by configure_dark_scrollbar)
        style = ttk.Style()
            
        style.configure("Treeview", 
                        background=BG_DARK,
                        foreground=FG_PRIMARY,
                        fieldbackground=BG_DARK,
                        borderwidth=0,
                        font=FONT_UI_MEDIUM,
                        rowheight=24)
                        
        style.map('Treeview', 
                  background=[('selected', '#37373d')], 
                  foreground=[('selected', FG_BRIGHT)])
                  
        style.configure("Treeview.Heading", 
                        background=BG_MEDIUM, 
                        foreground=FG_DIM, 
                        font=FONT_UI_BOLD, 
                        borderwidth=0,
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', BG_HOVER)])
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.tree_frame, style="Dark.Vertical.TScrollbar")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(
            self.tree_frame, selectmode="browse", 
            yscrollcommand=self.scrollbar.set
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("#0", text="Composants", anchor="w")
        self.tree.column("#0", width=200, stretch=True)

    def refresh(self, parent_widget):
        self.tree.delete(*self.tree.get_children())
        preview_node = self.tree.insert("", "end", text="Fenetre Principale", open=True)
        self._populate_tree(preview_node, parent_widget)

    def _populate_tree(self, parent_node, current_widget):
        for child in current_widget.winfo_children():
            class_name = child.__class__.__name__
            
            extra_info = ""
            try:
                text = child.cget("text")
                if text:
                    display_text = text if len(text) < 20 else text[:17] + "..."
                    extra_info = f'  "{display_text}"'
            except:
                pass
            
            # Clean type indicators
            prefix = "\u2500"  # ─
            if class_name in ("Frame", "LabelFrame", "PanedWindow"):
                prefix = "\u25B8"  # ▸
            elif class_name in ("Button", "Radiobutton", "Checkbutton"):
                prefix = "\u25CB"  # ○
            elif class_name in ("Label", "Message"):
                prefix = "\u2012"  # ‒
            elif class_name in ("Entry", "Text", "Spinbox"):
                prefix = "\u25A1"  # □
            elif class_name in ("Canvas",):
                prefix = "\u25C7"  # ◇
                
            node_text = f"{prefix} {class_name}{extra_info}"
            node_id = self.tree.insert(parent_node, "end", text=node_text, open=True)
            self._populate_tree(node_id, child)
