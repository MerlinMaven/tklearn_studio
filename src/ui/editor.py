import tkinter as tk

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # Create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # Let the actual widget perform the requested action
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
        except tk.TclError:
            return None

        # Generate an event if something changed that affects line numbers
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
            if dline is None: pass # sometimes at bottom it's None before full render
            elif getattr(self.text_widget, "yview")()[1] != 1.0 or dline is not None:
                y = dline[1]
                linenum = str(i).split(".")[0]
                self.create_text(self.winfo_width() - 5, y, anchor="ne", 
                                 text=linenum, font=("Consolas", 12), fill="#858585")
            
            i = self.text_widget.index(f"{i}+1line")
            if self.text_widget.compare(i, ">", "end-1c"):
                break


class CodeEditor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#252526")
        
        # Header
        self.header = tk.Label(self, text=" ÉDITEUR DE CODE (PYTHON)", bg="#252526", fg="#cccccc", font=("Segoe UI", 9), anchor="w", padx=15, pady=8)
        self.header.pack(side=tk.TOP, fill=tk.X)
        
        # Text area container
        self.text_frame = tk.Frame(self, bg="#1e1e1e")
        self.text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # CustomText instead of normal Text
        self.text_widget = CustomText(self.text_frame, wrap=tk.NONE, yscrollcommand=self.scrollbar.set, 
                                   font=("Consolas", 12), bg="#1e1e1e", fg="#d4d4d4",
                                   insertbackground="white", selectbackground="#264f78",
                                   relief=tk.FLAT, padx=10, pady=10, borderwidth=0)
        
        # Line numbers canvas
        self.line_numbers = LineNumbers(self.text_frame, self.text_widget, width=40, bg="#1e1e1e", highlightthickness=0)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.text_widget.yview)

        # Event bindings to redraw line numbers
        self.text_widget.bind("<<Change>>", self._on_change)
        self.text_widget.bind("<Configure>", self._on_change)
        
        # Configure syntax highlighting tags
        self._setup_syntax_highlighting()
        
        # Smart typing features
        self._setup_smart_typing()
        
        # Initial draw
        self.after(50, self.line_numbers.redraw)

    def _setup_smart_typing(self):
        # Auto-close brackets and quotes
        self.text_widget.bind("<KeyRelease-parenleft>", lambda e: self._insert_and_move(")", -1))
        self.text_widget.bind("<KeyRelease-bracketleft>", lambda e: self._insert_and_move("]", -1))
        self.text_widget.bind("<KeyRelease-braceleft>", lambda e: self._insert_and_move("}", -1))
        self.text_widget.bind("<KeyRelease-quotedbl>", lambda e: self._auto_quote("\""))
        self.text_widget.bind("<KeyRelease-quoteright>", lambda e: self._auto_quote("'"))
        # Using apostrophe for single quote on some keyboards
        self.text_widget.bind("<KeyRelease-apostrophe>", lambda e: self._auto_quote("'"))
        
        # Smart Return (Indentation)
        self.text_widget.bind("<Return>", self._smart_indent)
        
    def _insert_and_move(self, char, offset):
        self.text_widget.insert(tk.INSERT, char)
        self.text_widget.mark_set(tk.INSERT, f"{tk.INSERT}{offset}c")
        
    def _auto_quote(self, char):
        # Prevent double closing if user types the closing quote manually
        current_pos = self.text_widget.index(tk.INSERT)
        prev_char = self.text_widget.get(f"{current_pos}-1c", current_pos)
        next_char = self.text_widget.get(current_pos, f"{current_pos}+1c")
        
        # If we just typed a quote and the next char is already that quote, 
        # it means user typed closing quote. Delete what we just typed and move forward.
        if prev_char == char and next_char == char:
            self.text_widget.delete(f"{current_pos}-1c", current_pos)
            self.text_widget.mark_set(tk.INSERT, f"{current_pos}+1c")
        else:
            self._insert_and_move(char, -1)

    def _smart_indent(self, event):
        # Custom Return handling
        current_line_idx = self.text_widget.index("insert - 1 line")
        current_line_text = self.text_widget.get(f"{current_line_idx} linestart", f"{current_line_idx} lineend")
        
        # Find current indentation
        indent = ""
        for char in current_line_text:
            if char in (" ", "\t"):
                indent += char
            else:
                break
                
        # If line ends with colon, increase indentation
        if current_line_text.strip().endswith(":"):
            indent += "    " # 4 spaces
            
        # Insert the calculated indentation
        if indent:
            self.text_widget.insert(tk.INSERT, indent)
            return "break" # Prevent default return if we modified something, though tk already did the newline.
        

    def _setup_syntax_highlighting(self):
        # VS Code Dark+ Theme colors
        self.text_widget.tag_configure("Keyword", foreground="#569cd6", font=("Consolas", 12, "bold"))
        self.text_widget.tag_configure("Builtin", foreground="#4ec9b0")
        self.text_widget.tag_configure("String", foreground="#ce9178")
        self.text_widget.tag_configure("Comment", foreground="#6a9955", font=("Consolas", 12, "italic"))
        self.text_widget.tag_configure("Number", foreground="#b5cea8")
        self.text_widget.tag_configure("Self", foreground="#569cd6", font=("Consolas", 12, "italic"))

    def _highlight_syntax(self):
        import re
        
        # Effacer tous les anciens tags
        for tag in ["Keyword", "Builtin", "String", "Comment", "Number", "Self"]:
            self.text_widget.tag_remove(tag, "1.0", tk.END)

        code = self.text_widget.get("1.0", tk.END)

        # Mots-clés Python (Keyword)
        keywords = ["def", "class", "import", "from", "as", "return", "pass", "if", "elif", "else", 
                    "while", "for", "in", "break", "continue", "True", "False", "None", "and", "or", "not"]
        kw_pattern = r'\b(' + '|'.join(keywords) + r')\b'
        self._apply_tag("Keyword", kw_pattern, code)

        # Builtins souvent utilisés par l'utilisateur
        builtins = ["print", "len", "range", "str", "int", "float", "list", "dict", "super"]
        bi_pattern = r'\b(' + '|'.join(builtins) + r')\b'
        self._apply_tag("Builtin", bi_pattern, code)
        
        # Self
        self._apply_tag("Self", r'\bself\b', code)
        
        # Nombres
        self._apply_tag("Number", r'\b\d+\.?\d*\b', code)

        # Chaines de caractères (simples et doubles)
        self._apply_tag("String", r"'.*?'|\".*?\"", code)

        # Commentaires
        self._apply_tag("Comment", r'#.*$', code)

    def _apply_tag(self, tag_name, pattern, text):
        import re
        for match in re.finditer(pattern, text, re.MULTILINE):
            start = match.start()
            end = match.end()
            
            # Convert str index to Tkinter text index
            # This is a bit slow for huge files, but perfect for a learning studio
            line_start = text.count('\n', 0, start) + 1
            col_start = start - text.rfind('\n', 0, start) - 1
            if start < text.find('\n'): col_start = start # first line fix
            
            line_end = text.count('\n', 0, end) + 1
            col_end = end - text.rfind('\n', 0, end) - 1
            if end < text.find('\n'): col_end = end
                
            self.text_widget.tag_add(tag_name, f"{line_start}.{col_start}", f"{line_end}.{col_end}")

    def _on_change(self, event=None):
        self.line_numbers.redraw()
        # On debounce légèrement la coloration pour ne pas lagger à chaque touche
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
