import tkinter as tk
from src.ui.theme import (
    BG_SURFACE, BG_ACTIVITY, BG_HOVER, BG_ACTIVE, BG_DARK, BG_MEDIUM,
    FG_PRIMARY, FG_DIM, FG_BRIGHT, ACCENT_BLUE, ACCENT_GREEN,
    FONT_ICON, FONT_ICON_SMALL, SASH_WIDTH, ACTIVITY_BAR_WIDTH,
    configure_dark_scrollbar
)
from src.ui.menus import AppMenu
from src.ui.editor import CodeEditor
from src.ui.preview import PreviewFrame
from src.ui.console import ConsoleOutput
from src.ui.status_bar import StatusBar
from src.core.executor import CodeExecutor
from src.core.file_manager import FileManager
from src.core.ai_client import MistralClient
from src.ui.ai_assistant import AIPanel


class ToolTip:
    """Tooltip discret."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)
    
    def show(self, event=None):
        if self.tip_window:
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 4
        y = self.widget.winfo_rooty()
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, bg="#1e1e1e", fg="#cccccc",
                         font=("Segoe UI", 8), padx=6, pady=3,
                         borderwidth=1, relief=tk.SOLID)
        label.pack()
    
    def hide(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class ActivityBarButton(tk.Frame):
    """Bouton epure pour l'Activity Bar avec indicateur lateral."""
    def __init__(self, parent, text, tooltip_text, command, fg_color=FG_DIM, active_fg=FG_BRIGHT, **kwargs):
        super().__init__(parent, bg=BG_ACTIVITY, cursor="hand2")
        
        self.command = command
        self.default_fg = fg_color
        self.active_fg = active_fg
        
        self.indicator = tk.Frame(self, bg=BG_ACTIVITY, width=2)
        self.indicator.pack(side=tk.LEFT, fill=tk.Y)
        
        self.label = tk.Label(self, text=text, font=("Segoe UI", 13), 
                              bg=BG_ACTIVITY, fg=fg_color, padx=0, pady=9)
        self.label.pack(expand=True)
        
        for w in (self, self.label):
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)
            w.bind("<Button-1>", self._on_click)
        
        ToolTip(self, tooltip_text)
    
    def _on_enter(self, e):
        self.config(bg=BG_HOVER)
        self.label.config(bg=BG_HOVER, fg=self.active_fg)
        self.indicator.config(bg=FG_DIM)
    
    def _on_leave(self, e):
        self.config(bg=BG_ACTIVITY)
        self.label.config(bg=BG_ACTIVITY, fg=self.default_fg)
        self.indicator.config(bg=BG_ACTIVITY if not getattr(self, '_is_active', False) else ACCENT_BLUE)
    
    def _on_click(self, e):
        self.indicator.config(bg=ACCENT_BLUE)
        self.after(150, lambda: self.indicator.config(bg=FG_DIM if not getattr(self, '_is_active', False) else ACCENT_BLUE))
        self.command()
    
    def set_active(self, active):
        self._is_active = active
        if active:
            self.default_fg = FG_BRIGHT
            self.label.config(fg=FG_BRIGHT)
            self.indicator.config(bg=ACCENT_BLUE)
        else:
            self.default_fg = FG_DIM
            self.label.config(fg=FG_DIM)
            self.indicator.config(bg=BG_ACTIVITY)


class TkLearnStudio:
    # Sidebar modes
    SIDEBAR_INSPECTOR = "inspector"
    SIDEBAR_AI = "ai"
    SIDEBAR_NONE = "none"
    
    def __init__(self, root):
        self.root = root
        self.root.title("TkLearn Studio")
        self.root.geometry("1200x800")
        self.root.configure(bg=BG_SURFACE)
        self.root.minsize(900, 600)
        
        configure_dark_scrollbar(root)
        
        # Current sidebar state
        self._sidebar_mode = self.SIDEBAR_INSPECTOR
        
        # Container principal
        self.main_container = tk.Frame(self.root, bg=BG_SURFACE)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Activity Bar
        self.activity_bar = tk.Frame(self.main_container, bg=BG_ACTIVITY, width=ACTIVITY_BAR_WIDTH)
        self.activity_bar.pack(side=tk.LEFT, fill=tk.Y)
        self.activity_bar.pack_propagate(False)
        
        # Content
        self.content_container = tk.Frame(self.main_container, bg=BG_SURFACE)
        self.content_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Vertical split: top area / console
        self.vpaned = tk.PanedWindow(self.content_container, orient=tk.VERTICAL, 
                                      sashwidth=SASH_WIDTH, bg=BG_SURFACE, sashrelief=tk.FLAT)
        self.vpaned.pack(fill=tk.BOTH, expand=True)
        
        # Horizontal split: sidebar | editor | preview
        self.hpaned = tk.PanedWindow(self.vpaned, orient=tk.HORIZONTAL, 
                                      sashwidth=SASH_WIDTH, bg=BG_SURFACE, sashrelief=tk.FLAT)
        self.vpaned.add(self.hpaned, minsize=300)
        
        # Inspector
        from src.ui.inspector import WidgetInspector
        self.inspector = WidgetInspector(self.hpaned)
        self.hpaned.add(self.inspector, minsize=180)
        
        # Editor
        self.editor = CodeEditor(self.hpaned)
        self.hpaned.add(self.editor, minsize=350)
        
        # Preview
        self.preview = PreviewFrame(self.hpaned)
        self.hpaned.add(self.preview, minsize=300)
        
        # Console
        self.console = ConsoleOutput(self.vpaned)
        self.vpaned.add(self.console, minsize=80)
        
        # Status Bar
        self.status_bar = StatusBar(self.content_container)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Core
        self.executor = CodeExecutor(
            editor=self.editor, preview=self.preview, 
            console=self.console, inspector=self.inspector,
            status_bar=self.status_bar
        )
        self.ai_client = MistralClient(console=self.console)
        self.file_manager = FileManager(root=self.root, editor=self.editor, console=self.console, status_bar=self.status_bar)
        
        # AI Panel (cree mais pas affiche)
        self.ai_panel = AIPanel(self.hpaned, self.editor, self.ai_client)
        
        # Menus
        self.menus = AppMenu(root=self.root, editor=self.editor, 
                             executor=self.executor, file_manager=self.file_manager)
        
        # Activity Bar buttons
        tk.Frame(self.activity_bar, bg=BG_ACTIVITY, height=8).pack(side=tk.TOP)
        
        self.toggle_btn = ActivityBarButton(
            self.activity_bar, text="\u2630", tooltip_text="Explorer",
            command=self._show_inspector
        )
        self.toggle_btn.pack(side=tk.TOP, fill=tk.X)
        self.toggle_btn.set_active(True)
        
        self.ai_btn = ActivityBarButton(
            self.activity_bar, text="\u2726", tooltip_text="Assistant IA",
            command=self._show_ai_panel
        )
        self.ai_btn.pack(side=tk.TOP, fill=tk.X)
        
        # Separator
        tk.Frame(self.activity_bar, bg="#404040", height=1).pack(side=tk.TOP, fill=tk.X, padx=10, pady=6)
        
        self.run_btn = ActivityBarButton(
            self.activity_bar, text="\u25B6", tooltip_text="Executer  F5",
            command=self.executor.run_code, fg_color=ACCENT_GREEN, active_fg=ACCENT_GREEN
        )
        self.run_btn.pack(side=tk.TOP, fill=tk.X)
        
        self.clear_btn = ActivityBarButton(
            self.activity_bar, text="\u2715", tooltip_text="Vider la console",
            command=self.console.clear
        )
        self.clear_btn.pack(side=tk.TOP, fill=tk.X)
        
        # Cursor tracking
        self.editor.text_widget.bind("<KeyRelease>", self._update_cursor_pos)
        self.editor.text_widget.bind("<ButtonRelease-1>", self._update_cursor_pos)
    
    def _update_cursor_pos(self, event=None):
        try:
            pos = self.editor.text_widget.index(tk.INSERT)
            line, col = pos.split(".")
            self.status_bar.update_cursor(line, int(col) + 1)
        except:
            pass
    
    def _show_inspector(self):
        """Affiche l'inspecteur dans la sidebar (ou le masque si deja actif)."""
        if self._sidebar_mode == self.SIDEBAR_INSPECTOR:
            # Toggle off
            self.hpaned.forget(self.inspector)
            self.toggle_btn.set_active(False)
            self._sidebar_mode = self.SIDEBAR_NONE
        else:
            # Remove current sidebar panel
            self._remove_sidebar_panel()
            # Add inspector
            self.hpaned.add(self.inspector, before=self.editor, minsize=180)
            self.toggle_btn.set_active(True)
            self.ai_btn.set_active(False)
            self._sidebar_mode = self.SIDEBAR_INSPECTOR
        
        self.editor.text_widget.focus_set()
    
    def _show_ai_panel(self):
        """Affiche le panneau IA dans la sidebar (ou le masque si deja actif)."""
        if self._sidebar_mode == self.SIDEBAR_AI:
            # Toggle off
            self.hpaned.forget(self.ai_panel)
            self.ai_btn.set_active(False)
            self._sidebar_mode = self.SIDEBAR_NONE
        else:
            # Remove current sidebar panel
            self._remove_sidebar_panel()
            # Add AI panel
            self.hpaned.add(self.ai_panel, before=self.editor, minsize=220)
            self.ai_btn.set_active(True)
            self.toggle_btn.set_active(False)
            self._sidebar_mode = self.SIDEBAR_AI
            # Focus the prompt
            self.ai_panel.prompt_text.focus_set()
    
    def _remove_sidebar_panel(self):
        """Retire le panneau sidebar actuel."""
        if self._sidebar_mode == self.SIDEBAR_INSPECTOR:
            self.hpaned.forget(self.inspector)
        elif self._sidebar_mode == self.SIDEBAR_AI:
            self.hpaned.forget(self.ai_panel)


def main():
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.25)
    except: pass
    app = TkLearnStudio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
