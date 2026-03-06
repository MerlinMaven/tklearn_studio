import tkinter as tk
from tkinter import ttk
import re
from src.ui.theme import (
    BG_MEDIUM, BG_DARK, FG_SECONDARY, FG_PRIMARY, FG_DIM, FG_BRIGHT,
    ACCENT_BLUE, FONT_UI_BOLD, FONT_CODE, FONT_CODE_BOLD, FONT_CODE_ITALIC,
    SYNTAX_KEYWORD, SYNTAX_BUILTIN, SYNTAX_STRING, SYNTAX_COMMENT,
    SYNTAX_NUMBER, SYNTAX_SELF, BG_HOVER
)


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
        except tk.TclError:
            return None

        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        return result


class LineNumbers(tk.Canvas):
    def __init__(self, parent, text_widget, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.text_widget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(self.winfo_width() - 5, y, anchor="ne", 
                             text=linenum, font=FONT_CODE, fill=FG_DIM)
            
            i = self.text_widget.index(f"{i}+1line")
            if self.text_widget.compare(i, ">=", "end"):
                break


class CodeEditor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_MEDIUM)
        
        # Header
        self.header_frame = tk.Frame(self, bg=BG_MEDIUM)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.accent = tk.Frame(self.header_frame, bg=ACCENT_BLUE, width=3)
        self.accent.pack(side=tk.LEFT, fill=tk.Y)
        
        self.header = tk.Label(
            self.header_frame, text="  EDITEUR", 
            bg=BG_MEDIUM, fg=FG_DIM, font=FONT_UI_BOLD, 
            anchor="w", padx=10, pady=5
        )
        self.header.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Tab bar
        self.tab_frame = tk.Frame(self, bg="#1a1a1a", height=28)
        self.tab_frame.pack(side=tk.TOP, fill=tk.X)
        self.tab_frame.pack_propagate(False)
        
        # Active tab
        self.tab_container = tk.Frame(self.tab_frame, bg=BG_DARK)
        self.tab_container.pack(side=tk.LEFT, fill=tk.Y)
        
        self.tab_accent = tk.Frame(self.tab_container, bg=ACCENT_BLUE, height=2)
        self.tab_accent.pack(side=tk.TOP, fill=tk.X)
        
        self.tab_label = tk.Label(
            self.tab_container, text="  sans_titre.py", 
            bg=BG_DARK, fg=FG_PRIMARY, font=("Segoe UI", 8),
            anchor="w", padx=12, pady=3
        )
        self.tab_label.pack(fill=tk.BOTH, expand=True)
        
        # Rest of tab bar (darker fill)
        tk.Frame(self.tab_frame, bg="#1a1a1a").pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Editor area
        self.text_frame = tk.Frame(self, bg=BG_DARK)
        self.text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=1, pady=(0, 1))
        
        self.scrollbar = ttk.Scrollbar(self.text_frame, style="Dark.Vertical.TScrollbar")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_widget = CustomText(
            self.text_frame, wrap=tk.NONE, yscrollcommand=self.scrollbar.set, 
            font=FONT_CODE, bg=BG_DARK, fg=FG_PRIMARY,
            insertbackground="white", selectbackground="#264f78",
            relief=tk.FLAT, padx=10, pady=10, borderwidth=0
        )
        
        self.line_numbers = LineNumbers(
            self.text_frame, self.text_widget, width=45, 
            bg=BG_DARK, highlightthickness=0
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.text_widget.yview)

        self.text_widget.bind("<<Change>>", self._on_change)
        self.text_widget.bind("<Configure>", self._on_change)
        
        self._setup_syntax_highlighting()
        self._setup_smart_typing()
        self._insert_welcome()
        self.after(50, self.line_numbers.redraw)

    def _insert_welcome(self):
        """Code de démarrage simple et utile."""
        welcome = '''import tkinter as tk

root = tk.Tk()
root.title("Mon Application")

label = tk.Label(root, text="Bienvenue dans TkLearn Studio", font=("Arial", 14))
label.pack(pady=20)

bouton = tk.Button(root, text="Cliquez-moi", command=lambda: print("Bravo !"))
bouton.pack(pady=10)

root.mainloop()
'''
        self.text_widget.insert("1.0", welcome)
        self._highlight_syntax()

    def _setup_smart_typing(self):
        self.text_widget.bind("<KeyRelease-parenleft>", lambda e: self._insert_and_move(")", -1))
        self.text_widget.bind("<KeyRelease-bracketleft>", lambda e: self._insert_and_move("]", -1))
        self.text_widget.bind("<KeyRelease-braceleft>", lambda e: self._insert_and_move("}", -1))
        self.text_widget.bind("<KeyRelease-quotedbl>", lambda e: self._auto_quote("\""))
        self.text_widget.bind("<KeyRelease-quoteright>", lambda e: self._auto_quote("'"))
        self.text_widget.bind("<KeyRelease-apostrophe>", lambda e: self._auto_quote("'"))
        self.text_widget.bind("<Return>", self._smart_indent)
        
    def _insert_and_move(self, char, offset):
        self.text_widget.insert(tk.INSERT, char)
        self.text_widget.mark_set(tk.INSERT, f"{tk.INSERT}{offset}c")
        
    def _auto_quote(self, char):
        current_pos = self.text_widget.index(tk.INSERT)
        prev_char = self.text_widget.get(f"{current_pos}-1c", current_pos)
        next_char = self.text_widget.get(current_pos, f"{current_pos}+1c")
        
        if prev_char == char and next_char == char:
            self.text_widget.delete(f"{current_pos}-1c", current_pos)
            self.text_widget.mark_set(tk.INSERT, f"{current_pos}+1c")
        else:
            self._insert_and_move(char, -1)

    def _smart_indent(self, event):
        current_line_idx = self.text_widget.index("insert linestart")
        current_line_text = self.text_widget.get(current_line_idx, "insert lineend")
        
        indent = ""
        for char in current_line_text:
            if char in (" ", "\t"):
                indent += char
            else:
                break
                
        if current_line_text.strip().endswith(":"):
            indent += "    "
            
        if indent:
            self.text_widget.insert(tk.INSERT, indent)
            return "break"

    def _setup_syntax_highlighting(self):
        self.text_widget.tag_configure("Keyword", foreground=SYNTAX_KEYWORD, font=FONT_CODE_BOLD)
        self.text_widget.tag_configure("Builtin", foreground=SYNTAX_BUILTIN)
        self.text_widget.tag_configure("String", foreground=SYNTAX_STRING)
        self.text_widget.tag_configure("Comment", foreground=SYNTAX_COMMENT, font=FONT_CODE_ITALIC)
        self.text_widget.tag_configure("Number", foreground=SYNTAX_NUMBER)
        self.text_widget.tag_configure("Self", foreground=SYNTAX_SELF, font=FONT_CODE_ITALIC)

    def _highlight_syntax(self):
        
        for tag in ["Keyword", "Builtin", "String", "Comment", "Number", "Self"]:
            self.text_widget.tag_remove(tag, "1.0", tk.END)

        code = self.text_widget.get("1.0", tk.END)

        keywords = ["def", "class", "import", "from", "as", "return", "pass", "if", "elif", "else", 
                    "while", "for", "in", "break", "continue", "True", "False", "None", "and", "or", "not",
                    "try", "except", "finally", "with", "yield", "lambda", "global", "nonlocal", "raise",
                    "del", "assert", "is"]
        kw_pattern = r'\b(' + '|'.join(keywords) + r')\b'
        self._apply_tag("Keyword", kw_pattern, code)

        builtins = ["print", "len", "range", "str", "int", "float", "list", "dict", "super",
                    "type", "isinstance", "hasattr", "getattr", "setattr", "enumerate", "zip", "map", "filter"]
        bi_pattern = r'\b(' + '|'.join(builtins) + r')\b'
        self._apply_tag("Builtin", bi_pattern, code)
        
        self._apply_tag("Self", r'\bself\b', code)
        self._apply_tag("Number", r'\b\d+\.?\d*\b', code)
        self._apply_tag("String", r"'.*?'|\".*?\"", code)
        self._apply_tag("Comment", r'#.*$', code)

    def _apply_tag(self, tag_name, pattern, text):
        for match in re.finditer(pattern, text, re.MULTILINE):
            start = match.start()
            end = match.end()
            
            line_start = text.count('\n', 0, start) + 1
            col_start = start - text.rfind('\n', 0, start) - 1
            if start < text.find('\n'): col_start = start
            
            line_end = text.count('\n', 0, end) + 1
            col_end = end - text.rfind('\n', 0, end) - 1
            if end < text.find('\n'): col_end = end
                
            self.text_widget.tag_add(tag_name, f"{line_start}.{col_start}", f"{line_end}.{col_end}")

    def _on_change(self, event=None):
        self.line_numbers.redraw()
        if hasattr(self, '_highlight_id'):
            self.after_cancel(self._highlight_id)
        self._highlight_id = self.after(200, self._highlight_syntax)

    def get_code(self):
        return self.text_widget.get("1.0", tk.END)
        
    def set_code(self, code):
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", code)
        self.line_numbers.redraw()
        self._highlight_syntax()
    
    def set_tab_name(self, filename):
        self.tab_label.config(text=f"  {filename}")
