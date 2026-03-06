import tkinter as tk
from tkinter import ttk
from src.ui.theme import (
    BG_MEDIUM, BG_DARK, FG_BRIGHT, FG_DIM, FG_PRIMARY, FG_SECONDARY,
    ACCENT_BLUE, FONT_UI_BOLD, FONT_UI, BG_HOVER, BG_ACTIVE, CONSOLE_BG
)
from src.core.ai_client import AVAILABLE_MODELS


class AIPanel(tk.Frame):
    """Panneau IA style chat avec historique de conversation."""
    
    # Couleurs internes coherentes avec le theme
    INPUT_BG = "#2a2a2d"
    BUBBLE_USER = "#2a2d3a"
    BUBBLE_AI = "#252528"
    
    def __init__(self, parent, editor, ai_client):
        super().__init__(parent, bg=BG_DARK)
        self.editor = editor
        self.ai_client = ai_client
        
        # Header
        header_frame = tk.Frame(self, bg=BG_MEDIUM)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        tk.Frame(header_frame, bg=ACCENT_BLUE, width=3).pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(
            header_frame, text="  ASSISTANT", 
            bg=BG_MEDIUM, fg=FG_DIM, font=FONT_UI_BOLD, 
            anchor="w", padx=10, pady=5
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Clear chat button
        self.clear_chat_btn = tk.Label(
            header_frame, text="\u2715", bg=BG_MEDIUM, fg=FG_DIM,
            font=("Segoe UI", 9), cursor="hand2", padx=6
        )
        self.clear_chat_btn.pack(side=tk.RIGHT, padx=(0, 4))
        self.clear_chat_btn.bind("<Button-1>", lambda e: self._clear_chat())
        self.clear_chat_btn.bind("<Enter>", lambda e: self.clear_chat_btn.config(fg=FG_BRIGHT))
        self.clear_chat_btn.bind("<Leave>", lambda e: self.clear_chat_btn.config(fg=FG_DIM))
        
        # ─── Chat area (scrollable) ─────────────────────────────
        chat_container = tk.Frame(self, bg=BG_DARK)
        chat_container.pack(fill=tk.BOTH, expand=True, padx=1, pady=(1, 0))
        
        self.chat_canvas = tk.Canvas(
            chat_container, bg=BG_DARK, highlightthickness=0, borderwidth=0
        )
        self.chat_scrollbar = ttk.Scrollbar(
            chat_container, orient=tk.VERTICAL, 
            command=self.chat_canvas.yview,
            style="Dark.Vertical.TScrollbar"
        )
        
        self.chat_frame = tk.Frame(self.chat_canvas, bg=BG_DARK)
        self.chat_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(
            scrollregion=self.chat_canvas.bbox("all")
        ))
        
        self.chat_window = self.chat_canvas.create_window(
            (0, 0), window=self.chat_frame, anchor="nw"
        )
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        self.chat_canvas.bind("<Configure>", self._on_canvas_resize)
        
        self._chat_labels = []  # Track labels for dynamic wraplength
        
        self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Mouse wheel scrolling
        self.chat_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.chat_frame.bind("<MouseWheel>", self._on_mousewheel)
        
        # Welcome message (Centered)
        self.welcome_frame = tk.Frame(self.chat_canvas, bg=BG_DARK)
        
        # Spacer top
        tk.Frame(self.welcome_frame, bg=BG_DARK, height=40).pack(fill=tk.X)
        
        # Brand label like Gemini
        tk.Label(
            self.welcome_frame, text="\u2726", font=("Segoe UI", 24), 
            bg=BG_DARK, fg=FG_DIM
        ).pack(pady=(0, 10))
        
        tk.Label(
            self.welcome_frame, text="Bonjour !", font=("Segoe UI", 16, "bold"), 
            bg=BG_DARK, fg=FG_PRIMARY
        ).pack(pady=(0, 5))
        
        tk.Label(
            self.welcome_frame, text="Decrivez l'interface Tkinter que vous souhaitez creer.", 
            bg=BG_DARK, fg=FG_DIM, font=("Segoe UI", 10)
        ).pack()
        
        self.welcome_window = None
        self._show_welcome()
        
        # ─── Bottom: Input area ──────────────────────────────────
        bottom = tk.Frame(self, bg=BG_DARK)
        bottom.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Input container with border
        input_outer = tk.Frame(bottom, bg="#3e3e42")
        input_outer.pack(fill=tk.X, padx=8, pady=(4, 2))
        
        input_container = tk.Frame(input_outer, bg=self.INPUT_BG)
        input_container.pack(fill=tk.X, padx=1, pady=1)
        
        # Send button (pack first so it gets its space on the RIGHT)
        self.btn_send = tk.Frame(input_container, bg=ACCENT_BLUE, cursor="hand2")
        self.btn_send.pack(side=tk.RIGHT, padx=4, pady=4)
        
        self.btn_send_label = tk.Label(
            self.btn_send, text="\u2191", bg=ACCENT_BLUE, fg=FG_BRIGHT,
            font=("Segoe UI", 11, "bold"), padx=6, pady=2
        )
        self.btn_send_label.pack()
        
        for w in (self.btn_send, self.btn_send_label):
            w.bind("<Button-1>", lambda e: self._on_generate())
            w.bind("<Enter>", lambda e: (
                self.btn_send.config(bg="#005a9e"),
                self.btn_send_label.config(bg="#005a9e")
            ))
            w.bind("<Leave>", lambda e: (
                self.btn_send.config(bg=ACCENT_BLUE),
                self.btn_send_label.config(bg=ACCENT_BLUE)
            ))
        
        # Text input (pack after button so it fills remaining space)
        self.prompt_text = tk.Text(
            input_container, height=2, font=("Segoe UI", 10), 
            bg=self.INPUT_BG, fg=FG_PRIMARY, insertbackground="white", 
            relief=tk.FLAT, padx=10, pady=7, borderwidth=0,
            wrap=tk.WORD
        )
        self.prompt_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Placeholder
        self.prompt_text.insert("1.0", "Decrivez votre interface...")
        self.prompt_text.config(fg=FG_DIM)
        self._has_placeholder = True
        self.prompt_text.bind("<FocusIn>", self._on_focus_in)
        self.prompt_text.bind("<FocusOut>", self._on_focus_out)
        self.prompt_text.bind("<Return>", self._on_enter)
        
        # Action row
        action_row = tk.Frame(bottom, bg=BG_DARK)
        action_row.pack(fill=tk.X, padx=10, pady=(1, 6))
        
        # Model selector button
        self.model_var = tk.StringVar(value=self._short_model_name(AVAILABLE_MODELS[0]))
        
        model_frame = tk.Frame(action_row, bg="#3e3e42", cursor="hand2")
        model_frame.pack(side=tk.LEFT)
        
        model_inner = tk.Frame(model_frame, bg=self.INPUT_BG)
        model_inner.pack(padx=1, pady=1)
        
        self.model_btn = tk.Label(
            model_inner, textvariable=self.model_var, 
            bg=self.INPUT_BG, fg=FG_DIM,
            font=("Segoe UI", 8), padx=6, pady=1
        )
        self.model_btn.pack(side=tk.LEFT)
        
        self.model_arrow = tk.Label(
            model_inner, text="\u25BE", bg=self.INPUT_BG, fg=FG_DIM,
            font=("Segoe UI", 7), padx=2, pady=1
        )
        self.model_arrow.pack(side=tk.LEFT)
        
        for w in (model_frame, model_inner, self.model_btn, self.model_arrow):
            w.bind("<Button-1>", self._show_model_menu)
        
        # Model popup menu
        self.model_menu = tk.Menu(
            self, tearoff=0, bg="#2d2d30", fg="#cccccc",
            activebackground=ACCENT_BLUE, activeforeground="white",
            relief=tk.FLAT, borderwidth=1
        )
        for m in AVAILABLE_MODELS:
            short = self._short_model_name(m)
            self.model_menu.add_command(
                label=f"  {short}", 
                command=lambda model=m, s=short: self._select_model(model, s)
            )
        
        # State
        self._loading_dots = 0
        self._loading_after_id = None
        self._loading_label = None
    
    def _short_model_name(self, model):
        parts = model.split("-")
        return parts[1] if len(parts) >= 2 else model
    
    def _show_model_menu(self, event):
        try:
            self.model_menu.tk_popup(event.x_root, event.y_root - 50)
        finally:
            self.model_menu.grab_release()
    
    def _select_model(self, model_full, model_short):
        self.model_var.set(model_short)
        self.ai_client.set_model(model_full)
    
    def _on_canvas_resize(self, event):
        self.chat_canvas.itemconfig(self.chat_window, width=event.width)
        
        # Center welcome window if it exists
        if self.welcome_window:
            self.chat_canvas.coords(self.welcome_window, event.width / 2, event.height / 3)
            
        # Update wraplength of all tracked labels
        wrap = max(100, event.width - 50)
        for lbl in self._chat_labels:
            try:
                if lbl.winfo_exists():
                    lbl.config(wraplength=wrap)
            except:
                pass
    
    def _get_wraplength(self):
        w = self.chat_canvas.winfo_width()
        return max(100, w - 50) if w > 1 else 220
    
    def _on_mousewheel(self, event):
        self.chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _on_focus_in(self, event):
        if self._has_placeholder:
            self.prompt_text.delete("1.0", tk.END)
            self.prompt_text.config(fg=FG_PRIMARY, insertbackground="white")
            self._has_placeholder = False
    
    def _on_focus_out(self, event):
        content = self.prompt_text.get("1.0", tk.END).strip()
        if not content:
            self.prompt_text.insert("1.0", "Decrivez votre interface...")
            self.prompt_text.config(fg=FG_DIM, insertbackground=FG_DIM)
            self._has_placeholder = True
    
    def _on_enter(self, event):
        if not event.state & 0x1:  # Enter without Shift
            self._on_generate()
            return "break"
    
    # ─── Chat messages ───────────────────────────────────────────
    
    def _add_user_message(self, text):
        msg_frame = tk.Frame(self.chat_frame, bg=BG_DARK)
        msg_frame.pack(fill=tk.X, padx=8, pady=(8, 2))
        
        tk.Label(
            msg_frame, text="Vous", bg=BG_DARK, fg=FG_SECONDARY,
            font=("Segoe UI", 8, "bold"), anchor="w"
        ).pack(fill=tk.X)
        
        bubble = tk.Frame(msg_frame, bg=self.BUBBLE_USER)
        bubble.pack(fill=tk.X, pady=(3, 0))
        
        lbl = tk.Label(
            bubble, text=text, bg=self.BUBBLE_USER, fg=FG_PRIMARY,
            font=("Segoe UI", 9), anchor="w", justify=tk.LEFT,
            wraplength=self._get_wraplength(), padx=10, pady=7
        )
        lbl.pack(fill=tk.X)
        self._chat_labels.append(lbl)
        
        self._scroll_to_bottom()
    
    def _add_ai_message(self, text, is_error=False):
        msg_frame = tk.Frame(self.chat_frame, bg=BG_DARK)
        msg_frame.pack(fill=tk.X, padx=8, pady=(8, 2))
        
        tk.Label(
            msg_frame, text="Assistant", bg=BG_DARK, fg=ACCENT_BLUE,
            font=("Segoe UI", 8, "bold"), anchor="w"
        ).pack(fill=tk.X)
        
        fg_color = "#f44747" if is_error else FG_SECONDARY
        bubble = tk.Frame(msg_frame, bg=self.BUBBLE_AI)
        bubble.pack(fill=tk.X, pady=(3, 0))
        
        tk.Label(
            bubble, text=text, bg=self.BUBBLE_AI, fg=fg_color,
            font=("Segoe UI", 9), anchor="w", justify=tk.LEFT,
            wraplength=self._get_wraplength(), padx=10, pady=7
        ).pack(fill=tk.X)
        self._chat_labels.append(msg_frame.winfo_children()[-1].winfo_children()[-1])
        
        self._scroll_to_bottom()
    
    def _show_welcome(self):
        """Affiche le message d'accueil centre."""
        if not self.welcome_window:
            self.chat_canvas.update_idletasks()
            w = self.chat_canvas.winfo_width()
            h = self.chat_canvas.winfo_height()
            self.welcome_window = self.chat_canvas.create_window(
                w / 2, h / 3, window=self.welcome_frame, anchor="center"
            )
            
    def _hide_welcome(self):
        """Masque le message d'accueil."""
        if self.welcome_window:
            self.chat_canvas.delete(self.welcome_window)
            self.welcome_window = None
            
    def _add_system_message(self, text):
        msg_frame = tk.Frame(self.chat_frame, bg=BG_DARK)
        msg_frame.pack(fill=tk.X, padx=12, pady=(12, 4))
        
        tk.Label(
            msg_frame, text=text, bg=BG_DARK, fg=FG_DIM,
            font=("Segoe UI", 8), anchor="w", justify=tk.LEFT,
            wraplength=self._get_wraplength()
        ).pack(fill=tk.X)
        self._chat_labels.append(msg_frame.winfo_children()[-1])
    
    def _add_loading_indicator(self):
        msg_frame = tk.Frame(self.chat_frame, bg=BG_DARK)
        msg_frame.pack(fill=tk.X, padx=8, pady=(8, 2))
        
        tk.Label(
            msg_frame, text="Assistant", bg=BG_DARK, fg=ACCENT_BLUE,
            font=("Segoe UI", 8, "bold"), anchor="w"
        ).pack(fill=tk.X)
        
        self._loading_label = tk.Label(
            msg_frame, text=".", bg=BG_DARK, fg=FG_DIM,
            font=("Segoe UI", 9), anchor="w", padx=10
        )
        self._loading_label.pack(fill=tk.X)
        self._loading_frame = msg_frame
        
        self._scroll_to_bottom()
    
    def _scroll_to_bottom(self):
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
    
    def _clear_chat(self):
        for child in self.chat_frame.winfo_children():
            child.destroy()
        self._chat_labels.clear()
        self._show_welcome()
    
    # ─── Generation ──────────────────────────────────────────────
    
    def _on_generate(self):
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        if not prompt or self._has_placeholder:
            return
            
        self._hide_welcome()
        
        self._add_user_message(prompt)
        self.prompt_text.delete("1.0", tk.END)
        
        # Disable
        self.prompt_text.config(state=tk.DISABLED)
        self.btn_send.config(bg="#3e3e42")
        self.btn_send_label.config(bg="#3e3e42", fg=FG_DIM)
        
        self._add_loading_indicator()
        self._start_loading()
        
        self.ai_client.generate_code_async(prompt, self._on_result)
    
    def _start_loading(self):
        if self._loading_label and self._loading_label.winfo_exists():
            dots = "." * ((self._loading_dots % 3) + 1)
            self._loading_label.config(text=f"Generation{dots}")
        self._loading_dots += 1
        self._loading_after_id = self.after(400, self._start_loading)
    
    def _stop_loading(self):
        if self._loading_after_id:
            self.after_cancel(self._loading_after_id)
            self._loading_after_id = None
        self._loading_dots = 0
        if hasattr(self, '_loading_frame') and self._loading_frame.winfo_exists():
            self._loading_frame.destroy()
        self._loading_label = None
    
    def _on_result(self, success, result_data):
        self.winfo_toplevel().after(0, self._handle_result, success, result_data)
    
    def _handle_result(self, success, result_data):
        self._stop_loading()
        
        if success:
            self.editor.set_code(result_data)
            lines = result_data.strip().count("\n") + 1
            self._add_ai_message(f"Code genere ({lines} lignes) et injecte dans l'editeur.")
        else:
            self._add_ai_message(f"Erreur : {result_data}", is_error=True)
        
        # Re-enable
        self.prompt_text.config(state=tk.NORMAL, fg=FG_PRIMARY, insertbackground="white")
        self._has_placeholder = False
        self.prompt_text.focus_set()
        self.btn_send.config(bg=ACCENT_BLUE)
        self.btn_send_label.config(bg=ACCENT_BLUE, fg=FG_BRIGHT)
